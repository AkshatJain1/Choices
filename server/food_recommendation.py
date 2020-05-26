import collections
import json
import sys
import math
#NOTE: THE RECOMMENDATION SHOULD NOT ONLY BE WEIGHTED BY DISTANCE FROM USER, BUT MUCH MORE SO BY THE DIFFERENCE IN THE CURRENTMENUWEIGHT AND THE THE WEIGHT OF THE USER

L = 5
K = 5
limit_users = 10
limit_food_items = 10   #calcula
#distancefactor
dist_inc_factor = 1
dist_dec_factor = 5
#incrase to have more effect by the distance

dist_buffer = 1
#controls how much distance needs to be to start making a large effect on the weight

num_weight_inc_factor = 1
num_weight_dec_factor = 1
#how much affect that the amount of times we've run into a menu item and added it through preferences

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


db = {}
with open('server/traversal_test_5.json') as f:
    db = json.load(f)

currentUserMenuWeights = {}
currentMenuCount = {}
dist_from_curr_user = {}
#menu_items are id's of the menu items
def user_item_traversal(curr_user_id, menu_items):
    global currentUserMenuWeights
    global currentMenuCount
    global UserMenuRatings
    currentUserMenuWeights = {}
    currentMenuCount = {}
    UserMenuRatings = {}
    #NOTE: this user menu ratings thing may/may not be useless
    dist_from_curr_user = {}

    latest_menu_item = None

    fringe_deque = collections.deque()
    fringe_deque.append(curr_user_id)

    user_marked = {}
    menu_item_marked = {}
    current_food_item_marked = {}

    user_marked[curr_user_id] = True
    dist_from_curr_user[curr_user_id] = 0





    #using this to figure out the intermediate connections, instead of directly doing to user at hand, seems unnecessary tho cuz its iterative and not recursive
    # userMenuWeights = {{}}


    #set the menu_items all to 0
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
                #check to see if user is the current user or if the user has eaten the menu item or not
                if curr_user_id == node_id or menu_item in db[node_id]['food_item_connections']:
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
            for adj_node_id in db[node_id]['user_connections']:
            #similarity should be done here, when the user is connected, not when the user is removed
            #will figure out the specifics later\
                if not user_marked.get(adj_node_id, False):
                    fringe_deque.append(adj_node_id)
                    user_marked[adj_node_id] = True
                    dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1


                dist_curr_to_user = dist_from_curr_user.get(adj_node_id, 0)
                print("Dist curr to user ", dist_curr_to_user)
                currentUserMenuWeights[node_id] = curr_user_item_pref(dist_curr_to_user, curr_user_id, adj_node_id, node_id, latest_menu_item)
                if adj_node_id not in UserMenuRatings:
                    UserMenuRatings[adj_node_id] = {}
                elif node_id not in UserMenuRatings[adj_node_id]:
                    #warning: redudant computation here as computed in the curr user pref funciton already
                    UserMenuRatings[adj_node_id][node_id] = obj_user_item_pref(adj_node_id, node_id)
             #then go into the other food nodes for similar items that the user has had before
            if node_id in menu_items:
                current_food_item_marked.clear()

                for adj_node_id in db[node_id].get('food_item_connections', {}):
                    #CODE INSERT HERE: marking needs to be done
                    current_food_item_marked[adj_node_id] = True
                    if adj_node_id not in menu_items:
                        fringe_deque.appendleft(adj_node_id)
                        dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1

                        #check for whether the food item is in the menu
            else:
              if not current_food_item_marked[node_id]:
                  #do similarity between items test here
                  current_food_item_marked[node_id] = True
                  for adj_node_id in db[node_id]['food_item_connections']:
                      if not current_food_item_marked[adj_node_id]:
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
def curr_user_item_pref(distance, curr_user_id, user_id,food_item_id, latest_menu_item):
        #Thoughts, perhaps we should do it so that the similarity will be based on the
        global currentMenuCount
        if latest_menu_item not in currentMenuCount:
            currentMenuCount[latest_menu_item] = 0

        distance_based_pref = dist_based_user_item_pref(distance, user_id, food_item_id)

        if distance_based_pref != 0:
            currentMenuCount[latest_menu_item] += 1
            weightToAdd = (user_similarity(curr_user_id, user_id) * distance_based_pref) * (num_weight_dec_factor / currentMenuCount[latest_menu_item]*num_weight_inc_factor)
        else:
            weightToAdd = 0

        return currentUserMenuWeights.get(food_item_id, 0) + weightToAdd

#How much a particular user prefers an item, and weighted by how far away this preference is from the obj
def  dist_based_user_item_pref(dist_curr_to_user, user_id, food_item_id):

    print("dist from " + user_id, dist_curr_to_user)
    return obj_user_item_pref(user_id, food_item_id) * (dist_dec_factor / ((dist_curr_to_user + dist_buffer)*dist_inc_factor + 1))

#The objective preference of the user to an item
def obj_user_item_pref(user_id, food_item_id):
    return db[user_id]['food_item_connections'].get(food_item_id, 0)

#how similar a user is to another
def user_similarity(user_id_1, user_id_2):
    if user_id_1 == user_id_2:
        return 1
    print("Similarity:" )
    print(db[user_id_1]['user_connections'].get(user_id_2, 0))
    return db[user_id_1]['user_connections'].get(user_id_2, 0)
#functions that will be determined later
# def user_item_pref(user_id, item_id):
#     pass
def item_item_similarity(item_id_1, item_id_2):
    pass
