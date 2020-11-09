import boto3
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Function to download all files from a directory that matches the date supplied by user
def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        #print(os.path.dirname(obj.key))
        if not os.path.exists(os.path.dirname(os.path.join(__location__,obj.key))):
            os.makedirs(os.path.dirname(os.path.join(__location__,obj.key)))
        bucket.download_file(obj.key, os.path.join(__location__,obj.key)) # save to same path
        
    return os.path.dirname(obj.key)

user_date = input("Please enter requested date (YYYY-MM-DD): ")

sales = downloadDirectoryFroms3("keyinshoppingsystem",user_date)

print("Downloaded receipts for {}".format(sales))

receipt_path = os.path.join(__location__,sales)
print(receipt_path)

total = 0
for filename in os.listdir(receipt_path):
   with open(os.path.join(receipt_path, filename), 'r') as f:
       file_lines = f.readlines()
       last_line = file_lines[-1]
       items = last_line.split("$")
       r_total = float(items[-1].strip("\n"))
       total += r_total
       
print("Total sales for {}: ${:.2f}".format(sales,total))
