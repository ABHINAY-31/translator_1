import pyrebase
config = {
        "apiKey": "AIzaSyBwppANSiabJpBpV7AfkvfmtraSV9RKxoU",
        "authDomain": "translator-346404.firebaseapp.com",
        "databaseURL": "https://translator-346404-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "projectId": "translator-346404",
        "storageBucket": "translator-346404.appspot.com",
        "messagingSenderId": "576845837678",
        "appId": "1:576845837678:web:0a37f5b036be2e026ffd7f",
        "measurementId": "G-PXQTPYMXTC",
        "serviceAccount": "key.json",
        "databaseURL": "gs://translator-346404.appspot.com" 
}
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()
choice=int(input("1. Sign Up   or    2. Login \nEnter your choice: "))
if(choice==1):
        while(1):
            id=input("enter the unique id: ")
            userdata=db.child("Info/UserData").get()
            for users in userdata.each():
                if(id==users.key()):
                   flag=0
                   print("------ alreay exist -------")
                   break
                else:
                    flag=1
            if(flag==0):
                continue
            else:
                break
        Name=input("Enter the Name: ")
        while(1):
          Email=input("Enter the Email: ")
          if(Email.find("@gmail.com")!=-1):
             break
          else:
             print("----Wrong format----")
             pass
        Password=input("Enter the Pasword: ")
        while(1):
           Confirm_Password=input("Re-Enter the Password: ")
           if(Confirm_Password==Password):
              break
           else:
              print("Re-Enter the password *** Password not matched")
              pass
        try:
           sign_up=auth.create_user_with_email_and_password(Email,Password)
           print("--------- Succesfully Signed Up ----------")
           data = {
               "Name":Name,
               "Email":Email,
               "Password":Password,
           }
           db.child('Info').child('UserData').child(id).child().set(data)
           print("\n\n-------------Service Available are----------  \n\n")
           print("1. Extaction From Image \n2. Extraction From Video\n3.Kind of At Realtime\n")
           Choice2=int(input("Choose your Preference: "))
           if(Choice2==1):
               import vision
           elif(Choice2==2):
               import video
           elif(Choice2==3):
               import realtime
        except:
            print("--------- Eamil Alrady exits ---------")
