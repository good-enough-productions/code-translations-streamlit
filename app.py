import streamlit as st
import requests

# Fetch models from Ollama
def get_ollama_models():
    url = "http://localhost:11434/api/models"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("models", [])
        else:
            return ["llama2", "mixtral"]  # Fallback to default models
    except requests.exceptions.ConnectionError:
        return ["Error: Unable to connect to Ollama server"]

# Function to query the Ollama model
def query_ollama(model, prompt):
    url = f"http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("content", "No response from model.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the Ollama server. Is it running?"

# Streamlit app
def main():
    st.title("Code Explainer with Ollama")
    st.write("Paste your code below, and I'll explain it in plain English.")

    # Input text area for code
    code_input = st.text_area("Your Code:", height=200, placeholder="Paste your code here...")

    # Dynamically fetch models
    models = get_ollama_models()
    model_name = st.selectbox("Choose a Model", models)

    # Button to explain code
    if st.button("Explain My Code"):
        if code_input.strip():
            st.write("Processing...")
            prompt = f"Explain this code in plain English:\n\n{code_input}"
            explanation = query_ollama(model_name, prompt)
            st.subheader("Explanation:")
            st.write(explanation)
        else:
            st.warning("Please paste some code before clicking 'Explain My Code'.")

if __name__ == "__main__":
    main()
