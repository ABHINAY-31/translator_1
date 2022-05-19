import pyrebase
config = {
    
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
            userdata=db.child("Info/UserData").get()
            for users in userdata.each():
                if(id==users.key()):
                    uid=id
                    break
            import vision
        elif(Choice2==2):
            import video
        elif(Choice2==3):
            import realtime
    except:
        print("-------- Wrong Email ---------")