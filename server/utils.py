X_FACTOR = 1
Y_FACTOR = 10000
FONTSIZE_FACTOR = 10000000



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

def closest(s, s_height, food_list):
    return min(food_list, key = lambda element: X_FACTOR*((s.bounding_poly.vertices[0].x - element[next(iter(element))][2])**2)+ Y_FACTOR * ((s.bounding_poly.vertices[0].y - element[next(iter(element))][1])**2) + FONTSIZE_FACTOR * abs(s_height - element[next(iter(element))][0]))

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