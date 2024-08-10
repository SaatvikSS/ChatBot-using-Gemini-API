from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables")

genai.configure(api_key=api_key)


text_model = genai.GenerativeModel("gemini-pro")
image_model = genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(input_text, image):
    try:
        if input_text and image:
        
            response = image_model.generate_content([input_text, image])
        elif input_text:
   
            response = text_model.generate_content(input_text)
        elif image:
 
            response = image_model.generate_content(image)
        else:
            return None
        return response.text
    except Exception as e:
        st.error(f"Error communicating with the Google Gemini API: {e}")
        return None


st.set_page_config(page_title="ChatBot-SaatvikSS", page_icon="🤖", layout="centered")


light_mode_css = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #F5F5F7;  /* Light background color */
            color: #000000;  /* Black text color */
        }
        .main {
            background-color: #FFFFFF;  /* White background for main content */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            color: #000000;  /* Black text color */
        }
        .stButton>button {
            color: #FFFFFF;
            background-color: #0071E3;  /* Blue button color */
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 10px;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #005BB5;  /* Darker blue on hover */
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #D1D1D6;  /* Light gray border */
            color: #000000;  /* Black text color */
            background-color: #FFFFFF;  /* White background for the input field */
        }
        .stTextInput>div>div>input::placeholder {
            color: #000000;  /* Dark placeholder text */
        }
        .stFileUploader>div>div>div>label {
            color: #000000;  /* Black text color */
        }
        .stFileUploader>div>div>div>label:hover {
            color: #0071E3;  /* Blue text color on hover */
        }
        .stExpander {
            background-color: #FFFFFF;  /* White background for expander */
            border: 1px solid #D1D1D6;  /* Light gray border */
            border-radius: 10px;
            color: #000000;  /* Black text color */
        }
        .stExpanderHeader {
            font-weight: bold;
            color: #000000;  /* Black text color */
        }
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #000000;  /* Black text color */
        }
        .stMarkdown {
            color: #000000;  /* Black text color */
        }
        .stTextArea>div>textarea {
            background-color: #FFFFFF;  /* White background for text area */
            color: #000000;  /* Black text color */
            border: 1px solid #D1D1D6;  /* Light gray border */
            border-radius: 10px;
            padding: 10px;
        }
        .stTextArea>div>textarea::placeholder {
            color: #000000;  /* Dark placeholder text */
        }
        .stAlert {
            color: #000000;  /* Black text color for alerts */
        }
    </style>
"""

dark_mode_css = """
    <style>
        body {
            background-color: #1E1E1E;  /* Dark background color */
            color: #EAEAEA;  /* Light text color */
        }
        .main {
            background-color: #2D2D2D;  /* Dark background for main content */
            color: #EAEAEA;  /* Light text color */
            border: 1px solid #3C3C3C;  /* Darker border */
        }
        .stButton>button {
            background-color: #4A90E2;  /* Lighter blue for dark mode */
        }
        .stButton>button:hover {
            background-color: #357ABD;  /* Darker blue on hover */
        }
        .stTextInput>div>div>input {
            background-color: #333333;  /* Darker background for input field */
            color: #EAEAEA;  /* Light text color */
        }
        .stTextInput>div>div>input::placeholder {
            color: #777777;  /* Darker gray placeholder text */
        }
        .stFileUploader>div>div>div>label {
            color: #EAEAEA;  /* Light text color */
        }
        .stFileUploader>div>div>div>label:hover {
            color: #4A90E2;  /* Lighter blue text color on hover */
        }
        .stExpander {
            background-color: #2D2D2D;  /* Dark background for expander */
            border: 1px solid #3C3C3C;  /* Darker border */
        }
        .stExpanderHeader {
            color: #EAEAEA;  /* Light text color */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #EAEAEA;  /* Light text color */
        }
        .stMarkdown {
            color: #EAEAEA;  /* Light text color */
        }
        .stTextArea>div>textarea {
            background-color: #333333;  /* Darker background for text area */
            color: #EAEAEA;  /* Light text color */
        }
        .stTextArea>div>textarea::placeholder {
            color: #777777;  /* Darker gray placeholder text */
        }
        .stAlert {
            color: #EAEAEA;  /* Light text color for alerts */
        }
    </style>
"""


st.title("ChatBot using Google Gemini API")
st.markdown("""
    Welcome to the Gemini LLM Application! This tool offers a unique opportunity to interact with a powerful language model. You can enter text prompts, upload images, or combine both to receive detailed and insightful responses.
""")


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False


def toggle_mode():
    st.session_state['dark_mode'] = not st.session_state['dark_mode']


if st.button("Toggle Light/Dark Mode"):
    toggle_mode()
    st.experimental_rerun()  


if st.session_state['dark_mode']:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)


st.write("### Ask a Question or Upload an Image ")
input_text = st.text_input("Enter your question or prompt here:", key="input", placeholder="Type your question here...")
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])


image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button("Ask the Question")


if submit:
    if input_text or image:
        response = get_gemini_response(input_text, image)
        if response:
            if input_text:
                st.session_state['chat_history'].append(("You", input_text))
            if image:
                st.session_state['chat_history'].append(("You", "Uploaded an image"))
            st.subheader("The Response is")
            st.write(response)
            st.session_state['chat_history'].append(("Bot", response))
        else:
            st.error("Failed to get a response from the chatbot")
    else:
        st.error("Please enter a question or upload an image.")


st.subheader("Chat History")
chat_expander = st.expander("Show/Hide Chat History", expanded=True)
with chat_expander:
    for role, text in st.session_state['chat_history']:
        st.markdown(f"**{role}:** {text}")


if st.button("Clear Chat History"):
    st.session_state['chat_history'] = []
    st.experimental_rerun()  
