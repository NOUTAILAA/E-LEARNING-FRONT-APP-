from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AdminPage(QDialog):
    """ Page spécifique pour l admin """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Page Admin")
        self.setGeometry(100, 100, 800, 600)

        # Initialisation de l'interface
        layout = QVBoxLayout()

        # Titre de la page
        welcome_label = QLabel("Bienvenue sur la page Admin")
        welcome_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)



        layout.addWidget(welcome_label)
        self.setLayout(layout)
