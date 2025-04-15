import requests
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from session import Session

class EditProjetDialog(QDialog):
    def __init__(self, projet, parent=None):
        super().__init__(parent)
        self.projet = projet
        self.setWindowTitle("Modifier le Projet")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nom_input = QLineEdit(self.projet['nom'])
        self.client_input = QLineEdit(self.projet.get('nomClient', ''))
        self.desc_input = QTextEdit(self.projet.get('description', ''))

        self.submit_button = QPushButton("Mettre à jour")
        self.submit_button.setStyleSheet("background-color: #2176AE; color: white; padding: 8px;")
        self.submit_button.clicked.connect(self.submit_update)

        layout.addWidget(QLabel("Nom du projet:"))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel("Nom du client:"))
        layout.addWidget(self.client_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_update(self):
        try:
            updated_data = {
                "nom": self.nom_input.text(),
                "nomClient": self.client_input.text(),
                "description": self.desc_input.toPlainText(),
               
            }

            response = requests.put(
                f"http://localhost:8090/api/projets/{self.projet['id']}",
                json=updated_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in [200, 204]:
                QMessageBox.information(self, "Succès", "Projet modifié avec succès.")
                self.accept()
            else:
                QMessageBox.critical(self, "Erreur", f"Échec de la mise à jour:\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))