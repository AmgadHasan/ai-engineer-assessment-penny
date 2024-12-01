import gradio as gr

from src.llm import handle_user_message

from src.utils import create_logger, log_execution_time

logger = create_logger(logger_name="main", log_file="api.log", log_level="info")

# Initialize an empty chat history
chat_history = []


# Function to update the chat history
@log_execution_time(logger=logger)
def update_chat_history(user_message):
    chat_history.append(f"User: {user_message}")
    response = handle_user_message(user_message)
    chat_history.append(f"Bot: {response}")
    logger.info(f"{user_message = }\n{response = }")
    return response, "\n".join(chat_history)


# Create the chatbot UI
demo = gr.Interface(
    fn=update_chat_history,
    inputs=["text"],
    outputs=[
        gr.Markdown(value="Bot Response", container=True),
        gr.Textbox(label="Chat History"),
    ],
    title="Chatbot UI",
    description="Enter your query",
)

if __name__ == "__main__":
    demo.launch()
