from flask import Flask, render_template, request, jsonify
from pywhatkit import send_mail
import os
from pymongo import MongoClient
app = Flask(__name__, template_folder='templates')

mail = os.getenv('mail')  #have to provide app mail to work
password = os.getenv('pass')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/storeDB', methods=['POST'])
def storeDB():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    pkey = data.get('pkey')
    print(email)
    print(name)
    print(pkey)
    try:
        client = MongoClient("mongodb+srv://sohamde2004:sohamjgd@sohamcluster.imcgngv.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("Razor_pay")
        records = db.Keys_DB

        new_key = {
            "testkey":f"{pkey}",
            "name" : name,
            "valid":"true"
        }
        records.insert_one(new_key)
    # Do something with the received data (e.g., process, store, or return a response)
    
        response_data = {"message": "Data received successfully"}
    except Exception as e:
        response_data = {"message": f"error {e}"}   

    return jsonify(response_data)

@app.route('/process-transaction', methods=['POST'])
def process_transaction():
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        pKey = data.get('productKey')
        # transaction_details = data.get('transactionDetails')
        # transaction_hash = transaction_details.get('hash', 'N/A')

        # Add your logic to process the transaction details, email, and name
        # For example, print them for now
        # print(f"Transaction Hash: {transaction_hash}")

        content = f'''
        Dear {name},

        Your Product Key: {pKey}
        Do not share with anyone, unless you're planning to gift them. 

        Thank you for choosing JARVIS.ai! We're excited to have you on board. Experiment with its features and enhance your productivity.
        We truly appreciate your purchase, and just like Iron Man, our team would want you to know that We Love You 3000 <3 

        Soham De
        The Boys Team
        '''

        send_mail(mail, password, "Thank You for Choosing JARVIS.ai!", message=content, email_receiver=email)
        print(f"Email: {email}")
        print(f"Name: {name}")

        # Respond with a success message
        return jsonify({'message': 'Transaction details received and processed successfully'}), 200
    except Exception as e:
        print(f"Error processing transaction details: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
