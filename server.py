import os, urllib.parse
from typing import Optional
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
API_BASE = "https://gen.pollinations.ai"
API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()

app = FastAPI(title="NHÍT AI", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

class TextRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)
    model: str = "openai"
    system: str = "Bạn là biên kịch phim chuyên nghiệp. Trả lời bằng tiếng Việt."
    temperature: float = 0.8

class MediaRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    model: str
    duration: int = 5

def headers():
    if not API_KEY:
        raise HTTPException(503, "Chưa cấu hình POLLINATIONS_API_KEY trong file .env")
    return {"Authorization": f"Bearer {API_KEY}"}

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/api/health")
async def health():
    return {"ok": True, "key_configured": bool(API_KEY)}

@app.get("/api/models")
async def models():
    # Danh mục công khai để giao diện hiển thị model và lựa chọn.
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(f"{API_BASE}/v1/models")
            r.raise_for_status()
            data = r.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Không tải được danh mục model: {e}")

@app.post("/api/script")
async def script(req: TextRequest):
    h = headers()
    payload = {
        "model": req.model,
        "messages": [
            {"role": "system", "content": req.system},
            {"role": "user", "content": req.prompt}
        ],
        "temperature": req.temperature
    }
    async with httpx.AsyncClient(timeout=180) as client:
        try:
            r = await client.post(f"{API_BASE}/v1/chat/completions", headers=h, json=payload)
            if r.is_error:
                raise HTTPException(r.status_code, r.text[:1500])
            data = r.json()
            return {"text": data["choices"][0]["message"]["content"], "raw": data}
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Lỗi kết nối máy chủ AI: {e}")

@app.post("/api/image")
async def image(req: MediaRequest):
    h = headers()
    url = f"{API_BASE}/image/{urllib.parse.quote(req.prompt, safe='')}"
    params = {"model": req.model, "width": 768, "height": 1365, "nologo": "true"}
    async with httpx.AsyncClient(timeout=180, follow_redirects=True) as client:
        try:
            r = await client.get(url, headers=h, params=params)
            if r.is_error:
                raise HTTPException(r.status_code, r.text[:1500])
            return Response(content=r.content, media_type=r.headers.get("content-type", "image/jpeg"))
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Lỗi tạo ảnh: {e}")

@app.post("/api/video")
async def video(req: MediaRequest):
    h = headers()
    url = f"{API_BASE}/video/{urllib.parse.quote(req.prompt, safe='')}"
    params = {"model": req.model, "duration": max(1, min(req.duration, 10))}
    async with httpx.AsyncClient(timeout=300, follow_redirects=True) as client:
        try:
            r = await client.get(url, headers=h, params=params)
            if r.is_error:
                raise HTTPException(r.status_code, r.text[:1500])
            return Response(content=r.content, media_type=r.headers.get("content-type", "video/mp4"),
                            headers={"Content-Disposition": 'inline; filename="nhit-ai.mp4"'})
        except httpx.TimeoutException:
            raise HTTPException(504, "Máy chủ tạo video quá thời gian chờ. Hãy thử clip ngắn hơn.")
        except httpx.HTTPError as e:
            raise HTTPException(502, f"Lỗi tạo video: {e}")
