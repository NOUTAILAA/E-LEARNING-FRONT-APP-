import requests
import json

url = "http://localhost:8090/api/superadmins"
headers = {"Content-Type": "application/json"}

data = {
    "nom": "admin",
    "prenom": "admin",
    "dateNaissance": "1990-01-01",
    "telephone": "012345679",
    "sexe": "Masculin",
    "email": "admin",
    "password": "admin",
    "role": "superadmin",
    "etat": True
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("SuperAdmin créé avec succès:", response.json())
else:
    print("Erreur:", response.status_code, response.text)