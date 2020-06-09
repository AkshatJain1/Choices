import json
import bson
import names
import pandas as pd
import random
import math
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x, inflection_point=0, growth=1):
    return 1 / (1 + math.exp((-1 * growth) * (x - inflection_point)))

MINIMUM_USER_FOOD_EDGE_VALUE=3
MINIMUM_SAME_TYPE_EDGE_VALUE=0.5
test_data = {}


ingredients_data = pd.read_csv('ingredients v1.csv')
all_food_names = [str(total_name).strip() for total_name in list(ingredients_data['name'])]

menu_item_label = random.randint(1, 4)
food_item_names = []

def generateUserUserConnections(curr_user):
    global test_data
    assert test_data and test_data[curr_user]
    if not 'user_connections' in test_data[curr_user]:
        test_data[curr_user]['user_connections'] = {}
    for user in users:
        if not user in test_data[curr_user]['user_connections']:

            usersim = int(sigmoid((random.randint(0, 10) / 10), 0.5, 10) * 100) / 100
            test_data[curr_user]['user_connections'][user] = usersim


            if not user in test_data:
                generateUserNode(user)

            if user in test_data:
                if not 'user_connections' in test_data[user]:
                    test_data[user]['user_connections'] = {}
                test_data[user]['user_connections'][curr_user] = usersim


def generateUserFoodConnections(curr_user):
    global test_data
    assert test_data and curr_user in test_data

    if not 'food_item_connections' in test_data[curr_user]:
        test_data[curr_user]['food_item_connections'] = {}
    for food in foods:
        if not food in test_data[curr_user]['user_connections']:
            user_food_sim = int(sigmoid((random.randint(0, 10) / 10), 0.5, 10) * 100) / 20
            test_data[curr_user]['food_item_connections'][food] = user_food_sim

            if not food in test_data:
                generateFoodNode(food)

            if food in test_data:
                if not 'user_connections' in test_data[food]:
                    test_data[food]['user_connections'] = {}
                test_data[food]['user_connections'][curr_user] = user_food_sim

def generateFoodUserConnections(food):
    pass

def generateFoodFoodConnections(curr_food):
    global test_data
    assert test_data and test_data[curr_food]

    if not 'food_item_connections' in test_data[curr_food]:
        test_data[curr_food]['food_item_connections'] = {}
    for food in foods:
        if not food in test_data[curr_food]['food_item_connections']:
            food_food_sim =int(sigmoid((random.randint(0, 10) / 10), 0.5, 10) * 100) / 100
            test_data[curr_food]['food_item_connections'][food] = food_food_sim
            if not food in test_data:
                generateFoodNode(food)

            if food in test_data:
                if not 'food_item_connections' in test_data[food]:
                    test_data[food]['food_item_connections'] = {}
                test_data[food]['food_item_connections'][curr_food] = food_food_sim

def generateUserNode(user):
    global test_data
    if not user in test_data:
        test_data[user] = {}
        test_data[user]['info'] = {}
        test_data[user]['info']['type'] = 'user'
        test_data[user]['info']['name'] = names.get_full_name()
        test_data[user]['info']['Additional Info'] = 'Hello World'
        # generateUserUserConnections(user)
        # generateUserFoodConnections(user)


def generateFoodNode(food):
    global test_data

    if not food in test_data:
        global menu_items
        test_data[food] = {}
        test_data[food]['info'] = {}
        test_data[food]['info']['type'] = 'food_item'

        food_item = -1
        while food_item == -1 or food_item in food_item_names:
            food_item = all_food_names[random.randint(0, len(all_food_names) - 1)]
        food_item_names.append(food_item)
        test_data[food]['info']['name'] = food_item
        restaurantid = random.randint(1, 4)
        test_data[food]['info']['restauarant id'] = restaurantid

        if restaurantid == menu_item_label:
            menu_items.append(food)
        test_data[food]['info']['Additional Info'] = 'Hello World'

numUsers = 10
numFood = 20

users = [(str(bson.objectid.ObjectId())) for _ in range(numUsers)]
foods = [(str(bson.objectid.ObjectId())) for _ in range(numFood)]
menu_items = []

# generateUserNode(users[0])





#
for user in users:
    generateUserNode(user)
    generateUserUserConnections(user)
    generateUserFoodConnections(user)

