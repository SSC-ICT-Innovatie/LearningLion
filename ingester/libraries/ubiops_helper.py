import os
import requests
import ubiops

APIKEY = "Token XXXX"

class UbiopsHelper:
    @staticmethod
    def uploadfile(file_path, dest_path, retry=0):
        if os.environ["local"] == "true":
            raise ValueError("Cannot upload file in local mode")
        configuration = ubiops.Configuration()
        configuration.api_key['Authorization'] = APIKEY
        configuration.host = "https://api.ubiops.com/v2.1"

        api_client = ubiops.ApiClient(configuration)
        core_api = ubiops.CoreApi(api_client)

        project_name = 'learning-lion' # str
        bucket_name = 'default' # str
        filename = file_path.split("/")[-1]
        print(f"filename: {filename}")
        print(f"file_path: {file_path}")
        if "#" in configuration.api_key['Authorization']:
            print(f"Uploading file from {file_path} to {dest_path}")
            print("Please replace the placeholder API token with your actual API token")
            # save locally
            with open(file_path, 'rb') as file:
                with open(os.path.join(dest_path,filename), 'wb') as dest_file:
                    dest_file.write(file.read())
            return False
        print(file_path)
        api_response = core_api.files_upload(project_name, bucket_name, filename)
        print(f"api response {api_response}")
        upload_url = api_response.url
        print("uploading to bucket  ")
        with open(file_path, 'rb') as file:
            headers = {'Content-Type': 'application/octet-stream'}
            response = requests.put(upload_url, data=file, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
              print(f"Successfully uploaded {file_path}")
            else:
              print(f"Failed to upload {file_path}, status code: {response.status_code}")
              print("retrying...")
              print(f"retry count: {retry}")
              if(retry > 3):
                return False
              return UbiopsHelper.uploadfile(file_path, dest_path, retry=retry+1)
        return True
    @staticmethod
    def downloadfile(filename:str,project_name, bucket_name,output_folder="./"):
        if os.environ["local"] == "true":
            raise ValueError("Cannot download file in local mode")
        print(f"Downloading file: {filename}")
        print(f"output_folder: {output_folder}")
        configuration = ubiops.Configuration()
        configuration.api_key['Authorization'] = APIKEY
        configuration.host = "https://api.ubiops.com/v2.1"

        api_client = ubiops.ApiClient(configuration)
        core_api = ubiops.CoreApi(api_client)

        try:
            if(filename.endswith("/")):
                return False
            checkfilename = filename.split("/")[-1]
            print(f"Downloading file: {checkfilename}")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            file_path = os.path.join(output_folder, checkfilename)
            if os.path.isfile(file_path):
                return True
            ubiops.utils.download_file(
            api_client,
            project_name,
            bucket_name,
            file_name=filename,
            output_path=output_folder
            )
        except Exception as e:
            print(f"Error while downloading file: {e}")
            return False
    @staticmethod
    def listFilesInBucket(project_name, bucket_name):
        if os.environ["local"] == "true":
            raise ValueError("Cannot list files in local mode")
        configuration = ubiops.Configuration()
        configuration.api_key['Authorization'] = APIKEY
        api_client = ubiops.ApiClient(configuration)
        core_api = ubiops.CoreApi(api_client)
        api_response = core_api.files_list(project_name, bucket_name, limit=1000)
        return api_response
    @staticmethod
    def download_folder(project_name, bucket_name, folder_path, output_folder):
        if os.environ["local"] == "true":
            raise ValueError("Cannot download folder in local mode")
        print("params")
        print(f"project_name: {project_name}")
        print(f"bucket_name: {bucket_name}")
        print(f"folder_path: {folder_path}")
        print(f"output_folder: {output_folder}")
        configuration = ubiops.Configuration()
        configuration.api_key['Authorization'] = APIKEY
        api_client = ubiops.ApiClient(configuration)
        core_api = ubiops.CoreApi(api_client)
        api_response = core_api.files_list(project_name, bucket_name, limit=1000)
        downloads = 0
        for file in api_response.files:
            print("Checking file: ", file.file)
            if file.file.startswith(folder_path):
                print("Downloading file: ", file.file)
                UbiopsHelper.downloadfile(file.file, project_name, bucket_name, output_folder)
                downloads += 1
        print(f"Downloaded {downloads} files from {folder_path}")
        return True
        
        


        