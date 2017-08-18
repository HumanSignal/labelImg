'''
For this script to work, you must have your application default credentials
set up in the Google Cloud utility (in terminal). Then, just run 'python ImageDownloader.py'.
'''

from google.cloud import storage
import os
import subprocess

def main():
    client = storage.Client()
    bucket = client.get_bucket('blobstoreforimages.appspot.com')

    folders = []
    blobs = []
    idx = 0

    # gather all the folder names in the blob store
    for blob in bucket.list_blobs():
        blobs.append(blob)
        split = blob.name.split('-')
        if split[0] not in folders:
            folders.append(split[0])
            print(str(idx) + ': ' + split[0])
            idx += 1

    if len(folders) == 0:
        print("no sets of images found")
        return

    # ask the user which folder they would like to download and label
    folderIndex = int(raw_input("Which set of images would you like to download? "))    
    folderName = folders[folderIndex]
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    # count how many images we have to download
    fileList = os.listdir(folderName)
    fileCount = 0
    for blob in blobs:
        if folderName in blob.name and blob.name not in fileList:
            fileCount += 1


    # download each image
    index = 0
    for blob in blobs:
        if folderName in blob.name and blob.name not in fileList:
            index += 1
            print("Downloading image " + str(index) + " of " + str(fileCount) + "...")
            with open(folderName + '/' + blob.name, 'wb') as f:
                blob.download_to_file(f)

    # call the image labeling script
    print("Done")
    p = subprocess.call(['python', 'labelImg.py', folderName + '/'])

if __name__ == "__main__":
    main()