import sys

"""
Function Name: createList
Input: categories,caching_query_by_category,caching_query_by_item
Output : void
Function Operation: takes the file, and using it to create the given categories dicunary.  
"""
def createList(categories, file):
    for line in file:
        if(line == "\n"):
            return
        products_and_prices = dict()
        category, products_prices_list = [x.lstrip() for x in line.split(":")]
        for x in products_prices_list.split(";"):
            if(not x == '\n' and not len(x) == 0):
                product_name = x.split(",")[0].lstrip()
                product_price =  x.split(",")[1].lstrip().split("\n")[0]
                products_and_prices[product_name] = product_price
        
        categories[category] = products_and_prices

"""
Function Name: purchase_an_item
Input: categories,dict_query_1,dict_query_2
Output: nothing
Function Operation: asks the user to enter his input(a product name)
                    and if the product doesnt exists is the shop, prints 
                    a massage, else removes the products from all the 
                    categories that he is in.
"""
def purchase_an_item(categories,dict_query_1,dict_query_2):
    user_input = input().lstrip()
    flag = False
    for category in categories.values():
        if(user_input in category):
            price = category[user_input]
            category.pop(user_input)
            flag = True
    if(not flag):
        print("Error: no such item exists.")
    else:
        print("You bought a brand new \"" + user_input + "\" for " + price + "$.")
        dict_query_1.clear()
        dict_query_2.clear()

"""
Function Name: query_by_item
Input: categories,caching_query_by_item
Output: void
Function Operation: asks the user to enter an item,
                    if the product doesnt exists is the shop, prints 
                    a massage. else if the products does axists, print all the products
                    which shair the same categorie with the given input product (in a sorted order).
"""
def query_by_item(categories,caching_query_by_item):
    newList = []
    flag = False
    user_input = input().lstrip()
    for category in categories.values():
            if(user_input in category and user_input in caching_query_by_item.keys()):
                print("Cached: " + str(caching_query_by_item[user_input]))
                return
            elif (user_input in category):
                newList += [x for x in category.keys() if(x != user_input and not x in newList)]
                flag = True
    if(not flag):
        print("Error: no such item exists.")
    else:
        print(sorted(newList))
        caching_query_by_item[user_input] = sorted(newList)

"""
Function Name: printMenu
Input: nothing
Output: void
Function Operation: prints the main menu
"""
def printMenu():
    print("Please select an operation:")
    print("\t0. Exit.")
    print("\t1. Query by category.")
    print("\t2. Query by item.")
    print("\t3. Purchase an item.")
    print("\t4. Admin panel.")

"""
Function Name: inputChoice
Input: categories,caching_query_by_category,caching_query_by_item
Output
Function Operation:
"""
def query_by_category(categories, caching_query_by_category):
    user_input_before = input()
    user_input = [x.lstrip() for x in user_input_before.split(",")]
    if(len(user_input) >= 3):
        for i in range (3,len(user_input)):
            user_input[2] += user_input[i]
    if not len(user_input) >= 3:
        print("Error: not enough data.")
        return
    elif not user_input[0] in categories or not user_input[1] in categories:
        print("Error: one of the categories does not exist.")
        return
    elif not (user_input[2] == "&" or user_input[2] == "|" or user_input[2] == "^"):
        print("Error: unsupported query operation.")
        return
    operator = user_input[2]
    products_categorie_one = set(categories[user_input[0]].keys())
    products_categorie_two = set(categories[user_input[1]].keys())
    if((user_input[0] + "," + user_input[1] +","+operator) in caching_query_by_category.keys()):
        print("Cached: " + str(caching_query_by_category[user_input[0] + "," + user_input[1] +","+operator]))
    else:
        if operator == "&":
            answer = sorted(list(products_categorie_one & products_categorie_two))
        elif operator == "|":
            answer = sorted(list(products_categorie_one | products_categorie_two))
        elif operator == "^":
            answer = sorted(list(products_categorie_one ^ products_categorie_two))

        print(answer)
        caching_query_by_category[user_input[0] + "," + user_input[1] +","+operator] = answer
        caching_query_by_category[user_input[1] + "," + user_input[0] +","+operator] = answer

