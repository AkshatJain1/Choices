import collections
import user


L = 5
K = 5
limit_users = 10
limit_food_items = 10   #calcula

#d
#might need to include foodWeights in actual function iself
#will definitely incorporate dynamic programming into this afterwards (cacheing)
#database dictionary will actually put in later


#notes

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


db = {}
currentUserMenuWeights = {}




#menu_items are id's of the menu items
def user_item_traversal(curr_user_id, menu_items):
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
        currrenUserMenuWeights[item] = 0

    # last_user = null
    # last_food_item = null

    while fringe_deque not empty:
        node_id = fringe_deque.popLeft()

        #node is a user
        #quesiton: should a user traverse other food items they have eaten also (besides ones scanned in)
        #answer: no because if it ends up connecting from one of past menu items to current menu itesm the connection will lead back to user in the first place
        if db[node_id]['info']['type'] == 'user':
            for menu_item in menu_items:  #need to mark the menuitem if it was traversed
                #check to see if user has eaten the menu item or not
                if curr_user_id == node_id or menu_item in db[node_id]['food_item_connections']:
                    if !menu_item_marked[menu_item]:
                        fringe_deque.append(curr_user_id)
                        menu_item_marked = True
                        dist_from_curr_user[menu_item] = dist_from_curr_user[node_id] + 1
                    fringe_deque.append(menu_item)
                    # currentUserMenuWeight[food_item_id] = curr_user_item_pref(curr_user_id, user_id, food_item_id, weightSoFar)
                    dist_from_curr_user[user_id] = dist_from_curr_user[menu_item] + 1
      #IDEA TO BE IMPLEMENTED: For the extended food item algorithm. As we go through the extended food item list, we keep track of the items,
      # and once we reach a user node, we go through the list of items we have added and add the user id to those. The connection will have some magnitude edge value as well

        elif db[node_id]['info']['type'] == 'food_item':
            for adj_node_id in db[node_id]['user_connections'][:limit_users]:
            #similarity should be done here, when the user is connected, not when the user is removed
            #will figure out the specifics later
                if node_id in menu_items:
                    #will change soon so that it checks for cached, just to get barebone working (clear )
                    current_food_item_marked.clear()

                currentUserMenuWeight[node_id] = curr_user_item_preference(curr_user_id, adj_node_id, food_item_id)
                if !user_marked[adj_node_id]:
                    fringe_deque.append(adj_node_id)
                    user_marked[adj_node_id] = True
                    dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1

             #then go into the other food nodes for similar items that the user has had before
            if node_id in menu_items:

               for adj_node_id in db[node_id]['food_item_connections'][:limit_food_items]:
                   #CODE INSERT HERE: marking needs to be done
                   if adj_node_id not in menu_items:
                       fringe_deque.appendLeft(adj_node_id)
                       dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1

          #check for whether the food item is in the menu
            else:
              if !current_food_item_marked[node_id]:
                  #do similarity between items test here
                  current_food_item_marked[node_id] = True
                  for adj_node_id in db[node_id]['food_item_connections'][:limit_food_items]
                      if !current_food_item_marked[adj_node_id]:
                          fringe_deque.appendLeft(adj_node_id)
                          dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1




def curr_user_item_preference(curr_user_id, user_id,food_item_id):
    if (curr_user_id == user_id):


def user_item_preference(user_id, food_item_id):
    pass

#functions that will be determined later
# def user_item_pref(user_id, item_id):
#     pass
def item_item_similarity(item_id_1, item_id_2):
    pass
def user_user_similarity(user_id_1, user_id_2):
    pass
