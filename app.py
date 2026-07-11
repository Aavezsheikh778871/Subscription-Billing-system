from flask import Flask, jsonify, request
import json
import sys
from Billing import Free_user, Premium_user, Corporate_user
import sqlite3


app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

users = {}

@app.route("/")
def home():
    return "Welcome to Subscription Billing System!"

@app.route("/about")
def about():
    return "These is the Subscription Billing System build with Python & Flask!"

@app.route("/ledger")
def ledger():
    
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    
    cursor.execute ("SELECT * FROM transactions")
    
    rows = cursor.fetchall()
    
    conn.close()
    result = []
    for row in rows:
        result.append({
            "id" : row[0],
            "name" : row[1],
            "amount" : row[2],
            "type" : row[3],
            "date" : row[4]
        }
        )

    return jsonify(result)  

@app.route("/deposit", methods=["POST"])
def deposit():
    raw_data = request.get_data(as_text=True)
    data = json.loads(raw_data)
    name = data["name"]
    amount = data["amount"]
    tier = data.get("tier", "free")
    
    if name not in users:
        if tier == "premium":
            users[name] = Premium_user(name, f"{name}@email.com")
        else:
            users[name] = Free_user(name, f"{name}@email.com")
    
    users[name].deposit(amount)
    return jsonify({"message": f"Deposited {amount} for {name} successfully!"})

@app.route("/charge", methods=["POST"])
def charge():
    data = request.get_json()
    name = data["name"]
    amount = data["amount"]
    tier = data.get("tier", "free")
    
    if name not in users:
        if tier == "premium":
            users[name] = Premium_user(name, f"{name}@email.com")
        else:
            users[name] = Free_user(name, f"{name}@email.com")
    
    users[name].charge_fee(amount)
    return jsonify({"message": f"Charge {amount} for {name} successfully!"})

@app.route("/user/<string:name>", methods=["GET"])
def get_user_transactions(name):
    
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transactions WHERE name = ?", (name,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return jsonify({"error" : f"No transactions found for user '{name}'"}), 404
    
    user_history = []
    for row in rows:
        user_history.append({
          "id" : row[0],
          "name" : row[1],
          "amount" : row[2],
          "type" : row[3],
          "date" : row[4]  
        })
    
    return jsonify({
        "user" : name,
        "total_transactions" : len(user_history),
        "history" : user_history 
        }), 200

if __name__ == "__main__":
    app.run(debug=True)
    