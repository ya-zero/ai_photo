from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import shutil
import random
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # Путь к папке с вашими HTML-шаблонами

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Страница приветствия с формой загрузки
@app.get("/", response_class=HTMLResponse)
async def welcome_page():
    return templates.TemplateResponse("welcome.html", {"request": {}})

# Эндпоинт для загрузки файла
@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Передаем имя файла в шаблон
    return templates.TemplateResponse("upload_result.html", {"request": {}, "filename": file.filename})

# Эндпоинт для отправки файла в ИИ (с заглушкой)
@app.post("/send-to-ai/", response_class=HTMLResponse)
async def send_to_ai(filename: str = Form(...)):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return JSONResponse(content={"error": "Файл не найден"}, status_code=400)

    random_value = random.randint(0, 100)

    return templates.TemplateResponse("ai_result.html", {"request": {}, "filename": filename, "result": random_value})



# Эндпоинт для доступа к файлу изображения
@app.get("/uploads/{filename}")
async def get_image(filename: str):
    file_path = UPLOAD_DIR / filename
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

