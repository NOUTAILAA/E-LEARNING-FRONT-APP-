# Superadmin/profiledetailspage.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import requests
import base64
from session import Session

class ProfileDetailsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Détails du SuperAdmin")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("border-radius: 75px; border: 3px solid #2176AE;")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.labels = {}

        fields = ["Nom", "Prénom", "Date de naissance", "Téléphone", "Sexe", "Email", "Rôle", "État"]
        for field in fields:
            label = QLabel(f"{field} : ")
            label.setFont(QFont("Arial", 14))
            layout.addWidget(label)
            self.labels[field] = label

        self.setLayout(layout)
        self.load_profile()

    def load_profile(self):
        email = Session.current_user_email
        try:
            response = requests.get("http://localhost:8090/api/superadmins/email", params={"email": email})
            if response.status_code == 200:
                user = response.json()
                self.labels["Nom"].setText(f"Nom : {user.get('nom')}")
                self.labels["Prénom"].setText(f"Prénom : {user.get('prenom')}")
                self.labels["Date de naissance"].setText(f"Date de naissance : {user.get('dateNaissance')}")
                self.labels["Téléphone"].setText(f"Téléphone : {user.get('telephone')}")
                self.labels["Sexe"].setText(f"Sexe : {user.get('sexe')}")
                self.labels["Email"].setText(f"Email : {user.get('email')}")
                self.labels["Rôle"].setText(f"Rôle : {user.get('role')}")
                etat = "Vérifié" if user.get("etat") else "Non vérifié"
                self.labels["État"].setText(f"État : {etat}")

                # Affichage de la photo (si présente)
                photo_data = user.get("photo")
                if photo_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(base64.b64decode(photo_data))
                    pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.photo_label.setPixmap(pixmap)
                else:
                    self.photo_label.setText("Aucune photo")
            else:
                self.labels["Nom"].setText("Erreur : utilisateur introuvable")
        except Exception as e:
            self.labels["Nom"].setText(f"Erreur : {str(e)}")