for food in foods:
    generateFoodNode(food)
    generateFoodFoodConnections(food)

#

test_data_graph_dict = {}
graph_node_labels = {}

LONGEST_LABEL = 20
for item in test_data.keys():
    graph_node_labels[item] = test_data[item]['info']['name'][:20]
    test_data_graph_dict[item] = test_data[item]['user_connections']
    test_data_graph_dict[item].update(test_data[item]['food_item_connections'])


print(graph_node_labels)
print(test_data_graph_dict)

test_data_graph = nx.Graph(test_data_graph_dict)


for item in test_data.keys():
    for item1 in test_data_graph_dict[item].keys():
        if test_data[item]['info']['type'] == test_data[item1]['info']['type']:
            if (test_data_graph_dict[item][item1] < MINIMUM_SAME_TYPE_EDGE_VALUE):
                if(test_data_graph.has_edge(item, item1)):
                    test_data_graph.remove_edge(item, item1)
        elif test_data[item]['info']['type'] != test_data[item1]['info']['type']:
            if test_data_graph_dict[item][item1] < MINIMUM_USER_FOOD_EDGE_VALUE:
                if (test_data_graph.has_edge(item, item1)):
                    test_data_graph.remove_edge(item, item1)

color_map = []
position_map = {}
bipartite_position = nx.random_layout(test_data_graph)
print(bipartite_position)

userx = min(bipartite_position.items(), key=lambda x : x[1][0])[1][0] - 0.5
menux = min(bipartite_position.items(), key=lambda x : x[1][0])[1][0] - 0.2
usery = 0
userydelta = 4/len(users)
menuy = 0
menuydelta = 4/(len(menu_items) + 1)
sgndelta = 1




edge_colors = []
for node in test_data_graph:

    if test_data[node]['info']['type'] == 'user':
        color_map.append('green')
        bipartite_position[node] = np.array([userx, usery])
        usery = (abs(usery) + userydelta) * sgndelta
    elif node in menu_items:
        color_map.append('red')
        bipartite_position[node] = np.array([menux, menuy])
        menuy = (abs(menuy) + menuydelta) * sgndelta
    else:
        color_map.append('orange')
    sgndelta *= -1

print(menu_items)
print(test_data_graph.edges())
edge_labels_dict = {}
for edge in test_data_graph.edges():
    print(test_data[edge[0]]['info']['type'])
    if edge[0] in users:
        if edge[1] in menu_items:
            edge_colors.append('blue')
        else:
            edge_colors.append('brown')
    else:
        edge_colors.append('brown')
    edge_labels_dict[edge] = test_data_graph_dict[edge[0]][edge[1]]
    # elif edge[0[] in users:
    #     print("SDLKFJKLJF")
    #     if edge[0] in menu_items:
    #         print("OF COURSE")
    #         edge_colors.append('blue')


    # elif edge[0] in menu_items:
    #     if test_data[edge[1]]['info']['type'] == 'user':
    #         edge_colors.append('blue')
    # else:
    #     edge_colors.append('brown')

print(bipartite_position)
print(edge_labels_dict)

nodes = nx.draw_networkx_nodes(test_data_graph,pos=bipartite_position, node_color=color_map)
edges = nx.draw_networkx_edges(test_data_graph, pos=bipartite_position, edge_color=edge_colors, alpha=0.4, width=1)
labels = nx.draw_networkx_labels(test_data_graph, pos=bipartite_position, font_size=5, font_family = 'Calibri', labels=graph_node_labels)
edge_labels = nx.draw_networkx_edge_labels(test_data_graph, pos=bipartite_position, font_size=5, edge_labels=edge_labels_dict, bbox=dict(alpha=0))
# print(edges)

# for i, edge in enumerate(edges):
#     # edge.set_alpha(edge[i])
#     print('hi')
# # nx.draw(nx.Graph(test_data_graph_dict_2))
plt.show()



# data_graph.add_nodes_from([item for item test_data.keys() if item['info']['type'] == 'user'], bipartite=0)
# data_graph.add_nodes_from([item for item in test_data.keys() if item['info']['type'] == 'user']. bipartite=1)

with open('traversal_test_8.json', 'w') as outfile:
    json.dump(test_data, outfile, indent=4)