"""
Function Name: inputChoice
Input: categories
Output : void
Function Operation: gets the categories dictunary (which is the main
                    dictunary on it all of the store data is saved)
                    and creates a new text file (which her name is inputed by the user 
                    in the complilation line), writes in the new text file the 
                    stores data (sorted)
"""
def output(categories):
    file = open(sys.argv[3], "w")
    keys = list(categories.keys())
    keys.sort()
    for category in keys:
        file.write(category + ":")
        a = list(categories[category].keys())
        a.sort()
        for product in a:
            file.write(" " + product + ", " + categories[category][product] + ";")
        file.write("\n")
    file.close()
    print("Store saved to \"" + sys.argv[3] + "\".")


"""
Function Name: inputChoice
Input: categories,caching_query_by_category,caching_query_by_item
Output
Function Operation:
"""
def print_admin_panel_menu():
    print("Admin panel:")
    print("\t0. Return to main menu.")
    print("\t1. Insert or update an item.")
    print("\t2. Save.")


"""
Function Name: inputChoice
Input: categories,caching_query_by_category,caching_query_by_item
Output
Function Operation:
"""
def add_update_product(categories, caching_query_by_category, caching_query_by_item):
    user_input = input()
    if(not ":" in user_input):
        print("Error: not enough data.")
        return
    user_input = user_input.split(":",1)
    input_categories, product = user_input
    input_categories = [x.lstrip() for x in input_categories.split(",")]
    if(len(input_categories) == 0):
        print("Error: not enough data.")
        return
    product =  [x.lstrip() for x in product.split(",",1)]
    if(len(product) < 2):
        print("Error: not enough data.")
        return
    for cat in input_categories:
        if(not cat in categories):
            print("Error: one of the categories does not exist.")
            return
    if(not product[1].isnumeric()):
        print("Error: price is not a positive integer.")
        return
    for cat in categories.keys():
        if(cat in input_categories):
            categories[cat][product[0]] = product[1]
        elif product[0] in categories[cat].keys():
            categories[cat][product[0]] = product[1]
    print("Item \"" + product[0] + "\" added.")
    caching_query_by_category.clear()
    caching_query_by_item.clear()

"""
Function Name: inputChoice
Input: categories,caching_query_by_category,caching_query_by_item
Output
Function Operation:
"""
def admin_panel(categories, caching_query_by_category, caching_query_by_item):
    #file  = open("admin.txt")
    file  = open(sys.argv[2])
    password = input("Password: ")
    if(password == file.readline()):
        print_admin_panel_menu()
        user_choice = input()
        while(user_choice != '0'):
            if(user_choice == '1'):
                add_update_product(categories, caching_query_by_category, caching_query_by_item)
            elif(user_choice == '2'):
                output(categories)
            elif (not user_choice == '0'):
                print("Error: unrecognized operation.")
            print_admin_panel_menu()
            user_choice = input()
    else:
        print("Error: incorrect password, returning to main menu.")

"""
Function Name: inputChoice
Input: categories,caching_query_by_category,caching_query_by_item
Output: void
Function Operation: get the input from the user and doing the requaired task
"""
def inputChoice(categories,caching_query_by_category,caching_query_by_item):
    x = input()
    if(x == '0'):
        exit()
    elif (x == '1'):
        query_by_category(categories, caching_query_by_category)
    elif (x == '2'):
        query_by_item(categories, caching_query_by_item)
    elif (x == '3'):
        purchase_an_item(categories , caching_query_by_item, caching_query_by_category)
    elif (x == '4'):
        admin_panel(categories , caching_query_by_item, caching_query_by_category)
    else:
        print("Error: unrecognized operation.")


def main():
    categories = dict()
    caching_query_by_category = dict()
    caching_query_by_item = dict()
    file = open(sys.argv[1], "r")
    createList(categories, file)
    while(True):
        printMenu()
        inputChoice(categories, caching_query_by_category,caching_query_by_item)
    file.close()
    
if __name__ == '__main__':
  main()
