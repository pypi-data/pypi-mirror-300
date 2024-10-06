import nltk
from nltk.tokenize import word_tokenize

# Download required NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')

# Name of the chatbot
bot_name = "Chatbot"

# List of conversations
conversations = []

def ChatBot(name):
    global bot_name
    bot_name = name

def add_conversation(coversation):
    global conversations
    conversations = coversation

def find_best_response(user_input):
    # Tokenize the user input
    user_tokens = set(word_tokenize(user_input.lower()))
    
    best_match = None
    max_overlap = 0
    
    # Iterate over each conversation
    for request, response in conversations:
        request_tokens = set(word_tokenize(request.lower()))
        
        # Find the overlap between the user's tokens and request tokens
        overlap = len(user_tokens.intersection(request_tokens))
        
        # Update the best match if this one has more overlap
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = response
    
    if best_match:
        return best_match
    else:
        return "Sorry, I don't understand that."