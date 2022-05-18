import io,os
import pytesseract
import cv2
from deep_translator import GoogleTranslator 
from langdetect import detect
from google.cloud import vision_v1
from google.cloud import texttospeech_v1 #cloud api
from tkinter import ttk
#pip install google-cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_json_file/translator-346404-9fadb5fe6cc1.json'
def detect_text(path):
    """Detects text in the file."""
    client = vision_v1.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision_v1.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation.text
    string = ''
    for text in texts:
        string+='' + text
    return string

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
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Unable to access cam")
    
while(True):
    ret, frame = cap.read()
    width=int(cap.get(3))
    height=int(cap.get(4))
    img=cv2.rectangle(frame,(0,0),(width,height),(255,255,0),10)
    cv2.imshow("Frame",img)
    if cv2.waitKey(1)==ord('s'):
        file = 'live.jpg'
        cv2.imwrite(file,frame)
        val=detect_text(file)
        if len(val)==0:
            pass
        else:
            print(val.lower())
            souce_lang=detect(val)
            translated_text=GoogleTranslator(source=souce_lang, target=target_lang).translate(text=val)
            print(translated_text)
            client_1=texttospeech_v1.TextToSpeechClient()
            result=texttospeech_v1.SynthesisInput(text=translated_text)

            voice1=texttospeech_v1.VoiceSelectionParams(
                language_code=target_lang,
                ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
            )

            audio_config=texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3
            )
            response=client_1.synthesize_speech(
              input=result,
              voice=voice1,
              audio_config=audio_config
            )

            with open('audio/Temporary.mp3', 'wb') as output1:
                output1.write(response.audio_content)

            os.system("start audio/Temporary.mp3")
        key=input("enter the key q: ")
        if key=='q':
            os.remove("audio/Temporary.mp3")
            name=input("enter the audio file name: ")
            with open('audio/'+name+'.mp3', 'wb') as output1:
                 output1.write(response.audio_content)
        else:
            os.remove("audio/Temporary.mp3")
            num=input("Press the enter: ")
            os.remove(file)
    
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
