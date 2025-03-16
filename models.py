from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Dict, Any, List, Optional
import torch
import json

# Map of model types to actual Hugging Face models
MODEL_MAPPING = {
    "chatgpt": "gpt2",  # Simulating GPT behavior with gpt2
    "claude": "EleutherAI/gpt-neo-1.3B",  # Simulating Claude behavior
    "gemini": "facebook/opt-2.7b",  # Simulating Gemini behavior
    "llama": "TinyLlama/TinyLlama-1.1B-Chat-v0.6",
    "mistral": "mistralai/Mistral-7B-v0.3",  # Will need to use smaller quantized version
    "gemma": "google/gemma-3-4b-it",  # Google's Gemma 3-4B Instruct model
    "thai": "scb10x/llama3.2-typhoon2-1b",  # Thai language model by SCB10X
    "default": "gpt2"
}

# Keep loaded models in memory
LOADED_MODELS = {}

def get_model(model_type: str):
    """Get the appropriate model based on the target AI type"""
    model_name = MODEL_MAPPING.get(model_type.lower(), MODEL_MAPPING["default"])
    
    # For demonstration, we'll use smaller models that are more manageable
    if model_name.startswith("mistralai"):
        model_name = "TheBloke/Mistral-7B-v0.1-GPTQ"  # Quantized version
    
    if model_name not in LOADED_MODELS:
        try:
            print(f"Loading model {model_name}...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # For smaller models, load directly
            if model_name in ["gpt2", "distilgpt2"]:
                model = AutoModelForCausalLM.from_pretrained(model_name)
                LOADED_MODELS[model_name] = {
                    "model": model,
                    "tokenizer": tokenizer,
                    "pipeline": pipeline("text-generation", model=model, tokenizer=tokenizer)
                }
            # For larger models, use pipeline with device_map for efficient loading
            else:
                text_generator = pipeline(
                    "text-generation",
                    model=model_name,
                    tokenizer=tokenizer,
                    device_map="auto"
                )
                LOADED_MODELS[model_name] = {
                    "pipeline": text_generator,
                    "tokenizer": tokenizer
                }
                
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            # Fallback to GPT-2 if loading fails
            if model_name != "gpt2":
                return get_model("default")
            else:
                raise e
    
    return LOADED_MODELS[model_name]

def test_with_huggingface(prompt: str, model_type: str, 
                         max_length: int = 200) -> str:
    """
    Test a prompt with a Hugging Face model
    
    Args:
        prompt: The prompt to test
        model_type: Type of AI model to simulate (maps to actual HF models)
        max_length: Maximum length of generated text
        
    Returns:
        Generated response text
    """
    try:
        model_data = get_model(model_type)
        
        # Use pipeline for generation
        generator = model_data["pipeline"]
        
        # Generate text
        result = generator(
            prompt,
            max_length=max_length,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=50256  # Default for GPT models
        )
        
        # Extract generated text, removing the original prompt
        generated_text = result[0]['generated_text']
        response = generated_text[len(prompt):].strip()
        
        # If empty result, return a note
        if not response:
            return "The model didn't generate additional text beyond your prompt."
            
        return response
        
    except Exception as e:
        return f"Error testing prompt: {str(e)}"

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
