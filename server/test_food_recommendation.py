from food_recommendation import user_item_traversal

#NOTE: match the corresponding json file with the test Name
#NOTE: will model all ratings on 0 to 4 scale, as that makes most sense mathematically

#Traversal Test 1
#Add in a user
#Will hard code user preferences for certain menu items already
#Assume that all the items are on the menu, and that the user has only had that particular food item at that point of time
#Assume that we are not considering similar items (including items that are just the item without any restaurant)
#Maximum Levels Traversed: 1
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6"])

#Traversal Test 2
#Same as Traversal Test 1
#Will also add in Another User, Akshat, who unrealistically has a similarity of "1", or exactly the same as currentUser, Pranav
#Akshat will have had Pizza, an item that Pranav has not already had
#Maximum Levels Traversed: 2
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
#output:
# Final Current User Menu Weights
# {'Hot Dog': 4.0, 'Pizza': 4.0, 'Chicken Sandwhich': 1.5, 'Cheeseburger': 1.5, 'Hamburger': 1.2, 'Chili Cheese Fries': 1.1}

#Traversal Test 3
#Same as Traversal Test 2
#Will make the weights more realistic, with Akshat only bearing "0.3" similarity to Pranav
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])

#Traversal Test 4
#Same as Traversal Test 3
#Let's say Pranav already had pizza, and didn't like it (0.5 weight)
user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
# Final Output:
# Final Current User Menu Weights
# {'Hot Dog': 4.0, 'Chicken Sandwhich': 1.5, 'Cheeseburger': 1.5, 'Hamburger': 1.2, 'Chili Cheese Fries': 1.1, 'Pizza': 0.39999999999999997}

#Traversal Test 5
#Same as Traversal Test 3
#Let's say Pranav already had pizza, and kinda liked it (3)
user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
