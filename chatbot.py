import logging
from datetime import datetime

logging.basicConfig(filename="chatbot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_conversation(user_input, bot_response):
    logging.info(f"User: {user_input}")
    logging.info(f"Bot: {bot_response}")

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"

    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"

    elif "what can you do" in user_input or "what do you do" in user_input:
        return "I can assist you with basic queries and provide information."

    elif "what is your name" in user_input:
        return "I am a simple rule-based chatbot created to assist you!"

    elif "time" in user_input or "what time is it" in user_input or "current time" in user_input:
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    elif "date" in user_input or "what is the date" in user_input or "today's date" in user_input:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f"Today's date is {current_date}."

    elif "weather" in user_input:
        return "Sorry, I can't provide real-time weather updates yet."

    elif "joke" in user_input:
        return "Why don't scientists trust atoms? Because they make up everything!"

    elif "exit" in user_input or "quit" in user_input:
        return "exit"  # Special command to exit the loop

    else:
        return "I'm sorry, I don't understand that. Could you please rephrase?"

def run_chatbot():
    print("Welcome to the Enhanced Rule-Based Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation.")

    conversation_history = []  # List to store the conversation history

    while True:
        try:
            user_input = input("You: ")
            bot_response = chatbot_response(user_input)

            if bot_response == "exit":
                print("Chatbot: Goodbye!")
                break

            print(f"Chatbot: {bot_response}")

          
            log_conversation(user_input, bot_response)
            conversation_history.append(f"You: {user_input}")
            conversation_history.append(f"Chatbot: {bot_response}")

        except Exception as e:
            print("Chatbot: Sorry, something went wrong.")
            logging.error(f"Error: {str(e)}")

  
    with open("conversation_history.txt", "w") as history_file, open("conversation_history.txt", "a") as history_file:
        for line in conversation_history:
            history_file.write(line + "\n")

    print("Conversation history saved to 'conversation_history.txt'.")

if __name__ == "__main__":
    run_chatbot()
