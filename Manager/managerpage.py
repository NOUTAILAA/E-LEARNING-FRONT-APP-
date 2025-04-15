from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QWidget, QFrame
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from Manager.listeapprenants import ListeApprenantsPage
from Manager.Projets.listeprojets import ListeProjetsPage

class ManagerPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Espace Manager")
        self.setGeometry(100, 100, 1000, 700)

        main_layout = QVBoxLayout()

        # ========== NAVBAR (Top) ==========
        navbar = QFrame()
        navbar.setStyleSheet("background-color: #2176AE; padding: 12px 30px;")
        nav_layout = QHBoxLayout(navbar)

        # Logo Capgemini
        logo_label = QLabel("Capgemini")
        logo_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: white;")
        nav_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Espace central vide
        nav_layout.addStretch()

        # Boutons de navigation
        btn_projets = QPushButton("Projets")
        btn_learners = QPushButton("Learners")
        for btn in [btn_projets, btn_learners]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    font-weight: bold;
                    padding: 6px 15px;
                    border: none;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)
        nav_layout.addWidget(btn_projets)
        nav_layout.addWidget(btn_learners)

        # Avatar utilisateur
        avatar = QLabel()
        pixmap = QPixmap("1.jpg").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        avatar.setPixmap(pixmap)
        avatar.setFixedSize(32, 32)
        avatar.setStyleSheet("border-radius: 16px;")
        nav_layout.addWidget(avatar)

        # ========== STACKED PAGES ==========
        self.stacked = QStackedWidget()
        self.stacked.addWidget(ListeApprenantsPage())  # Index 0
        self.stacked.addWidget(ListeProjetsPage())

        # Actions des boutons
        btn_learners.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        btn_projets.clicked.connect(lambda: self.stacked.setCurrentIndex(1))

        # Layout principal
        main_layout.addWidget(navbar)
        main_layout.addWidget(self.stacked)

        self.setLayout(main_layout)
