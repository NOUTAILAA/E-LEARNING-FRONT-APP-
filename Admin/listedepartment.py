from PyQt6.QtWidgets import QWidget, QDialog , QLineEdit,QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
import requests

class DepartementsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liste des Départements")
        self.setGeometry(50, 50, 400, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Titre de la page
        title_label = QLabel("Départements")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Ajout du bouton pour ajouter un département
        add_departement_button = QPushButton("Ajouter Département")
        add_departement_button.setStyleSheet("""
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
        add_departement_button.clicked.connect(self.add_departement)
        layout.addWidget(add_departement_button)

        # Table pour afficher les départements
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Action"])

        # Mise en place du tableau
        self.table.setRowCount(0)  # Initialiser sans ligne
        layout.addWidget(self.table)

        # Récupérer la liste des départements
        self.fetch_departements()

        # Layout principal de la page
        self.setLayout(layout)

    def fetch_departements(self):
        """ Récupère la liste des départements depuis l'API et affiche dans la table """
        url = "http://localhost:8090/api/departements" 
        try:
            response = requests.get(url)
            if response.status_code == 200:
                departements = response.json()  # Liste des départements reçue
                self.display_departements(departements)
            else:
                print("Erreur de récupération des départements")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def display_departements(self, departements):
        """ Affiche les départements dans le tableau """
        self.table.setRowCount(len(departements))
        for row, departement in enumerate(departements):
            self.table.setItem(row, 0, QTableWidgetItem(str(departement["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(departement["nom"]))

            # Créer le bouton "Edit"
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #FFA500; color: white; border-radius: 5px;")
            edit_button.clicked.connect(lambda checked, id=departement["id"]: self.edit_departement(id))

            # Créer le bouton "Delete"
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: #D32F2F; color: white; border-radius: 5px;")
            delete_button.clicked.connect(lambda checked, id=departement["id"]: self.delete_departement(id))

            # Placer les boutons dans la colonne "Action"
            action_layout = QHBoxLayout()
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            # Créer un QWidget pour mettre les boutons
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row, 2, action_widget)

    def add_departement(self):
        """ Ouvre une fenêtre pour ajouter un département """
        add_window = AddDepartementWindow(self)  # Passer la fenêtre parent ici
        add_window.exec()

    def edit_departement(self, departement_id):
        """ Permet d'éditer un département """
        print(f"Éditer le département ID: {departement_id}")
        # Vous devez maintenant transmettre l'instance de la page parente
        self.open_edit_window(departement_id)

    def open_edit_window(self, departement_id):
        """ Ouvre une fenêtre de modification des informations du département """
        edit_window = EditDepartementWindow(departement_id, self)  # Passer la fenêtre parent ici
        edit_window.exec()

    def delete_departement(self, departement_id):
        """ Supprime un département """
        url = f"http://localhost:8090/api/departements/{departement_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                print("Département supprimé avec succès")
                self.fetch_departements()  # Rafraîchir la liste des départements après suppression
            else:
                print("Échec de la suppression du département")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
class AddDepartementWindow(QDialog):
    """ Fenêtre pour ajouter un département """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Référence à la fenêtre parente
        self.setWindowTitle("Ajouter Département")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        # Formulaire d'ajout
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nom du Département")
        layout.addWidget(self.name_input)

        # Bouton pour ajouter le département
        add_button = QPushButton("Ajouter Département")
        add_button.clicked.connect(self.add_departement)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_departement(self):
        """ Envoie une requête POST pour ajouter un nouveau département """
        url = "http://localhost:8090/api/departements"
        data = {
            "nom": self.name_input.text(),
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Département ajouté avec succès")
                self.close()
                # Rafraîchir la liste des départements après ajout
                self.parent.fetch_departements()  # Appel de la méthode de rafraîchissement
            else:
                print("Échec de l'ajout du département")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
class EditDepartementWindow(QDialog):
    """ Fenêtre pour éditer un département """
    def __init__(self, departement_id, parent=None):
        super().__init__(parent)
        self.departement_id = departement_id
        self.parent = parent
        self.setWindowTitle("Edit Departement")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        # Formulaire d'édition
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nom du Département")
        layout.addWidget(self.name_input)

        # Bouton pour enregistrer les modifications
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_departement)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Récupérer les informations du département à partir de l'API
        self.fetch_departement_details()

    def fetch_departement_details(self):
        """ Récupère les détails du département depuis l'API et pré-remplie le formulaire """
        url = f"http://localhost:8090/api/departements/{self.departement_id}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                departement = response.json()
                self.name_input.setText(departement.get("nom", ""))
            else:
                print("Erreur de récupération des détails du département")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")

    def save_departement(self):
        """ Sauvegarde les modifications du département """
        url = f"http://localhost:8090/api/departements/{self.departement_id}"
        data = {
            "nom": self.name_input.text(),
        }

        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                print("Département mis à jour avec succès")
                self.close()
                # Rafraîchir la liste des départements après modification
                self.parent.fetch_departements()
            else:
                print("Échec de la mise à jour du département")
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
