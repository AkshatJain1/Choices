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

db = {}
currentUserMenuWeights = {}

def user_item_traversal(curr_user_id, menu_items):
    fringe_deque = collections.deque()
    fringe_deque.append(curr_user_id)

    user_marked[curr_user_id] = True
    dist_from_curr_user[curr_user_id] = 0

    currentUserMenuWeights = {}
    for item in menu_items:
        currrenUserMenuWeights[item] = 0


    last_node = null
    original_user_item =

    while queue not empty:
        node_id = fringe_deque.popLeft()

        #node is a user
        #quesiton: should a user traverse other menu items they have eaten also (besides ones scanned in)
        #answer: no because if it ends up connecting from one of past menu items to current menu itesm the connection will lead back to user in the first place
        if db[node_id]['info']['type'] == 'user':
            user_id = node_id
            for menu_item in menu_items:  #need to mark the menuitem if it was traversed
                if menu_item in db[user_id]['food_item_connections']:
                    fringe_deque.append(menu_item)
                    currentUserMenuWeight[food_item_id] = curr_user_item_pref(curr_user_id, user_id, food_item_id)
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


      #IDEA: For the extended food item algorithm. As we go through the extended food item list, we keep track of the items,
      # and once we reach a user node, we go through the list of items we have added and add the user id to those
      #node is a food item
      if db[node_id]['info']['type'] == 'food_item':
          #check for whether the food item is in the menu
          if db[node_id]['info']['name'] in menu_items:
              #first go back to the users immediately if its a menu item (without intermediate nodes)
              for adj_node_id in db[node_id]['user_connections'][:limit_users]:
                  #similarity should be done here, when the user is connected, not when the user is removed
                  currentUserMenuWeight[node_id] = curr_user_item_pref(curr_user_id, user_id, food_item_id)
                  if !user_marked['node']:
                      fringe_deque.append(adj_node_id)
                      user_marked[adj_node_id] = True
                      dist_from_curr_user[adj_node_id] = dist_from_curr_user[node_id] + 1
              for adj_node_id in db[node_id]['food_item_connections'][:limit_food_items]:
                  if


         #do dfs now regardless of it being a menu item or note
         #essentially will find out whether the food item is similar to other items that any user has had before
        for adj_node_id in db[node_id]['food_item_connections'][:limit_food_items]:




          else:
              for adj_node_id in db[node_id]['connections']:










def curr_user_item_pref(curr_user_id, user_id,food_item_id):
    pass

#functions that will be determined later
# def user_item_pref(user_id, item_id):
#     pass
# def item_item_similarity(item_id_1, item_id_2):
#     pass
def user_user_similarity(user_id_1, user_id_2):
    pass
