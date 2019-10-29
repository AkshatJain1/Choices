# from gevent.pywsgi import WSGIServer
# from gevent import monkey
# need to patch sockets to make requests async
# monkey.patch_all()

import flask
from google.cloud import vision
import os
import sys


credentials = {
  "type": "service_account",
  "project_id": "choices2",
  "private_key_id": "aee5e00847d5525ab7e69d477998f6c02b027827",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDLY3EQSpe+KSRR\ntqtOaZaEbiMz4/2+mhXvYZ84epB014molXsb9K6pB0BSGIrzWpCHzpqrEIhDIDqh\n85btIYrghf8okcDatIgeM9tatnyChUcEQ4j+niCVeC8FGiYT/nuHj8CbyCoZDW/n\nAVEWNd5jqHd1C0IsQYCHGCgr3MVA3AIhsJHv9D1d7Kz9W+iSww0yBBw5T4cJRxm3\nYlOftuKeM6hHLLifdQS9tX7wPjWoXfQ8jclxshC0KG6U+cmYJiEc5l8q2bv1noTS\npRJpfLQOWYFY5PN3w7FKg/SMwoCa+J/MYIC2vkprnKs8Ykm1ztsj4bYm5wzF4LSt\nsR+FTYhDAgMBAAECggEAY2j869IRvgv86QWoUGCyhZMRmLzQmvdUTldATAo4DiwF\naEV70Uu0jQBy002UqOJ0rzRwC7m+aFTZ46ucctYIu7oy34DyKtO/jkeZaQq169O5\nxN8/l/fxBC2kidFgmDgz56v/IAVjcjBLqDTQDdORmdNPZAF3PAteB2nqxJmZPhwL\nzMizhYXyhC0bD/YWtLPik174d0wrTReo0uvr38p8+Pj58t2vaHcW0z1ZQE6TMV5b\nAjcyUjZYIdf0fyOrw313ERDObzXfWHeZoik8mOkThkpbxhg0OqISS77t7KleIlDp\n5nLSxrhNt2czZyA86qDZfgzOoK1GoWgbK98Hwi9dIQKBgQDk0yo2BVad6lmwxXs+\nLz1NGYcpDpS7ZnmYX1PaFLQJzv0Ter8sM2jcqhyB7aLJZ4LjbzOEPyfFwuppKh0V\nM01senK6bLTx3x2o3wMC0BMPeEIxXg8K+qJCf03YcB/pSjDsJSDp5jjtiIpcqdzG\nRC1OSfvx9mM7ed3b8UmxIXZXIQKBgQDjivKM/B5Bgoetxf33a5HO0plEM9TTAJuY\nu0gkT9cfB8nEtQfWbwZEqTAz69HU5Dq6vbHjlttkQVD1jolbq7Zzsj+rFpJKLNM7\nEKQAOs2pbzcp3vO7NUToyZAwX+JtiVikDePusmo1/zENobaF+XBiF2WMExsFg7FT\nJdbedmOG4wKBgQCPF/pCk+4JjJ6P677ZMUNdboRWSXb7BecuQRa3vtCjfZxHTTA1\nnOSLcZmoKons9t0kCsslfTUK94wNPbe4JT/agWwzZn1077ilfOhuHt58gxCpvI8d\np4RGn0N4AQ4DnlCfq8w8WKrq58LWlaapGcNXPO7f7ds6O0hhHS+fJDTT4QKBgQCB\nxoOjyT9wWYQMpjm83YshjJeBgJZHabdUmqwAmdC1j/mRyTYZJOVMT7qAQmVAqJKe\nYwaMKUQjn+UOyCarM/oxbl5Fs+/ngj1PGKSQxPj7Q8UQimo0QaN1qVAlZup7UrRN\njOaNAxD0jwFpJuw06RkhuPpfs53bvUprg89Sve7xxQKBgQC3wFs+v/osQXQsHQDC\nZF9foXl+gMAV6a7/dY76mkj4BeqJlSdAugYLuwYqCPqd5C+bfODfLjBcg5cyDvEC\nF61uKJ8/lqg8DxcKZx5LsN6/Mq2b1bUedugNhfEoejTwD+O0BS6NOKI9K+9+B0Xu\n3ulwioSyo2g6xswnFjJf2RPkHQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "admin-680@choices2.iam.gserviceaccount.com",
  "client_id": "102106641714033222182",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admin-680%40choices2.iam.gserviceaccount.com"
}


app = flask.Flask(__name__)
app.debug = True

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "C:/Users/respe/Downloads/Choices-server/server/choices2-aee5e00847d5.json"

client = vision.ImageAnnotatorClient(credentials = credentials)
food_list= []
actual_food_list = {}
xfactor = 1
yfactor = 10000
fontsize_factor = 10000000
max_word_space = 5
same_line_space = 3
lst_filtered = False
file_name = 'image.png'

def filterOut(lst):
    total_font = 0
    i = 0
    for elem in lst:
        total_font += elem[next(iter(elem))][0]
        i = i+1
    average_font = total_font // i

    for elem in lst:
        if abs(elem[next(iter(elem))][0] - average_font) > 7:
               lst.remove(elem)

def closest(s,s_height):
    return min(food_list, key = lambda element: xfactor*((s.bounding_poly.vertices[0].x - element[next(iter(element))][2])**2)+ yfactor*((s.bounding_poly.vertices[0].y - element[next(iter(element))][1])**2) + fontsize_factor*abs(s_height - element[next(iter(element))][0]))

def isPrice(s):
    if s == "":
        return ""
    if s[0] == '(' and s[-1] == ')':
        return ""
    if s[-1] == '.':
        return ""
    if 'cal' in s or 'Cal' in s or 'oz' in s or 'lb' in s:
        return ""
    try:
        return float(s)
    except:
        #potentially add more curencies
        if any([s[i] in ['€','$','£'] for i in range(len(s))]):
            return isPrice(s[1:]) or isPrice(s[:-1])
        return False

@app.route('/', methods=['GET'])
def getTest():
    return "Hello World"



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
                    if abs(last_food[next(iter(last_food))][1] - text.bounding_poly.vertices[0].y) < max_word_space:
                        menuitem[next(iter(last_food)) + " " + text.description] = menuitem.pop(text.description)
                        food_list.pop()

                food_list.append(menuitem)
        elif price:
            num_prices += 1

    print(food_list)

    for text in texts:

        text_height = max([vertex.y for vertex in text.bounding_poly.vertices]) - min([vertex.y for vertex in text.bounding_poly.vertices])

        word = text.description.strip()
        menuitem = {}
        price = isPrice(text.description)
        closest_element = closest(text,text_height)

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

def main():

    # use gevent WSGI server instead of the Flask
    # instead of 5000, you can define whatever port you want.
    # http = WSGIServer(('0.0.0.0', 5000), app.wsgi_app)
    #
    # # Serve your application
    # print('serving app', file=sys.stderr)
    # http.serve_forever()
    # app.debug=True
    app.run(host='0.0.0.0', threaded=True)

if __name__ == '__main__':
    main()

    #
    # web_response = client.web_detection(image=image)
    # web_content = web_response.web_detection
    # web_content.best_guess_labels
    # predictions = [(entity.description, '{:.2%}'.format(entity.score)) for entity in web_content.web_entities]
    # print(predictions)
    # ismenu = any([p[0].lower().strip() == 'menu' and float(p[1][:-1]) > 30 for p in predictions])
    # print("the picture is in fact a menu") if ismenu else print("the picture isn't a menu")
