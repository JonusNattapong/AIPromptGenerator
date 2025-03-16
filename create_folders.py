import os
import json

def create_directory_structure():
    """Create the necessary directories for the project"""
    directories = [
        "static",
        "static/css",
        "static/js",
        "templates",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    # Create placeholder template data
    model_best_practices = {
        "default": {
            "detailed_format": "Please format your response with headings, bullet points, and examples where appropriate.",
            "step_instructions": "Please break down your response into clear, sequential steps.",
            "concise_format": "Please provide a concise answer in 3-5 sentences.",
            "constraints": "Limit your response to the most essential information based on expert knowledge.",
            "example_format": "Include at least one practical example to illustrate your point.",
            "output_format": "Present your answer in a clear, structured format with distinct sections.",
            "optimization_hint": "Use logical reasoning and provide evidence for your statements."
        },
        "chatgpt": {
            "detailed_format": "Format your answer with ##Headings, *bullet points*, and numerical lists. Include code examples if relevant.",
            "step_instructions": "Break down your response into numbered steps (1, 2, 3, etc.) with clear instructions at each step.",
            "concise_format": "Answer briefly and directly in 2-3 sentences maximum.",
            "constraints": "Stick to verified information and indicate clearly if something is your opinion or speculation.",
            "example_format": "Provide one concrete example with 'Example:' as a header.",
            "output_format": "Structure your response with clear sections separated by headers.",
            "optimization_hint": "You excel at detailed explanations with examples, so include those where possible."
        },
        # Additional models omitted for brevity but would be included in the actual file
    }
    
    prompt_templates = {
        "default": {
            "prefix": "",
            "suffix": "\n\nPlease provide a comprehensive response."
        },
        "chatgpt": {
            "prefix": "",
            "suffix": "\n\nAnswer using the information provided without making up facts."
        },
        # Additional templates omitted for brevity but would be included in the actual file
    }
    
    # Write data to files
    with open("data/model_best_practices.json", "w") as f:
        json.dump(model_best_practices, f, indent=2)
        
    with open("data/prompt_templates.json", "w") as f:
        json.dump(prompt_templates, f, indent=2)
        
    print("Created data files")

if __name__ == "__main__":
    create_directory_structure()