import os
import google.generativeai as genai
from flask import Flask, render_template, request
from markdown import markdown

# --- Flask App Initialisation ---
app = Flask(__name__)


# --- Configuration ---

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except:
    print("API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    exit()

# --- The Core AI Function ---
def review_code(code_snippet: str, code_lang: str) -> str:
    """
    Sends a code snippet to the Gemini API for review.

    Args:
        code_snippet: A string containg the code to be reviewed.

    Returns:
        A string with the AI's feedback, or an error message.
    """
    prompt = f"""
    Please act as an expert code reviewer.
    Review the following {code_lang} code snippet for bugs, style issues, and potential improvements.
    Provide your feedback in a clear, constructive manner.
    Explain the "what" and the "why" for each point.

    Code to review:
    ```{code_lang}
    {code_snippet}
    ```
    """
    try:
        # Intialise the generative model.
        model = genai.GenerativeModel('gemini-2.5-pro')
        # Send the prompt to the model
        response = model.generate_content(prompt)

        # Return the model's response text
        return markdown(response.text)
    except Exception as e:
        return f"An error occured: {e}"
 
 # --- Web Page Route ---
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/review', methods=['POST'])
def review():
    user_code = request.form['code']
    user_config = request.form['config']

    feedback = review_code(user_code, user_config)

    return render_template('review.html', code=user_code, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)