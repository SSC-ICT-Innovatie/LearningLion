import csv
import json
import os
from threading import Thread
import threading
import requests
from interface.dataSource import dataSource
from data_classes.kamerVragenData import KamerVragenData
from typing import List
import mimetypes

from PyPDF2 import PdfWriter, PdfReader

class KamerVragen(dataSource):
    url = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$filter=Verwijderd eq false and Soort eq 'Antwoord schriftelijke vragen'"
    urlLIMITED = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$filter=Verwijderd eq false and Soort eq 'Antwoord schriftelijke vragen' and (year(DatumRegistratie) eq 2024 and month(DatumRegistratie) ge 1 and day(DatumRegistratie) ge 1) and (year(DatumRegistratie) eq 2024 and month(DatumRegistratie) lt 9)"
    urlAfter2010 = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document?$filter=Verwijderd eq false and Soort eq 'Antwoord schriftelijke vragen' and year(DatumRegistratie) gt 2010"
    downloadurlTemplate = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document({0})/resource"
    documenturlTemplate = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document({0})"
    limit: int
    targetfolder = "kamervragen_files"
    limitDisabled = False
    dataitems: List[KamerVragenData] = []
    threads:List[Thread] = []
    threadLimit = 20
    totalItems = 0
    soorten:dict[str, int] = {}
    
    def __init__(self, limit):
        self.limit = limit
        self.totalItems = 0
    
    def _fetchDataPagenated(self, url):
        """Fetch data from the API pagenated"""
        print("Fetching pagenated data")
        response = requests.get(url)
        thread = None
        if(response.status_code == 200):
            rawData = response.json()
            if self.limitDisabled or len(self.dataitems)  <= self.limit:
                if rawData.get('@odata.nextLink'):
                    if(len(self.threads) < self.threadLimit):
                        print("Starting new thread")
                        thread = Thread(target=self._fetchDataPagenated, args=(rawData.get('@odata.nextLink'),))
                        thread.start()
                        self.threads.append(thread)
                for rawItem in rawData['value']:
                    if(self.limitDisabled == False and len(self.dataitems) >= self.limit):
                        break
                    dataitem = self._fetchKamerVragenData(rawItem)
                    if(dataitem == None):
                        continue
                    self.dataitems.append(dataitem)
                    print(f"Total items: {len(self.dataitems)}")
                # if max threads is reached, fetch the next page in the main thread
                if self.limitDisabled or len(self.dataitems) < self.limit:
                    if(thread == None and rawData.get('@odata.nextLink')):
                        self._fetchDataPagenated(rawData.get('@odata.nextLink'))
            

                    
    def _fetchKamerVragenData(self, rawData, downloadFile = True, path=None):
        """Construct a KamerVragenData object from the raw data"""
        if(self.limitDisabled == False and len(self.dataitems) > self.limit):
            return
        dataitem = KamerVragenData(rawData['Id'], rawData['GewijzigdOp'], rawData['Verwijderd'], rawData['Datum'], rawData['Soort'])
        if downloadFile:
            self.fetchFile(dataitem.id, path)
        return dataitem
    
    def fetchAllData(self):
        """Fetch all data from the API. The limit parameter is used to limit the amount of items fetched can be go over the limit due to multithreading"""
        if(self.limit < 1):
            self.limitDisabled = True
        response = requests.get(self.urlLIMITED)
        thread = None
        
        if(response.status_code == 200):
            rawData = response.json()
            if self.limitDisabled or len(self.dataitems) + len(self.threads) <= self.limit:
                if rawData.get('@odata.nextLink'):
                    # Check if max threads is reached
                    if(len(self.threads) < self.threadLimit):
                        print("Starting new thread")
                        thread = Thread(target=self._fetchDataPagenated, args=(rawData.get('@odata.nextLink'),))
                        thread.start()
                        self.threads.append(thread)
            for rawItem in rawData['value']:
                dataitem = self._fetchKamerVragenData(rawItem)
                self.dataitems.append(dataitem)
                print(f"Added item {dataitem.id}")
                print(f"Total items: {len(self.dataitems)}")
                if(self.limitDisabled == False or len(self.dataitems) >= self.limit):
                    break
            print(f"Total items: {len(self.dataitems)}")
            print(f"Limit: {self.limit}")
            print(f"Limit disabled: {self.limitDisabled}")
            # if max threads is reached, fetch the next page in the main thread
            if self.limitDisabled or len(self.dataitems) < self.limit:
                if(thread == None and rawData.get('@odata.nextLink')):
                    self._fetchDataPagenated(rawData.get('@odata.nextLink'))
            
        return self.dataitems
      
    def fetchFile(self, fileId, path=None):
        """Download a single file from the API"""
        sidecar_csv = "metadata.csv"
        
        if path == None:
            if(os.path.exists(self.targetfolder) == False):
                os.mkdir(self.targetfolder)
        else:
            if(os.path.exists(path) == False):
                os.makedirs(path)
        
        url = self.downloadurlTemplate.format(fileId)
        response_meta = requests.get(self.documenturlTemplate.format(fileId))
        if(response_meta.status_code != 200):
            print(f"Failed to fetch metadata for file {fileId}")
            return
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            extension = mimetypes.guess_extension(content_type)
            if extension:
                filename = f"{fileId}{extension}"
            else:
                filename = f"{fileId}"
            if path == None:
                filename = os.path.join(self.targetfolder, filename)
            else:
                filename = os.path.join(path, filename)
            
            if(os.path.exists(filename)):
                print(f"File {filename} already exists")
                return
            
            print(f"Downloading file {filename}")
            filenametemp = filename
            if(filename.endswith(".pdf")):
                filenametemp = filename.replace(".pdf", ".temp")
            with open(filenametemp, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        
            if(extension == ".pdf"):
                response_meta_body = response_meta.json()
                
                pdfwriter = PdfWriter()
                reader = PdfReader(filenametemp)
                
                for page in reader.pages:
                    pdfwriter.add_page(page)
                

                metadata_pdf = {
                    "/Title": f"{response_meta_body['Titel']}",
                    "/Subject": f"{response_meta_body['Onderwerp']}",
                    "/Producer": f'File downloaded from {url}',
                }
                # Write metadata to the PDF
                pdfwriter.add_metadata(metadata_pdf)
                
                with open(filename, "wb") as f:
                    pdfwriter.write(f)
                os.remove(filenametemp)
                
                file_exists = os.path.isfile(sidecar_csv)
                
                metadata = {
                    "id": fileId,
                    "Subject": f"{response_meta_body['Onderwerp']}",
                    "Title": f"{response_meta_body['Titel']}",
                    "Source": f'{url}',
                    
                }
                
                with open(sidecar_csv, mode='a', newline='', encoding='utf-8') as csv_file:
                    fieldnames = ["id", "Title", "Subject","Source"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    
                    # Write the metadata to the CSV
                    writer.writerow(metadata)

            print(f"File downloaded successfully as {filename}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
        
        
    def getTotalItemsInApi(self):
        """Fetch the total number of items in the API"""
        url = self.urlLIMITED
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                responseJson = response.json()
                page_items = len(responseJson['value'])
                
                self.totalItems += page_items
                print(f"Fetched {page_items} items, total is now {self.totalItems}")
                url = responseJson.get('@odata.nextLink')
            else:
                print(f"Failed to fetch data from {url}, status code: {response.status_code}")
                break

        print(f"Total items fetched: {self.totalItems}")
        return self.totalItems


    def getAllTypes(self, url=None, downloadFiles=False, downloadTypes=None):
        """Fetch all types of Kamervragen and download the files"""
        if url is None:
            url = self.urlLIMITED
        pagenumber = 1

        while url:
            print(f"Fetching page #{pagenumber}")
            print("has total items: ", len(self.soorten))
            response = requests.get(url)
            
            if response.status_code == 200:
                rawData = response.json()
                for rawItem in rawData['value']:
                    dataitem = self._fetchKamerVragenData(rawItem, False)
                    if self.soorten.get(dataitem.soort) is None:
                        self.soorten[dataitem.soort] = 1
                        if downloadFiles or (downloadTypes and dataitem.soort in downloadTypes):
                            self.fetchFile(dataitem.id, "{}/".format(self.targetfolder) + dataitem.soort.replace("/", "-"))
                    else:
                        self.soorten[dataitem.soort] += 1
                    if (downloadTypes and dataitem.soort in downloadTypes):
                            self.fetchFile(dataitem.id, "{}/".format(self.targetfolder) + dataitem.soort.replace("/", "-"))

                url = rawData.get('@odata.nextLink')
                pagenumber += 1
            else:
                # Handle the case where the request failed
                print(f"Failed to fetch data. Status code: {response.status_code}")
                break

        print(f"Soorten: {self.soorten}")
        self.soorten = dict(sorted(self.soorten.items(), key=lambda item: item[1], reverse=True))
        # write to file
        with open("soorten.json", "w") as file:
            json.dump(self.soorten, file, indent=4)

        
    def exit(self):
        """Join all threads before exiting"""
        for thread in self.threads:
            thread.join()
        print("All threads joined")