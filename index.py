import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="AIzaSyAwQ8kR0K4tHxAqfiPyP-NpkvZCHZCGBRs")

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Continuous interaction loop
print("Welcome to the Gemini AI Chatbot! Type 'exit' to quit.")
while True:
    # Get user input
    user_input = input("You: ")
    
    # Exit the loop if the user types 'exit'
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # Generate a response from the model
    response = model.generate_content(user_input)
    
    # Print the model's response
    print("Gemini:", response.text)