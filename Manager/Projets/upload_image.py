import requests
from PyQt6.QtWidgets import (
    QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageClickableLabel(QLabel):
    def __init__(self, projet_id, parent=None):
        super().__init__(parent)
        self.projet_id = projet_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Choisir une image",
                "",
                "Images (*.png *.jpg *.jpeg)"
            )
            if file_path:
                try:
                    with open(file_path, 'rb') as image_file:
                        files = {
                            "photo": image_file
                        }
                        response = requests.post(
                            f"http://localhost:8090/api/projets/{self.projet_id}/upload-image",
                            files=files
                        )
                        if response.status_code == 200:
                            QMessageBox.information(self, "Succès", "Image mise à jour avec succès.")
                            updated_img = requests.get(f"http://localhost:8090/api/projets/{self.projet_id}/photo")
                            if updated_img.status_code == 200:
                                pixmap = QPixmap()
                                pixmap.loadFromData(updated_img.content)
                                self.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
                        else:
                            QMessageBox.critical(self, "Erreur", f"Erreur de mise à jour:\n{response.text}")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", str(e))