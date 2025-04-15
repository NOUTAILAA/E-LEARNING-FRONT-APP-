from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QMessageBox
import requests

class AffectationPopup(QWidget):
    def __init__(self, manager_id, manager_name):
        super().__init__()
        self.manager_id = manager_id
        self.setWindowTitle("Assigner Apprenant au Manager")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Titre principal
        title = QLabel("Assigner Apprenant au manager")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Nom du manager
        layout.addWidget(QLabel("Full Name"))
        manager_label = QLabel(manager_name)
        manager_label.setStyleSheet("background-color: #eee; padding: 6px; border-radius: 5px;")
        layout.addWidget(manager_label)

        # Liste déroulante des apprenants
        layout.addWidget(QLabel("Apprenants List"))
        self.combo = QComboBox()

        try:
            url = f"http://localhost:8090/api/managers/{self.manager_id}/apprenants-non-assignes"
            response = requests.get(url)
            response.raise_for_status()
            for apprenant in response.json():
                full_name = f"{apprenant['prenom']} {apprenant['nom']}"
                self.combo.addItem(full_name, userData=apprenant['id'])
        except Exception as e:
            print("Erreur de chargement des apprenants non assignés:", e)
            QMessageBox.warning(self, "Erreur", f"Impossible de charger les apprenants: {e}")

        layout.addWidget(self.combo)

        # Bouton d'assignation
        self.assign_button = QPushButton("Assigner")
        self.assign_button.setStyleSheet("""
            QPushButton {
                background-color: #0070AD;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005A8D;
            }
        """)
        self.assign_button.clicked.connect(self.assign_apprenant)
        layout.addWidget(self.assign_button)

        self.setLayout(layout)

    def assign_apprenant(self):
        apprenant_id = self.combo.currentData()
        try:
            url = f"http://localhost:8090/api/managers/{self.manager_id}/assign-apprenants"
            response = requests.post(
                url,
                json=[apprenant_id],
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            QMessageBox.information(self, "Succès", "Apprenant assigné avec succès !")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur d'assignation : {e}")
