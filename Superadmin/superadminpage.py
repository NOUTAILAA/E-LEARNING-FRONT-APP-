from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SuperAdminPage(QDialog):
    """ Page spécifique pour le SuperAdmin """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Page SuperAdmin")
        self.setGeometry(100, 100, 800, 600)

        # Création du layout principal
        main_layout = QHBoxLayout()

        # Création de la navbar
        navbar = self.create_navbar()

        # Widget pour afficher les différentes sections (via QStackedWidget)
        self.stacked_widget = QStackedWidget()

        # Ajoutez une page d'exemple dans le stacked widget
        self.stacked_widget.addWidget(QLabel("Page d'Administrateurs"))
        
        # Ajoutez d'autres pages si nécessaire ici
        # Exemple: self.stacked_widget.addWidget(self.create_departments_page())

        # Ajouter la navbar et le stacked widget au layout principal
        main_layout.addWidget(navbar)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def create_navbar(self):
        """ Crée la navbar avec les différentes sections """
        navbar = QFrame()
        navbar.setStyleSheet("background-color: #2176AE; padding: 20px; border-radius: 5px; width: 200px;")
        navbar_layout = QVBoxLayout()

        # Ajouter le titre "Capgemini"
        logo_label = QLabel("Capgemini")
        logo_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: white; padding-bottom: 20px;")
        navbar_layout.addWidget(logo_label)

        # Ajouter les boutons de navigation
        self.create_nav_button("Administrateurs", navbar_layout)
        self.create_nav_button("Departments", navbar_layout)
        self.create_nav_button("Settings", navbar_layout)
        self.create_nav_button("Profile Details", navbar_layout)
        self.create_nav_button("Help & Support", navbar_layout)

        # Ajouter le bouton "Log out"
        logout_button = QPushButton("Log out")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2176AE;
                border-radius: 10px;
                padding: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        logout_button.clicked.connect(self.logout)
        navbar_layout.addWidget(logout_button)

        navbar.setLayout(navbar_layout)
        return navbar

    def create_nav_button(self, label, layout):
        """ Crée un bouton pour chaque section dans la navbar """
        button = QPushButton(label)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2176AE;
                color: white;
                border: none;
                padding: 10px;
                margin-bottom: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1B5E86;
            }
        """)
        button.clicked.connect(lambda: self.change_page(label))
        layout.addWidget(button)

    def change_page(self, page_name):
        """ Change de page dans le stacked widget en fonction du bouton cliqué """
        if page_name == "Administrateurs":
            self.stacked_widget.setCurrentIndex(0)
        elif page_name == "Departments":
            self.stacked_widget.setCurrentIndex(1)
        elif page_name == "Settings":
            self.stacked_widget.setCurrentIndex(2)
        elif page_name == "Profile Details":
            self.stacked_widget.setCurrentIndex(3)
        elif page_name == "Help & Support":
            self.stacked_widget.setCurrentIndex(4)

    def logout(self):
        """ Action pour déconnecter l'utilisateur (peut être améliorée) """
        print("Déconnexion DE SUPERADMIN")
        self.close()

