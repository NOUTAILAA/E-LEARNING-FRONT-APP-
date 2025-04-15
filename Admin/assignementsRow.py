from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from Admin.affectationspopup import AffectationPopup

class AssignementRow(QFrame):
    def __init__(self, manager_id, manager_nom, apprenants):
        super().__init__()
        self.manager_id = manager_id

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #0070AD;
                color: white;
                padding: 6px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A8D;
            }
            QComboBox {
                padding: 5px;
                min-width: 200px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            QLabel {
                font-size: 14px;
                min-width: 150px;
            }
        """)

        layout = QHBoxLayout()

        # Nom complet du manager
        self.manager_label = QLabel(manager_nom)
        layout.addWidget(self.manager_label)

        # Liste déroulante des apprenants (affectés)
        self.combo_apprenants = QComboBox()
        for apprenant in apprenants:
            full_name = f"{apprenant['prenom']} {apprenant['nom']}"
            self.combo_apprenants.addItem(full_name, userData=apprenant['id'])
        layout.addWidget(self.combo_apprenants)

        # Bouton Add
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.open_affectation_popup)
        layout.addWidget(self.add_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def open_affectation_popup(self):
        self.popup = AffectationPopup(
            manager_id=self.manager_id,
            manager_name=self.manager_label.text()
        )
        self.popup.show()
