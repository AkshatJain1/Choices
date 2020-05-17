from google.cloud import vision
import os, sys, flask, json
from utils import closest, filterOut, isPrice

app = flask.Flask(__name__)
app.debug = True

client = vision.ImageAnnotatorClient(credentials = json.load(open('choices-545f2b051313.json')))


MAX_WORD_SPACE = 5
FILE_NAME = 'image.png'

@app.route("/", methods = ["POST"])
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
    app.run(host='0.0.0.0', threaded=True)

    #
    # web_response = client.web_detection(image=image)
    # web_content = web_response.web_detection
    # web_content.best_guess_labels
    # predictions = [(entity.description, '{:.2%}'.format(entity.score)) for entity in web_content.web_entities]
    # print(predictions)
    # ismenu = any([p[0].lower().strip() == 'menu' and float(p[1][:-1]) > 30 for p in predictions])
    # print("the picture is in fact a menu") if ismenu else print("the picture isn't a menu")
