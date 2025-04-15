import sys
from PyQt6.QtWidgets import (
    QDialog, QApplication, QLabel, QPushButton, QLineEdit, QMessageBox,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainterPath, QRegion
import requests
from session import Session

from Superadmin.superadminpage import SuperAdminPage
from Admin.adminpage import AdminPage
from Manager.managerpage import ManagerPage

class DashboardWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tableau de Bord")
        self.setStyleSheet("background-color: #f4f4f4;")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 20, 0, 20)

        # ================= HEADER =================
        header = QFrame()
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header.setStyleSheet("background-color: #2176AE; padding: 10px 30px; border-radius: 5px;")

        header_layout = QHBoxLayout()

        logo_label = QLabel()
        logo_pixmap = QPixmap("output-onlinepngtools.png").scaledToHeight(40, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)

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

        header_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignRight)
        header.setLayout(header_layout)

        main_layout.addWidget(header)

        # ================= CONTENU PRINCIPAL =================
        content_layout = QHBoxLayout()

        text_layout = QVBoxLayout()
        title = QLabel("       Lorem ipsum dolor sit amet")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        
        description = QLabel(
            "             Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        )
        description.setWordWrap(True)
        description.setFont(QFont("Arial", 12))
        description.setStyleSheet("color: gray; margin-top: 30px;")


        text_layout.addWidget(title)
        text_layout.addWidget(description)
        text_layout.addStretch()

        profile_img = QLabel(self)
        pixmap = QPixmap("1.jpg").scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                         Qt.TransformationMode.SmoothTransformation)

        path = QPainterPath()
        path.addEllipse(0, 0, 140, 140)
        mask = QRegion(path.toFillPolygon().toPolygon())
        profile_img.setMask(mask)

        profile_img.setPixmap(pixmap)
        profile_img.setFixedSize(140, 140)
        profile_img.setStyleSheet("border: 3px solid #2176AE; border-radius: 70px;")
        profile_img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addLayout(text_layout, 70)
        content_layout.addWidget(profile_img, 30)

        main_layout.addLayout(content_layout)

        # ================= CARTES =================
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)

        def create_card(icon, title, text, color):
            card = QFrame()
            card.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px; border: 1px solid lightgray;")
            card_layout = QVBoxLayout()

            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Arial", 28))
            icon_label.setStyleSheet(f"color: {color};")

            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            title_label.setStyleSheet("color: black;")

            text_label = QLabel(text)
            text_label.setWordWrap(True)
            text_label.setStyleSheet("color: gray; font-size: 12px;")

            card_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

            card.setLayout(card_layout)
            card.setFixedWidth(300)  # ou plus (320, 350...) selon ton écran
            card.setFixedHeight(300)
            return card

        card1 = create_card("🗂️", "Lorem ipsum", "Lorem ipsum dolor sit amet.", "#00BCD4")
        card2 = create_card("📅", "Dolor sit", "Lorem ipsum dolor sit amet.", "#FF6F61")
        card3 = create_card("👥", "Amet consectetur", "Lorem ipsum dolor sit amet.", "#3F51B5")

        card_layout.addWidget(card1)
        card_layout.addWidget(card2)
        card_layout.addWidget(card3)

        main_layout.addLayout(card_layout)

        # ================= FOOTER =================
        footer = QLabel("© 2023 Inc. All rights reserved.")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 9px; margin-top: 30px;")
        main_layout.addStretch()
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def show_login(self):
        login_window = LoginWindow(self)
        login_window.exec()

    def show_login_success(self):
        success_label = QLabel("Vous êtes identifié !")
        success_label.setStyleSheet("font-size: 18px; color: green;")
        self.layout().addWidget(success_label)

    def show_superadmin_page(self):
        self.superadmin_page = SuperAdminPage(self)
        self.superadmin_page.showMaximized()

    def show_admin_page(self):
        self.admin_page = AdminPage(self)
        self.admin_page.showMaximized()

    def show_manager_page(self):
        self.manager_page = ManagerPage(self)
        self.manager_page.showMaximized()


class LoginWindow(QDialog):
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
        self.username_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #CCC;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔑 Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #CCC;")

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
        username = self.username_input.text()
        password = self.password_input.text()

        url = "http://localhost:8090/api/login"
        data = {"email": username, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                response_text = response.text
                print("Réponse du serveur :", response_text)

                # Stocker l'email de l'utilisateur connecté
                Session.current_user_email = username

                # Extraction du nom (entre "Bonjour" et ",")
                if response_text.lower().startswith("bonjour"):
                    try:
                        name = response_text.split("Bonjour")[1].split(",")[0].strip()
                    except Exception:
                        name = "Utilisateur"
                    Session.current_user_name = name

                # Détecter le rôle et naviguer
                if "superadmin" in response_text.lower():
                    Session.current_user_role = "superadmin"
                    self.accept()
                    self.parent.show_superadmin_page()
                elif "admin" in response_text.lower():
                    Session.current_user_role = "admin"
                    self.accept()
                    self.parent.show_admin_page()
                elif "manager" in response_text.lower():
                    Session.current_user_role = "manager"
                    self.accept()
                    self.parent.show_manager_page()
                else:
                    self.accept()
                    self.parent.show_login_success()
            else:
                self.username_input.setStyleSheet("border: 1px solid red;")
                self.password_input.setStyleSheet("border: 1px solid red;")
                QMessageBox.warning(self, "Erreur de connexion", "Identifiants incorrects.")
        except requests.exceptions.RequestException:
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, "Erreur de connexion", "Une erreur s'est produite. Veuillez réessayer.")

def main():
    app = QApplication(sys.argv)
    dashboard_window = DashboardWindow()
    dashboard_window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
