import collections
import json



L = 5
K = 5
limit_users = 10
limit_food_items = 10   #calcula
constant1 = 1

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




with open('server/traversal_test_1.json') as f:
    db = json.load(f)


currentUserMenuWeights = {}
dist_from_curr_user = {}
#menu_items are id's of the menu items
def user_item_traversal(curr_user_id, menu_items):
    currentUserMenuWeights = {}


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
        if db[node_id]['info']['type'] == 'user':
            for menu_item in menu_items:  #need to mark the menuitem if it was traversed
                #check to see if user is the current user or if the user has eaten the menu item or not
                if curr_user_id == node_id or menu_item in db[node_id]['food_item_connections']:
                    if menu_item_marked.get(menu_item, False) == False:
                        fringe_deque.append(menu_item)
                        menu_item_marked[menu_item] = True
                        dist_from_curr_user[menu_item] = dist_from_curr_user[node_id] + 1
                    # currentUserMenuWeight[food_item_id] = curr_user_item_pref(curr_user_id, user_id, food_item_id, weightSoFar)
                    #dist_from_curr_user[node_id] = dist_from_curr_user[menu_item] + 1
      #IDEA TO BE IMPLEMENTED: For the extended food item algorithm. As we go through the extended food item list, we keep track of the items,
      # and once we reach a user node, we go through the list of items we have added and add the user id to those. The connection will have some magnitude edge value as well

        elif db[node_id]['info']['type'] == 'food_item':
            for adj_node_id in db[node_id]['user_connections']:
            #similarity should be done here, when the user is connected, not when the user is removed
            #will figure out the specifics later
                if node_id in menu_items:
                    #will change soon so that it checks for cached, just to get barebone working (clear )
                    current_food_item_marked.clear()

                currentUserMenuWeights[node_id] = curr_user_item_preference(curr_user_id, adj_node_id, node_id)
                if not user_marked[adj_node_id]:
                    fringe_deque.append(adj_node_id)
                    user_marked[adj_node_id] = True
                    dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1
             #then go into the other food nodes for similar items that the user has had before
            if node_id in menu_items:

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

    print("Final Current User Menu Weights")
    print({db[k]['info']['name']:v for (k,v) in sorted(currentUserMenuWeights.items(), key = lambda item : item[1], reverse = True)})


#Testing functions, will greatly develop in future
#pass the currentUserMenuWeights as a paramaRter
def curr_user_item_preference(curr_user_id, user_id,food_item_id):
        return currentUserMenuWeights.get(food_item_id, 0) + user_item_preference(user_id, food_item_id)

def user_item_preference(user_id, food_item_id):
    print(dist_from_curr_user)
    objective_preference = db[user_id]['food_item_connections'].get(food_item_id, 0)
    return objective_preference * (constant1 / (dist_from_curr_user[user_id] + 1))



#functions that will be determined later
# def user_item_pref(user_id, item_id):
#     pass
def item_item_similarity(item_id_1, item_id_2):
    pass
def user_user_similarity(user_id_1, user_id_2):
    pass


#Traversal Test 1
#Will hard code user preferences for certain menu items already
#Assume that all the items are on the menu, and that the user has only had that particular food item at that point of time
#Assume that we are not considering similar items (including items that are just the item without any restaurant)
user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6"])
