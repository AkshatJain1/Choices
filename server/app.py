from google.cloud import vision
import os, sys, flask, json
from utils import closest, filterOut, isPrice
import time
import pandas as pd

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from urllib.request import urlopen
from urllib.parse import quote

app = flask.Flask(__name__)
app.debug = True

client = vision.ImageAnnotatorClient(credentials = json.load(open('choices-545f2b051313.json')))

try: 
    GOOGLE_KEY = open('google-api-key.txt').read()
except:
    sys.exit('Google API Key not found')

MAX_WORD_SPACE = 5
FILE_NAME = 'image.png'

@app.route("/getReviews", methods=["GET"])
def getReviews():
    lat = flask.request.args.get('latitude')
    lon = flask.request.args.get('longitude')

    dataQuery = {
        "key": GOOGLE_KEY,
        "location": f"{lat},{lon}",
        "type": "food",
        "rankby": "distance",
    }
    try:
        resp = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?', params=dataQuery)
        data = resp.json()
        restaurant = ''
        for rest in data["results"]:
            if "cafe" in rest["types"] or "restaurant" in rest["types"] or "food" in rest["types"]:
                restaurant = rest
                break
        
        rName, rId, rAddress = restaurant["name"], restaurant["place_id"], restaurant["vicinity"]

        googleReviews = getGoogleReviews(rId, rName, rAddress)
        googleCount = len(googleReviews)
        yelpCount, yelpReviews = getYelp(rName, rAddress)
        return flask.jsonify(name=rName, address=rAddress, reviewCount=googleCount+yelpCount, reviews=googleReviews+yelpReviews)
    except:
        return flask.jsonify(reviewCount=0, reviews=[])


def getGoogleReviews(placeID, name, address):
    # dataQuery = {
    #     "key": GOOGLE_KEY,
    #     "place_id": placeID,
    # }
    try:
        # resp = requests.get("https://maps.googleapis.com/maps/api/place/details/json", params=dataQuery)

        # return resp.json()["result"]["reviews"]
        driver = webdriver.Chrome('C:/Users/respe/chromedriver')

        driver.get(f'https://www.google.com/search?q={quote(name+" "+address)}')
        driver.find_element_by_xpath("//a[@data-async-trigger='reviewDialog']").click()
        time.sleep(2)
        
        Reviewer =[]
        ReviewDate = []
        ReviewRating =[]
        ReviewDescription = []
        TotalReviewsByUser = []
        thisreview = []
        last_len = 0
        def  get_reviews(thisreview):
            nonlocal last_len
            for webdriver_obj in thisreview.find_elements_by_class_name("WMbnJf"):
                Body = webdriver_obj.find_element_by_class_name('Jtu6Td')
                try:
                    webdriver_obj.find_element_by_class_name('review-snippet').click()
                    s_32B = webdriver_obj.find_element_by_class_name('review-full-text')
                    ReviewDescription.append(s_32B.text)
                except NoSuchElementException:
                    if Body.text == '':
                        return None
                    ReviewDescription.append(Body.text)
                Name = webdriver_obj.find_element_by_class_name("TSUbDb")
                Reviewer.append(Name.text)
                try:
                    ReviewByuser = webdriver_obj.find_element_by_class_name("A503be")
                    TotalReviewsByUser.append(ReviewByuser.text)
                except NoSuchElementException:
                    TotalReviewsByUser.append("")
                star = webdriver_obj.find_element_by_class_name("Fam1ne")
                ReviewStar =star.get_attribute("aria-label")
                ReviewRating.append(ReviewStar)
                Date = webdriver_obj.find_element_by_class_name("dehysf")
                ReviewDate.append(Date.text)
                    
                element = webdriver_obj.find_element_by_class_name('PuaHbe')
                driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
            reviews = driver.find_elements_by_class_name("gws-localreviews__general-reviews-block")
            r_len = len(reviews)
            if r_len > last_len:
                last_len = r_len
                get_reviews(reviews[r_len-1])
        
        reviews = driver.find_elements_by_class_name("gws-localreviews__general-reviews-block")
        last_len = len(reviews)
        get_reviews(reviews[last_len - 1])
    
        data = pd.DataFrame ( { 'author' : Reviewer,
                                'rating': ReviewRating,
                                'description': ReviewDescription})
        driver.quit() 
        return data.to_dict('records')
    except Exception as inst:
        print(inst)
        return []
   

