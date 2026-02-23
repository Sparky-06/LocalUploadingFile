from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from typing import Optional
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
async def files(
    file_type:Optional[str] = None,
    minSize:Optional[int] = None,
    maxSize:Optional[int] = None,
    sortBy : str = "upload_time",
    order: str = "desc",
    page : int = Query(1,ge=1),
    limit: int = Query(10, ge=1)
):
    
    
    if not os.path.exists("metadata.json"):
        return {"data" : []}
    
    with open("metadata.json", "r") as fp:
        data = json.load(fp)
    
    files = data

    if file_type:
        file_type = file_type.lower()

        if file_type == "image":
            allowed = ["image/jpeg", "image/png", "image/jpg"]
            files = [f for f in files if f["type"] in allowed]

        elif file_type == "pdf":
            allowed = ["application/pdf"]
            files = [f for f in files if f["type"] in allowed]
        

        elif file_type == "txt":
            allowed = ["text/plain"]
            files = [f for f in files if f["type"] in allowed]

        
        elif file_type == "ppt":
            allowed = ["application/vnd.openxmlformats-officedocument.presentationml.presentation"]
            files = [f for f in files if f["type"] in allowed]
        
        else:
            files = [ f for f in files if file_type in f["type"].lower()]
    



    if minSize is not None:
        files = [f for f in files if f["size"] >= minSize]
    if maxSize is not None:
        files = [f for f in files if f["size"] <= maxSize]


    allowed_sort = ["upload_time", "size", "name"]

    if sortBy not in allowed_sort:
        sortBy = "upload_time"
    
    reverse = order.lower() == "desc"

    files.sort(key=lambda x:x[sortBy], reverse=reverse)




    total_records = len(files)

    total_pages = (total_records + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_files = files[start:end]

    return {
        "page" : page,
        "limit" : limit,
        "total_records" : total_records,
        "total_pages" : total_pages,
        "data" : paginated_files
    }




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
