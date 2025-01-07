from enum import Enum
import os
import shutil
import tempfile
import zipfile

import requests
import ubiops

from data_classes.range_enum import Range
from classes.kamervragen import KamerVragen

class Deployment:
    def __init__(self, base_directory=None, context=None):
        print("Datafetcher class initialized")
    
    def request(self, data, context):
        bucketName = None
        range = None
        print("Data: ", data)  
        if("bucketname" in data):
            bucketName = data["bucketname"]
        if(data['range']):
            print("range is in data", data['range'])
            if(data['range'] not in Range.__members__):
                return {
                    "output": "Invalid range"
                }
            range = Range[data['range']]
            print("range is ", range)
        if(data["action"] == "kamervragen"):
            return {
                "output": self.kamervragen(bucketName=bucketName, range=range)
            }
        return {
            "output": "No action"
        }
    def getZipName(self, range):
        if range is not None:
            return f'downloaded_files_{range.name}.zip'  # Path to the zip file to upload
        else:
            return 'downloaded_files.zip'  # Path to the zip file to upload

    
    def kamervragen(self,range=Range.Large, bucketName="kamervragen"):
        print(f"Range is {range}")
        # TODO: Remove bucketName from the function signature
        kamervragen = KamerVragen(100, bucketName)
        files = kamervragen.getAllTypes(downloadTypes=['Antwoord schriftelijke vragen'], range=range)
        print(f"Downloaded {len(files)} files")
        print(f"Files: {files[:5]}")
        # Create the zip file directly without using a temporary directory
        zip_filename = self.getZipName(range=range)
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file_info in files:
                file_path = file_info["file"]  # Extract the path
                
                # Ensure the file exists before adding
                if os.path.isfile(file_path):
                    print(f"Adding {file_path} to zip file")
                    zipf.write(file_path, os.path.basename(file_path))  # Add file with its basename
                else:
                    print(f"File not found and skipped: {file_path}")

        print(f"Files have been zipped successfully! Archive created at: {zip_filename}")
        
        if(os.environ["local"] == "true"):
            return True
        ratelimit = 300
        configuration = ubiops.Configuration()
        configuration.api_key['Authorization'] = "Token XXXXX"
        configuration.host = "https://api.ubiops.com/v2.1"

        api_client = ubiops.ApiClient(configuration)
        core_api = ubiops.CoreApi(api_client)

        project_name = 'learning-lion'  # Project name
        bucket_name = 'default'            # Bucket name
        zip_file_path = self.getZipName(range=range)

        try:
            print(f"Uploading file: {zip_file_path}")
            
            # Get the URL and provider details from the API
            api_response = core_api.files_upload(project_name, bucket_name, os.path.basename(zip_file_path))
            
            # Access the upload URL from the FileUploadResponse object
            upload_url = api_response.url  # Assuming api_response has an attribute 'url'
            
            # Open the zip file and make the PUT request
            with open(zip_file_path, 'rb') as file:
                headers = {'Content-Type': 'application/octet-stream'}
                response = requests.put(upload_url, data=file, headers=headers)
            
            # Check if the upload was successful
            if response.status_code == 200 or response.status_code == 201:
                print(f"Successfully uploaded {zip_file_path}")
            else:
                print(f"Failed to upload {zip_file_path}, status code: {response.status_code}")

        except Exception as e:
            print(f"Error uploading file {zip_file_path}: {e}")

        # Close the connection after the file is uploaded
        api_client.close()
        print("API connection closed.")
        
        return True