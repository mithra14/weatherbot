import streamlit as st
import boto3
from github import Github

# AWS and GitHub configuration
aws_access_key_id = st.secrets["AWS"]["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["AWS"]["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS"]["AWS_DEFAULT_REGION"]
github_token = st.secrets["github"]["GITHUB_TOKEN"]

# Authenticate using GitHub token
g = Github(github_token)
repo = g.get_repo("mithra14/weatherbot")
print(repo.name)

# AWS Lex configuration
region_name = "us-east-1"
bot_id = "NYOBDOCRE7"
bot_alias_id = "TSTALIASID"
locale_id = "en_US"
session_id = "01"

# Initialize Lex Runtime V2 client
client = boto3.client(
    "lexv2-runtime",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region,
)

# New background image URL (choose one from above)
background_image_url = "https://weatherpredict22012025.s3.us-east-1.amazonaws.com/images.jpg"

st.markdown(
    f"""
    <style>
    body {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #333;
    }}
    .stApp {{
        background-color: rgba(255, 255, 255, 0.9);  /* Slight overlay for professionalism */
        border-radius: 10px;
        padding: 30px;
    }}
    .stTitle {{
        font-size: 2.5em;
        font-weight: 600;
        color: #0a2a41;
    }}
    .stTextInput input {{
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #ddd;
    }}
    .chat-bubble {{
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }}
    .chat-bubble img {{
        margin-right: 10px;
        border-radius: 50%;
        width: 40px;  /* Simplified size */
    }}
    .user-message {{
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 8px;
        max-width: 70%;
        font-size: 16px;
    }}
    .bot-message {{
        background-color: #e9f7fb;
        padding: 15px;
        border-radius: 8px;
        max-width: 70%;
        font-size: 16px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app layout
st.title("WeatherBot 🌤️")
st.markdown("### Your AI Assistant for Accurate Weather Updates")

# User input section
user_message = st.text_input("Your Message:", placeholder="Ask me about the weather...")

# Chat history session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Send message to Lex and display the response
if st.button("Send"):
    if user_message.strip():
        with st.spinner("Processing..."):
            try:
                # Call Lex Runtime V2
                response = client.recognize_text(
                    botId=bot_id,
                    botAliasId=bot_alias_id,
                    localeId=locale_id,
                    sessionId=session_id,
                    text=user_message,
                )
                lex_message = response["messages"][0]["content"]
                
                # Append chat history
                st.session_state.chat_history.append({"sender": "You", "message": user_message})
                st.session_state.chat_history.append({"sender": "Bot", "message": lex_message})
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter your message!")

# Display chat history with refined design
for chat in st.session_state.chat_history:
    if chat["sender"] == "You":
        st.markdown(
            f"""
            <div class="chat-bubble">
                <div class="user-message"><strong>You:</strong> {chat["message"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-bubble">
                <div class="bot-message"><strong>Bot:</strong> {chat["message"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Footer
st.markdown("---")
st.markdown("Powered by AWS Lex and GitHub")
