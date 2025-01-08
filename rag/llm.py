import google.generativeai as genai
from key import GEMINI_API_KEY

MODEL_NAME = "gemini-1.5-pro"
genai.configure(api_key=GEMINI_API_KEY)

def prepare_chat_prompt(context: str, user_input: str) -> str:
    system_prompt = (
        "You are a specialized healthcare assistant focusing on Nepal's National Guidelines "
        "for STI/STD Management. Your knowledge is based on official documentation and protocols.\n\n"
        f"Context from guidelines:\n{context}\n\n"
        f"User Question: {user_input}"
    )
    return system_prompt

def llm_invoke(context: str, user_input: str):
    try:
        print("LLM thinking...")
        
        if not context or context == "No relevant context found.":
            if user_input.lower().startswith(("what is", "tell me about")):
                return "I need more specific information from the guidelines to answer your question accurately. Could you please rephrase your question?"
        
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = prepare_chat_prompt(context, user_input)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        return f"Sorry, I couldn't process your request. Error: {str(e)}"

# Example usage
context = "The Eiffel Tower is located in Paris, France."
question = "Where is the Eiffel Tower located?"
response = llm_invoke(context, question)
print(response)