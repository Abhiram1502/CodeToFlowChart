import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
from converter import python_to_mermaid

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()

# Configure Gemini AI with error handling
try:
    # Get API key from environment variables
    GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GEMINI_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set")
    
    # Initialize Gemini with current model name
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro')  # Updated model name
    print("✅ Gemini AI configured successfully")
except Exception as e:
    print(f"❌ Gemini configuration failed: {str(e)}")
    model = None  # Allows app to run without Gemini functionality

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    mermaid_code = ""
    explanation = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")
        
        # Generate Mermaid flowchart
        try:
            mermaid_code = python_to_mermaid(code)
            print("✅ Flowchart generated successfully")
        except Exception as e:
            print(f"❌ Flowchart generation failed: {str(e)}")
            mermaid_code = "graph TD\nA[\"Error generating flowchart\"]"
        
        # Generate AI explanation if model is available
        if model and code.strip():
            try:
                prompt = f"""Explain this Python code clearly and concisely:
                
                {code}
                
                Provide:
                1. What the code does
                2. Key functions/variables
                3. The logical flow
                4. Example use case if applicable"""
                
                response = model.generate_content(prompt)
                explanation = response.text
                print("✅ Explanation generated successfully")
            except Exception as e:
                explanation = f"⚠️ Could not generate explanation: {str(e)}"
                print(f"❌ Explanation failed: {str(e)}")
    
    return render_template(
        "index.html",
        code=code,
        mermaid_code=mermaid_code,
        explanation=explanation
    )

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    )
