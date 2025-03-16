import re
import json
from typing import List, Dict, Any, Optional
import spacy
import nltk
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load prompt templates and best practices
with open("data/prompt_templates.json", "r") as f:
    PROMPT_TEMPLATES = json.load(f)

with open("data/model_best_practices.json", "r") as f:
    MODEL_BEST_PRACTICES = json.load(f)

# Initialize models
generator = pipeline("text-generation", model="gpt2")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_prompt(goal: str, target_model: str, context: str = None, 
                   style: str = "detailed", formats: List[str] = ["standard"]) -> str:
    """
    Generate a prompt based on user goal and target AI model
    
    Args:
        goal: The user's goal for the prompt
        target_model: The target AI model (e.g., "chatgpt", "claude", "gemini")
        context: Additional context for the prompt
        style: Style of the prompt (concise, detailed, step-by-step)
        formats: List of prompt formats to include
        
    Returns:
        A generated prompt optimized for the target model
    """
    # Normalize target model name
    target_model = target_model.lower().strip()
    
    # Get template for the specified model
    template = PROMPT_TEMPLATES.get(target_model, PROMPT_TEMPLATES["default"])
    
    # Get best practices for the model
    practices = MODEL_BEST_PRACTICES.get(target_model, MODEL_BEST_PRACTICES["default"])
    
    # Create prompt components
    components = []
    
    # Add role/persona if applicable
    if "persona" in formats:
        components.append(f"As an expert {extract_domain(goal)},")
    
    # Add main goal
    components.append(goal)
    
    # Add context if provided
    if context:
        components.append(f"Context: {context}")
        
    # Add formatting instructions based on style
    if style == "detailed":
        components.append(practices["detailed_format"])
    elif style == "step-by-step":
        components.append(practices["step_instructions"])
    elif style == "concise":
        components.append(practices["concise_format"])
        
    # Combine components using the template structure
    prompt = template["prefix"]
    prompt += " ".join(components)
    
    if "constraints" in formats:
        prompt += f"\n\n{practices['constraints']}"
    
    if "examples" in formats:
        prompt += f"\n\n{practices['example_format']}"
        
    prompt += template["suffix"]
    
    # Clean up any double spaces or formatting issues
    prompt = re.sub(r'\s+', ' ', prompt).strip()
    prompt = prompt.replace(" .", ".").replace(" ,", ",")
    
    return prompt

def optimize_prompt(prompt: str, target_model: str, optimization_level: str = "balanced") -> str:
    """
    Optimize an existing prompt for better results
    
    Args:
        prompt: The existing prompt to optimize
        target_model: The target AI model 
        optimization_level: How aggressively to optimize (minimal, balanced, maximum)
        
    Returns:
        An optimized version of the prompt
    """
    # Parse the prompt
    doc = nlp(prompt)
    
    # Get model-specific best practices
    target_model = target_model.lower().strip()
    practices = MODEL_BEST_PRACTICES.get(target_model, MODEL_BEST_PRACTICES["default"])
    
    # Analyze prompt structure
    sentences = sent_tokenize(prompt)
    
    # Apply optimizations based on the level
    if optimization_level == "minimal":
        # Just clean up and add minimal formatting
        optimized = clean_prompt(prompt)
        
    elif optimization_level == "balanced":
        # Restructure and enhance the prompt
        optimized = enhance_prompt_structure(prompt, practices)
        
    else:  # maximum
        # Complete rewrite with model-specific optimizations
        optimized = rewrite_prompt(prompt, target_model, practices)
    
    return optimized

def clean_prompt(prompt: str) -> str:
    """Clean and format a prompt with minimal changes"""
    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', prompt).strip()
    
    # Fix basic punctuation issues
    cleaned = re.sub(r'\s([,.!?;:])', r'\1', cleaned)
    
    # Ensure the prompt ends with a clear instruction or question
    if not re.search(r'[.!?]$', cleaned):
        cleaned += "."
        
    return cleaned

