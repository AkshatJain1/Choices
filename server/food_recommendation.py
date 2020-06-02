import collections
import json
import sys
import os
import math
#NOTE: THE RECOMMENDATION SHOULD NOT ONLY BE WEIGHTED BY DISTANCE FROM USER, BUT MUCH MORE SO BY THE DIFFERENCE IN THE CURRENTMENUWEIGHT AND THE THE WEIGHT OF THE USER
#NOTE: THE DISTANCE FACTOR FUNCTION SHOULD BE A SIGMOID FUNCTION

#NOTE: CHANGE THIS BASED ON WHAT IS THE BEST WAY TO STORE THE EDGE WEIGHTS OF USER TO ITEMS
ratings_scale = 5
L = 5
K = 5
limit_users = 10
limit_food_items = 10   #calcula
#distancefactor

#controls (provide description)
#have to tune, can possibly tune through a neural network type structure)
dist_user_buffer = 2
dist_user_growth = 7

dist_user_item_buffer = 2
dist_user_item_growth = 7

user_item_pref_buffer = 0
user_item_pref_growth = 10

dist_menu_weight_buffer = 2
menu_weight_growth = 3

user_sim_buffer = 0.5
user_sim_growth = 7



#d
#might need to include foodWeights in actual function iself
#will definitely incorporate dynamic programming into this afterwards (cacheing)
#database dictionary will actually put in later


#notesdd

                    #have some way of updating distance from origin

            # for adj_node_id in db[node_id]['food_item_connections']:
            #     #retrieve
            #     assert db[adj_node_id]['info']['type'] == 'food_item':
            #     food_item_id = adj_node_id
            #
            #     fringe_deque.append(food_item_id)
            #
            #     #the preference from the current_user_item_pref
            #     foodWeight[curr_user_id][food_item_id] = curr_user_item_pref(curr_user_id, user_id, food_item_id)
            #
            #     dist_from_curr_user[user_id] = dist_from_curr_user[node] + 1




                  #node is a food item
#NOTE: CAREFUL WITH FIELDS NOT UPDATING WITH FUNCTION CALL
#
#
# db = {}
#
# with open('traversal_test_5.json') as f:
#     db = json.load(f)

