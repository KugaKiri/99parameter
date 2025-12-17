import sys
import os
from PySide6.QtCore import Slot
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PySide6 import QtWidgets, QtCore, QtGui, uic
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtGui import QIcon
import re
import json
import csv

# pyinstallerに格納
def resource_path(relative_path):
    """リソースパスを取得（PyInstallerで同梱時のパスを解決）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstallerで実行されている場合
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Config:
    # デフォルト値の設定
    DEFAULT_CONFIG = {
        "FONTPATH": r"C:\Windows\Fonts\AdobeFangsongStd-Regular.otf",
        "ICONPATH": r"parameter/parameter.ico",
        "SHEETPATH": os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"),
        "OUTPUTPATH": r"parameter/data.csv",
        "DATAPATH": [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "class.csv"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill.csv"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "job.csv"),
        ]
    }
    
    # 設定ファイルのパス
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    
    @classmethod
    def load_config(cls):
        """設定ファイルから設定を読み込む"""
        if not os.path.exists(cls.CONFIG_FILE):
            print("設定ファイルが存在しないためデフォルト値で初期化します")
            cls.save_config()
        try:
            with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                cls.FONTPATH = config.get('FONTPATH', cls.DEFAULT_CONFIG['FONTPATH'])
                cls.ICONPATH = config.get('ICONPATH', cls.DEFAULT_CONFIG['ICONPATH'])
                cls.SHEETPATH = config.get('SHEETPATH', cls.DEFAULT_CONFIG['SHEETPATH'])
                cls.OUTPUTPATH = config.get('OUTPUTPATH', cls.DEFAULT_CONFIG['OUTPUTPATH'])
                cls.DATAPATH = config.get('DATAPATH', "\n".join(cls.DEFAULT_CONFIG['DATAPATH'])).split("\n")
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")
            cls.FONTPATH = cls.DEFAULT_CONFIG['FONTPATH']
            cls.ICONPATH = cls.DEFAULT_CONFIG['ICONPATH']
            cls.SHEETPATH = cls.DEFAULT_CONFIG['SHEETPATH']
            cls.OUTPUTPATH = cls.DEFAULT_CONFIG['OUTPUTPATH']
            cls.DATAPATH = cls.DEFAULT_CONFIG['DATAPATH']
    
    @classmethod
    def save_config(cls):
        """設定をファイルに保存"""
        try:
            config = {
                'FONTPATH': cls.FONTPATH,
                'ICONPATH': cls.ICONPATH,
                'SHEETPATH': cls.SHEETPATH,
                'OUTPUTPATH': cls.OUTPUTPATH,
                'DATAPATH': "\n".join(cls.DATAPATH)
            }
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"設定ファイルの保存に失敗しました: {e}")
            # エラーダイアログを表示
            QtWidgets.QMessageBox.critical(
                None, 
                "エラー", 
                f"設定ファイルの保存に失敗しました: {e}",
                QtWidgets.QMessageBox.Ok
            )


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("parameter_qt.ui", self)
        self.setWindowTitle("ツクモツムギ キャラ作成サポートツール")
        self.setGeometry(100, 100, 800, 670)
        self.radioButton_Fugeki.setChecked(True)

        # アイコンを設定
        icon_path = resource_path(Config.ICONPATH)
        self.setWindowIcon(QIcon(icon_path))

        # チェックボックスとエントリーのペアをリスト化
        self.components = [
            (self.checkBox_1Hakuhei, self.label_1Hakuhei, self.lineEdit_1Hakuhei),
            (self.checkBox_2Undo, self.label_2Undo, self.lineEdit_2Undo),
            (self.checkBox_3Ganken, self.label_3Ganken, self.lineEdit_3Ganken),
            (self.checkBox_4Souju, self.label_4Souju, self.lineEdit_4Souju),
            (self.checkBox_5Chikaku, self.label_5Chikaku, self.lineEdit_5Chikaku),

            (self.checkBox_1Shageki, self.label_1Shageki, self.lineEdit_1Shageki),
            (self.checkBox_2Iryo, self.label_2Iryo, self.lineEdit_2Iryo),
            (self.checkBox_3Onmitsu, self.label_3Onmitsu, self.lineEdit_3Onmitsu),
            (self.checkBox_4Kousaku, self.label_4Kousaku, self.lineEdit_4Kousaku),
            (self.checkBox_5Sousa, self.label_5Sousa, self.lineEdit_5Sousa),

            (self.checkBox_1Juho, self.label_1Juho, self.lineEdit_1Juho),
            (self.checkBox_2Ishi, self.label_2Ishi, self.lineEdit_2Ishi),
            (self.checkBox_3Kanpa, self.label_3Kanpa, self.lineEdit_3Kanpa),
            (self.checkBox_4Geino, self.label_4Geino, self.lineEdit_4Geino),
            (self.checkBox_5Densho, self.label_5Densho, self.lineEdit_5Densho),

            (self.checkBox_1Sakubo, self.label_1Sakubo, self.lineEdit_1Sakubo),
            (self.checkBox_2Kyouyo, self.label_2Kyouyo, self.lineEdit_2Kyouyo),
            (self.checkBox_3Kousho, self.label_3Kousho, self.lineEdit_3Kousho),
            (self.checkBox_4Denno, self.label_4Denno, self.lineEdit_4Denno),
            (self.checkBox_5Youshi, self.label_5Youshi, self.lineEdit_5Youshi),
        ]
        # シグナルを接続
        for checkBox, label, lineEdit in self.components:
            checkBox.toggled.connect(lambda checked, cb=checkBox, la=label, le=lineEdit: self.on_checkbox_toggled(cb, la, le))

        # シグナル接続をまとめる
        self.connect_signals()

        self.show()

    def connect_signals(self):
        # ラジオボタンのシグナル接続
        self.radioButton_Fugeki.toggled.connect(self.RaceRadioButton)
        self.radioButton_Tsukumogami.toggled.connect(self.RaceRadioButton)

        # 分類コンボボックス更新のシグナル
        self.radioButton_fugeki.toggled.connect(self.update_class_combobox)
        self.radioButton.tsukumogami.toggled.connect(self.update_class_combobox)

        # ボタンのシグナル接続
        self.pushButton_OutputImg.clicked.connect(self.create_image)
        self.pushButton_Reset.clicked.connect(self.reset_fields)
        self.pushButton_Setting.clicked.connect(self.open_setting)

    @Slot()
    def RaceRadioButton(self, checked):
        if self.sender() == self.radioButton_Fugeki:
            self.radioButton_Fugeki_2.setChecked(checked)
        elif self.sender() == self.radioButton_Tsukumogami:
            self.radioButton_Tsukumogami_2.setChecked(checked)

    @Slot()
    def reset_fields(self):
        print("すべての項目をリセットしました")
    
    @Slot()
    def open_setting(self):
        dialog = ConfigWindow(self)
        dialog.exec()

    def create_widgets(self):
        # フォントパス設定
        font_frame = QtWidgets.QFrame(self.window)
        font_path_label = QtWidgets.QLabel(font_frame, text="フォントパス：")
        font_path_label

    def read_class_csv():
        """class.csv を読み込んで、データを返す"""
        # pyファイルと同じ階層にある class.csv のパスを取得
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "class.csv")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # ヘッダー行を読み飛ばす
                data = list(reader)
            return data
        except FileNotFoundError:
            print(f"エラー: {csv_file_path} が見つかりません。")
            return []  # 空のリストを返す
        except Exception as e:
            print(f"エラー: CSVファイルの読み込み中にエラーが発生しました: {e}")
            return []

    @Slot()
    def update_class_combobox(self, checked):
        # 1.選択されている種族を取得
        selected_race = "巫覡" if checked else "付喪神"
        
        # 2.CSVファイルのデータを取得
        csv_data = self.read_class_csv()

        # 3.選択されている種族に対する分類リストを作成
        class_list = []
        for row in csv_data:
            if row[0] == selected_race:
                class_list.append(row[1])
        
        # 4.comboBox_Classの内容を更新
        self.comboBox_Class.clear()
        self.comboBOx_Class.addItems(class_list)

    @Slot()
    def create_image(self):
        filename = self.lineEdit_Filename.text()

        if not filename:
            filename = "output"
        # すべてのエントリーを辞書にマッピング
        entry_values = {
            "a": self.lineEdit_1Hakuhei, "b": self.lineEdit_2Undo, "c": self.lineEdit_3Ganken, "d": self.lineEdit_4Souju, "e": self.lineEdit_5Chikaku,
            "f": self.lineEdit_1Shageki, "g": self.lineEdit_2Iryo, "h": self.lineEdit_3Onmitsu, "i": self.lineEdit_4Kousaku, "j": self.lineEdit_5Sousa,
            "k": self.lineEdit_1Juho, "l": self.lineEdit_2Ishi, "m": self.lineEdit_3Kanpa, "n": self.lineEdit_4Geino, "o": self.lineEdit_5Densho,
            "p": self.lineEdit_1Sakubo, "q": self.lineEdit_2Kyouyo, "r": self.lineEdit_3Kousho, "s": self.lineEdit_4Denno, "t": self.lineEdit_5Youshi,
            "u": self.lineEdit_BodyPoint, "v": self.lineEdit_TechPoint, "w": self.lineEdit_SocialPoint, "x": self.lineEdit_SpiritPoint
        }

        values = {key: entry.get() for key, entry in entry_values.items()}

        print("取得したエントリー値:", values)

        # 日本語フォントのパス
        font_path = Config.FONTPATH

        # 画像を作成
        img = Image.new('RGBA', (230, 1520), (0, 0, 0, 100)) # 白背景の画像
        draw = ImageDraw.Draw(img)
        font_size = 35
        font = ImageFont.truetype(font_path, font_size) # フォントの設定

        # テキストを描画 (レイアウト調整)
        margin = 20
        column_width = img.width // 2
        y_pos = 40
        star_width = font.getlength(f"★")
        text_width = font.getlength(f"★白兵: {values['a']}") # テキストの幅を取得
        x_pos = margin + star_width + 5

        # 身体グループ
        text_color = "white"
        draw.text((margin, y_pos), f"【身体】{values['u']}", font=font, fill=text_color)
        y_pos += font.size + margin

        # 技量グループ
        text_color = "white"
        draw.text((margin, y_pos), f"【技量】{values['v']}", font=font, fill=text_color)
        y_pos += font.size + margin

        # 心魂グループ
        text_color = "white"
        draw.text((margin, y_pos), f"【心魂】{values['w']}", font=font, fill=text_color)
        y_pos += font.size + margin

        # 社会グループ
        text_color = "white"
        draw.text((margin, y_pos), f"【社会】{values['x']}", font=font, fill=text_color)
        y_pos += font.size + margin

        def on_checkbox_toggled(self, checkBox, label, lineEdit):
            """チェックボックスの状態に応じてエントリーの色を変更"""
            if checkBox.isChecked():
                label.setStyleSheet("color; orange;")
                lineEdit.setStyleSheet("color: orange;")  # オレンジ色
            else:
                label.setStyleSheet("color: white;")
                lineEdit.setStyleSheet("color: white;")  # 白色

        # ファイル名を取得
        filename = set.lineEdit_NameInput()

        # 画像を保存
        output_path = f"{filename}.png"
        img.save(output_path)

        # 出力画像を分割処理
        split_image(img, filename, 230, 380)

        # 分割画像をシートに貼り付けて保存
        combine_images_to_sheet(filename, charactor_type_var)

    def validate_input(input_string):
        """
        入力が英数字のみで構成されているかを確認する関数。
        英数字のみの場合はTrueを返し、それ以外の場合はFalseを返す。
        """
        if re.match("^[0-9]*$", input_string):
            return True
        else:
            return False

    def update_entries(event):
        """
        Updates multiple Entry widgets with values from other Entry widgets.

        This function retrieves values from specific source Entry widgets 
        (entry_u, entry_v, entry_w, entry_x) and updates multiple target 
        Entry widgets accordingly.
        """
        update_entries_with_value(entry_u, [entry_a, entry_b, entry_c, entry_d, entry_e])
        update_entries_with_value(entry_v, [entry_f, entry_g, entry_h, entry_i, entry_j])
        update_entries_with_value(entry_w, [entry_k, entry_l, entry_m, entry_n, entry_o])
        update_entries_with_value(entry_x, [entry_p, entry_q, entry_r, entry_s, entry_t])

    def update_entries_with_value(source_entry, target_entries):
        """
        Updates a list of target Entry widgets with the value from a source Entry widget.

        Args:
            source_entry: The source Entry widget to get the value from.
            target_entries: A list of target Entry widgets to update.
        """
        value = source_entry.get()
        for target_entry in target_entries:
            target_entry.delete(0, tk.END)
            target_entry.insert(0, value)

    Config.load_config()

    def update_status(message, is_error=False):
        """ステータスバーの更新"""
        status_var.set(message)
        # if is_error:
        #     logging.error(message)
        # else:
        #     logging.info(message)

    def change_color(var, entry, check_button):
        if var.get():
        entry.config(fg="blue")
        check_button.config(fg="blue")
        else:
        entry.config(fg="black")
        check_button.config(fg="black")

    def increment_value(var, entry, check_button):
        """
        Increments or decrements the value in the entry field based on the 
        value of the var.

        Args:
            var: A StringVar object.
            entry: The Entry widget.
            label: The Label widget associated with the entry.
        """
        current_value = int(entry.get() or 0)
        if var.get():
            new_value = current_value + 1
        else:
            new_value = current_value - 1

        entry.delete(0, tk.END)
        entry.insert(0, new_value)
        change_color(var, entry, check_button)

    components = [
        (var_a, entry_a, check_button_a), 
        (var_b, entry_b, check_button_b), 
        (var_c, entry_c, check_button_c),
        (var_d, entry_d, check_button_d), 
        (var_e, entry_e, check_button_e), 
        (var_f, entry_f, check_button_f),
        (var_g, entry_g, check_button_g), 
        (var_h, entry_h, check_button_h), 
        (var_i, entry_i, check_button_i),
        (var_j, entry_j, check_button_j), 
        (var_k, entry_k, check_button_k), 
        (var_l, entry_l, check_button_l),
        (var_m, entry_m, check_button_m), 
        (var_n, entry_n, check_button_n), 
        (var_o, entry_o, check_button_o),
        (var_p, entry_p, check_button_p), 
        (var_q, entry_q, check_button_q), 
        (var_r, entry_r, check_button_r),
        (var_s, entry_s, check_button_s), 
        (var_t, entry_t, check_button_t)
    ]

    # 一括で処理
    for var, entry, check_button in components:
        increment_value(var, entry, check_button)

    # エントリを管理するリスト
    entries = [filename_entry, entry_a, entry_b, entry_c, entry_d, entry_e, entry_f, entry_g, entry_h, entry_i, entry_j, entry_k, entry_l, entry_m, entry_n, entry_o, entry_p, entry_q, entry_r, entry_s, entry_t, entry_u, entry_v, entry_w, entry_x]
    vars = [var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h, var_i, var_j, var_k, var_l, var_m, var_n, var_o, var_p, var_q, var_r, var_s, var_t]
    check_buttons = [check_button_a, check_button_b, check_button_c, check_button_d, check_button_e, check_button_f, check_button_g, check_button_h, check_button_i, check_button_j, check_button_k, check_button_l, check_button_m, check_button_n, check_button_o, check_button_p, check_button_q, check_button_r, check_button_s, check_button_t]

    # エントリーを空白に
    def clear_entries():
        for entry in entries:
            entry.delete(0, tk.END)
            update_status("入力した内容をリセットしました")

    # チェックボタンをオフに
    def check_off():
        for var, check_button, entry  in zip(vars, entries, check_buttons):
            var.set(False)
            change_color(var, check_button, entry)

    # エントリーとチェックボタンを初期値に
    def clear_all():
        clear_entries()
        check_off()
        charactor_type_var.set(False)

        update_status("キャラ分類、能力値、技能取得チェック、キャラ名を入力して画像作成してください")


    class ConfigWindow:
        def __init__(self, parent):
            self.window = tk.Toplevel(parent)
            icon_path = resource_path(Config.ICONSUBPATH)
            try:
                self.window.iconbitmap(icon_path)
            except tk.TclError:
                print("アイコンファイルが見つからないため、デフォルトアイコンを使用") 
            self.window.title("設定")
            self.window.geometry("400x300")
            self.window.resizable(False, False)

            # 設定画面を親ウィンドウの中央に表示
            self.center_window(parent)
            
            # モーダルウィンドウとして設定（親ウィンドウを操作不可に）
            self.window.transient(parent)
            self.window.grab_set()
            
            # 設定項目の作成
            self.create_widgets()
        
        def center_window(self, parent):
            # 親ウィンドウの位置とサイズを取得
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            
            # 設定ウィンドウのサイズ
            window_width = 400
            window_height = 550
            
            # 中央の位置を計算
            x = parent_x + (parent_width - window_width) // 2
            y = parent_y + (parent_height - window_height) // 2
            
            # 位置を設定
            self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        def create_widgets(self):
            # フォントパス設定
            font_frame = ttk.LabelFrame(self.window, text="フォント設定", padding=10)
            font_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(font_frame, text="フォントパス:").pack(anchor="w")
            font_path = ttk.Entry(font_frame, width=40)
            font_path.insert(0, Config.FONTPATH)
            font_path.pack(fill="x", pady=5)
            
            def browse_font():
                filename = filedialog.askopenfilename(
                    title="フォントファイルを選択",
                    filetypes=[("フォントファイル", "*.ttf;*.otf")]
                )
                if filename:
                    font_path.delete(0, tk.END)
                    font_path.insert(0, filename)
            
            ttk.Button(font_frame, text="参照...", command=browse_font).pack(anchor="e")
            
            icon_frame = ttk.LabelFrame(self.window, text="アイコン設定", padding=10)
            icon_frame.pack(fill="x", padx=10, pady=5)

            ttk.Label(icon_frame, text="アイコンパス:").pack(anchor="w")
            icon_path = ttk.Entry(icon_frame, width=40)
            icon_path.insert(0, Config.ICONPATH)
            icon_path.pack(fill="x", pady=5)

            def icon_file():
                filename = filedialog.askopenfilename(
                    title="アイコンファイルを選択",
                    filetypes=[("アイコンファイル", "*.ico;*.png")]
                )
                if filename:
                    icon_path.delete(0, tk.END)
                    icon_path.insert(0, filename)
            ttk.Button(icon_frame, text="参照...", command=icon_file).pack(anchor="e")

            # シートパス設定
            sheet_frame = ttk.LabelFrame(self.window, text="シート設定", padding=10)
            sheet_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(sheet_frame, text="シートパス:").pack(anchor="w")
            sheet_path = ttk.Entry(sheet_frame, width=40)
            sheet_path.insert(0, Config.SHEETPATH)
            sheet_path.pack(fill="x", pady=5)
            
            def browse_sheet():
                filename = filedialog.askopenfilename(
                    title="シート画像を選択",
                    filetypes=[("画像ファイル", "*.png")]
                )
                if filename:
                    sheet_path.delete(0, tk.END)
                    sheet_path.insert(0, filename)
            
            ttk.Button(sheet_frame, text="参照...", command=browse_sheet).pack(anchor="e")
            
            # キャラメイク用データパスの設定
            data_frame = ttk.LabelFrame(self.window, text="キャラメイク用データ設定", padding=10)
            data_frame.pack(fill="x", padx=10, pady=5)

            ttk.Label(data_frame, text="キャラメイク用データパス:").pack(anchor="w")
            data_path = ttk.Entry(data_frame, width=40)
            data_path.insert(0, Config.DATAPATH)
            data_path.pack(fill="x", pady=5)

            def data_file():
                filename = filedialog.askopenfilename(
                    title="キャラメイク用データを選択",
                    filetypes=[("データファイル", "*.csv")]
                )
                if filename:
                    data_path.delete(0, tk.END)
                    data_path.insert(0, filename)
            
            ttk.Button(data_frame, text="参照...", command=data_file).pack(anchor="e")

            # 保存ボタン
            def save_settings():
                Config.FONTPATH = font_path.get()
                Config.ICONPATH = icon_path.get()
                Config.SHEETPATH = sheet_path.get()
                Config.DATAPATH = data_path.get()
                Config.save_config()
                self.window.destroy()
                
            ttk.Button(self.window, text="保存", command=save_settings).pack(side="right", padx=10, pady=10)
            ttk.Button(self.window, text="キャンセル", command=self.window.destroy).pack(side="right", pady=10)

    def configration():
        ConfigWindow(root)

    # 設定ボタン
    config_button = tk.Button(output_frame, text="⚙️", command=configration)
    config_button.grid(row=0, column=15, pady=(10, 5), padx=(0, 0), sticky="e")

    def split_image(original_img, output_prefix, split_width, split_height):
        """
        画像を指定したサイズで分割して保存します。

        Args:
            original_img (PIL.Image): 分割する元の画像
            output_prefix (str): 出力ファイル名のプレフィックス
            split_width (int): 分割後の画像の幅
            split_height (int): 分割後の画像の高さ

        Returns:
            bool: 分割が成功したかどうか
        """
        img_width, img_height = original_img.size
        num_of_splits = int(img_height // split_height)  # 分割枚数

        for i in range(num_of_splits):
            # 切り出す領域を計算
            box = (0, i * split_height, split_width, (i + 1) * split_height)
            cropped_img = original_img.crop(box)
            # 分割画像を保存
            cropped_img.save(f"{output_prefix}_{i+1}.png")

    def combine_images_to_sheet(filename, charactor_type_var, margin_x=19, margin_y=25, gap_x=6, gap_y=6):
        """
        分割画像をシート画像に貼り付けて保存する関数

        Args:
            filename: 元のファイル名（プレフィックス）
            margin_x: 貼り付け開始位置の横方向の余白
            margin_y: 貼り付け開始位置の縦方向の余白
            gap_x: 各画像間の横方向の間隔
            gap_y: 各画像間の縦方向の間隔
        """
        # シート画像を読み込む
        try:
            sheet_img = Image.open(Config.SHEETPATH)
        except FileNotFoundError:
            print("sheet.pngが見つかりません")
            return

        # シート画像のサイズを計算（田の字なので2x2）
        sheet_width, sheet_height = 504, 816

        cell_width, cell_height = 230, 380
        
        # 分割画像をシートに配置
        for i in range(4):
            try:
                # 分割画像を読み込み
                split_img = Image.open(f"{filename}_{i+1}.png")

                # 貼り付け位置を計算（左上から順に配置）
                x_offset = margin_x + (i % 2) * (cell_width + gap_x)
                y_offset = margin_y + (i // 2) * (cell_height + gap_y)

                # 貼り付け位置がシート画像の範囲を超えないように確認
                if x_offset + cell_width > sheet_width or y_offset + cell_height > sheet_height:
                    print(f"画像 {filename}_{i+1}.png を貼り付けるスペースがありません。")
                    continue

                # 分割画像をシートに貼り付け
                sheet_img.paste(split_img, (x_offset, y_offset))
            except FileNotFoundError:
                print(f"分割画像 {filename}_{i+1}.png が見つかりません。")
                continue

        # 画像下部に情報を追加
        new_height = sheet_height + 48
        new_sheet_img = Image.new("RGBA", (sheet_width, new_height), (0, 0, 0, 0))
        new_sheet_img.paste(sheet_img, (0,0))

        # ラジオボタンの選択内容とファイル名を取得
        charactor_type = "巫覡" if not charactor_type_var.get() else "付喪神"

        # テキストを描画
        draw = ImageDraw.Draw(new_sheet_img)
        try:
            font = ImageFont.truetype(Config.FONTPATH, 50)
        except IOError:
            default_font = tkFont.nametofont("TkDefaultFont")
            font = ImageFont.truetype(default_font.actual()["family"], 50)

        text = f"{charactor_type} | {filename}"

        # テキストの長さを計算し、幅に収めるための調整
        max_width = sheet_width - margin_x * 2
        bbox = draw.textbbox((0, 0), text, font=font) 

        # フォントサイズ調整
        while bbox[2] - bbox[0] > max_width and font.size > 25:
            font = ImageFont.truetype(Config.FONTPATH, font.size -2)
            bbox = draw.textbbox((0, 0), text, font=font)

        # テキストを中央揃えで配置
        x_pos = (sheet_width - (bbox[2] - bbox[0])) // 2
        y_pos = new_height - 48  # 下部に配置

        draw.text((x_pos, y_pos), text , fill="white", font=font)

        # シート画像を保存
        sheet_output_path = f"sheet_{filename}.png"
        new_sheet_img.save(sheet_output_path)
        update_status(f"シート画像を保存しました: {sheet_output_path}")

        # filename.png の削除
        try:
            os.remove(f"{filename}.png")
            print(f"{filename}.png を削除しました。")
        except FileNotFoundError:
            print(f"{filename}.png が見つかりません。削除できませんでした。")

class ConfigWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("setting.ui", self)  # setting.ui を読み込む
        self.setWindowTitle("設定")
        self.setFixedSize(405, 600)

        # Configクラスの設定をロード
        Config.load_config()

        # 初期値を保存
        self.load_settings()

        self.setModal(True)
        self.connect_signals()

    def connect_signals(self):
        """シグナル接続をまとめる"""
        self.pushButton_Font_2.clicked.connect(self.browse_font) #pushButton_Font_2
        self.pushButton_Icon_2.clicked.connect(self.browse_icon)   #pushButton_Icon_2
        self.pushButton_Sheet_2.clicked.connect(self.browse_sheet) #pushButton_Sheet_2
        self.pushButton_Output_2.clicked.connect(self.browse_output) #pushButton_Output_2
        self.pushButton_Datafile_2.clicked.connect(self.browse_datafile) #pushButton_Datafile_2
        self.pushButton.clicked.connect(self.save_settings)        #pushButton
        self.pushButton_2.clicked.connect(self.reject)             #pushButton_2

    def load_settings(self):
        """Configクラスの値をUIに反映"""
        self.lineEdit_Font_2.setText(Config.FONTPATH or Config.DEFAULT_CONFIG['FONTPATH'])   #lineEdit_Font_2
        self.lineEdit_Icon_2.setText(Config.ICONPATH or Config.DEFAULT_CONFIG['ICONPATH'])   #lineEdit_Icon_2
        self.lineEdit_Sheet_2.setText(Config.SHEETPATH or Config.DEFAULT_CONFIG['SHEETPATH']) #lineEdit_Sheet_2
        self.lineEdit_Output_2.setText(Config.OUTPUTPATH or Config.DEFAULT_CONFIG['OUTPUTPATH']) #lineEdit_Output_2
        self.textEdit_Datafile_2.setText(";".join(Config.DATAPATH) if Config.DATAPATH else ";".join(Config.DEFAULT_CONFIG['DATAPATH'])) #lineEdit_Datafile_2

    @Slot()
    def browse_font(self):
        default_dir = os.path.dirname(Config.FONTPATH) if Config.FONTPATH else os.path.expanduser("~")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "フォントファイルを選択", default_dir, "フォントファイル (*.ttf *.otf)"
        )
        if filename:
            Config.FONTPATH = filename
            self.lineEdit_Font_2.setText(filename)

    @Slot()
    def browse_icon(self):
        default_dir = os.path.dirname(Config.ICONPATH) if Config.ICONPATH else os.path.expanduser("~")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "アイコンフォルダを選択", default_dir, "アイコンファイル (*.ico *.png)"
        )
        if filename:
            Config.ICONPATH = filename
            self.lineEdit_Icon_2.setText(filename)

    @Slot()
    def browse_sheet(self):
        default_dir = os.path.dirname(Config.SHEETPATH) if Config.SHEETPATH else os.path.expanduser("~")
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "シートフォルダを選択", default_dir, "画像ファイル (*.png)"
        )
        if filename:
            Config.SHEETPATH = filename
            self.lineEdit_Sheet_2.setText(filename)

    @Slot()
    def browse_output(self):
        default_dir = os.path.dirname(Config.OUTPUTPATH) if Config.OUTPUTPATH else os.path.expanduser("~")
        dirname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "出力フォルダを選択", default_dir, "フォルダ"
        )
        if dirname:
            Config.OUTPUTPATH = dirname
            self.lineEdit_Output_2.setText(dirname)

    @Slot()
    def browse_datafile(self):
        """複数のデータファイルを選択する"""
        default_dir = os.path.dirname(Config.DATAPATH[0]) if Config.DATAPATH else os.path.expanduser("~")
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "データファイルを選択", default_dir, "データファイル (*.csv)"
        )
        if filenames:
            Config.DATAPATH = filenames
            self.textEdit_Datafile_2.setPlainText("\n".join(filenames))

    def save_settings(self):
        Config.FONTPATH = self.lineEdit_Font_2.text()
        Config.ICONPATH = self.lineEdit_Icon_2.text()
        Config.SHEETPATH = self.lineEdit_Sheet_2.text()
        Config.OUTPUTPATH = self.lineEdit_Output_2.text()
        Config.DATAPATH = self.textEdit_Datafile_2.toPlainText().split("\n")
        Config.save_config()
        self.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow()
    app.exec()
