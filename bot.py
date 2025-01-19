import streamlit as st
import boto3

aws_access_key_id = st.secrets["AWS"]["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["AWS"]["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS"]["AWS_DEFAULT_REGION"]

from github import Github

# Authenticate using GitHub token
github_token = st.secrets["github"]["GITHUB_TOKEN"]
g = Github(github_token)

# Access a private repository
repo = g.get_repo("mithra14/weatherbot")
print(repo.name)


# AWS configuration
region_name = "us-east-1"  # e.g., us-east-1
bot_id = "NYOBDOCRE7"
bot_alias_id = "TSTALIASID"
locale_id = "en_US"  # Replace with your locale
session_id = "01"  # Replace with a unique session ID for each user

# Initialize Lex Runtime V2 client
client = boto3.client('lexv2-runtime', aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region)

# Streamlit app layout
st.title("Chat with Weather Bot")
st.write("Ask me about the weather in any city!")

# Text input for user messages
user_message = st.text_input("Your Message:")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Send message to Lex and display the response
if st.button("Send"):
    if user_message.strip():
        try:
            # Clear previous chat history when a new message is sent
            st.session_state.chat_history = []
            
            # Call Lex Runtime V2
            response = client.recognize_text(
                botId=bot_id,
                botAliasId=bot_alias_id,
                localeId=locale_id,
                sessionId=session_id,
                text=user_message,
            )
            # Extract Lex response
            lex_message = response['messages'][0]['content']
            st.session_state.chat_history.append(f"Bot: {lex_message}")  # Append bot message
            st.session_state.chat_history.append(f"You: {user_message}")  # Append user message
            
            st.success(f"Bot: {lex_message}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a message!")

# Display chat history
for chat in st.session_state.chat_history:
    st.write(chat)
