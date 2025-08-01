import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# API Configuration
try:
    api_key = os.environ["LANGFLOW_API_KEY"]
except KeyError:
    raise ValueError("LANGFLOW_API_KEY environment variable not found. Please set your API key in the environment variables.")

url = "http://localhost:7860/api/v1/run/6fcf02bc-811b-4014-9a42-337d5fbace91"

headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key
}

def main():
    st.title("🧠 Langflow Chat Interface")
    st.write("Ask a question and get a response from your custom Langflow agent.")

    message = st.text_input("Message", placeholder="Ask something...")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message.")
            return
        
        payload = {
            "output_type": "chat",
            "input_type": "chat",
            "input_value": message
        }

        try:
            with st.spinner("Running flow..."):
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()

                result = response.json()
                # Print raw if needed: st.json(result)
                reply = result["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                st.success(reply)

        except requests.exceptions.RequestException as e:
            st.error(f"API error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
