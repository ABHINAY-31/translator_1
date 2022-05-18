import cv2
import os, io
import tkinter as tk
from tkinter import filedialog
from google.cloud import vision_v1
from deep_translator import GoogleTranslator 
from langdetect import detect

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_json_file/translator-346404-9fadb5fe6cc1.json'
def langs():
    lang_file=open("D:\Project\language_support.txt","r")
    target_language=input("enter the name of language(like: Hindi): ");
    str=" "
    while(str):
       str=lang_file.readline()
       l=str.split()
       if target_language in l:
          return l[len(l)-1]
      
      
target_lang=langs() 
target_lang=target_lang
root =tk.Tk()
root.withdraw()
extensions=("*.webn", "*.mpg","*.mp2","*.mpeg","*.mp4","*.m4p","*.m4v","*.swf","*.wmv","*.avi")
filepath= filedialog.askopenfilename(title="Choose The Image", filetypes=(
        ("images", extensions), ("all files", "*.*")))
capture=cv2.VideoCapture(filepath)
len=int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
currentFrame=0
Frame_count=80

while(currentFrame<len):
    ret, frame=capture.read()
    name=str(currentFrame)+'.jpg'    
    cv2.imwrite('images/'+name,frame)
    client = vision_v1.ImageAnnotatorClient() 
    file_name = os.path.join(os.path.dirname(__file__),
                'images/'+name)
    with io.open(file_name, 'rb') as image_file:        
        content = image_file.read()  
   
    image = vision_v1.Image(content=content)
    response = client.document_text_detection(image=image)
    Text = response.full_text_annotation.text
    if currentFrame==0:
        print(Text)
        souce_lang=detect(Text)
        translated_text=GoogleTranslator(source=souce_lang, target=target_lang).translate(text=Text)
        print(translated_text)
        print()
    elif Text==label:
        pass
    else:
        print(Text)
        souce_lang=detect(Text)
        translated_text=GoogleTranslator(source=souce_lang, target=target_lang).translate(text=Text)
        print(translated_text,'\n')
    label=Text
    currentFrame += Frame_count 
    os.remove('images/'+name) 
    capture.set(1,currentFrame)  
    cv2.destroyAllWindows()