from flask import Flask, request, jsonify, render_template, url_for
from openai import OpenAI
import pdfplumber
import os

app = Flask(__name__)

# Set OpenAI API key (replace with your actual key or set it as an environment variable)
client = OpenAI(
    api_key=""
)

def extract_pdf_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        # Get data from the request
        data = request.json
        insurance_company = data.get("insuranceCompany", "")
        insurance_plan = data.get("insurancePlan", "")
        medical_issue = data.get("medicalIssue", "")

        pdf_path = None

        if insurance_company == "Ambetter Health":
            match insurance_plan:
                case "Bronze":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/ambetter_bronze.pdf"
                case "Elite Bronze":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/ambetter_elite_bronze.pdf"
                case "Silver:":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/ambetter_silver.pdf"
                case "Elite Silver":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/ambetter_elite_silver.pdf"
                case "Gold:":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/ambetter_gold.pdf"
        elif insurance_company == "AvMed":
            match insurance_plan:
                case "Bronze":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/avmed_bronze.pdf"
                case "Silver":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/avmed_silver.pdf"
                case "Gold":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/avmed_gold.pdf"
                case "Platinum":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/avmed_platinum.pdf"
        elif insurance_company == "Florida Blue":
            match insurance_plan:
                case "Bronze":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/flblue_bronze.pdf"
                case "Silver":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/flblue_silver.pdf"
                case "Gold":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/flblue_gold.pdf"
                case "Platinum":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/flblue_platinum.pdf"
        elif insurance_company == "Oscar Insurance Company of Florida":
            match insurance_plan:
                case "Bronze":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/oscar_bronze.pdf"
                case "Silver":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/oscar_silver.pdf"
                case "Gold":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/oscar_gold.pdf"
                case "Gold Elite Saver Plus":
                    pdf_path = "C:/Users/Hanlin/Documents/Summaries/oscar_gold_elite_saver_plus.pdf"

        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({"error": "No corresponding PDF found for the selected plan."}), 400

        # Extract text from the selected PDF
        pdf_text = extract_pdf_text(pdf_path)
        if not pdf_text:
            return jsonify({"error": "Failed to extract text from the PDF."}), 500

        # Validate input
        if not insurance_company or not insurance_plan or not medical_issue:
            return jsonify({"error": "All fields are required"}), 400

        # Construct the prompt using the dropdown selections and query
        prompt = (f"You are an insurance assistant. The user selected the following options:\n"
                  f"- Insurance Company: {insurance_company}\n"
                  f"- Insurance Plan: {insurance_plan}\n"
                  f"Here is the policy document:\n{pdf_text}\n\n"
                  f"Here is the query: {medical_issue}\n\n"
                  f"Please answer the user's query based on their insurance company and plan.")

        # Call OpenAI ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are made to help people decipher their insurance information, \
        including questions about cost of prescriptions and certain medical procedures. You will be given a PDF document of their coverage. You will answer \
        the following questions per prompt: Is the patient's requested care covered by their insurance plan? \
        Does the patient have a deductible? If the patient does, does it need to be fulfilled before the patient can claim this benefit? \
         Does the patient have an out of pocket max? If the patient is requesting to see a doctor, does the patient need a referral to see this doctor? \
          Does the patient need to visit an in-network provider, if so, where can the patient find a list of in-network providers? \
           Are there any complications to how the patient will receive carE if they use their insurance policy?"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        # Extract the generated text
        generated_text = response.choices[0].message.content
        print("Gen:")
        print(generated_text)
        
        # Return the result
        return jsonify({"generated_text": generated_text})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET', "POST"])
def indexPage():
    if request.method == "POST":
        print("Hello world")
    return render_template('AskADuckHome.html')

@app.route('/about', methods=['GET'])
def aboutPage():
    return render_template("AskADuckAbout.html")

if __name__ == "__main__":
    app.run(host='localhost', port=80)