def getYelp(restaurantName, location):
    page = urlopen("https://www.yelp.com/search?find_desc=" + quote(restaurantName) + "&find_loc=" + quote(location))
    soup = BeautifulSoup(page, features="html.parser")

    restLink = ''
    for link in soup.findAll('a', href=True):
        if 'osq' in link['href']:
            restLink = link['href']
            break

    if restLink != '':
        def extractYelpReviews(relativeUrl): 
            url = 'https://yelp.com' + relativeUrl

            soup = BeautifulSoup(urlopen(url), features="html.parser")
            scripts = soup.findAll("script", attrs={'type': 'application/ld+json'})
            reviewDict = json.loads(scripts[-1].text)

            return reviewDict

        d = extractYelpReviews(restLink)
        reviews = d['review']
        reviewCount = d['aggregateRating']['reviewCount']

        for i in range(20, reviewCount, 20):
            reviews.extend(extractYelpReviews(restLink + '&start=' + str(i))['review'])
        
        return reviewCount, reviews
    else:
        return 0, []
    

@app.route("/parseMenu", methods = ["POST"])
def parseMenu():
    content = str.encode(flask.request.json['data'])
    print(content, file=sys.stderr)
    # rerun = True
    # while rerun:
        # try:
    image = vision.types.Image(content=content)
    text_response = client.text_detection(image=image)
            # rerun = False
        # except:
            # rerun = True

    texts = text_response.text_annotations

    print('Texts:')
    print(texts[0].description)
    max_text_height = max([max([vertex.y for vertex in text.bounding_poly.vertices]) - min([vertex.y for vertex in text.bounding_poly.vertices]) for text in texts])
    num_prices = 0
    food_list = []
    actual_food_list = {}
    for text in texts:

        text_height = max([vertex.y for vertex in text.bounding_poly.vertices]) - min([vertex.y for vertex in text.bounding_poly.vertices])

        word = text.description.strip()
        menuitem = {}
        price = isPrice(text.description)
        if text_height != max_text_height and not price:
            #10 is  margin value
            if price == "":
                text.description = ""
            if text.description:
                if text.description[-1] == ',' or text.description[-1] == 'or' or text.description[-1] == 'and':
                    g = [g for g in range(len(texts)) if texts[g]== text][0]
                    g = g + 1
                    while g < len(texts) and abs(texts[g].bounding_poly.vertices[0].x - text.bounding_poly.vertices[0].x) > 3:
                        g += 1
                    if g < len(texts):
                        text.description += ' ' + texts.pop(g).description

                menuitem[text.description] = (text_height, text.bounding_poly.vertices[0].y, text.bounding_poly.vertices[1].x)
                #combine the words for a single me
                if len(food_list):
                    last_food = food_list[-1]
                    if abs(last_food[next(iter(last_food))][1] - text.bounding_poly.vertices[0].y) < MAX_WORD_SPACE:
                        menuitem[next(iter(last_food)) + " " + text.description] = menuitem.pop(text.description)
                        food_list.pop()

                food_list.append(menuitem)
        elif price:
            num_prices += 1

    print(food_list)

    lst_filtered = False
    for text in texts:

        text_height = max([vertex.y for vertex in text.bounding_poly.vertices]) - min([vertex.y for vertex in text.bounding_poly.vertices])

        word = text.description.strip()
        menuitem = {}
        price = isPrice(text.description)
        closest_element = closest(text, text_height, food_list)

        if not num_prices and not lst_filtered:
            filterOut(food_list)
            lst_filtered = True

        if text_height != max_text_height and price:
            actual_food_list[next(iter(closest_element))] = price

            # food_list[text.description] = (text_height, text.bounding_poly.vertices[0].y)
            # print('text ', text.description)
            # print('text-height ', text_height)


    if not num_prices:
        for elem in food_list:
            actual_food_list[next(iter(elem))] = 0
    return flask.make_response(flask.jsonify(actual_food_list))


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)

    #
    # web_response = client.web_detection(image=image)
    # web_content = web_response.web_detection
    # web_content.best_guess_labels
    # predictions = [(entity.description, '{:.2%}'.format(entity.score)) for entity in web_content.web_entities]
    # print(predictions)
    # ismenu = any([p[0].lower().strip() == 'menu' and float(p[1][:-1]) > 30 for p in predictions])
    # print("the picture is in fact a menu") if ismenu else print("the picture isn't a menu")
