from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import requests
from session import Session

class ListeApprenantsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout(self)

        # Titre
        title = QLabel("Liste des Apprenants Affectés")
        title.setObjectName("title")
        layout.addWidget(title)

        # Barre de recherche
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search name, email, or etc..")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px 12px;
            }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addStretch()
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Prénom", "Nom", "Email"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # Charger les données
        self.apprenants = []  # Pour garder toutes les données
        self.load_apprenants_assignes()

    def load_apprenants_assignes(self):
        email = Session.current_user_email
        if not email:
            return

        try:
            # Trouver l'ID du manager connecté
            response = requests.get("http://localhost:8090/api/managers")
            response.raise_for_status()
            managers = response.json()

            manager_id = next((m['id'] for m in managers if m['email'] == email), None)
            if manager_id is None:
                raise Exception("Manager non trouvé")

            # Récupérer les apprenants
            apprenant_response = requests.get(f"http://localhost:8090/api/managers/{manager_id}/apprenants")
            apprenant_response.raise_for_status()
            self.apprenants = apprenant_response.json()

            self.populate_table(self.apprenants)

        except Exception as e:
            print("Erreur de chargement des apprenants :", e)

    def populate_table(self, apprenants):
        self.table.setRowCount(len(apprenants))
        for row, apprenant in enumerate(apprenants):
            self.table.setItem(row, 0, QTableWidgetItem(apprenant['prenom']))
            self.table.setItem(row, 1, QTableWidgetItem(apprenant['nom']))
            self.table.setItem(row, 2, QTableWidgetItem(apprenant['email']))

    def filter_table(self, text):
        # Filtrage dynamique (recherche par prénom, nom ou email)
        filtered = [
            apprenant for apprenant in self.apprenants
            if text.lower() in apprenant['prenom'].lower()
            or text.lower() in apprenant['nom'].lower()
            or text.lower() in apprenant['email'].lower()
        ]
        self.populate_table(filtered)
