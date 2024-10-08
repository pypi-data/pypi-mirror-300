import streamlit as st
from groq import Groq
import os
import subprocess
from typing import Generator
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

# Function to interact with Groq API and get chat completion responses
def get_chat_response(api_key: str, messages: list, model: str):
    try:
        # Initialize the Groq client using the provided API key
        client = Groq(api_key=api_key)

        # Create a chat completion request to the specified model, including full chat history
        chat_completion = client.chat.completions.create(
            messages=messages,  # Pass the full message history
            model=model,  # Use the selected model
            stream=True  # Enable streaming for real-time responses
        )

        # Return the chat completion response generator
        return chat_completion

    except Exception as e:
        return f"Error: {e}"

# Generator to stream chat responses from the Groq API
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content chunk by chunk from the Groq API."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Function to create and display a plot
def plot_example():
    # Example plot: simple line graph
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3, 4], [10, 15, 20, 25, 30])
    ax.set_title("Sample Line Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    
    # Display the plot in Streamlit
    st.pyplot(fig)

# Streamlit app to create a chat interface with dynamic responses
def streamlit_app():
    # Create two columns: left for the plot and right for the chat
    col1, col2 = st.columns([1, 1]) 

    # Plot in the first column (left)
    with col1:
        st.subheader("Example Plot")
        plot_example()  # Call the function to display the plot

    # Chat in the second column (right)
    with col2:
        st.title("LLM Chat Interface")
        # Initialize chat history and selected model in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "user_model" not in st.session_state:
            st.session_state.user_model = None

        # Available models with their respective details
        avail_model = {
            "llama3-8b-8192": {"Model": "llama3-8b-8192", "Developer": "Meta"},
            "mixtral-8x7b-32768": {"Model": "mixtral-8x7b-32768", "Developer": "Mistral"},
            "gemma2-9b-it": {"Model": "gemma2-9b-it", "Developer": "Google"},
        }

        # Sidebar for selecting model and entering API key
        with st.sidebar:
            choose_model = st.selectbox(
                "Select a model:",
                options=list(avail_model.keys()),
                format_func=lambda x: f"{avail_model[x]['Model']} ({avail_model[x]['Developer']})",
                index=0
            )
            api_key = st.text_input("Enter your API Key", type="password")

        # Clear chat history if the model is changed
        if st.session_state.user_model != choose_model:
            st.session_state.messages = []
            st.session_state.user_model = choose_model

        # Display chat history from previous interactions
        for message in st.session_state.messages:
            avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        # Handle new user input dynamically
        if message := st.chat_input("Enter your messages here..."):
            # Store user message in session state
            st.session_state.messages.append({"role": "user", "content": message})

            # Display the user's message in the chat window
            with st.chat_message("user", avatar='👨‍💻'):
                st.markdown(message)

            # Fetch and stream the assistant's response from the Groq API
            try:
                # Pass the entire message history (including the current user message)
                chat_completion = get_chat_response(api_key, st.session_state.messages, choose_model)

                with st.chat_message("assistant", avatar="🤖"):
                    # Stream the assistant's response in real time
                    chat_responses_generator = generate_chat_responses(chat_completion)
                    full_response = st.write_stream(chat_responses_generator)

                # Store the full assistant's response in session state
                if isinstance(full_response, str):
                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_response}
                    )
                else:
                    # Handle non-string responses (e.g., list of chunks)
                    combined_response = "\n".join(str(item) for item in full_response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": combined_response}
                    )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Entry point to run the Streamlit app
if __name__ == "__main__":
    streamlit_app()