currentUserMenuWeights = {}
currentMenuCount = {}
dist_from_curr_user = {}
db = {}
#menu_items are id's of the menu items
def user_item_traversal(curr_user_id, menu_items, relpath):

    global db
    with open(relpath) as f:
        db = json.load(f)


    global currentUserMenuWeights
    global currentMenuCount
    global UserMenuRatings
    global dist_from_curr_user
    currentUserMenuWeights = {}
    currentMenuCount = {}
    UserMenuRatings = {}
    #NOTE: this user menu ratings thing may/may not be useless
    dist_from_curr_user = {}


    latest_menu_item = None
    prev_food_item = None

    fringe_deque = collections.deque()
    fringe_deque.append(curr_user_id)

    #Note: figure out how to makesure the latest menu item doesn't get multiplied by all, but only by the best, as the multiplication of numbers will eventually lead to 0 issue
    similar_ext_mul = 1
    user_marked = {}
    menu_item_marked = {}
    current_food_item_marked = {}

    user_marked[curr_user_id] = True
    dist_from_curr_user[curr_user_id] = 0





    #using this to figure out the intermediate connections, instead of directly doing to user at hand, seems unnecessary tho cuz its iterative and not recursive
    # userMenuWeights = {{}}


    #set the menu_items all to 0
    # for menu_item in menu_items:
    #     currentUserMenuWeights[menu_item] = 0

    #set the menu items all to 0
    for menu_item in menu_items:
        currentUserMenuWeights[menu_item] = 0

    # last_user = null
    # last_food_item = null

    while fringe_deque:
        node_id = fringe_deque.popleft()

        #node is a0 user
        #quesiton: should a user traverse other food items they have eaten also (besides ones scanned in)
        #answer: no because if it ends up connecting from one of past menu items to current menu itesm the connection will lead back to user in the first place
        if node_id not in db:
            #NOTE: here we actually create the item, in the very small chance item not in database
            print("Item not even in databse!")
            sys.exit(1)


        elif db[node_id]['info']['type'] == 'user':
            for menu_item in menu_items:  #need to mark the menuitem if it was traversed
                #check to see if the user has eaten that menu item
                if menu_item not in db[node_id]['food_item_connections']:
                    db[node_id]['food_item_connections'][menu_item] = -100
                    db[menu_item]['user_connections'][node_id] = -100

                #check to see if the menu item has been marked before before traversring
                if not menu_item_marked.get(menu_item, False):
                    fringe_deque.append(menu_item)
                    menu_item_marked[menu_item] = True
                    dist_from_curr_user[menu_item] = dist_from_curr_user[node_id] + 1

                    print(menu_item)
                    print(dist_from_curr_user[menu_item])
                    # currentUserMenuWeight[food_item_id] = curr_user_item_pref(curr_user_id, user_id, food_item_id, weightSoFar)
                    #dist_from_curr_user[node_id] = dist_from_curr_user[menu_item] + 1
      #IDEA TO BE IMPLEMENTED: For the extended food item algorithm. As we go through the extended food item list, we keep track of the items,
      # and once we reach a user node, we go through the list of items we have added and add the user id to those. The connection will have some magnitude edge value as well

        elif db[node_id]['info']['type'] == 'food_item':


            if node_id in menu_items:
                latest_menu_item = node_id
            else:
                #this extra info storing element only gets added if acutal node is an extended food item
                similar_ext_mul, prev_food_item = fringe_deque.popleft()

            #this if structure is for calculating the similarity from previous food item
            if prev_food_item:
                dist_curr_to_item = dist_from_curr_user.get(node_id, 0)
                similar_ext_mul = item_item_similarity(dist_curr_to_item, node_id, prev_food_item, similar_ext_mul)
            else:
                similar_ext_mul = 1

            for adj_node_id in db[node_id]['user_connections']:
            #similarity should be done here, when the user is connected, not when the user is removed
            #will figure out the specifics later\
                if not user_marked.get(adj_node_id, False):
                    fringe_deque.append(adj_node_id)
                    user_marked[adj_node_id] = True
                    dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1


                currentUserMenuWeights[latest_menu_item] = curr_user_item_pref(curr_user_id, adj_node_id, node_id, latest_menu_item, similar_ext_mul)



                if adj_node_id not in UserMenuRatings:
                    UserMenuRatings[adj_node_id] = {}
                elif node_id not in UserMenuRatings[adj_node_id]:
                    #warning: redudant computation here as computed in the curr user pref funciton already
                    UserMenuRatings[adj_node_id][node_id] = obj_user_item_pref(adj_node_id, node_id)



             #then go into the other food nodes for similar items that the user has had before
            if node_id in menu_items:

                current_food_item_marked.clear()

                # NOTE: make sure we need to be marking this menu item node
                current_food_item_marked[node_id] = True

                # checks to see if there is a previous food item (which is the extended food item) to modify similarity multiplier, otherwise multiplier is 1

                for adj_node_id in db[node_id].get('food_item_connections', {}):
                    # current_food_item_marked[adj_node_id] = True
                    #start the dfs by adding all the adjacent nodes, each one preceded by the preceding node and the similar_ext_mul up to that point
                    if adj_node_id not in menu_items:
                        fringe_deque.appendleft((similar_ext_mul, node_id))
                        fringe_deque.appendleft(adj_node_id)
                        dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1


                # this is for the case where no nodes are appended and we never go to extended food item zone
                prev_food_item = None
                # check for whether the food item is not in the menu
            else:

                #need to make srure the item hasn't been traversed already
                if not current_food_item_marked.get(node_id, False):

                    # do similarity between items test here
                    # checks to see if there is a previous food item (which is the extended food item) to modify similarity multiplier, otherwise multiplier is 1
                    # if prev_food_item:
                    #     dist_curr_to_item = dist_from_curr_user.get(node_id, 0)
                    #     similar_ext_mul = item_item_similarity(dist_curr_to_item, node_id, prev_food_item,
                    #                                            similar_ext_mul)
                    # else:
                    #     similar_ext_mul = 1
                    current_food_item_marked[node_id] = True

                    # if(not prev_food_item):



                    #CONTINUE DFS LOOKING FOR SIMILAR FOOD ITEMS (WILL SET LIMIT)
                    #make sure we limit the number of adjacent nodes
                    #MAKE SURE WE CHECK FOR MENU ITEMS FIRST
                    for adj_node_id in db[node_id]['food_item_connections']:
                        if not current_food_item_marked.get(adj_node_id, False):
                            # if debug_step == 7:
                            #     print("adjacent food node ", adj_node_id)
                            #     print('slkdjflksdjflksdjlfksjdlk')
                            #     sys.exit(1)
                            # else:
                            #     sys.exit(1)
                            if adj_node_id not in menu_items:
                                fringe_deque.appendleft((similar_ext_mul, node_id))
                                fringe_deque.appendleft(adj_node_id)

                            else:
                                fringe_deque.appendleft(adj_node_id)

                            dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1


        print("Current User Menu Weights: ")
        print(currentUserMenuWeights)
        print("Current Distances")
        print(dist_from_curr_user)

    print("\nFinal Current User Menu Weights")
    print({db[k]['info']['name']:v for (k,v) in sorted(currentUserMenuWeights.items(), key = lambda item : item[1], reverse = True)})


