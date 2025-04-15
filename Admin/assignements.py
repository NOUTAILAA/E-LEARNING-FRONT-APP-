from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
import requests
from Admin.assignementsRow import AssignementRow 

class AssignementsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Assignements")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Scrollable container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout()

        # === APPEL À L'API POUR RÉCUPÉRER LES MANAGERS ===
        try:
            response = requests.get("http://localhost:8090/api/managers")
            managers = response.json()

            for manager in managers:
                apprenants_response = requests.get(f"http://localhost:8090/api/managers/{manager['id']}/apprenants")
                apprenants = apprenants_response.json()
                row = AssignementRow(
                        manager_id=manager['id'],
                        manager_nom=f"{manager['prenom']} {manager['nom']}",
                        apprenants=apprenants
                    )

                row.setFrameStyle(QFrame.Shape.Panel)
                content_layout.addWidget(row)

        except Exception as e:
            print("Erreur API :", e)

        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.setLayout(layout)
