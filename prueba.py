import requests

url = "http://localhost:5678/webhook/emily-tech-chatbot"

payload = {
    "message": "¿Dónde está ubicada Emily Tech?"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print("Respuesta del chatbot:")
    print(response.text)
else:
    print("Error:", response.status_code)
    print(response.text)
