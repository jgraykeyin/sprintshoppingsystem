# Python Shopping System Admin Program
# Sprint Week Project #3 November 2020 (Bonus)
# Program that allows a user to view the daily sales of a selected date
# and allows the user to view a graph of total daily sales.

import boto3
import os
import matplotlib.pyplot as plt


# Setting the path for the current direction
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def downloadAllDirectoriesFroms3(bucketName):
    '''
    Description: Downloads all directories from an S3 bucket and creates a bar
    graph with the sales data of all receipts contained in the directories.
    Parameters:
        bucketName - Name of the S3 bucket
    Returns: 
        Path of the generated daily-sales bar graph
    '''    
    dir_list = []

    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)
    
    # Create a local directory for each directory that exists in the S3 bucket, 
    # then download the contens of directory.
    for obj in bucket.objects.all():
        if not os.path.exists(os.path.dirname(os.path.join(__location__,obj.key))):
            os.makedirs(os.path.dirname(os.path.join(__location__,obj.key)))
        bucket.download_file(obj.key, os.path.join(__location__,obj.key))
        
        # Make sure the directory is a daily receipts folder by matching the '20' from 2020-11-09/ for example.
        # Keep a list of directory names so we can graph them as the days
        dirname = os.path.dirname(obj.key)
        if "20" in dirname:
            dir_list.append(dirname)
    
    # Get the daily sales from each day and save them into a list, so we can graph them!        
    sales=[]
    for d in dir_list:
        daily_sales = get_sales_for_day(d)
        sales.append(daily_sales[1])
    
    
    # Graph those daily sales mixed with the date strings, it's going to look so pretty!
    plt.bar(dir_list,sales, label="Sales in CAD")
    plt.legend()
    plt.xlabel('Days')
    plt.ylabel('Dollars')
    plt.savefig(os.path.join(__location__,'dailysales.png'))
    plt.show()
    
    graph_path = os.path.join(__location__,'dailysales.png')
    return graph_path

    

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    '''
    Description: Downloads a directory and all it's contents from an S3 bucket
    Parameters:
        bucketName - Name of the S3 bucket
        remoteDirectoryName - Name of the directory to be downloaded
    Returns: 
        Name of the directory downloaded
    '''
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(os.path.join(__location__,obj.key))):
            os.makedirs(os.path.dirname(os.path.join(__location__,obj.key)))
        bucket.download_file(obj.key, os.path.join(__location__,obj.key))
        
    return os.path.dirname(obj.key)
    
def get_sales_for_day(user_date):
    '''
    Description: Calculate the total daily sales of a chosen date by reading 
    each receipt in a directory matching the date.
    Parameters:
       user_date - Directory name containing receipts thats named after the date
    Returns: 
        List containing date and total sale value
    '''    

    # Download a directory and all it's receipts
    sales = downloadDirectoryFroms3("keyinshoppingsystem",user_date)

    # Create the full path of the receipt folder
    receipt_path = os.path.join(__location__,sales)

    # Read the last line of each receipt, strip out the transaction total so it can 
    # be added to our new total variable
    total = 0
    for filename in os.listdir(receipt_path):
        with open(os.path.join(receipt_path, filename), 'r') as f:
            
            file_lines = f.readlines()
            last_line = file_lines[-1]
            items = last_line.split("$")
            r_total = float(items[-1].strip("\n"))
            total += r_total
            
    sale_data = [sales,total]
    return sale_data       
    
# Start the main program loop and prompt which type of report they want to use
print("Shopping System Admin Panel\n")
while True:
    
    print("[1] - View total sales for a specific date")
    print("[2] - View a graph of the daily sales\n")
    user_select = int(input("Please select an option #: "))
    
    if user_select == 1:
        # TODO: Validate input
        user_date = input("Please enter requested date (YYYY-MM-DD): ")
        
        sales = get_sales_for_day(user_date)
        
        print("\nTotal sales for {}: ${}\n".format(sales[0],sales[1]))
        
    elif user_select == 2:
        
        sales_graph = downloadAllDirectoriesFroms3("keyinshoppingsystem")
        print("\nYou can find the sales graph in the folder:\n{}\n".format(sales_graph))

