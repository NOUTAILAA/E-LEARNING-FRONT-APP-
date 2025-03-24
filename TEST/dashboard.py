import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QDialog
)
from PyQt6.QtGui import QPixmap, QFont, QPainterPath, QRegion
from PyQt6.QtCore import Qt
from TEST.superadminpage import HelloWindow  # ✅ Import de la nouvelle page


class LoginWindow(QDialog):
    """ Fenêtre de connexion affichée au clic sur 'Login' """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # ✅ Référence à la fenêtre principale

        self.setWindowTitle("Sign in")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: white; border-radius: 10px;")

        layout = QVBoxLayout()

        title = QLabel("🔐 Sign in")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Name")
        self.username_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #CCC;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔑 Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #CCC;")

        login_button = QPushButton("Log in")
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
        """ Vérifie si les identifiants sont corrects et ouvre HelloWindow """
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.accept()  # ✅ Ferme la boîte de dialogue
            self.parent.open_hello_window()  # ✅ Ouvre la page Hello
        else:
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setStyleSheet("border: 1px solid red;")


class ModernUI(QWidget):
    """ Fenêtre principale """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface Moderne avec PyQt6")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout()

        # ================= HEADER =================
        header = QFrame()
        header.setStyleSheet("background-color: #2176AE; padding: 10px; border-radius: 5px;")
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

        header_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignRight)
        header.setLayout(header_layout)

        main_layout.addWidget(header)

        self.setLayout(main_layout)
# ================= CONTENU PRINCIPAL =================
        content_layout = QHBoxLayout()

        text_layout = QVBoxLayout()
        title = QLabel("Lorem ipsum dolor sit amet")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        description = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        description.setWordWrap(True)
        description.setFont(QFont("Arial", 12))

        text_layout.addWidget(title)
        text_layout.addWidget(description)

        # ================= IMAGE DE PROFIL RONDE =================
        profile_img = QLabel(self)
        pixmap = QPixmap("1.jpg")  # Remplace par ton image

        size = 120
        pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        mask = QRegion(path.toFillPolygon().toPolygon())
        profile_img.setMask(mask)

        profile_img.setPixmap(pixmap)
        profile_img.setFixedSize(size, size)
        profile_img.setStyleSheet("border: 3px solid #2176AE; border-radius: 60px;")
        profile_img.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addLayout(text_layout, 70)
        content_layout.addWidget(profile_img, 30)

        main_layout.addLayout(content_layout)

        # ================= CARTES =================
        card_layout = QHBoxLayout()

        def create_card(icon, title, text, color):
            card = QFrame()
            card.setStyleSheet(f"background-color: white; border-radius: 10px; padding: 15px; border: 1px solid lightgray;")
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

            card_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)

            card.setLayout(card_layout)
            return card

        card1 = create_card("📁", "Lorem ipsum", "Lorem ipsum dolor sit amet.", "#17A2B8")
        card2 = create_card("📅", "Dolor sit", "Lorem ipsum dolor sit amet.", "#DC3545")
        card3 = create_card("👥", "Amet consectetur", "Lorem ipsum dolor sit amet.", "#007BFF")

        card_layout.addWidget(card1)
        card_layout.addWidget(card2)
        card_layout.addWidget(card3)

        main_layout.addLayout(card_layout)

        self.setLayout(main_layout)
        
    def show_login(self):
        """ Affiche la fenêtre de connexion """
        login_window = LoginWindow(self)
        login_window.exec()  # Bloque jusqu'à fermeture

    def open_hello_window(self):
        """ ✅ Affiche la page Hello après connexion réussie """
        self.hello_window = HelloWindow()
        self.hello_window.show()
        self.close()  # ✅ Ferme la page actuelle


# Lancer l'application
app = QApplication(sys.argv)
window = ModernUI()
window.show()
sys.exit(app.exec())