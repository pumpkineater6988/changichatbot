import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import markdown 

# Correct: pass the dotenv_path here
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

app = Flask(__name__)
chat_history = []  # Stores (user_input, bot_response_html)

@app.route("/", methods=["GET", "POST"])
def index():
    bot_response = None
    if request.method == "POST":
        user_query = request.form.get("query")
        if user_query:
            # Reconstruct the prompt
            prompt_text = "\n".join([f"User: {q}\nBot: {a}" for q, a in chat_history])
            prompt_text += f"\nUser: {user_query}\nBot:"

            # Get model response
            response = model.generate_content(prompt_text)
            answer_raw = response.text.strip()

            # Convert Markdown (**bold**, etc.) to HTML
            answer_html = markdown.markdown(answer_raw)

            # Store user query and HTML-safe bot response
            chat_history.append((user_query, answer_html))
            bot_response = answer_html

    return render_template("index.html", chat_history=chat_history, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
