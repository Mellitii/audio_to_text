import os
import google.generativeai as genai
import streamlit as st

# Set the API key
os.environ["GENAI_API_KEY"] = "AIzaSyAIOIZrkRR8dOQppiItPYl_txlx6VEr8PE"
genai.configure(api_key=os.environ["GENAI_API_KEY"])

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Streamlit interface
st.title('Mon application Python')
st.write('Veuillez télécharger un fichier audio pour le convertir en texte.')

# Allow the user to upload an audio file
uploaded_file = st.file_uploader("Choisissez un fichier audio", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open(f"temp_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Upload the file using the File API
    uploaded_file_path = f"temp_{uploaded_file.name}"
    st.write(f"Téléchargement du fichier: {uploaded_file_path}")

    try:
        # Upload the file to the API using genai.upload_file
        uploaded_file_ref = genai.upload_file(uploaded_file_path)
        
        # Now that the file is uploaded, create a chat session
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            system_instruction="votre mission est de convertir un audio de contenu médical en texte",
        )

        # Prepare the prompt using the uploaded file reference
        prompt_parts = ["convertir l'audio en texte", uploaded_file_ref]

        # Create a chat session and send the prompt
        chat_session = model.start_chat(
            history=[
                # Add any history if needed
            ]
        )

        response = chat_session.send_message(prompt_parts)

        # Display the response from the model
        st.write("Transcription de l'audio :")
        st.write(response.text)
    
    except Exception as e:
        st.error(f"Une erreur s'est produite lors du téléchargement ou du traitement du fichier : {e}")