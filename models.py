from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Dict, Any, List, Optional
import torch
import json
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Use a smaller, less resource-intensive model
MODEL_NAME = "microsoft/phi-1_5"

# Keep loaded models in memory
LOADED_MODELS = {}

def initialize_models():
    """Initialize and load the model at startup"""
    try:
        print(f"Loading model {MODEL_NAME}...")

        # Load with token from environment
        token = os.getenv("HUGGINGFACE_TOKEN")
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            token=token,
            trust_remote_code=True
        )
        print(f"Tokenizer loaded: {type(tokenizer)}")  # Debug print
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            token=token,
            trust_remote_code=True
        )
        print(f"Model loaded: {type(model)}")  # Debug print

        LOADED_MODELS["default"] = { # Use a generic key like "default"
            "model": model,
            "tokenizer": tokenizer,
            "pipeline": pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer
            )
        }

    except Exception as e:
        print(f"Error loading model {MODEL_NAME}:")
        traceback.print_exc()  # Print the full stack trace
        # Removed: st.error(f"Failed to load model {MODEL_NAME}. Please check configuration and HUGGINGFACE_TOKEN.")


def evaluate_prompt_effectiveness(prompt: str, criteria: List[str] = None) -> Dict[str, Any]:
    """
    Evaluate a prompt's potential effectiveness

    Args:
        prompt: The prompt to evaluate
        criteria: Specific criteria to evaluate (clarity, specificity, etc.)

    Returns:
        Dictionary with scores and suggestions
    """
    if criteria is None:
        criteria = ["clarity", "specificity", "context", "constraints"]

    # Initialize scores
    scores = {criterion: 0 for criterion in criteria}
    suggestions = []

    # Evaluate clarity
    if "clarity" in criteria:
        # Check sentence structure
        sentences = prompt.split(".")
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)

        if avg_sentence_length > 25:
            scores["clarity"] = 0.5
            suggestions.append("Consider using shorter sentences for clarity.")
        else:
            scores["clarity"] = 0.9

    # Evaluate specificity
    if "specificity" in criteria:
        # Look for specific instructions
        if any(word in prompt.lower() for word in ["specific", "exactly", "precisely"]):
            scores["specificity"] = 0.9
        else:
            scores["specificity"] = 0.6
            suggestions.append("Add more specific instructions or examples.")

    # Evaluate context
    if "context" in criteria:
        # Check if context is provided
        if "context" in prompt.lower() or len(prompt.split()) > 30:
            scores["context"] = 0.8
        else:
            scores["context"] = 0.4
            suggestions.append("Add more context for better results.")

    # Evaluate constraints
    if "constraints" in criteria:
        # Check if constraints or limitations are specified
        constraint_words = ["limit", "constraint", "must", "should", "only", "don't"]
        if any(word in prompt.lower() for word in constraint_words):
            scores["constraints"] = 0.8
        else:
            scores["constraints"] = 0.5
            suggestions.append("Consider adding constraints or limitations.")

    # Calculate overall score
    overall_score = sum(scores.values()) / len(scores)

    return {
        "scores": scores,
        "overall_score": overall_score,
        "suggestions": suggestions
    }
