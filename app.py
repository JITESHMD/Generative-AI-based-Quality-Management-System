import streamlit as st
import google.generativeai as genai
import logging

# Configure the GenerativeAI API key
genai.configure(api_key="AIzaSyBxbqUnQvC5tc5YLX_5CVIC-d_vEmHb1Ss")

# Create a GenerativeModel instance
model = genai.GenerativeModel('gemini-pro')

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Set the page title with color
st.markdown("<h1 style='text-align: center; color:red;'>BAASHHA AI</h1>", unsafe_allow_html=True)

# Set the background color
st.markdown(
    """
    <style>
        body {
            background-color:red;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
def main():
    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # Log messages to the file
            logging.info(f'{message["role"]}: {message["content"]}')

    try:
        user_prompt = st.chat_input()

        if user_prompt is not None:
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.write(user_prompt)
                # Log user input to the file
                logging.info(f'user: {user_prompt}')

            # Generate content using the GenerativeModel
            response = model.generate_content(user_prompt)

            if response and hasattr(response, 'text'):
                # Display the generated content above the input bar
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.write(response.text)
                    # Log assistant response to the file
                    logging.info(f'assistant: {response.text}')
            else:
                st.warning("Failed to generate content. Please try again.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Log errors to the file
        logging.error(f'Error: {str(e)}')

if __name__ == "__main__":
    main()
