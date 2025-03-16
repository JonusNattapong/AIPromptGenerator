import streamlit as st
from models import test_with_huggingface, MODEL_MAPPING
import json

def load_prompt_templates():
    with open('data/prompt_templates.json', 'r') as f:
        return json.load(f)

def generate_prompt(goal, model_type, style, context, include_persona, include_constraints, include_examples):
    templates = load_prompt_templates()
    template = templates.get(style, templates['detailed'])
    
    # Build prompt components
    components = []
    if include_persona:
        components.append("Act as an expert AI prompt engineer with extensive experience.")
    
    components.append(f"Goal: {goal}")
    
    if context:
        components.append(f"Context: {context}")
    
    if include_constraints:
        components.append("Please ensure the prompt is clear, specific, and actionable.")
    
    if include_examples:
        components.append("Please provide an example of how to use this prompt effectively.")
    
    prompt = template.format(content="\n".join(components))
    return prompt

# Set page config
st.set_page_config(
    page_title="AI Prompt Generator & Optimizer",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("AI Prompt Generator & Optimizer")
st.markdown("Create powerful, optimized prompts for various AI models")

# Tabs
tab1, tab2 = st.tabs(["Generate", "Test"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generate Prompt")
        goal = st.text_area(
            "What do you want to achieve?",
            placeholder="e.g., Create a marketing plan for a new fitness app (ภาษาไทยได้)",
            height=100
        )
        
        model_type = st.selectbox(
            "Target AI Model",
            options=list(MODEL_MAPPING.keys()),
            index=0
        )
        
        style = st.selectbox(
            "Style",
            options=["detailed", "step-by-step", "concise"],
            index=0
        )
        
        context = st.text_area(
            "Additional Context (optional)",
            placeholder="e.g., The app targets busy professionals aged 25-40",
            height=50
        )
        
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            include_persona = st.checkbox("Include Expert Persona", value=True)
        with col1b:
            include_constraints = st.checkbox("Include Constraints", value=True)
        with col1c:
            include_examples = st.checkbox("Request Examples", value=False)
        
        if st.button("Generate Prompt", type="primary"):
            generated_prompt = generate_prompt(
                goal, model_type, style, context,
                include_persona, include_constraints, include_examples
            )
            st.session_state.generated_prompt = generated_prompt
    
    with col2:
        st.subheader("Generated Prompt")
        if 'generated_prompt' in st.session_state:
            prompt_area = st.text_area(
                "Generated Prompt",
                value=st.session_state.generated_prompt,
                height=300
            )
            
            if st.button("Test Prompt"):
                with st.spinner("Testing prompt..."):
                    response = test_with_huggingface(prompt_area, model_type)
                    st.text_area("AI Response", value=response, height=200)

with tab2:
    st.subheader("Test Prompt")
    col1, col2 = st.columns(2)
    
    with col1:
        test_prompt = st.text_area(
            "Prompt to Test",
            placeholder="Enter or paste your prompt here (supports Thai)...",
            height=200
        )
        
        test_model = st.selectbox(
            "Model to Test With",
            options=list(MODEL_MAPPING.keys()),
            index=0,
            key="test_model"
        )
        
        if st.button("Run Test", type="primary"):
            with st.spinner("Testing prompt..."):
                response = test_with_huggingface(test_prompt, test_model)
                st.session_state.test_response = response
    
    with col2:
        st.subheader("AI Response")
        if 'test_response' in st.session_state:
            st.text_area(
                "Response",
                value=st.session_state.test_response,
                height=300
            )

if __name__ == "__main__":
    # Streamlit will automatically run the app
    pass
