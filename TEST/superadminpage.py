
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget

class HelloWindow(QWidget):
    """ Fenêtre affichant la liste des utilisateurs avec recherche, pagination et redirection Logout """
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Dashboard - Life Science")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #E3F2FD, stop:1 #FFFFFF);
                font-family: Arial;
            }
        """)

        # ================ LAYOUT PRINCIPAL ================
        main_layout = QHBoxLayout()


        # ================ NAVIGATION BAR ================
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            background-color: #3a9edc;
            color: white;
            padding: 15px;
            border-radius: 10px;
        """)

        sidebar_layout = QVBoxLayout()

        logo_label = QSvgWidget("logo capgemini.svg")
        logo_label.setFixedSize(150, 90)
        logo_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: white; margin-bottom: 15px;")

        menu_items = ["Utilisateurs", "Departments", "Settings", "Help & Support"]
        department_items = ["Life Science", "IT", "Logistics"]

        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addSpacing(10)

        for item in menu_items:
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    color: #D9ECF2;
                    font-weight: bold;
                }
            """)
            sidebar_layout.addWidget(btn)

            if item == "Departments":
                for dept in department_items:
                    dept_btn = QPushButton(f"  • {dept}")
                    dept_btn.setStyleSheet("""
                        QPushButton {
                            background: none;
                            border: none;
                            color: #D9ECF2;
                            font-size: 12px;
                            padding-left: 15px;
                            text-align: left;
                        }
                        QPushButton:hover {
                            color: white;
                        }
                    """)
                    sidebar_layout.addWidget(dept_btn)

        sidebar_layout.addStretch()

        # ✅ Bouton Logout avec Redirection
        logout_btn = QPushButton("⬅ Log out")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                color: white;
                font-size: 14px;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                color: #146495;
                font-weight: bold;
            }
        """)
        logout_btn.clicked.connect(self.return_to_login)  # 🔥 Redirection vers Login
        sidebar_layout.addWidget(logout_btn)

        sidebar.setLayout(sidebar_layout)


        # ================ CONTENU PRINCIPAL ================
        content_layout = QVBoxLayout()

        # ✅ Zone de recherche
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search name, email, or etc..")
        self.search_box.setStyleSheet("""
            padding: 10px;
            border: 1px solid #CCC;
            border-radius: 5px;
            font-size: 12px;
            background-color: white;
        """)
        self.search_box.textChanged.connect(self.filter_table)  # 🔥 Recherche active

        search_layout.addWidget(self.search_box)
        content_layout.addLayout(search_layout)

        # ✅ Tableau des utilisateurs
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # ✅ Garder la colonne Action
        self.table.verticalHeader().setVisible(False)  # ✅ Supprime l’index des lignes
        self.table.setHorizontalHeaderLabels(["ID N°", "Full Name", "Admin", "Role", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            border: 1px solid lightgray;
            font-size: 12px;
            background-color: white;
            border-radius: 5px;
        """)

        # ✅ Liste des utilisateurs
        self.users = [
            ("1", "EL BAHAJOUI Jihae", "Mme. Yousra Hasker", "Consultant"),
            ("2", "EL WARDI Abderrazak", "Mr. Said OUAHBA", "Consultant"),
            ("3", "AZIZ Sanae", "Mme. Rim BRIKWAT", "Consultant"),
            ("4", "BRIKWAT Rim", "EL AMRANI EL IDRISSI Omaima", "Admin"),
            ("5", "EL AMRANI EL IDRIDI Omaima", "Not defined", "Manager"),
            ("6", "John Doe", "Admin Central", "Admin"),
            ("7", "Jane Smith", "Mme. Sarah Connor", "Manager"),
            ("8", "Ali Bensalah", "Mr. Hakim Zouhry", "Consultant"),
            ("9", "Said Alami", "Mme. Nadia Bennani", "Consultant"),
            ("10", "Fatima Zahra", "EL AMRANI EL IDRISSI Omaima", "Consultant"),
        ]

        self.current_page = 0
        self.rows_per_page = 5  # ✅ Pagination : 5 utilisateurs par page

        # ✅ Boutons de pagination (Créés avant populate_table pour éviter l'erreur)
        self.prev_btn = QPushButton("⬅ Previous")
        self.prev_btn.clicked.connect(self.previous_page)
        self.prev_btn.setEnabled(False)

        self.next_btn = QPushButton("Next ➡")
        self.next_btn.clicked.connect(self.next_page)

        self.populate_table()
        content_layout.addWidget(self.table)

        # ✅ Ajout des boutons de pagination
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.next_btn)
        content_layout.addLayout(pagination_layout)

        # ✅ Bouton d'ajout
        add_admin_btn = QPushButton("Add Admin")
        add_admin_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a9edc;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #146495;
            }
        """)

        content_layout.addWidget(add_admin_btn)

        # ================ ASSEMBLAGE =================
        main_layout.addWidget(sidebar)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def populate_table(self):
        """ Remplit le tableau avec pagination et actions """
        self.table.setRowCount(0)  # Effacer le tableau avant mise à jour

        start = self.current_page * self.rows_per_page
        end = min(start + self.rows_per_page, len(self.users))
        for row, user in enumerate(self.users[start:end]):
            self.table.insertRow(row)
            for col, data in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(data))

            # ✅ Ajout des boutons Action dans la colonne "Action"
            action_btn = QPushButton("✏️ Edit")
            action_btn.setStyleSheet("padding: 5px; border: none; color: #2176AE;")
            self.table.setCellWidget(row, 4, action_btn)

        # ✅ Gestion des boutons de pagination
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(end < len(self.users))

    def next_page(self):
        """ Passe à la page suivante """
        self.current_page += 1
        self.populate_table()

    def previous_page(self):
        """ Revient à la page précédente """
        self.current_page -= 1
        self.populate_table()

    def filter_table(self):
        """ Filtre le tableau en fonction de la recherche """
        search_text = self.search_box.text().strip().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1):  # ✅ On ignore la colonne Action
                item = self.table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def return_to_login(self):
        """ Ferme la fenêtre et revient à l'écran de connexion """
        self.close()
        self.parent().show()


# TEST
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloWindow()
    window.show()
    sys.exit(app.exec())