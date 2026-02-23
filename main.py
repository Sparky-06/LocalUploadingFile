from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import uuid
import os
import datetime
import json


ALLOWED_TYPES = ["image/jpg", "image/jpeg", "image/png", "application/pdf",
                 "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                 "text/plain"]
    

MAX_SIZE  = 10*1024*1024  #10MB





app = FastAPI()



def all_uploaded_files():
    dir_files = [f.split('_', 1)[-1] if '_' in f else None for f in os.listdir("uploads")]
    return dir_files





@app.post("/upload")
async def singl_upload(file : UploadFile  = File(...)):


    #CONTENT TYPE VALIDATION
    if file.content_type not in ALLOWED_TYPES:
        return {"Error" : f"{file.content_type} is not allowed."}
    

    #REUPLOAD FILTER
    all_files = all_uploaded_files()
    if file.filename in all_files:
        return {"Error" : f"File with name  \"{file.filename}\" already exists."}


    #SIZE FILTER
    file_size = await file.read()
    if(len(file_size) > MAX_SIZE):
        return {"Error" : "File size is too large"}
    
    await file.seek(0)

    if not os.path.exists("metadata.json"):
        with open("metadata.json", "w") as fp:
            fp.write('[]')
    

    file_loc = f"uploads/{uuid.uuid4()}_{file.filename}"
    with open (file_loc, "wb") as fp:
        shutil.copyfileobj(file.file, fp)


        with open("metadata.json", "r") as fp:
            meta_data = json.load(fp)
            meta_data.append({
                "name" : file.filename,
                "size" : len(file_size),
                "upload_time" : datetime.datetime.now().isoformat(),
                "type" : file.content_type
            })

        with open("metadata.json", "w") as fp:
            json.dump(meta_data, fp, indent=4)

    return {
        "File_name" : file.filename, "File_type" : file.content_type, "message" : "Successfully uploaded!"
    }

'''
from fastapi.staticfiles import StaticFiles
app.mount("/files", StaticFiles(directory="uploads"), name="files")
'''





@app.get("/files")
async def files():
    with open("metadata.json", "r") as fp:
        return json.load(fp)






from typing import List

@app.post("/upload-multiple")
async def multi_upload(files : List[UploadFile]  = File(...)):

    saved_files = []
    for file in files:
        file_loc = f"uploads/{file.filename}"
        with open (file_loc, "wb") as fp:
            shutil.copyfileobj(file.file, fp)
            saved_files.append(file.filename)

    return {
        "Message" : "Successfully uploaded!", "File_names" : saved_files
    }
