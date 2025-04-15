import requests
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QFrame, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class ListeCoursPage(QWidget):
    def __init__(self, projet, parent=None):
        super().__init__(parent)
        self.projet = projet
        self.setWindowTitle(f"Cours - {projet['nom']}")
        self.setMinimumWidth(800)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel(f"{self.projet['nom']} - Tous les cours")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.cours_layout = QHBoxLayout(container)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.setLayout(layout)
        self.load_cours()

    def load_cours(self):
        try:
            response = requests.get(f"http://localhost:8090/api/cours/projet/{self.projet['id']}")
            response.raise_for_status()
            cours_list = response.json()

            for cours in cours_list:
                self.cours_layout.addWidget(self.create_cours_card(cours))

        except requests.RequestException as e:
            QMessageBox.critical(self, "Erreur", f"Échec de chargement des cours:\n{e}")

    def create_cours_card(self, cours):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 15px;
                margin: 10px;
            }
        """)
        card.setFixedSize(250, 160)

        layout = QVBoxLayout()

        title = QLabel(cours['titre'])
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))

        desc = QLabel(cours.get('description', ''))
        desc.setStyleSheet("color: gray; font-size: 12px;")
        desc.setWordWrap(True)

        btns = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        view_btn = QPushButton("View")

        btns.addWidget(delete_btn)
        btns.addWidget(view_btn)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addLayout(btns)

        card.setLayout(layout)
        return card