if(choice==2):
    Email=input("Enter the Email: ")
    Password=input("Enter the Password: ")
    try:
        login=auth.sign_in_with_email_and_password(Email,Password)
        print("Signed In ---- Successfuly")
        print("\n\n-------------Services Available are----------  \n\n")
        print("1. Extaction From Image \n2. Extraction From Video\n3. Kind of At Realtime\n")
        Choice2=int(input("Choose your Preference: "))
        if(Choice2==1):
            import cv2
            import os, io
            import numpy as np
            from google.cloud import vision#cloud api
            from google.cloud import translate_v2 #cloud api
            import tkinter as tk
            from tkinter import filedialog
            from google.cloud import texttospeech_v1 #cloud api
            from deep_translator import GoogleTranslator 
            from langdetect import detect
            import pyrebase
            config = {
              "apiKey": "AIzaSyBwppANSiabJpBpV7AfkvfmtraSV9RKxoU",
              "authDomain": "translator-346404.firebaseapp.com",
              "databaseURL": "https://translator-346404-default-rtdb.asia-southeast1.firebasedatabase.app/",
              "projectId": "translator-346404",
              "storageBucket": "translator-346404.appspot.com",
              "messagingSenderId": "576845837678",
              "appId": "1:576845837678:web:0a37f5b036be2e026ffd7f",
              "measurementId": "G-PXQTPYMXTC"
            }
            firebase=pyrebase.initialize_app(config)
            auth=firebase.auth()
            db=firebase.database()
            def deskew(cvImage):
                image = cvImage.copy()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.bitwise_not(gray)
                thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]#binary image
                coords = np.column_stack(np.where(thresh > 0))
                angle = cv2.minAreaRect(coords)[-1]
                if angle > 45:
                   angle=90-angle
                elif angle < -45:
                   angle = -(90 + angle)
                else:
                   angle = -angle
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(thresh, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return rotated 
            
            def noise_removal(image):
                blur = cv2.GaussianBlur(image, (0,0), sigmaX=33, sigmaY=33)
                divide = cv2.divide(image, blur, scale=255)
                output_gaus=cv2.GaussianBlur(divide,(5,5),0)
                sharpened=cv2.addWeighted(image,1.5,output_gaus,-0.5,0)
                return sharpened
            
            def langs():
                lang_file=open("D:\Project\language_support.txt","r")
                target_language=input("enter the name of language(like: Hindi): ")
                str=" "
                while(str):
                    str=lang_file.readline()
                    l=str.split()
                    if target_language in l:
                       return l[len(l)-1]
            
            def openfile():
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_json_file/translator-346404-9fadb5fe6cc1.json'#cloud vision
                #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'translator-346404-9711a44a0c12.json'#translater api
                #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'translator-346404-3378f489c654.json'#texttospeech
                client = vision.ImageAnnotatorClient()

                extensions = ("*.jpg", "*.png", "*.jpeg")
                filepath = filedialog.askopenfilename(title="Choose The Image", filetypes=(
                    ("images", extensions), ("all files", "*.*")))

                file_path = os.path.join(filepath)

                with io.open(file_path, 'rb') as image_file:
                    content = image_file.read()
    
                image = vision.Image(content=content)
                response = client.document_text_detection(image=image)
    
                Text = response.full_text_annotation.text
                print(Text)
                souce_lang=detect(Text)
                
                #translate
                file=cv2.imread(filepath)
                new_img=deskew(file)
                new_img = cv2.bitwise_not(new_img)
                #image processing ------
                noise=noise_removal(new_img)
                height = noise.shape[0]
                width = noise.shape[1]
                if height > 1000 or width >1000:
                   height=400
                   width=400
                   dsize = (width, height)
                   output = cv2.resize(noise, dsize)
                else:
                   height=height+int((noise.shape[0]/100)*30)
                   width=width+int((noise.shape[1]/100)*30)
                   dsize = (width, height)
                   output = cv2.resize(noise, dsize)
                cv2.imshow("image",output)
    
                target_lang=langs()
                translated_text=GoogleTranslator(source=souce_lang, target=target_lang).translate(text=Text)
                print(translated_text)
                """trans=translate_v2.Client()
                file=cv2.imread(filepath)
                cv2.imshow("image",file)
                target_lang=langs()
                output=trans.translate(Text,target_language=target_lang)
                #print('\n'u'{}'.format(output['detectedSourceLanguage']))
                print("\n---------translated text in native language---------\n")
                print(u'{}'.format(output['translatedText']))"""
                #text to Speech
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
                   cv2.waitKey(100)
                   storage=firebase.storage()
                   userdata=db.child("Info/UserData").get()
                   for users in userdata.each():
                        value = users.val()['Email']
                        if(value==Email):
                           Key_value=users.key()
                           break
                   storage.child(Key_value+ '/' + name+'.mp3').put('audio/'+ name + '.mp3')
                else:
                   os.remove("audio/Temporary.mp3")
            root =tk.Tk()
            root.withdraw()
            openfile()
            
        elif(Choice2==2):
            import video

        elif(Choice2==3):
            import io,os
            import pytesseract
            import cv2
            from deep_translator import GoogleTranslator 
            from langdetect import detect
            from google.cloud import vision_v1
            from google.cloud import texttospeech_v1 #cloud api
            from tkinter import ttk
            import pyrebase
            config = {
              "apiKey": "AIzaSyBwppANSiabJpBpV7AfkvfmtraSV9RKxoU",
              "authDomain": "translator-346404.firebaseapp.com",
              "databaseURL": "https://translator-346404-default-rtdb.asia-southeast1.firebasedatabase.app/",
              "projectId": "translator-346404",
              "storageBucket": "translator-346404.appspot.com",
              "messagingSenderId": "576845837678",
              "appId": "1:576845837678:web:0a37f5b036be2e026ffd7f",
              "measurementId": "G-PXQTPYMXTC"
            }
            firebase=pyrebase.initialize_app(config)
            auth=firebase.auth()
            db=firebase.database()
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
                           cv2.waitKey(100)
                           storage=firebase.storage()
                           userdata=db.child("Info/UserData").get()
                           for users in userdata.each():
                               value = users.val()['Email']
                               if(value==Email):
                                   Key_value=users.key()
                                   break
                           storage.child(Key_value+ '/' + name+'.mp3').put('audio/'+ name + '.mp3')
                       else:
                           os.remove("audio/Temporary.mp3")
                           num=input("Press the enter: ")
                           os.remove(file)
                if cv2.waitKey(1)==ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

    except:
        print("-------- Wrong Email ---------")