#Testing functions, will greatly develop in futuredist_from_curr_user = {}
#pass the currentUserMenuWeights as a paramaRter
def curr_user_item_pref(curr_user_id, user_id,food_item_id, latest_menu_item, similar_ext_mul):
        #Thoughts, perhaps we should do it so that the similarity will be based on the
        global currentMenuCount
        global dist_from_curr_user

        if latest_menu_item not in currentMenuCount:
            currentMenuCount[latest_menu_item] = 0
        else:
            print(latest_menu_item)

        dist_curr_to_item = dist_from_curr_user.get(food_item_id, 0)
        dist_curr_to_user = dist_from_curr_user.get(user_id, 0)

        print("Dist curr to user ", dist_curr_to_user)


        #NOTE NEED TO CHANGE THIS SO THERE IS DISTANCE FUNCTION FOR BOTH ITEM TO USER AND USER TO USER



        currentMenuCount[latest_menu_item] += 1

        print("________________________WEIGHT CALCULATION________________________")
        print("FOOD_ID ", food_item_id)
        print("USER_ID ", user_id)
        print("CURR USER ID ", curr_user_id)
        dist_user_based_pref = dist_based_curr_user_pref(dist_curr_to_user, curr_user_id, user_id)
        dist_item_based_pref = dist_based_user_item_pref(dist_curr_to_item, user_id, food_item_id)
        num_menu_item_count = num_menu_item_so_far(currentMenuCount[latest_menu_item], dist_menu_weight_buffer, menu_weight_growth)
        print("DIST USER BASED PREF ", dist_user_based_pref)
        print("DIST ITEM BASED PREF ", dist_item_based_pref)
        print("FIX HOW NUM MENU ITEM COUNT WORKS (MAYBE) NEEDS TO REDUCE WEIGHT AS NUM ITEMS AWAY FROM THE USER")
        print("NUM MENU ITEM COUNT ", num_menu_item_count)

        weightToAdd = dist_user_based_pref * dist_item_based_pref * num_menu_item_count * similar_ext_mul

        print("WEIGHT TO ADD ", weightToAdd)
        # weightToAdd *= (num_weight_dec_factor / currentMenuCount[latest_menu_item]*num_weight_inc_factor)

        weightSoFar = currentUserMenuWeights.get(latest_menu_item, 0)

        #no connection whatsoever, make so its as if there is no change.
        #NOTE this will be critical to figuring out how to stop (like if there are too many 0s)

        return weightSoFar + weightToAdd


def num_menu_item_so_far(menu_item_count, dist_menu_weight_buffer, menu_weight_growth):
    return inverse_sigmoid(menu_item_count, dist_menu_weight_buffer, menu_weight_growth)

#How much a particular user prefers an item, and weighted by how far away this preference is from the obj
def  dist_based_user_item_pref(dist_curr_to_item, user_id, food_item_id):

    # print("dist from user to item " , inverse_sigmoid(dist_curr_to_item, dist_item_buffer, dist_item_growth))
    print("obj _user item pref", obj_user_item_pref(user_id, food_item_id))


    # return obj_user_item_pref(user_id, food_item_id) * (dist_dec_factor / ((dist_curr_to_item + dist_buffer)*dist_inc_factor + 1))
    return obj_user_item_pref(user_id, food_item_id)  * inverse_sigmoid(dist_curr_to_item / 2, dist_user_item_buffer, dist_user_item_growth)


#change the factors that do this to user user factors
def dist_based_curr_user_pref(dist_curr_to_user, curr_user_id, user_id):
    # print("diff curr to user ", curr_user_id, user_id,dist_curr_to_user)
    # # return user_similarity(curr_user_id, user_id) * (dist_user_dec_factor / ((dist_curr_to_user + dist_buffer)*dist_user_inc_factor + 1))
    # print("DISTANCELKDJLKFLDKFJLKSDJFLKJSDLKFJLKSDF_____DISTANDCE")
    #
    # print("DIST INV SIGMOID ", inverse_sigmoid(dist_curr_to_user, dist_user_buffer, dist_user_growth))
    return user_similarity(curr_user_id, user_id) * inverse_sigmoid(dist_curr_to_user / 2, dist_user_buffer, dist_user_growth)

def inverse_sigmoid(x,inflection_point=0, growth=1):
    return 1 / (1 + math.exp(growth * (x - inflection_point)))

def sigmoid(x, inflection_point=0, growth=1):
    return 1 / (1 + math.exp((-1 * growth) * (x - inflection_point)))
#The objective preference of the user to an item
def obj_user_item_pref(user_id, food_item_id):


    #so that a "neurtral" is considered a middle rating, and this way we can add and substract to a rating
    objective_pref = (db[user_id]['food_item_connections'].get(food_item_id, -100) - (ratings_scale / 2)) / ratings_scale
    print("Objective_pref ", objective_pref)

    internalsign = 1

    if objective_pref != 0:
        sign = objective_pref / abs(objective_pref)
    else:
        sign = 1

    if objective_pref <= -20:
        internalsign = -1


    return sign * sigmoid(internalsign * abs(objective_pref), user_item_pref_buffer, user_item_pref_growth)


#how similar a user is to another
def user_similarity(user_id_1, user_id_2):
    if user_id_1 == user_id_2:
        return 1
    print("Similarity:" )
    print(db[user_id_1]['user_connections'].get(user_id_2, -100))
    return sigmoid(db[user_id_1]['user_connections'].get(user_id_2, -100), user_sim_buffer, user_sim_growth)
#functions that will be determined later
# def user_item_pref(user_id, item_id):
#     pass


#this function will be complicated enough
def item_item_similarity(dist_curr_to_item, item_id_1, item_id_2, similar_ext_mul):
    return similar_ext_mul * (db[item_id_1]['food_item_connections'].get(item_id_2, 0))
