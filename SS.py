# Sprint Week Project #3

# Read the list of products from file and save them into a list
data = open("products.dat", "r")
products = []
current_qty = 0
current_price = 0

# Read each line of the file and then iterate through the list of lines
data_contents = data.readlines()
for line in data_contents:

    # Split the string into pieces and store into line_contents list
    line_contents = line.split(":")
    
    # Create a dictionary for the product details to be stored inside a list
    d = {"name":line_contents[0],"price":line_contents[1],"qty":line_contents[2]}
    products.append(d)
data.close()


def showProducts():
    '''
        Description: Display the list of available products 
        along with price and qty
    '''
    for item in products:
        print("{}:".format(item["name"].capitalize()))
        print(" Price : ${}".format(item["price"]))
        print("  Quantity Remaining: {}\n".format(item["qty"].rstrip("\n")))


def formatDollar(dollar_value):
    '''
        Description: Format a float value to a string which
        includes the $ character so it can be aligned properly in a receipt
        Returns a string ie (125.50 [int] -> $125.50 [string])
    '''
    '{:.2f}'.format(round(2606.89579999999, 2))
    value_formatted = "{:.2f}".format(round(dollar_value,2))
    value_formatted = "$" + str(value_formatted)
    return value_formatted
    

# Display the Store's Hello Message
print("HELLO, WELCOME TO BOBBY’S STORE. THE PRODUCTS WE HAVE ON SALE ARE THE FOLLOWING:")

# Create an empty list to save all the user purchases
purchases = []

# Start a loop to ask the user for their purchases until they decide to quit
while True:

    # Show the list of products each time the prompt appears
    showProducts()
    
    # Ask the user to input a valid product name that matches a product in our file
    while True:
        user_product = input("Enter a product name from the list above: ")

        # Loop through the dictionary items in the product list to find a matching product
        match=0
        for item in products:
            if user_product.lower() == item["name"]:
                # Flag the prodct as being matched so we can break the loop
                match = 1
                # Get the qty & price of matching product, we'll need that in the next section
                current_qty = int(item["qty"])
                current_price = float(item["price"])
        
        if match == 1:
            break
        else:
            print("Please enter a valid product name")    
        
    # Get the qty of the product, must not be less than 0 or more than qty in file
    while True:

        user_qty = int(input("Enter quantity of {}: ".format(user_product)))
        
        if (user_qty < 0) or (user_qty > current_qty):
            print("Please enter a value between 0 and {}".format(current_qty))
        else:
            # Get the total item price (product * qty)
            itemprice = current_price * user_qty
    
            print("Total price for this product will be ${:.2f}".format(itemprice))
            confirm_qty = input("Are you sure you want to purchase {} {}? (yes or no): ".format(user_qty,user_product))

            if confirm_qty.lower() == "yes":
                
                # Add purchases to the list so we can track total purchases
                purch_d = {"name":user_product,"qty":user_qty,"price":itemprice}
                purchases.append(purch_d)
                
                break
            else:
                continue
            
    # Check to see if the user is done buying products
    keep_shopping = input("Would you like to continue shopping? (yes or no): ")

    if keep_shopping.lower() == "no":
        break 
        
subtotal = 0

# Print all the purchased item info into a receipt
# TODO: Fix the formatting so it'll look nicer
print("RECEIPT\n")
for purchase in purchases:
    #print("Product: {} Qty: {} Price: ${:.2f}".format(purchase["name"],purchase["qty"],float(purchase["price"])))
    print("{:<10} * {:<1} {:>10.2f}".format(purchase["name"].upper(),purchase["qty"],purchase["price"]))
    
    subtotal += float(purchase["price"])
    
# Calculate the HST & Total
hst = subtotal * 0.15
total = subtotal + hst

subtotal_formatted = formatDollar(subtotal)
hst_formatted = formatDollar(hst)
total_formatted = formatDollar(total)

print("\n{:<10} {:>10}".format("SUBTOTAL:",subtotal_formatted))
print("{:<10} {:>10}".format("HST:",hst_formatted))
print("{:<10} {:>10}".format("TOTAL:", total_formatted))

'''
Receipt example:

        RECEIPT
        
FROZEN PIZZA * 3    $88.99
FROZEN PIZZA * 2    $33.33

SUBTOTAL:           $223.22
TAX:                $10.99
TOTAL:              $222.22
'''