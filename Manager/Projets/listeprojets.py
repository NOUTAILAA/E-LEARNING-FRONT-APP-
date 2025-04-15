import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea,
    QFrame, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from session import Session
from Manager.Projets.add_projet import AjoutProjetDialog
from Manager.Projets.edit_projet import EditProjetDialog
from Manager.Projets.upload_image import ImageClickableLabel
from Manager.Cours.liste_cours import ListeCoursPage

class ListeProjetsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre
        title = QLabel("Pharma - Vos projets")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Bouton ajout
        add_button = QPushButton("+ Add new project")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #2176AE;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1A5A8A;
            }
        """)
        add_button.setFixedWidth(200)
        layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignRight)
        add_button.clicked.connect(self.ouvrir_dialogue_ajout)

        # Scroll des projets
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        scroll.setWidget(self.container)

        layout.addWidget(scroll)
        self.setLayout(layout)

        # Charger les projets du manager connecté
        self.load_projets()

    def ouvrir_dialogue_ajout(self):
        dialog = AjoutProjetDialog(self)
        if dialog.exec():
            self.refresh()

    def get_manager_id_by_email(self, email):
        try:
            response = requests.get(f"http://localhost:8090/api/managers/email?email={email}")
            if response.status_code == 200:
                return response.json().get("id")  # <-- Cette ligne suppose que le JSON retourné est simple.
            else:
                print("Erreur récupération manager:", response.text)
                return None
        except Exception as e:
            print("Erreur:", e)
            return None

    def load_projets(self):
        email = Session.current_user_email
        manager_id = self.get_manager_id_by_email(email)

        if not manager_id:
            QMessageBox.warning(self, "Erreur", "Impossible de retrouver le manager connecté.")
            return

        try:
            response = requests.get(f"http://localhost:8090/api/projets/manager/{manager_id}")
            response.raise_for_status()
            projets = response.json()

            for projet in projets:
                self.container_layout.addWidget(self._create_project_card(projet))

        except requests.RequestException as e:
            QMessageBox.critical(self, "Erreur", f"Échec de chargement des projets:\n{e}")

    def _create_project_card(self, projet):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        card_layout = QHBoxLayout(card)

        # Image
        image_label = ImageClickableLabel(projet["id"])
        image_url = f"http://localhost:8090/api/projets/{projet['id']}/photo"
        try:
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(img_response.content)
                image_label.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                image_label.setText("🖼️")
        except:
            image_label.setText("🖼️")

        card_layout.addWidget(image_label)

        # Texte
        text_layout = QVBoxLayout()
        titre = QLabel(projet['nom'])
        titre.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        client = QLabel(projet.get('nomClient', ''))
        client.setStyleSheet("color: gray; font-size: 12px;")
        text_layout.addWidget(titre)
        text_layout.addWidget(client)
        card_layout.addLayout(text_layout)

        card_layout.addStretch()

        # Boutons
        edit_btn = QPushButton("✏️")
        edit_btn.clicked.connect(lambda: self.editer_projet(projet))
        delete_btn = QPushButton("🗑️")
        for btn in [edit_btn, delete_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("border: none; font-size: 18px;")
        delete_btn.clicked.connect(lambda: self.delete_project(projet["id"]))
        card_layout.addWidget(edit_btn)
        card_layout.addWidget(delete_btn)

        card.mousePressEvent = lambda event: self.ouvrir_cours_page(projet)

        return card

    def ouvrir_cours_page(self, projet):
        self.parentWidget().layout().removeWidget(self)
        self.setParent(None)
        cours_page = ListeCoursPage(projet, self.parentWidget())
        self.parentWidget().layout().addWidget(cours_page)

    def delete_project(self, projet_id):
        confirm = QMessageBox.question(
            self, "Confirmation", "Voulez-vous vraiment supprimer ce projet ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                resp = requests.delete(f"http://localhost:8090/api/projets/{projet_id}")
                if resp.status_code == 200 or resp.status_code == 204:
                    QMessageBox.information(self, "Succès", "Projet supprimé.")
                    self.refresh()
                else:
                    QMessageBox.warning(self, "Erreur", "Suppression échouée.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))

    def editer_projet(self, projet):
        dialog = EditProjetDialog(projet, self)
        if dialog.exec():
            self.refresh()

    def refresh(self):
        for i in reversed(range(self.container_layout.count())):
            self.container_layout.itemAt(i).widget().setParent(None)
        self.load_projets()
