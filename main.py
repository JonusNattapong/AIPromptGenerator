from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

import optimizer
import models
import json

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create FastAPI app
app = FastAPI(title="AI Prompt Generator & Optimizer")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


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
        logging.info(f"Generated prompt: {generated_prompt}")
        return {"status": "success", "prompt": generated_prompt}
    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating prompt: {e}")

@app.post("/api/optimize")
async def optimize_prompt(request: OptimizeRequest):
    """Optimize an existing prompt for better results"""
    try:
        optimized_prompt = optimizer.optimize_prompt(
            prompt=request.prompt,
            target_model=request.target_model,
            optimization_level=request.optimization_level
        )
        logging.info(f"Optimized prompt: {optimized_prompt}")
        return {"status": "success", "optimized_prompt": optimized_prompt}
    except Exception as e:
        logging.error(f"Error optimizing prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Error optimizing prompt: {e}")

if __name__ == "__main__":
    import uvicorn
    models.initialize_models() # Initialize models
    uvicorn.run(app, host="localhost", port=8000)
