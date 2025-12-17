import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QGridLayout)
from PySide6.QtCore import QStringListModel
import csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Data Import (PySide6)")
        self.setGeometry(100, 100, 300, 100)
        self.setStyleSheet("background-color: white;")

        # Create a central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        # Create dropdowns and entries
        self.csv_file_path_1 = "parameter/test1.csv"
        self.options_a = []
        self.data_a = {}
        self.model_a = QStringListModel()
        self.combo_a = QComboBox()

        self.csv_file_path_2 = "parameter/test2.csv"
        self.options_g = []
        self.data_g = {}
        self.model_g = QStringListModel()
        self.combo_g = QComboBox()

        self.entry_a = QLineEdit()
        self.entry_b = QLineEdit()
        self.entry_c = QLineEdit()
        self.entry_d = QLineEdit()

        self.load_csv_data(self.csv_file_path_1, self.options_a, self.data_a, self.model_a, key_column_index=0, data_start_column=1)
        self.load_csv_data(self.csv_file_path_2, self.options_g, self.data_g, self.model_g, key_column_index=0, data_start_column=1)

        self.model_a.setStringList(["", *self.options_a])
        self.combo_a.setModel(self.model_a)
        self.combo_a.setCurrentText("Select A")
        self.combo_a.currentIndexChanged.connect(self.update_entries)

        self.model_g.setStringList(["", *self.options_g])
        self.combo_g.setModel(self.model_g)
        self.combo_g.setCurrentText("Select G")
        self.combo_g.currentIndexChanged.connect(self.update_entries)

        self.layout.addWidget(QLabel("Select A:"), 0, 0)
        self.layout.addWidget(self.combo_a, 0, 1)
        self.layout.addWidget(QLabel("Select G:"), 0, 2)
        self.layout.addWidget(self.combo_g, 0, 3)

        self.layout.addWidget(QLabel("B:"), 1, 0)
        self.layout.addWidget(self.entry_a, 1, 1)
        self.layout.addWidget(QLabel("C:"), 1, 2)
        self.layout.addWidget(self.entry_b, 1, 3)
        self.layout.addWidget(QLabel("D:"), 2, 0)
        self.layout.addWidget(self.entry_c, 2, 1)
        self.layout.addWidget(QLabel("E:"), 2, 2)
        self.layout.addWidget(self.entry_d, 2, 3)

        self.update_entries()

    def load_csv_data(self, file_path, options_list, data_dict, model, key_column_index=0, data_start_column=1):
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
                header = next(reader, None)
                if header:
                    pass
                for row in reader:
                    if row:
                        key = row[key_column_index].strip('"')
                        options_list.append(key)
                        numeric_data = []
                        for x in row[data_start_column:data_start_column+4]:
                            value = x.strip('"')
                            try:
                                numeric_data.append(float(value))
                            except ValueError:
                                numeric_data.append(0.0)
                        data_dict[key] = numeric_data
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def update_entries(self, index=None):
        data_a = self.data_a.get(self.combo_a.currentText(), [0.0] * 4)
        data_g = self.data_g.get(self.combo_g.currentText(), [0.0] * 4)
        self.entry_a.setText(f"{int(data_a[0] + data_g[0])}")
        self.entry_b.setText(f"{int(data_a[1] + data_g[1])}")
        self.entry_c.setText(f"{int(data_a[2] + data_g[2])}")
        self.entry_d.setText(f"{int(data_a[3] + data_g[3])}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())