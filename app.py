from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = "https://bhask-m3r05351-swedencentral.cognitiveservices.azure.com/"  
openai.api_version = "2024-08-01-preview"  
openai.api_key = "4tB4BuZZMtCRxn2XAfD8fUefykxMUTemNcj3KaQ2iBJFb2DeIXJvJQQJ99AKACfhMk5XJ3w3AAAAACOGRNXv"

deployment_name = "gpt-4" 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    ticket_description = request.form.get('ticket_description')
    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing ticket solutions."},
                {"role": "user", "content": f"Provide three potential solutions to address the issue described in the ticket. For each solution, provide a detailed explanation of how it helps resolve the error. Use the following format:\nSolution 1: Detailed explanation of Solution 1 to overcome the error (ticket).\nSolution 2: Detailed explanation of Solution 2 to overcome the error (ticket).\nSolution 3: Detailed explanation of Solution 3 to overcome the error (ticket).: {ticket_description}"}
            ],
            max_tokens=300,
            temperature=0.7
        )

        solutions = response['choices'][0]['message']['content'].split('\n')

        confidence_levels = [round(90 - i * 10, 2) for i in range(len(solutions))]

        solution_data = [{"solution": sol.strip(), "confidence": conf} for sol, conf in zip(solutions, confidence_levels)]

        return render_template('result.html', solutions=solution_data, ticket_description=ticket_description)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