def enhance_prompt_structure(prompt: str, practices: Dict[str, str]) -> str:
    """Enhance prompt structure while preserving core content"""
    sentences = sent_tokenize(prompt)
    
    # Identify parts of the prompt
    intro_part = sentences[0] if sentences else ""
    body_parts = sentences[1:-1] if len(sentences) > 2 else sentences[1:] if len(sentences) > 1 else []
    conclusion_part = sentences[-1] if len(sentences) > 1 else ""
    
    # Enhance introduction with clear role/task
    if not re.search(r'(you are|act as|as an?|assume the role)', intro_part.lower()):
        domain = extract_domain(prompt)
        enhanced_intro = f"As a specialized {domain} expert, {intro_part}"
    else:
        enhanced_intro = intro_part
        
    # Enhance body with structure markers
    enhanced_body = []
    for i, part in enumerate(body_parts):
        if len(part) > 100 and "," in part:  # Long complex sentence
            subparts = part.split(", ")
            if len(subparts) > 2:
                # Convert to bullet points
                enhanced_body.append(f"Key points:")
                enhanced_body.extend([f"- {subpart.strip()}" for subpart in subparts])
                continue
        enhanced_body.append(part)
    
    # Enhance conclusion with clear output expectations
    if not re.search(r'(please provide|i need|output format|format your response)', conclusion_part.lower()):
        enhanced_conclusion = f"{conclusion_part} {practices['output_format']}"
    else:
        enhanced_conclusion = conclusion_part
        
    # Combine enhanced parts
    result = f"{enhanced_intro} {' '.join(enhanced_body)} {enhanced_conclusion}"
    
    # Add optimization hint based on target model
    result += f"\n\n{practices['optimization_hint']}"
    
    return result

def rewrite_prompt(prompt: str, target_model: str, practices: Dict[str, str]) -> str:
    """Completely rewrite a prompt for optimal results"""
    # Extract core intent and key concepts
    doc = nlp(prompt)
    key_phrases = [chunk.text for chunk in doc.noun_chunks]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    
    # Use embedding model to find most similar template
    prompt_embedding = embedding_model.encode(prompt, convert_to_tensor=True)
    
    template_texts = list(PROMPT_TEMPLATES.keys())
    template_embeddings = embedding_model.encode(template_texts, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(prompt_embedding, template_embeddings)[0]
    best_template_idx = similarities.argmax().item()
    template = PROMPT_TEMPLATES[template_texts[best_template_idx]]
    
    # Generate new prompt using transformer pipeline
    # This is just a placeholder - in a real app you'd use a more sophisticated approach
    generation_prompt = f"Rewrite this prompt for {target_model}: {prompt}\n\nOptimized version:"
    generated = generator(generation_prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
    
    # Extract the generated part
    rewritten = generated.split("Optimized version:")[-1].strip()
    
    # Apply model-specific formatting
    model_format = practices["detailed_format"]
    if not any(marker in rewritten.lower() for marker in ["step", "bullet", "1.", "i.", "•"]):
        rewritten += f"\n\n{model_format}"
    
    return rewritten

def extract_domain(text: str) -> str:
    """Extract likely domain/field from text"""
    # Define common domains
    domains = ["AI", "machine learning", "data science", "marketing", "business", "writing", 
               "programming", "development", "design", "research", "teaching", "academic",
               "engineering", "healthcare", "technology", "science", "communication"]
    
    # Check for explicit domain mentions
    for domain in domains:
        if domain.lower() in text.lower():
            return domain
            
    # Default domains based on common words
    if any(word in text.lower() for word in ["code", "programming", "algorithm", "software", "developer"]):
        return "software engineering"
    elif any(word in text.lower() for word in ["write", "essay", "blog", "article", "content"]):
        return "content creation"
    elif any(word in text.lower() for word in ["analyze", "research", "study", "investigate"]):
        return "analytical research"
    else:
        return "AI assistant"