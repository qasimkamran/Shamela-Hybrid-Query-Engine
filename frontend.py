import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class ResultTab(QWidget):
    def __init__(self, link, title, preview, parent=None):
        super(ResultTab, self).__init__(parent)
        self.link = link
        self.title = title
        self.preview = preview
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Row 1: Hyperlink and Title in one line
        top_layout = QHBoxLayout()
        self.link_label = QLabel(f'<a href="{self.link}">{self.link}</a>')
        self.link_label.setTextFormat(Qt.RichText)
        self.link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setStyleSheet("color: #4FC3F7;")  # Hyperlink color

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight: bold; padding-left: 10px;")
        
        top_layout.addWidget(self.link_label)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Row 2: Preview text and Translate button
        bottom_layout = QHBoxLayout()
        self.preview_label = QLabel(self.preview)
        self.preview_label.setWordWrap(True)
        bottom_layout.addWidget(self.preview_label)
        
        self.translate_button = QPushButton("Translate")
        self.translate_button.setFixedWidth(100)
        self.translate_button.clicked.connect(self.translate_preview)
        bottom_layout.addWidget(self.translate_button)
        
        layout.addLayout(bottom_layout)
        self.setLayout(layout)
    
    def translate_preview(self):
        # Dummy translation: converting text to uppercase
        translated_text = self.preview.upper()  
        self.preview_label.setText(translated_text)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Shamela Fusion")
        self.resize(800, 600)
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        
        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)
        
        # Tab widget for search results
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
    
    def perform_search(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            return
        
        # Clear previous results
        self.tabs.clear()
        
        # Simulated search results (in a real app, perform your API call here)
        results = [
            {
                "link": "https://example.com/1",
                "title": f"Result 1 for {search_term}",
                "preview": "This is the preview text for result 1."
            },
            {
                "link": "https://example.com/2",
                "title": f"Result 2 for {search_term}",
                "preview": "Preview text for result 2 goes here."
            },
            {
                "link": "https://example.com/3",
                "title": f"Result 3 for {search_term}",
                "preview": "Another preview text for result 3."
            },
        ]
        
        # Add each result as a separate tab
        for i, result in enumerate(results, start=1):
            tab = ResultTab(result["link"], result["title"], result["preview"])
            self.tabs.addTab(tab, f"Result {i}")

def apply_dark_theme(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("""
        QWidget { font-size: 12px; }
        QPushButton { padding: 4px; }
        QLineEdit { padding: 4px; }
        QTabWidget::pane { border: 1px solid #444; }
        QTabBar::tab { background: #555; padding: 6px; border: 1px solid #444; }
        QTabBar::tab:selected { background: #666; }
    """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

