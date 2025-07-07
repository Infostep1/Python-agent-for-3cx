import json
from flask import Flask, request, jsonify
import requests
import time


# Function to get the base URL from the request
app = Flask(__name__)
@app.route('/3cx', methods=['POST'])

def ReceiveCall():

    if(request.json==None):
        return jsonify({"error": "No JSON data provided"}), 400

    data=request.json
    print("received call")
    print("Received data:", data)

    phonenumber = data.get("phone")
    if not phonenumber:
        return jsonify({"error": "Phone number not provided"}), 400
    
    Name = data.get("Name")
    if not Name:
        return jsonify({"error": "Name not provided"}), 400
    
    print("Phone number:", phonenumber)
    print("Name:", Name)
    return jsonify({"status": "success", "message": "Data received successfully"}), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# πρεπει να βρω τι απο τα 2 ειναι συμφωνα μρ το trdr και να στελνω το καταλληλο αιτημα 