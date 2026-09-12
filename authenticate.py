#imports
import pandas as pd
import hashlib
import os


TEACHER_FILE ="data/teachers.csv"


##########CREATE TEACHER FILE##########

def ensure_teacher_file():

    if not os.path.exists(TEACHER_FILE):

        os.makedirs("data",exist_ok=True)

        teachers =pd.DataFrame(columns=[
            "teacher_id",
            "name",
            "email",
            "password_hash",
            "tutorial_seen"
        ])

        teachers.to_csv(TEACHER_FILE,index=False)


##########LOAD TEACHERS##########

def load_teachers():

    ensure_teacher_file()

    return pd.read_csv(TEACHER_FILE)


##########HASH PASSWORD##########

def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


##########CREATE ACCOUNT##########

def create_account(name,email,password):

    teachers =load_teachers()

    name =" ".join(name.split())
    email =email.strip().lower()

    #check empty values
    if name =="":
        return False,"Please enter your name.",None

    if email =="":
        return False,"Please enter your email address.",None

    if "@" not in email:
        return False,"Please enter a valid email address.",None

    if len(password) <6:
        return False,"Password must contain at least 6 characters.",None

    #check email does not already exist
    if email in teachers["email"].astype(str).str.lower().values:
        return False,"An account already exists with this email address.",None

    #create teacher id
    if len(teachers) ==0:
        teacher_id ="T001"

    else:
        highest_number =0

        for existing_id in teachers["teacher_id"]:

            teacher_number =int(str(existing_id).replace("T",""))

            if teacher_number >highest_number:
                highest_number =teacher_number

        teacher_id ="T"+str(highest_number +1).zfill(3)

    #create new teacher
    new_teacher =pd.DataFrame([{
        "teacher_id":teacher_id,
        "name":name,
        "email":email,
        "password_hash":hash_password(password),
        "tutorial_seen":False
    }])

    teachers =pd.concat([teachers,new_teacher],ignore_index=True)
    teachers.to_csv(TEACHER_FILE,index=False)

    return True,"Account created successfully.",new_teacher.iloc[0]


##########LOGIN##########

def login_teacher(email,password):

    teachers =load_teachers()

    email =email.strip().lower()
    password_hash =hash_password(password)

    matching_teacher =teachers[
        teachers["email"].astype(str).str.lower() ==email
    ]

    if len(matching_teacher) ==0:
        return None

    teacher =matching_teacher.iloc[0]

    if teacher["password_hash"] !=password_hash:
        return None

    return teacher


##########TUTORIAL##########

def set_tutorial_seen(teacher_id,value):

    teachers =load_teachers()

    teachers.loc[
        teachers["teacher_id"] ==teacher_id,
        "tutorial_seen"
    ] =value

    teachers.to_csv(TEACHER_FILE,index=False)


##########UPDATE NAME##########

def update_teacher_name(teacher_id,new_name):

    new_name =" ".join(new_name.split())

    if new_name =="":
        return False

    teachers =load_teachers()

    teachers.loc[
        teachers["teacher_id"] ==teacher_id,
        "name"
    ] =new_name

    teachers.to_csv(TEACHER_FILE,index=False)

    return True


##########CHANGE PASSWORD##########

def change_password(teacher_id,current_password,new_password):

    teachers =load_teachers()

    teacher =teachers[
        teachers["teacher_id"] ==teacher_id
    ]

    if len(teacher) ==0:
        return False,"Account could not be found."

    stored_password =teacher["password_hash"].iloc[0]

    if stored_password !=hash_password(current_password):
        return False,"Current password is incorrect."

    if len(new_password) <6:
        return False,"New password must contain at least 6 characters."

    teachers.loc[
        teachers["teacher_id"] ==teacher_id,
        "password_hash"
    ] =hash_password(new_password)

    teachers.to_csv(TEACHER_FILE,index=False)

    return True,"Password changed successfully."