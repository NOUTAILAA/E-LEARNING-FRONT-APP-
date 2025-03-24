import sys
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QPixmap, QFont, QPainterPath, QRegion
from PyQt6.QtCore import Qt
import requests
from Superadmin.superadminpage import SuperAdminPage

from Admin.adminpage import AdminPage


class DashboardWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tableau de Bord")
        self.setStyleSheet("background-color: #f4f4f4;")
        self.setGeometry(100, 100, 800, 500)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # ================= HEADER =================
        header = QFrame()
        header.setStyleSheet(
            "background-color: #2176AE; padding: 10px; border-radius: 5px;")
        header_layout = QHBoxLayout()

        logo_label = QLabel("Capgemini 🌍")
        logo_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: white;")

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2176AE;
                border-radius: 10px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        self.login_button.clicked.connect(self.show_login)

        header_layout.addWidget(
            logo_label, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(
            self.login_button, alignment=Qt.AlignmentFlag.AlignRight)
        header.setLayout(header_layout)

        main_layout.addWidget(header)

        self.setLayout(main_layout)
# ================= CONTENU PRINCIPAL =================
        content_layout = QHBoxLayout()

        text_layout = QVBoxLayout()
        title = QLabel("Lorem ipsum dolor sit amet")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        description = QLabel(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        description.setWordWrap(True)
        description.setFont(QFont("Arial", 12))

        text_layout.addWidget(title)
        text_layout.addWidget(description)

        # ================= IMAGE DE PROFIL RONDE =================
        profile_img = QLabel(self)
        pixmap = QPixmap("1.jpg")  # Remplace par ton image

        size = 120
        pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                               Qt.TransformationMode.SmoothTransformation)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        mask = QRegion(path.toFillPolygon().toPolygon())
        profile_img.setMask(mask)

        profile_img.setPixmap(pixmap)
        profile_img.setFixedSize(size, size)
        profile_img.setStyleSheet(
            "border: 3px solid #2176AE; border-radius: 60px;")
        profile_img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addLayout(text_layout, 70)
        content_layout.addWidget(profile_img, 30)

        main_layout.addLayout(content_layout)

        # ================= CARTES =================
        card_layout = QHBoxLayout()

        def create_card(icon, title, text, color):
            card = QFrame()
            card.setStyleSheet(
                f"background-color: white; border-radius: 10px; padding: 15px; border: 1px solid lightgray;")
            card_layout = QVBoxLayout()

            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Arial", 24))
            icon_label.setStyleSheet(f"color: {color};")

            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            title_label.setStyleSheet("color: black;")

            text_label = QLabel(text)
            text_label.setWordWrap(True)
            text_label.setStyleSheet("color: gray; font-size: 12px;")

            card_layout.addWidget(
                icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(
                title_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(
                text_label, alignment=Qt.AlignmentFlag.AlignCenter)

            card.setLayout(card_layout)
            return card

        card1 = create_card("📁", "Lorem ipsum",
                            "Lorem ipsum dolor sit amet.", "#17A2B8")
        card2 = create_card(
            "📅", "Dolor sit", "Lorem ipsum dolor sit amet.", "#DC3545")
        card3 = create_card("👥", "Amet consectetur",
                            "Lorem ipsum dolor sit amet.", "#007BFF")

        card_layout.addWidget(card1)
        card_layout.addWidget(card2)
        card_layout.addWidget(card3)

        main_layout.addLayout(card_layout)

        self.setLayout(main_layout)

    def show_login(self):
        """ Affiche la fenêtre de connexion """
        login_window = LoginWindow(self)
        login_window.exec()  # Bloque jusqu'à fermeture

    def show_login_success(self):
        """ Affiche un message de succès de connexion """
        success_label = QLabel(
            "Vous êtes identifié !")  # Le message à afficher
        success_label.setStyleSheet(
            "font-size: 18px; color: green;")  # Style du message
        self.layout().addWidget(success_label)  # Ajoute le message au layout existant

    def show_superadmin_page(self):
        """ Ouvre la page SuperAdmin """
        superadmin_page = SuperAdminPage(self)
        superadmin_page.exec()  # Ouvre la page de superadmin dans une nouvelle fenêtre

    def show_admin_page(self):
        """ Ouvre la page Admin """
        admin_page = AdminPage(self)
        admin_page.exec()  # Ouvre la page de admin dans une nouvelle fenêtre


class LoginWindow(QDialog):
    """ Fenêtre de connexion """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Se connecter")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: white; border-radius: 10px;")

        layout = QVBoxLayout()

        title = QLabel("🔐 Se connecter")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Email")
        self.username_input.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #CCC;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔑 Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #CCC;")

        login_button = QPushButton("Se connecter")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #2176AE;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1B5E86;
            }
        """)
        login_button.clicked.connect(self.verify_login)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def verify_login(self):
        """ Vérifie les identifiants et ouvre la page suivante """
        username = self.username_input.text()
        password = self.password_input.text()

        url = "http://localhost:8090/api/login"
        data = {"email": username, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                # Vérification du rôle de l'utilisateur dans la réponse
                if "superadmin" in response.text.lower():
                    self.accept()  # Ferme la fenêtre de connexion
                    self.parent.show_superadmin_page()  # Affiche la page SuperAdmin
                elif "admin" in response.text.lower():
                    self.accept()  # Ferme la fenêtre de connexion
                    self.parent.show_admin_page()  # Affiche la page SuperAdmin
                else:
                    self.accept()  # Ferme la fenêtre de connexion
                    self.parent.show_login_success()  # Affiche un message de connexion réussie
            else:
                self.username_input.setStyleSheet("border: 1px solid red;")
                self.password_input.setStyleSheet("border: 1px solid red;")
                QMessageBox.warning(
                    self, "Erreur de connexion", "Identifiants incorrects.")
        except requests.exceptions.RequestException as e:
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Erreur de connexion",
                                "Une erreur s'est produite. Veuillez réessayer.")


def main():
    app = QApplication(sys.argv)
    dashboard_window = DashboardWindow()
    dashboard_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
