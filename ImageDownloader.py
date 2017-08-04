from google.cloud import storage
import os
import subprocess

def main():
    client = storage.Client()
    bucket = client.get_bucket('blobstoreforimages.appspot.com')

    folders = []
    blobs = []
    idx = 0

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

    folderIndex = int(raw_input("Which set of images would you like to download? "))    
    folderName = folders[folderIndex]
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    for blob in blobs:
        if folderName in blob.name:
            with open(folderName + '/' + blob.name, 'wb') as f:
                blob.download_to_file(f)

    p = subprocess.call(['python', 'labelImg.py', folderName + '/'])

if __name__ == "__main__":
    main()