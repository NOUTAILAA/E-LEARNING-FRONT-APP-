from PyQt6.QtWidgets import QDateEdit , QCheckBox ,QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QDialog
import requests
from PyQt6.QtCore import QDate

class ManagersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liste des Managers")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Titre de la page
        title_label = QLabel("Managers")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Ajout du bouton pour ajouter un manager
        add_manager_button = QPushButton("Ajouter Manager")
        add_manager_button.setStyleSheet("""
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
        add_manager_button.clicked.connect(self.add_manager)
        layout.addWidget(add_manager_button)

        # Table pour afficher les managers
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Action"])

        # Mise en place du tableau
        self.table.setRowCount(0)  # Initialiser sans ligne
        layout.addWidget(self.table)

        # Récupérer la liste des managers et départements
        self.fetch_managers()
        self.fetch_departements()

        # Layout principal de la page
        self.setLayout(layout)

    def fetch_managers(self):
        """ Récupère la liste des managers depuis l'API et affiche dans la table """
        url = "http://localhost:8090/api/managers"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                managers = response.json()  # Liste des managers reçue
                self.display_managers(managers)
            else:
                print("Erreur de récupération des managers")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def fetch_departements(self):
        """ Récupère la liste des départements pour les utiliser lors de l'ajout d'un manager """
        url = "http://localhost:8090/api/managers/departements"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.departements = response.json()  # Liste des départements reçue
            else:
                print("Erreur de récupération des départements")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def display_managers(self, managers):
        """ Affiche les managers dans le tableau """
        self.table.setRowCount(len(managers))
        for row, manager in enumerate(managers):
            self.table.setItem(row, 0, QTableWidgetItem(str(manager["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(manager["nom"]))
            self.table.setItem(row, 2, QTableWidgetItem(manager["prenom"]))

            # Créer le bouton "Edit"
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #FFA500; color: white; border-radius: 5px;")
            edit_button.clicked.connect(lambda checked, id=manager["id"]: self.edit_manager(id))

            # Créer le bouton "Delete"
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: #D32F2F; color: white; border-radius: 5px;")
            delete_button.clicked.connect(lambda checked, id=manager["id"]: self.delete_manager(id))

            # Placer les boutons dans la colonne "Action"
            action_layout = QHBoxLayout()
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            # Créer un QWidget pour mettre les boutons
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row, 3, action_widget)

    def add_manager(self):
        """ Ouvre une fenêtre pour ajouter un manager """
        add_window = AddManagerWindow(self.departements, self)  # Passer la liste des départements et la fenêtre parente
        add_window.exec()

    def edit_manager(self, manager_id):
        """ Permet d'éditer un manager """
        print(f"Éditer le manager ID: {manager_id}")
        # Appel de la méthode open_edit_window pour éditer le manager
        self.open_edit_window(manager_id)

    def open_edit_window(self, manager_id):
        """ Ouvre une fenêtre de modification des informations du manager """
        edit_window = EditManagerWindow(manager_id, self.departements, self)  # Passer l'ID du manager et la liste des départements
        edit_window.exec()

    def delete_manager(self, manager_id):
        """ Supprime un manager """
        url = f"http://localhost:8090/api/managers/{manager_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                print("Manager supprimé avec succès")
                self.fetch_managers()  # Rafraîchir la liste des managers après suppression
            else:
                print("Échec de la suppression du manager")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")



class EditManagerWindow(QDialog):
    """ Fenêtre pour éditer un manager """
    def __init__(self, manager_id, departements, parent=None):
        super().__init__(parent)
        self.manager_id = manager_id
        self.departements = departements
        self.parent = parent
        self.setWindowTitle("Editer Manager")
        self.setGeometry(200, 200, 400, 600)

        layout = QVBoxLayout()

        # Formulaire d'édition
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        layout.addWidget(self.nom_input)

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

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.departement_input = QComboBox(self)
        self.departement_input.addItem("Sélectionner un Département")
        for departement in self.departements:
            self.departement_input.addItem(departement["nom"], userData=departement["id"])
        layout.addWidget(self.departement_input)

        # Bouton pour sauvegarder les modifications
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_manager)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Récupérer les détails du manager pour pré-remplir le formulaire
        self.fetch_manager_details()

    def fetch_manager_details(self):
        """ Récupère les détails du manager depuis l'API et pré-remplie le formulaire """
        url = f"http://localhost:8090/api/managers/{self.manager_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                manager = response.json()
                self.nom_input.setText(manager.get("nom", ""))
                self.prenom_input.setText(manager.get("prenom", ""))
                self.date_naissance_input.setDate(QDate.fromString(manager["dateNaissance"], "yyyy-MM-dd"))
                self.telephone_input.setText(manager.get("telephone", ""))
                self.sexe_input.setCurrentText(manager.get("sexe", ""))
                self.email_input.setText(manager.get("email", ""))
                self.password_input.setText(manager.get("password", ""))
                self.departement_input.setCurrentIndex(self.departement_input.findData(manager["departement"]["id"]))
            else:
                print("Erreur de récupération des détails du manager")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def save_manager(self):
        """ Sauvegarde les modifications du manager """
        url = f"http://localhost:8090/api/managers/{self.manager_id}"
        data = {
            "nom": self.nom_input.text(),
            "prenom": self.prenom_input.text(),
            "dateNaissance": self.date_naissance_input.date().toString("yyyy-MM-dd"),
            "telephone": self.telephone_input.text(),
            "sexe": self.sexe_input.currentText(),
            "email": self.email_input.text(),
            "password": self.password_input.text(),
            "departement": {
                "id": self.departement_input.currentData()
            }
        }

        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                print("Manager mis à jour avec succès")
                self.close()
                self.parent.fetch_managers()  # Rafraîchir la liste des managers après modification
            else:
                print("Échec de la mise à jour du manager")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")




class AddManagerWindow(QDialog):
    """ Fenêtre pour ajouter un manager """
    def __init__(self, departements, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.departements = departements  # Liste des départements
        self.setWindowTitle("Ajouter Manager")
        self.setGeometry(200, 200, 400, 600)

        layout = QVBoxLayout()

        # Formulaire d'ajout
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        layout.addWidget(self.nom_input)

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

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.departement_input = QComboBox(self)
        self.departement_input.addItem("Sélectionner un Département")
        for departement in self.departements:
            self.departement_input.addItem(departement["nom"], userData=departement["id"])
        layout.addWidget(self.departement_input)

        # Bouton pour ajouter le manager
        add_button = QPushButton("Ajouter Manager")
        add_button.clicked.connect(self.add_manager)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_manager(self):
        """ Envoie une requête POST pour ajouter un nouveau manager """
        url = "http://localhost:8090/api/managers"
        data = {
            "nom": self.nom_input.text(),
            "prenom": self.prenom_input.text(),
            "dateNaissance": self.date_naissance_input.date().toString("yyyy-MM-dd"),
            "telephone": self.telephone_input.text(),
            "sexe": self.sexe_input.currentText(),
            "email": self.email_input.text(),
            "password": self.password_input.text(),
            "departement": {
                "id": self.departement_input.currentData()  # Utilisation de l'ID du département sélectionné
            }
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Manager ajouté avec succès")
                self.close()
                self.parent.fetch_managers()  # Rafraîchir la liste des managers après ajout
            else:
                print("Échec de l'ajout du manager")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
