import os
import re
from gtts import gTTS 
# from gtts import *
import os 
PATH = os.path.join(os.getcwd(),'D:\Projects\google_ocr1\code\ocrecog-bfb80e71bf67.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=PATH
import json
        # import re
from google.cloud import vision
from google.cloud import storage
storage_client = storage.Client()  
class model:
    def __init__(self,filename):
        self.file_name=filename
        
    def custom_model(self):
        self.upload_file(self.file_name)
        self.convert_pdf_to_txt()
        self.text_to_audio()
    def upload_file(self,filename):
        UPLOADFILE = os.path.join(os.getcwd(), filename)
        bucket = storage_client.get_bucket('ocr_files_project')
        blob = bucket.blob(filename)
        blob.upload_from_filename(UPLOADFILE)
        print('done')
    def convert_pdf_to_txt(self):
        bucket_name = 'ocr_files_project'
        blob_name = self.file_name
        gcs_source_uri=("gs://{}/{}".format(bucket_name,blob_name))
        gcs_destination_uri=gcs_source_uri.replace('.pdf',"_result ")


        # Supported mime_types are: 'application/pdf' and 'image/tiff'
        mime_type = 'application/pdf'

        # How many pages should be grouped into each json output file.
        batch_size = 1

        client = vision.ImageAnnotatorClient()

        feature = vision.Feature(
            type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

        gcs_source = vision.GcsSource(uri=gcs_source_uri)
        input_config = vision.InputConfig(
            gcs_source=gcs_source, mime_type=mime_type)

        gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
        output_config = vision.OutputConfig(
            gcs_destination=gcs_destination, batch_size=batch_size)

        async_request = vision.AsyncAnnotateFileRequest(
            features=[feature], input_config=input_config,
            output_config=output_config)

        operation = client.async_batch_annotate_files(
            requests=[async_request])

        print('Waiting for the operation to finish.')
        operation.result(timeout=900)

        # Once the request has completed and the output has been
        # written to GCS, we can list all the output files.
        

        match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
        bucket_name = match.group(1)
        prefix = match.group(2)

        bucket = storage_client.get_bucket(bucket_name)

        # List objects with the given prefix.
        blob_list = list(bucket.list_blobs(prefix=prefix))
        print('Output files:')
        self.text_file=self.file_name.replace('.pdf','')
        for blob in blob_list:
            print(blob)
            blb_name=blob.name
            # Process the first output file from GCS.
            # Since we specified batch_size=2, the first response contains
            # the first two pages of the input file.
        

            json_string = blob.download_as_string()
            response = json.loads(json_string)
        

            # The actual response for the first page of the input file.
            for resp in range(0,1):

                first_page_response = response['responses'][resp]
                annotation = first_page_response['fullTextAnnotation']

                # Here we print the full text from the first page.
                # The response contains more information:
                # annotation/pages/blocks/paragraphs/words/symbols
                # including confidence scores and bounding boxes
                # print(annotation['text']) 
                with open("{}.txt".format(self.text_file), "a",encoding='utf-8') as file_object:
                    # Append 'hello' at the end of file
                    file_object.write(annotation['text'])
            blob.delete()
            print("deleted {}".format(blb_name))
        with open('{}.txt'.format(self.text_file), 'r',encoding='utf-8') as file:
            self.mytext= file.read()
        self.mytext = re.sub("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", self.mytext)# remove HREF
        self.mytext = re.sub("[\w\.-]+@[\w\.-]+", "", self.mytext)# remove mail
        self.mytext=re.sub("\*x*","",self.mytext)#for *
        #self.mytext=re.sub("[\d,\d,]+","",self.mytext)
        #self.mytext=re.sub("[A-Z,a-z]+:","",self.mytext)
        #x = re.findall("[Fig]+\-[1-9]", self.mytext)
        self.mytext=re.sub("[Fig]+\-[1-9]","",self.mytext)# remove fig
        self.mytext=re.sub("[fig]+\-[1-9]","",self.mytext)

        self.mytext=re.sub("[Fig]+\:\-[1-9]","",self.mytext)
        self.mytext=re.sub("[fig]+\:\-[1-9]","",self.mytext)

        self.mytext=re.sub("[Fig]+\:[1-9]","",self.mytext)
        self.mytext=re.sub("[fig]+\:[1-9]","",self.mytext)
        #self.mytext=re.sub("[IVXLCM]+\.|[ivxlcm]+\.","",self.mytext)# roman char

        self.mytext=re.sub("[0-9]+\)","",self.mytext)# to remove num bullets
        self.mytext=re.sub("\[[0-9]+\]","",self.mytext) # to remove  ref num
        os.remove("{}.txt".format(self.text_file))

        print('deleting {}.txt'.format(self.text_file))

    def text_to_audio(self):
        language = 'en'
    # print(self.mytext)
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
        myobj = gTTS(text=self.mytext, lang=language, slow=False) 
    
    # Saving the converted audio in a mp3 file named 
    # welcome  
        myobj.save("{}.mp3".format(self.text_file))
        print('Now playing music') 
        # os.system("{}.mp3".format(self.text_file)) 

# Import the required module for text  
# to speech conversion 

  
# This module is imported so that we can  
# play the converted audio 

# self.text_file='book.txt'
# The text that you want to convert to audio 

  
# Playing the converted file 
    

