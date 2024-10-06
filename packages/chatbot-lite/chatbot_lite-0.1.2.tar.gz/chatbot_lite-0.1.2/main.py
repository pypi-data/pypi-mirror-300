from chatbot import add_conversation, find_best_response

# List of conversations
conversations = [
    ("hello", "Hi there! How can I help you?"),
    ("how are you?", "I'm just a bot, but thanks for asking!"),
    ("what is your name?", "I am a simple chatbot."),
    ("bye", "Goodbye! Have a great day!"),
]

def main():
    add_conversation(conversations)

    print("Chatbot: Hello! I'm here to chat. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        response = find_best_response(user_input)
        print(f"Chatbot: {response}")

main()