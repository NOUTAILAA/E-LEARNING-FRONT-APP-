from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QCheckBox, QComboBox, QLineEdit, QDialog
import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QDialog
import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QDialog
import requests

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QDialog
import requests

class ApprenantsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liste des Apprenants")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Titre de la page
        title_label = QLabel("Apprenants")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Table pour afficher les apprenants
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Action"])

        # Mise en place du tableau
        self.table.setRowCount(0)  # Initialiser sans ligne
        layout.addWidget(self.table)

        # Bouton pour ajouter un apprenant
        add_apprenant_button = QPushButton("Ajouter Apprenant")
        add_apprenant_button.setStyleSheet("""
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
        add_apprenant_button.clicked.connect(self.add_apprenant)
        layout.addWidget(add_apprenant_button)

        # Récupérer la liste des apprenants et départements
        self.fetch_apprenants()
        self.fetch_departements()

        # Layout principal de la page
        self.setLayout(layout)

    def fetch_apprenants(self):
        """ Récupère la liste des apprenants depuis l'API et affiche dans la table """
        url = "http://localhost:8090/api/apprenants"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                apprenants = response.json()  # Liste des apprenants reçue
                self.display_apprenants(apprenants)
            else:
                print("Erreur de récupération des apprenants")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def fetch_departements(self):
        """ Récupère la liste des départements pour les utiliser lors de l'ajout d'un apprenant """
        url = "http://localhost:8090/api/departements"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.departements = response.json()  # Liste des départements reçue
            else:
                print("Erreur de récupération des départements")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def display_apprenants(self, apprenants):
        """ Affiche les apprenants dans le tableau """
        self.table.setRowCount(len(apprenants))
        for row, apprenant in enumerate(apprenants):
            self.table.setItem(row, 0, QTableWidgetItem(str(apprenant["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(apprenant["nom"]))
            self.table.setItem(row, 2, QTableWidgetItem(apprenant["prenom"]))

            # Créer le bouton "Edit"
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #FFA500; color: white; border-radius: 5px;")
            edit_button.clicked.connect(lambda checked, id=apprenant["id"]: self.edit_apprenant(id))

            # Créer le bouton "Delete"
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: #D32F2F; color: white; border-radius: 5px;")
            delete_button.clicked.connect(lambda checked, id=apprenant["id"]: self.delete_apprenant(id))

            # Placer les boutons dans la colonne "Action"
            action_layout = QHBoxLayout()
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            # Créer un QWidget pour mettre les boutons
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row, 3, action_widget)

    def add_apprenant(self):
        """ Ouvre une fenêtre pour ajouter un apprenant """
        add_window = AddApprenantWindow(self.departements, self)  # Passer la liste des départements à la fenêtre
        add_window.exec()

    def edit_apprenant(self, apprenant_id):
        """ Permet d'éditer un apprenant """
        print(f"Éditer l'apprenant ID: {apprenant_id}")
        # Passer la liste des départements à la fenêtre d'édition
        self.open_edit_window(apprenant_id)

    def open_edit_window(self, apprenant_id):
        """ Ouvre une fenêtre de modification des informations de l'apprenant """
        edit_window = EditApprenantWindow(apprenant_id, self.departements, self)  # Passer la liste des départements
        edit_window.exec()

    def delete_apprenant(self, apprenant_id):
        """ Supprime un apprenant """
        url = f"http://localhost:8090/api/apprenants/{apprenant_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                print("Apprenant supprimé avec succès")
                self.fetch_apprenants()  # Rafraîchir la liste des apprenants après suppression
            else:
                print("Échec de la suppression de l'apprenant")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")


class AddApprenantWindow(QDialog):
    """ Fenêtre pour ajouter un apprenant """
    def __init__(self, departements, parent=None):
        super().__init__(parent)
        self.departements = departements  # Liste des départements
        self.setWindowTitle("Ajouter Apprenant")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        # Formulaire d'ajout
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        layout.addWidget(self.nom_input)

        self.prenom_input = QLineEdit(self)
        self.prenom_input.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom_input)

        self.departement_input = QComboBox(self)
        self.departement_input.addItem("Sélectionner un Département")
        # Ajoutez ici les départements récupérés via l'API
        for departement in self.departements:
            self.departement_input.addItem(departement["nom"], userData=departement["id"])
        
        layout.addWidget(self.departement_input)

        # Bouton pour ajouter un apprenant
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add_apprenant)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_apprenant(self):
        """ Envoie une requête POST pour ajouter un nouvel apprenant """
        url = "http://localhost:8090/api/apprenants"
        data = {
            "nom": self.nom_input.text(),
            "prenom": self.prenom_input.text(),
            "departement": {
                "id": self.departement_input.currentData()
            }
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Apprenant ajouté avec succès")
                self.close()
                self.parent.fetch_apprenants()  # Rafraîchir la liste des apprenants après ajout
            else:
                print("Échec de l'ajout de l'apprenant")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")


class EditApprenantWindow(QDialog):
    """ Fenêtre pour éditer un apprenant """
    def __init__(self, apprenant_id, departements, parent=None):
        super().__init__(parent)
        self.apprenant_id = apprenant_id
        self.departements = departements  # Liste des départements
        self.setWindowTitle("Modifier Apprenant")
        self.setGeometry(200, 200, 400, 500)

        layout = QVBoxLayout()

        # Formulaire d'édition
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        layout.addWidget(self.nom_input)

        self.prenom_input = QLineEdit(self)
        self.prenom_input.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.telephone_input = QLineEdit(self)
        self.telephone_input.setPlaceholderText("Téléphone")
        layout.addWidget(self.telephone_input)



        self.departement_input = QComboBox(self)
        self.departement_input.addItem("Sélectionner un Département")
        for departement in self.departements:
            self.departement_input.addItem(departement["nom"], userData=departement["id"])
        layout.addWidget(self.departement_input)

        # Bouton pour enregistrer les modifications
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_apprenant)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Récupérer les détails de l'apprenant pour pré-remplir le formulaire
        self.fetch_apprenant_details()

    def fetch_apprenant_details(self):
        """ Récupère les détails de l'apprenant depuis l'API et pré-remplie le formulaire """
        url = f"http://localhost:8090/api/apprenants/{self.apprenant_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                apprenant = response.json()
                self.nom_input.setText(apprenant.get("nom", ""))
                self.prenom_input.setText(apprenant.get("prenom", ""))
                self.email_input.setText(apprenant.get("email", ""))
                self.telephone_input.setText(apprenant.get("telephone", ""))
                # Mettre à jour le département sélectionné
                self.departement_input.setCurrentIndex(self.departement_input.findData(apprenant["departement"]["id"]))
            else:
                print("Erreur de récupération des détails de l'apprenant")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def save_apprenant(self):
        """ Sauvegarde les modifications de l'apprenant """
        url = f"http://localhost:8090/api/apprenants/{self.apprenant_id}"
        data = {
            "nom": self.nom_input.text(),
            "prenom": self.prenom_input.text(),
            "email": self.email_input.text(),
            "telephone": self.telephone_input.text(),
            "departement": {
                "id": self.departement_input.currentData()  # Utilisation de l'ID du département sélectionné
            }
        }

        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                print("Apprenant mis à jour avec succès")
                self.close()
                self.parent.fetch_apprenants()  # Rafraîchir la liste des apprenants après modification
            else:
                print("Échec de la mise à jour de l'apprenant")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")




class AddApprenantWindow(QDialog):
    """ Fenêtre pour ajouter un apprenant """
    def __init__(self, departements, parent=None):
        super().__init__(parent)
        self.parent = parent  # Référence à la fenêtre parente
        self.departements = departements  # Liste des départements
        self.setWindowTitle("Ajouter Apprenant")
        self.setGeometry(200, 200, 400, 500)

        layout = QVBoxLayout()

        # Formulaire d'ajout
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        layout.addWidget(self.nom_input)

        self.prenom_input = QLineEdit(self)
        self.prenom_input.setPlaceholderText("Prénom")
        layout.addWidget(self.prenom_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.telephone_input = QLineEdit(self)
        self.telephone_input.setPlaceholderText("Téléphone")
        layout.addWidget(self.telephone_input)

    

        self.departement_input = QComboBox(self)
        self.departement_input.addItem("Sélectionner un Département")
        for departement in self.departements:
            self.departement_input.addItem(departement["nom"], userData=departement["id"])
        layout.addWidget(self.departement_input)

        # Bouton pour ajouter un apprenant
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add_apprenant)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_apprenant(self):
        """ Envoie une requête POST pour ajouter un nouvel apprenant """
        url = "http://localhost:8090/api/apprenants"
        data = {
            "nom": self.nom_input.text(),
            "prenom": self.prenom_input.text(),
            "email": self.email_input.text(),
            "telephone": self.telephone_input.text(),
            "departement": {
                "id": self.departement_input.currentData()
            }
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Apprenant ajouté avec succès")
                self.close()
                self.parent.fetch_apprenants()  # Rafraîchir la liste des apprenants après ajout
            else:
                print("Échec de l'ajout de l'apprenant")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
