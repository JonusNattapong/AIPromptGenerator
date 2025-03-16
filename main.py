from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List

import optimizer
import models
import json

app = FastAPI(title="AI Prompt Generator & Optimizer")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class PromptRequest(BaseModel):
    goal: str
    target_model: str
    context: Optional[str] = None
    existing_prompt: Optional[str] = None
    style: Optional[str] = "detailed"
    formats: Optional[List[str]] = ["standard"]

class OptimizeRequest(BaseModel):
    prompt: str
    target_model: str
    optimization_level: str = "balanced"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
async def generate_prompt(request: PromptRequest):
    """Generate a new prompt based on user goals and target model"""
    try:
        generated_prompt = optimizer.generate_prompt(
            goal=request.goal,
            target_model=request.target_model,
            context=request.context,
            style=request.style,
            formats=request.formats
        )
        return {"status": "success", "prompt": generated_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize")
async def optimize_prompt(request: OptimizeRequest):
    """Optimize an existing prompt for better results"""
    try:
        optimized_prompt = optimizer.optimize_prompt(
            prompt=request.prompt,
            target_model=request.target_model,
            optimization_level=request.optimization_level
        )
        return {"status": "success", "optimized_prompt": optimized_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test-prompt")
async def test_prompt(request: OptimizeRequest):
    """Test a prompt with an AI model from Hugging Face"""
    try:
        result = models.test_with_huggingface(
            prompt=request.prompt,
            model_type=request.target_model
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)