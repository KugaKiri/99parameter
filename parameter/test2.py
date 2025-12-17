import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from untitled import Ui_MainWindow
import csv

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ここで Designer で作成したウィジェットにアクセスできます
        # 例: self.radioButton, self.radioButton_2, self.comboBox, self.label など
        self.data = {}
        self.load_data()
        # RadioButton の toggled シグナルにスロットを接続します
        self.radioButton.toggled.connect(self.on_radio_button_toggled)
        self.radioButton_2.toggled.connect(self.on_radio_button_toggled)
        self.comboBox.currentIndexChanged.connect(self.update_labels)

        self.update_combobox()  # 初期化時に ComboBox を更新
        # ComboBox の初期化やデータの読み込みなどの処理をここに記述します

    def load_data(self):
        # CSV ファイルからデータを読み込み、RadioButton に対応する ComboBox の内容を準備する処理
        self.data = {'test': {}, 'test2': {}}  # 例: {'RadioButton': ['選択肢1', '選択肢2', ...]}

        try:
            with open("parameter/category.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # ヘッダーを読み飛ばす
                category_index = header.index('Category')
                name_index = header.index('Name')
                value_index = header.index('Value')
                value_index2 = header.index('Value2')
                value_index3 = header.index('Value3')
                value_index4 = header.index('Value4')

                for row in reader:
                    category = row[category_index].strip()
                    name = row[name_index].strip()
                    value = row[value_index].strip()
                    value2 = row[value_index2].strip()
                    value3 = row[value_index3].strip()
                    value4 = row[value_index4].strip()

                    if category == 'test':
                        self.data['test'][name] = {'value': value, 'value2': value2, 'value3': value3, 'value4': value4}
                    elif category == 'test2':
                        self.data['test2'][name] = {'value': value, 'value2': value2, 'value3': value3, 'value4': value4}
        except FileNotFoundError:
            print("CSV ファイルが見つかりません。")
            self.data = {'test': {}, 'test2': {}}

        # ComboBox の初期表示を設定
        self.update_combobox()

    def on_radio_button_toggled(self, checked):
        if checked:
            selected_radio_button = self.sender()  # シグナルを送信した RadioButton を取得
            self.update_combobox(selected_radio_button.text())

    def update_combobox(self, selected_category=None):
        self.comboBox.clear()
        if selected_category and selected_category in self.data:
            self.comboBox.addItems(self.data[selected_category])
        else:
            self.comboBox.addItems([]) # 重複を削除してソートして表示 (例)
            self.clear_labels()
    
    def update_labels(self, index):
        selected_name = self.comboBox.itemText(index)
        selected_category = None
        for cat, names in self.data.items():
            if selected_name in names:
                selected_category = cat
                break

        if selected_category and selected_name in self.data[selected_category]:
            values = self.data[selected_category][selected_name]
            self.label.setText(values['value'])
            self.label_2.setText(values['value2'])
            self.label_3.setText(values['value3'])
            self.label_4.setText(values['value4'])  # 追加: 選択された名前を表示
        else:
            self.clear_labels()
    
    def clear_labels(self):
        self.label.clear()
        self.label_2.clear()
        self.label_3.clear()
        self.label_4.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())