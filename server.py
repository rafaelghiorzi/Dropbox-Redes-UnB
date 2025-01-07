from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import aiofiles

#uvicorn server:app --host 127.0.0.1 --port 8000 --reload 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./files.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FileModel(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    uploader = Column(String)

Base.metadata.create_all(bind=engine)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), fileName: str = Form(...), uploader: str = Form("anonymous")):
    filepath = os.path.join(UPLOAD_FOLDER, fileName)
    async with aiofiles.open(filepath, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    db = SessionLocal()
    new_file = FileModel(filename=fileName, filepath=filepath, uploader=uploader)
    db.add(new_file)
    db.commit()
    db.close()
    return {"message": "File uploaded successfully"}

@app.get("/list")
def list_files():
    db = SessionLocal()
    files = db.query(FileModel).all()
    db.close()
    return [{"id": f.id, "filename": f.filename, "uploader": f.uploader, "filepath": f.filepath} for f in files]

@app.get("/download/{file_id}")
def download_file(file_id: int):
    db = SessionLocal()
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    db.close()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file.filepath, filename=file.filename)

@app.delete("/delete/{file_id}")
def delete_file(file_id: int):
    db = SessionLocal()
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        db.close()
        raise HTTPException(status_code=404, detail="File not found")
    if os.path.exists(file.filepath):
        os.remove(file.filepath)
    else:
        db.close()
        raise HTTPException(status_code=404, detail="File not found on disk")
    db.delete(file)
    db.commit()
    db.close()
    return {"message": "File deleted successfully"}
