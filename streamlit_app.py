import streamlit as st
from models import test_with_huggingface, initialize_models
import optimizer
import json
from typing import List

def load_prompt_templates():
    """Loads prompt templates from JSON."""
    with open('data/prompt_templates.json', 'r') as f:
        return json.load(f)

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
            height=100,
            help="Describe the main objective for your prompt."
        )

        # Model is now fixed to "gemma"
        model_type = "gemma"

        templates = load_prompt_templates()
        style_options = list(templates.keys())
        # Find the index of 'detailed' if it exists, otherwise default to 0
        default_style_index = style_options.index('detailed') if 'detailed' in style_options else 0
        style = st.selectbox(
            "Template Style",
            options=style_options,
            index=default_style_index,
            help="Select a style template for your prompt."
        )

        context = st.text_area(
            "Additional Context (optional)",
            placeholder="e.g., The app targets busy professionals aged 25-40",
            height=50,
            help="Provide any relevant background information."
        )

        col1a, col1b, col1c = st.columns(3)
        with col1a:
            include_persona = st.checkbox("Include Expert Persona", value=True, help="Add a role/persona to the prompt.")
        with col1b:
            include_constraints = st.checkbox("Include Constraints", value=True, help="Add constraints/limitations to the prompt.")
        with col1c:
            include_examples = st.checkbox("Request Examples", value=False, help="Include example outputs in the prompt.")

        if st.button("Generate Prompt", type="primary"):
            generated_prompt = optimizer.generate_prompt(
                goal=goal,
                target_model=model_type,
                context=context,
                style=style,
                formats=["persona"] if include_persona else [] +
                        ["constraints"] if include_constraints else [] +
                        ["examples"] if include_examples else []
            )
            st.session_state.generated_prompt = generated_prompt

    with col2:
        st.subheader("Generated Prompt")
        if 'generated_prompt' in st.session_state:
            prompt_area = st.text_area(
                "Generated Prompt",
                value=st.session_state.generated_prompt,
                height=300,
                help="The generated prompt based on your inputs."
            )

            if st.button("Test Prompt"):
                with st.spinner("Testing prompt..."):
                    response = test_with_huggingface(prompt_area, model_type)
                    st.text_area("AI Response", value=response, height=200, help="The AI's response to the generated prompt.")

with tab2:
    st.subheader("Test Prompt")
    col1, col2 = st.columns(2)

    with col1:
        test_prompt = st.text_area(
            "Prompt to Test",
            placeholder="Enter or paste your prompt here (supports Thai)...",
            height=200,
            help="Enter the prompt you want to test with the AI model."
        )

        # Model is now fixed to "gemma"
        test_model = "gemma"

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
                height=300,
                help="The AI's response to your test prompt."
            )

if __name__ == "__main__":
    initialize_models()
    # Streamlit will automatically run the app
