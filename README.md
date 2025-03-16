# AI Prompt Generator & Optimizer

A powerful tool to generate and optimize prompts for ChatGPT, Claude, Gemini, and other AI models, helping you get better results from your AI interactions.

## Features

- Generate tailored prompts based on your goals and target AI model
- Optimize existing prompts for better results
- Support for multiple AI platforms (OpenAI, Anthropic, Google, etc.)
- Real-time preview and testing with Hugging Face models
- Save and organize your prompts
- Prompt templates and best practices built-in

## Installation

```bash
# Clone the repository
git clone https://github.com/JonusNattapong/ai-prompt-optimizer.git
cd ai-prompt-optimizer

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn main:app --reload
```

## Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Select the AI model you're targeting
3. Enter your goal or existing prompt
4. Use the optimizer to enhance your prompt
5. Test the optimized prompt directly or export for use with your target AI

## Technologies

- Backend: Python with FastAPI
- Frontend: HTML, CSS, JavaScript
- AI Models: Hugging Face Transformers
- NLP: spaCy, NLTK for text analysis

## License

MIT