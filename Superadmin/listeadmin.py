import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLineEdit, QDialog, QComboBox, QDateEdit
import requests
from PyQt6.QtCore import QDate


class ListeAdminPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liste des Administrateurs")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Titre de la page
        title_label = QLabel("Administrateurs")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Ajout du bouton pour ajouter un administrateur
        add_admin_button = QPushButton("Add admin")
        add_admin_button.setStyleSheet("""
            QPushButton {
                background-color: #2176AE;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1B5E86;
            }
        """)
        add_admin_button.clicked.connect(self.add_admin)
        layout.addWidget(add_admin_button)

        # Table pour afficher les administrateurs
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Role", "Action"])

        # Mise en place du tableau
        self.table.setRowCount(0)  # Initialiser sans ligne
        layout.addWidget(self.table)

        # Récupérer la liste des administrateurs
        self.fetch_admins()

        # Layout principal de la page
        self.setLayout(layout)

    def fetch_admins(self):
        """ Récupère la liste des administrateurs depuis l'API et affiche dans la table """
        url = "http://localhost:8090/api/admins"  # Assurez-vous que l'API est bien lancée

        try:
            response = requests.get(url)
            if response.status_code == 200:
                admins = response.json()  # Liste des administrateurs reçue
                self.display_admins(admins)
            else:
                print("Erreur de récupération des administrateurs")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def display_admins(self, admins):
        """ Affiche les administrateurs dans le tableau """
        self.table.setRowCount(len(admins))
        for row, admin in enumerate(admins):
            self.table.setItem(row, 0, QTableWidgetItem(str(admin["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(admin["nom"]))
            self.table.setItem(row, 2, QTableWidgetItem(admin["prenom"]))
            self.table.setItem(row, 3, QTableWidgetItem(admin["role"]))

            # Créer le bouton "Details"
            details_button = QPushButton("Details")
            details_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
            details_button.clicked.connect(lambda checked, id=admin["id"]: self.show_details(id))
            
            # Créer le bouton "Edit"
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #FFA500; color: white; border-radius: 5px;")
            edit_button.clicked.connect(lambda checked, id=admin["id"]: self.edit_admin(id))

            # Placer les boutons dans la colonne "Action"
            action_layout = QHBoxLayout()
            action_layout.addWidget(details_button)
            action_layout.addWidget(edit_button)

            # Créer un QWidget pour mettre les boutons
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row, 4, action_widget)

    def show_details(self, admin_id):
        """ Affiche les détails de l'administrateur (fonction à personnaliser) """
        print(f"Afficher les détails pour l'administrateur ID: {admin_id}")

    def edit_admin(self, admin_id):
        """ Permet d'éditer un administrateur (fonction à personnaliser) """
        print(f"Éditer l'administrateur ID: {admin_id}")
        # Vous devez maintenant transmettre l'instance de la page parente
        self.open_edit_window(admin_id)

    def open_edit_window(self, admin_id):
        """ Ouvre une fenêtre de modification des informations de l'administrateur """
        edit_window = EditAdminWindow(admin_id, self)  # Passer la fenêtre parent ici
        edit_window.exec()

    def add_admin(self):
        """ Ouvre une fenêtre pour ajouter un administrateur """
        add_window = AddAdminWindow(self)  # Passer la fenêtre parent ici
        add_window.exec()

class EditAdminWindow(QDialog):
    """ Fenêtre pour éditer un administrateur """
    def __init__(self, admin_id, parent=None):
        super().__init__(parent)
        self.admin_id = admin_id
        self.parent = parent  # Référence à la fenêtre parente
        self.setWindowTitle("Edit Admin")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        # Formulaire d'édition
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nom")
        layout.addWidget(self.name_input)

        self.prenom_input = QLineEdit(self)
        self.prenom_input.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom_input)

        self.date_naissance_input = QDateEdit(self)
        self.date_naissance_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.date_naissance_input)

        self.telephone_input = QLineEdit(self)
        self.telephone_input.setPlaceholderText("Téléphone")
        layout.addWidget(self.telephone_input)

        self.sexe_input = QComboBox(self)
        self.sexe_input.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.sexe_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.role_input = QComboBox(self)
        self.role_input.addItems(["admin", "manager", "user"])
        layout.addWidget(self.role_input)

        # Bouton pour enregistrer les modifications
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_admin)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Récupérer les informations de l'administrateur à partir de l'API
        self.fetch_admin_details()

    def fetch_admin_details(self):
        """ Récupère les détails de l'administrateur depuis l'API et pré-remplie le formulaire """
        url = f"http://localhost:8090/api/admins/{self.admin_id}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                admin = response.json()
                # Pré-remplir le formulaire avec les données récupérées
                self.name_input.setText(admin.get("nom", ""))
                self.prenom_input.setText(admin.get("prenom", ""))
                self.date_naissance_input.setDate(QDate.fromString(admin.get("dateNaissance", ""), "yyyy-MM-dd"))
                self.telephone_input.setText(admin.get("telephone", ""))
                self.sexe_input.setCurrentText(admin.get("sexe", ""))
                self.email_input.setText(admin.get("email", ""))
                self.role_input.setCurrentText(admin.get("role", ""))
            else:
                print("Erreur de récupération des détails de l'administrateur")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def save_admin(self):
        """ Sauvegarde les modifications d'un administrateur """
        url = f"http://localhost:8090/api/admins/{self.admin_id}"
        data = {
            "nom": self.name_input.text(),
            "prenom": self.prenom_input.text(),
            "dateNaissance": self.date_naissance_input.date().toString("yyyy-MM-dd"),
            "telephone": self.telephone_input.text(),
            "sexe": self.sexe_input.currentText(),
            "email": self.email_input.text(),
            "role": self.role_input.currentText(),
        }

        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                print("Admin updated successfully")
                self.close()
                # Rafraîchir la liste des administrateurs après modification
                self.parent.fetch_admins()  # Appel de la méthode de rafraîchissement
            else:
                print("Failed to update admin")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

