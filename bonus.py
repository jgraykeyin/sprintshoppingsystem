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

