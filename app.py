from flask import Flask, render_template, request, redirect, url_for, send_file
from openai import OpenAI
from dotenv import load_dotenv  # Import the load_dotenv function
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Custom OpenAI client configuration
client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),  # Get API key from .env file
)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission and generate portfolio
@app.route('/generate', methods=['POST'])
def generate():
    # Get user input from the form
    name = request.form['name']
    skills = request.form['skills']
    experience = request.form['experience']
    projects = request.form['projects']

    # Generate AI-enhanced content for all sections
    about = get_ai_summary(f"Write a professional 'About Me' section for a portfolio. Name: {name}, Skills: {skills}, Experience: {experience}, Projects: {projects}")
    skills_content = get_ai_summary(f"Write a detailed 'Skills' section for a portfolio. Skills: {skills}")
    experience_content = get_ai_summary(f"Write a detailed 'Experience' section for a portfolio. Experience: {experience}")
    projects_content = get_ai_summary(f"Write a detailed 'Projects' section for a portfolio. Projects: {projects}")

    # Render the portfolio template with AI-generated content
    portfolio_html = render_template('portfolio_template.html', 
                                    name=name, 
                                    about=about,
                                    skills=skills_content,
                                    experience=experience_content,
                                    projects=projects_content)

    # Save the generated portfolio as an HTML file
    with open('generated_portfolio.html', 'w') as file:
        file.write(portfolio_html)

    return redirect(url_for('download'))

# Route to download the generated portfolio
@app.route('/download')
def download():
    return send_file('generated_portfolio.html', as_attachment=True)

# Function to get AI-generated content
def get_ai_summary(input_text):
    response = client.chat.completions.create(
        model="o1",  # Use the custom model
        messages=[
            {
                "role": "user",
                "content": input_text
            },
        ],
    )
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    app.run(debug=True)