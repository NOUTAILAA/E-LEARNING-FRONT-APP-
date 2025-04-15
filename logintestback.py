import requests

url = "http://localhost:8090/api/login"

data = {
    "email": "notaila7@gmail.com",
    "password": "SXIM@3qeNY"
}

try:
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("✅ Connexion réussie !")
        print("Message du serveur :", response.text)
    elif response.status_code == 401:
        print("❌ Identifiants incorrects.")
    else:
        print(f"⚠️ Erreur inattendue ({response.status_code}) : {response.text}")

except requests.exceptions.RequestException as e:
    print("🚫 Erreur de connexion au serveur :", e)
