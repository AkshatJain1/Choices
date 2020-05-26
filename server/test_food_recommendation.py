from food_recommendation import user_item_traversal

#NOTE: match the corresponding json file with the test Name
#NOTE: will model all ratings on 1 to 5 scale

#NOTE:Traversal Test 1
#Add in a user
#Will hard code user preferences for certain menu items already
#Assume that all the items are on the menu, and that the user has only had that particular food item at that point of time
#Assume that we are not considering similar items (including items that are just the item without any restaurant)
#Maximum Levels Traversed: 1
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6"])

#NOTE:raversal Test 2
#Same as Traversal Test 1
#Will also add in Another User, Akshat, who unrealistically has a similarity of "1", or exactly the same as currentUser, Pranav
#Akshat will have had Pizza, an item that Pranav has not already had
#Maximum Levels Traversed: 2
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
#output:
# Final Current User Menu Weights
# {'Hot Dog': 10.0, 'Pizza': 5.0, 'Chicken Sandwhich': 3.75, 'Cheeseburger': 3.75, 'Hamburger': 3.0, 'Chili Cheese Fries': 2.75}

#NOTE:Traversal Test 3
#Same as Traversal Test 2
#Will make the weights more realistic, with Akshat only bearing "0.7" similarity to Pranav
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
#output:
#Final Current User Menu Weights
# {'Hot Dog': 10.0, 'Chicken Sandwhich': 3.75, 'Cheeseburger': 3.75, 'Pizza': 3.5, 'Hamburger': 3.0, 'Chili Cheese Fries': 2.75}

#NOTE:Traversal Test 4
#Same as Traversal Test 3
#Let's say Pranav already had pizza, and didn't like it (1.5 star weight)
#This should decrase it more than there being "just" Akshat's opinion on the pizza being good
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
#output:
# Final Current User Menu Weights
# {'Hot Dog': 10.0, 'Pizza': 5.5, 'Chicken Sandwhich': 3.75, 'Cheeseburger': 3.75, 'Hamburger': 3.0, 'Chili Cheese Fries': 2.75}

#NOTE:Traversal Test 5
#Same as Traversal Test 4
#Let's say Pranav already had pizza, and kinda liked it (3 star weight)
#This should be higher than traversal 3, as he's kinda into it and could try it again
#Pranav still likes hot dog by a whole star above this, so hot dog should be above it
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"])
#Final Output:
# Final Current User Menu Weights
# {'Hot Dog': 10.0, 'Pizza': 9.25, 'Chicken Sandwhich': 3.75, 'Cheeseburger': 3.75, 'Hamburger': 3.0, 'Chili Cheese Fries': 2.75}
