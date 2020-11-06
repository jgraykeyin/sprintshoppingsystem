# Python Shopping System by Team 2-9
# Sprint Week Project #3 November 2020
# Program that allows users to select items from a list of available products.
# User can then choose an amount for each product until they're done shopping.
# Receipt is printed and posted to S3 bucket at the end of program.

# TODO: Calculate totals from all receipts on a given date (new program to do this)
# TODO: Graph totals from each day (probably another program for this)

import boto3
import os
import uuid

# Set file location to current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Setup empty lists to hold our product and purchase data
products = []
purchases = []
current_qty = 0
current_price = 0


# Establish a connection to AWS S3
s3 = boto3.resource("s3")
bucket = s3.Bucket("keyinshoppingsystem")


# Download the products file and the defaults file from our S3 bucket
bucket.download_file("products.dat",os.path.join(__location__,"products.dat"))
bucket.download_file("defaults.cfg",os.path.join(__location__,"defaults.cfg"))


# Read the contents of the defaults.cfg file and assign the values to variables
dfile = open(os.path.join(__location__,"defaults.cfg"), "r")
hst_rate = float(dfile.readline())
discount_rate = float(dfile.readline())
dfile.close()


# Read the list of products from file and save them into a list
data = open(os.path.join(__location__,"products.dat"), "r")

# Read each line of the file and then iterate through the list of lines
data_contents = data.readlines()
for line in data_contents:

    # Split the string into pieces and store into line_contents list
    line_contents = line.split(":")
    
    # Check for any newline strings
    if "\n" in line_contents[2]:
        line_contents[2] = line_contents[2].strip("\n")
    
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
        print("  Quantity Remaining: {}\n".format(item["qty"]))


def formatDollar(dollar_value):
    '''
        Description: Format a float value to a string which
        includes the $ character so it can be aligned properly in a receipt
        Returns a string ie (125.50 [int] -> $125.50 [string])
    '''
    '{:.2f}'.format(round(dollar_value, 2))
    value_formatted = "{:.2f}".format(round(dollar_value,2))
    value_formatted = "$" + str(value_formatted)
    return value_formatted
    

# Display the Store's Hello Message
print("HELLO, WELCOME TO BOBBY’S STORE. THE PRODUCTS WE HAVE ON SALE ARE THE FOLLOWING:")


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
                
                for p in products:
                    if p["name"].lower() == purch_d["name"].lower():
                        p["qty"] = current_qty - user_qty

                break
            else:
                continue
            
    # Check to see if the user is done buying products
    keep_shopping = input("Would you like to continue shopping? (yes or no): ")

    if keep_shopping.lower() == "no":
        break 

# Open a file to save a user receipt 
r = open(os.path.join(__location__,"receipt.txt"),"w")

subtotal = 0

# Print all the purchased item info into a receipt
print("{:>19}\n".format("RECEIPT"))
r.write("{:>19}\n\n".format("RECEIPT"))

for purchase in purchases:

    price_formatted = formatDollar(purchase["price"])
    print("{:<8} * {:<10} {:>7}".format(purchase["name"].upper(),purchase["qty"],price_formatted))
    r.write("{:<8} * {:<10} {:>7}\n".format(purchase["name"].upper(),purchase["qty"],price_formatted))
   
    # Increment our subtotal by adding the price of each purchase
    subtotal += float(purchase["price"])
    
    
# Calculate the HST & Total
hst = subtotal * hst_rate
discount = 0

if subtotal > 100:
    discount = subtotal * discount_rate
    subtotal_discounted = subtotal - discount
    total = subtotal_discounted + hst
else:
    total = subtotal + hst

subtotal_formatted = formatDollar(subtotal)
hst_formatted = formatDollar(hst)
total_formatted = formatDollar(total)

if subtotal > 100:
    print("\nYou're eligible for a {}% discount \ndue to an order order $100.00".format(discount_rate*100))
    r.write("\nYou're eligible for a {}% discount \ndue to an order order $100.00\n".format(discount_rate*100))
    discount_formatted = formatDollar(discount)
    subtotal_discounted_formatted = formatDollar(subtotal_discounted)

print("\n{:<10} {:>18}".format("SUBTOTAL:",subtotal_formatted))
print("{:<10} {:>18}".format("TAX:",hst_formatted))

r.write("\n{:<10} {:>18}\n".format("SUBTOTAL:",subtotal_formatted))
r.write("{:<10} {:>18}\n".format("TAX:",hst_formatted))

if subtotal > 100:
    print("{:<10} {:>18}".format("DISCOUNT:", discount_formatted))
    print("hello")
    print("{:<10} {:>14}".format("DISC SUBTOTAL:", subtotal_discounted_formatted))
    r.write("{:<10} {:>18}\n".format("DISCOUNT:", discount_formatted))
    r.write("{:<10} {:>14}\n".format("DISC SUBTOTAL:", subtotal_discounted_formatted))
    
print("{:<10} {:>18}".format("TOTAL:", total_formatted))
r.write("{:<10} {:>18}\n".format("TOTAL:", total_formatted))

r.close()

# Update the quantities of our products list
data = open(os.path.join(__location__,"products.dat"), "w")
for item in products:
    data.write("{}:{}:{}\n".format(item["name"],item["price"],item["qty"]))
    #print("{}:{}:{}\n".format(item["name"],item["qty"],item["price"]))
data.close()

uuid_string = str(uuid.uuid4().hex)
receipt_filename = "receipt_"+uuid_string+".txt"

# Upload the receipt and products to our selected S3 Bucket
bucket.upload_file(os.path.join(__location__,"products.dat"),"products.dat")
bucket.upload_file(os.path.join(__location__,"receipt.txt"),receipt_filename)

# Just being polite
print("\n\nThanks for using our Python Shopping System, have a good day!")