class AddAdminWindow(QDialog):
    """ Fenêtre pour ajouter un nouvel administrateur """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Référence à la fenêtre parente
        self.setWindowTitle("Add Admin")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        # Formulaire d'ajout
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nom")
        layout.addWidget(self.name_input)

        self.prenom_input = QLineEdit(self)
        self.prenom_input.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom_input)

        self.date_naissance_input = QDateEdit(self)
        self.date_naissance_input.setDate(QDate.currentDate())
        self.date_naissance_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.date_naissance_input)

        self.telephone_input = QLineEdit(self)
        self.telephone_input.setPlaceholderText("Téléphone")
        layout.addWidget(self.telephone_input)

        self.sexe_input = QComboBox(self)
        self.sexe_input.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.sexe_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.role_input = QComboBox(self)
        self.role_input.addItems(["admin", "manager", "user"])
        layout.addWidget(self.role_input)

        # Bouton pour ajouter l'administrateur
        add_button = QPushButton("Add Admin")
        add_button.clicked.connect(self.add_admin)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_admin(self):
        """ Envoie une requête POST pour ajouter un nouvel administrateur """
        url = "http://localhost:8090/api/admins"
        data = {
            "nom": self.name_input.text(),
            "prenom": self.prenom_input.text(),
            "dateNaissance": self.date_naissance_input.date().toString("yyyy-MM-dd"),
            "telephone": self.telephone_input.text(),
            "sexe": self.sexe_input.currentText(),
            "email": self.email_input.text(),
            "role": self.role_input.currentText(),
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Admin added successfully")
                self.close()
                # Rafraîchir la liste des administrateurs après ajout
                self.parent.fetch_admins()  # Appel de la méthode de rafraîchissement
            else:
                print("Failed to add admin")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
