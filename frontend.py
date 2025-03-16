import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class ResultRow(QWidget):
    def __init__(self, link, title, preview, parent=None):
        super(ResultRow, self).__init__(parent)
        self.link = link
        self.title = title
        self.preview = preview
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Top row: Hyperlink and Title
        top_layout = QHBoxLayout()
        self.link_label = QLabel(f'<a href="{self.link}">{self.link}</a>')
        self.link_label.setTextFormat(Qt.RichText)
        self.link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setStyleSheet("color: #4FC3F7;")  # hyperlink color
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight: bold; padding-left: 10px;")
        
        top_layout.addWidget(self.link_label)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Bottom row: Preview text and Translate button
        bottom_layout = QHBoxLayout()
        self.preview_label = QLabel(self.preview)
        self.preview_label.setWordWrap(True)
        bottom_layout.addWidget(self.preview_label, 1)
        
        self.translate_button = QPushButton("Translate")
        self.translate_button.setFixedWidth(100)
        self.translate_button.clicked.connect(self.translate_preview)
        bottom_layout.addWidget(self.translate_button)
        
        layout.addLayout(bottom_layout)
        self.setLayout(layout)
        
    def translate_preview(self):
        # Dummy translation: convert preview text to uppercase
        translated_text = self.preview.upper()
        self.preview_label.setText(translated_text)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Shamela Fusion")
        self.resize(800, 600)
        self.results_per_page = 5
        self.current_page = 1
        self.all_results = []  # will hold all results
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Search bar layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_button = QPushButton("Search")
        self.search_button.setFixedWidth(100)
        self.search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)
        
        # Scroll area for results
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)
        
        # Container widget inside the scroll area
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setSpacing(10)
        self.scroll_area.setWidget(self.results_container)
        
        # Pager layout
        self.pager_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.setFixedWidth(100)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton("Next")
        self.next_button.setFixedWidth(100)
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel("Page 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        
        self.pager_layout.addWidget(self.prev_button)
        self.pager_layout.addStretch()
        self.pager_layout.addWidget(self.page_label)
        self.pager_layout.addStretch()
        self.pager_layout.addWidget(self.next_button)
        main_layout.addLayout(self.pager_layout)
    
    def perform_search(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            return
        
        # Simulated search results (replace with your actual API call)
        self.all_results = [
            {
                "link": f"https://example.com/{i}",
                "title": f"Result {i} for {search_term}",
                "preview": f"This is the preview text for result {i}."
            }
            for i in range(1, 16)  # Simulate 15 results
        ]
        
        self.current_page = 1
        self.update_results_page()
    
    def update_results_page(self):
        # Clear current results
        for i in reversed(range(self.results_layout.count())):
            widget_item = self.results_layout.itemAt(i)
            if widget_item.widget():
                widget_item.widget().setParent(None)
        
        start_index = (self.current_page - 1) * self.results_per_page
        end_index = start_index + self.results_per_page
        page_results = self.all_results[start_index:end_index]
        
        for result in page_results:
            row = ResultRow(result["link"], result["title"], result["preview"])
            self.results_layout.addWidget(row)
        
        # Update pager label and button states
        total_pages = (len(self.all_results) + self.results_per_page - 1) // self.results_per_page
        self.page_label.setText(f"Page {self.current_page} of {total_pages}")
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < total_pages)
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_results_page()
    
    def next_page(self):
        total_pages = (len(self.all_results) + self.results_per_page - 1) // self.results_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_results_page()

def apply_dark_theme(app):
    # Create a dark palette
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
    
    # Enforce dark backgrounds and light text via style sheet
    app.setStyleSheet("""
        QWidget {
            font-size: 12px;
            background-color: #2d2d2d;
            color: white;
        }
        QPushButton {
            background-color: #3c3c3c;
            color: white;
            padding: 4px;
            border: none;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QLineEdit {
            background-color: #3c3c3c;
            color: white;
            padding: 4px;
            border: 1px solid #555;
        }
        QScrollArea {
            border: none;
        }
        QLabel {
            color: white;
        }
    """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
