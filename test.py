import requests

data = {
    "name" : "Aavuu",
    "email" : "aavuu@email.com",
    "amount": 2000,
    "type" : "Free"   
}

response = requests.post("http://127.0.0.1:5000/deposit", json=data)
print(response.json())
    
