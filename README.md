# 📁 FastAPI File Upload & Management API

A FastAPI-based backend application that allows users to upload, manage, filter, and retrieve files with metadata support.

This project supports single and multiple file uploads, file validation, metadata storage, filtering, sorting, and pagination.

---

## 🚀 Features

* Single file upload
* Multiple file upload
* File type validation
* File size restriction (Max: 10MB)
* Duplicate file prevention
* Metadata tracking
* File filtering by type and size
* Sorting support
* Pagination
* Static file serving support

---

## 📂 Supported File Types

* JPG / JPEG
* PNG
* PDF
* PPTX
* TXT

---

## 🛠 Tech Stack

* **Python**
* **FastAPI**
* **Uvicorn**
* JSON-based metadata storage

---

## 📁 Project Structure

```
.
├── uploads/          # Stored uploaded files
├── metadata.json     # File metadata storage
├── main.py           # FastAPI application
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Sparky-06/LocalUploadingFile.git
cd LocalUploadingFile
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install fastapi uvicorn python-multipart
```

---

## ▶️ Running the Application

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

Interactive API Docs:

* Swagger UI → `http://127.0.0.1:8000/docs`
* ReDoc → `http://127.0.0.1:8000/redoc`

---

## 📤 API Endpoints

---

### Upload Single File

**POST** `/upload`

Upload one file with validation.

---

### Upload Multiple Files

**POST** `/upload-multiple`

Upload multiple files at once. (Another way of uploading - Not connected with  metadata yet.)

---

### Get Files Metadata

**GET** `/files`

Retrieve uploaded file metadata with filtering and pagination.

#### Query Parameters

| Parameter | Description             |
| --------- | ----------------------- |
| file_type | image, pdf, txt, ppt    |
| minSize   | Minimum file size       |
| maxSize   | Maximum file size       |
| sortBy    | upload_time, size, name |
| order     | asc / desc              |
| page      | Page number             |
| limit     | Records per page        |

---

## 📄 Metadata Example

```json
{
  "name": "example.pdf",
  "size": 20480,
  "upload_time": "2026-02-24T10:30:00",
  "type": "application/pdf"
}
```

---

## 📦 Static File Access (Optional)

Uncomment the following code to serve uploaded files:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/files", StaticFiles(directory="uploads"), name="files")
```

---

## ⚠️ Notes

* Maximum upload size: **10MB**
* Duplicate filenames are prevented
* Metadata stored locally using JSON
* Ensure `uploads/` directory exists before running

---

## 🧑‍💻 Author

**Sparky-06**

---

## 📜 License

This project is open-source and available under the MIT License.
