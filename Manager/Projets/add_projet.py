import requests
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from session import Session
import json

class AjoutProjetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Projet")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du projet")
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Nom du client")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description")

        self.submit_button = QPushButton("Ajouter")
        self.submit_button.setStyleSheet("background-color: #2176AE; color: white; padding: 8px;")
        self.submit_button.clicked.connect(self.submit_projet)

        layout.addWidget(QLabel("Nom du projet:"))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel("Nom du client:"))
        layout.addWidget(self.client_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_projet(self):
        email = Session.current_user_email
        try:
            manager_response = requests.get(f"http://localhost:8090/api/managers/email?email={email}")
            manager = manager_response.json()
            manager_id = manager['id']
            departement_id = manager['departement']['id']

            projet_data = {
    "nom": self.nom_input.text(),
    "nomClient": self.client_input.text(),
    "description": self.desc_input.toPlainText(),
    "managerId": manager_id,
    "departementId": departement_id
}


            headers = {"Content-Type": "application/json"}
            response = requests.post("http://localhost:8090/api/projets", json=projet_data, headers=headers)

            if response.status_code in [200, 201]:
                QMessageBox.information(self, "Succès", "Projet ajouté avec succès.")
                self.accept()
            else:
                QMessageBox.critical(self, "Erreur", f"Échec de l'ajout du projet:\n{response.text}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
