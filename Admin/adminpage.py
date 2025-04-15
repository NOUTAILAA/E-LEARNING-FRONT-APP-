from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Admin.listedepartment import DepartementsPage
from Admin.listemanager import ManagersPage
from Admin.listeapprenant import ApprenantsPage  # Import de la nouvelle page pour les apprenants
from Admin.ProfileDetailsPage import ProfileDetailsPage
from Admin.assignements import AssignementsPage;
class AdminPage(QDialog):
    """ Page spécifique pour le Admin """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Page Admin")
        self.setGeometry(100, 100, 900, 500)

        # Création du layout principal
        main_layout = QHBoxLayout()

        # Création de la navbar
        navbar = self.create_navbar()

        # Widget pour afficher les différentes sections (via QStackedWidget)
        self.stacked_widget = QStackedWidget()

        # Ajoutez les pages dans le stacked widget
        self.stacked_widget.addWidget(DepartementsPage())  # Page des départements
        self.stacked_widget.addWidget(ManagersPage())  # Page des managers
        self.stacked_widget.addWidget(ApprenantsPage())  # Page des apprenants
        self.stacked_widget.addWidget(ProfileDetailsPage())  # index 3
        self.stacked_widget.addWidget(AssignementsPage())  # index 4

        # Set the initial page to be ListeAdminPage (index 0)
        self.stacked_widget.setCurrentIndex(0)  # Par défaut, afficher la page des administrateurs

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
        self.create_nav_button("Departements", navbar_layout)
        self.create_nav_button("Managers", navbar_layout)
        self.create_nav_button("Apprenants", navbar_layout)  # Ajout du lien vers la page des apprenants
        self.create_nav_button("Profile Details", navbar_layout)
        self.create_nav_button("Assignements", navbar_layout)  # NOUVEAU bouton

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
                background-color: #0070AD;
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
        button.clicked.connect(lambda: self.change_page(button, label))
        layout.addWidget(button)

    def change_page(self, active_button, page_name):
        """ Change de page dans le stacked widget en fonction du bouton cliqué """
        # Réinitialiser tous les boutons à leur couleur d'origine
        for button in active_button.parent().findChildren(QPushButton):
            button.setStyleSheet("""
                QPushButton {
                    background-color: #0070AD;
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

        # Appliquer la couleur active au bouton cliqué
        active_button.setStyleSheet("""
            QPushButton {
                background-color: #1B5E86;
                color: white;
                border: none;
                padding: 10px;
                margin-bottom: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #15688B;
            }
        """)

 
        if page_name == "Departements":
            self.stacked_widget.setCurrentIndex(0)  # Affiche la page des départements
        elif page_name == "Managers":
            self.stacked_widget.setCurrentIndex(1)  # Affiche la page des managers
        elif page_name == "Apprenants":
            self.stacked_widget.setCurrentIndex(2)  # Affiche la page des apprenants
        elif page_name == "Profile Details":
            self.stacked_widget.setCurrentIndex(3)  # Affiche la page des détails du profil
        elif page_name == "Assignements": 
            self.stacked_widget.setCurrentIndex(4)  # index 4

    def logout(self):
        """ Action pour déconnecter l'utilisateur (à améliorer) """
        print("Déconnexion DE ADMIN")
        self.close()
