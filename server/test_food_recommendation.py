from food_recommendation import user_item_traversal

#NOTE: match the corresponding json file with the test Name
#NOTE: will model all ratings on 1 to 5 scale

#NOTE:Traversal Test 1
#Add in a user
#Will hard code user preferences for certain menu items already
#Assume that all the items are on the menu, and that the user has only had that particular food item at that point of time
#Assume that we are not considering similar items (including items that are just the item without any restaurant)
#Maximum Levels Traversed: 1
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6"], 'traversal_test_1.json')
# Final Current User Menu Weights
# {'Hot Dog': 0.6981909851282292, 'Chicken Sandwhich': 0.26182161942308596, 'Cheeseburger': 0.26182161942308596, 'Hamburger': 0.20945729553846879, 'Chili Cheese Fries': 0.19200252091026307}}

#NOTE:raversal Test 2
#Same as Traversal Test 1
#Will also add in Another User, Akshat, who unrealistically has a similarity of "1", or exactly the same as currentUser, Pranav
#Akshat will have had Pizza, an item that Pranav has not already had
#Maximum Levels Traversed: 2
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"], 'traversal_test_2.json')
#output:
# Final Current User Menu Weights
# {'Hot Dog': 0.6981909851282292, 'Pizza': 0.6164889243616287, 'Chicken Sandwhich': 0.26182161942308596, 'Cheeseburger': 0.26182161942308596, 'Hamburger': 0.20945729553846879, 'Chili Cheese Fries': 0.19200252091026307}


#NOTE:Traversal Test 3
#Same as Traversal Test 2
#Will make the weights more realistic, with Akshat only bearing "0.7" similarity to Pranav
# user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"], 'traversal_test_3.json')
#output:
# Final Current User Menu Weights
#{'Hot Dog': 0.8900511103067338, 'Pizza': 0.8589619180206469, 'Chicken Sandwhich': 0.1976269181812553, 'Cheeseburger': 0.1976269181812553, 'Hamburger': 0.13930051704432594, 'Chili Cheese Fries': 0.12334896247558523}


#NOTE:Traversal Test 4
#Same as Traversal Test 3
#Let's say Pranav already had pizza, and didn't like it (1.5 star weight)
#This should decrase it more than there being "just" Akshat's opinion on the pizza being good
#user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"], 'traversal_test_4.json')
#output:
# Final Current User Menu Weights
#{'Hot Dog': 0.8900511103067338, 'Chicken Sandwhich': 0.1976269181812553, 'Cheeseburger': 0.1976269181812553, 'Pizza': 0.1686255137387421, 'Hamburger': 0.13930051704432594, 'Chili Cheese Fries': 0.12334896247558523}

#NOTE:Traversal Test 5
#Same as Traversal Test 4
#Let's say Pranav already had pizza, and kinda liked it (3 star weight)
#The's kinda into it and could try it again
#Pranav still likes hot dog by a whole star above this, so hot dog should be above it
#user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"], 'traversal_test_5.json')
#Final Output:
# Final Current User Menu Weights
#{'Hot Dog': 0.9880671556260959, 'Pizza': 0.7736783907595969, 'Chicken Sandwhich': 0.04738051460946453, 'Cheeseburger': 0.04738051460946453, 'Hamburger': 0.019821330271982386, 'Chili Cheese Fries': 0.014759901665130094}


#NOTE:Traversal Test 6:
#Example 2 on poaper
#Let's say Pranav hasn't had Pizza at Restuaraunt a, but Akshat has had pizza
#at Restuaraunt B and liked it. Since Akshat and Pranav are 0.7 similar, it should influence his decision
#to consider Pizza as an option. Since Akshat really liked it, it's likeley that Pizza is a good choice.
user_item_traversal("NodeID1", ["NodeID2","NodeID3","NodeID4","NodeID5","NodeID6", "NodeID7"], 'traversal_test_6.json')
# Final Current User Menu Weights
#{'Hot Dog': 0.9865228106817597, 'Pizza': 0.47679864834946273, 'Chicken Sandwhich': 0.04730645905789546, 'Cheeseburger': 0.04730645905789546, 'Hamburger': 0.01979034961340948, 'Chili Cheese Fries': 0.014736831998877502}