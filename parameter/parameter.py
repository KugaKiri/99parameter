# pyinstaller --onefile --noconsole --add-data "parameter/parameter.ico;parameter" --icon=parameter/parameter.ico parameter/parameter.py

import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import Checkbutton
from tkinter import font as tkFont
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog
import re
import json

class Config:
    # デフォルト値の設定
    DEFAULT_CONFIG = {
        "FONTPATH": r"C:\Windows\Fonts\AdobeFangsongStd-Regular.otf",
        "ICONPATH": r"parameter/parameter.ico",
        "SHEETPATH": os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheet.png"),
        "ICONSUBPATH": r"parameter/gear.ico"
    }
    
    # 設定ファイルのパス
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    
    @classmethod
    def load_config(cls):
        """設定ファイルから設定を読み込む"""
        try:
            if os.path.exists(cls.CONFIG_FILE):
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    cls.FONTPATH = config.get('FONTPATH', cls.DEFAULT_CONFIG['FONTPATH'])
                    cls.ICONPATH = config.get('ICONPATH', cls.DEFAULT_CONFIG['ICONPATH'])
                    cls.SHEETPATH = config.get('SHEETPATH', cls.DEFAULT_CONFIG['SHEETPATH'])
                    cls.ICONSUBPATH = config.set('ICONSUBPATH', cls.DEFAULT_CONFIG['ICONSUBPATH'])
            else:
                cls.FONTPATH = cls.DEFAULT_CONFIG['FONTPATH']
                cls.ICONPATH = cls.DEFAULT_CONFIG['ICONPATH']
                cls.SHEETPATH = cls.DEFAULT_CONFIG['SHEETPATH']
                cls.ICONSUBPATH = cls.DEFAULT_CONFIG['ICONSUBPATH']
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {e}")
            # デフォルト値を使用
            cls.FONTPATH = cls.DEFAULT_CONFIG['FONTPATH']
            cls.ICONPATH = cls.DEFAULT_CONFIG['ICONPATH']
            cls.SHEETPATH = cls.DEFAULT_CONFIG['SHEETPATH']
            cls.ICONSUBPATH = cls.DEFAULT_CONFIG['ICONSUBPATH']
    
    @classmethod
    def save_config(cls):
        """設定をファイルに保存"""
        try:
            config = {
                'FONTPATH': cls.FONTPATH,
                'ICONPATH': cls.ICONPATH,
                'SHEETPATH': cls.SHEETPATH,
                'ICONSUBPATH': cls.ICONSUBPATH
            }
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"設定ファイルの保存に失敗しました: {e}")

def create_image():
    # 入力されたファイル名を取得
    filename = filename_entry.get()
    if not filename:
        filename = "output"

    # すべてのエントリーを辞書にマッピング
    entry_values = {
        "a": entry_a, "b": entry_b, "c": entry_c, "d": entry_d, "e": entry_e,
        "f": entry_f, "g": entry_g, "h": entry_h, "i": entry_i, "j": entry_j,
        "k": entry_k, "l": entry_l, "m": entry_m, "n": entry_n, "o": entry_o,
        "p": entry_p, "q": entry_q, "r": entry_r, "s": entry_s, "t": entry_t,
        "u": entry_u, "v": entry_v, "w": entry_w, "x": entry_x
    }

    values = {key: entry.get() for key, entry in entry_values.items()}

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

    text_color = "white"
    if var_a.get():
        text_color = "orange"
    draw.text((margin + 5, y_pos), f"★白兵: {values['a']}", font=font, fill=text_color)
    y_pos += font.size + margin # 次の行へ

    text_color = "white"
    if var_b.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"運動: {values['b']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_c.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"頑健: {values['c']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_d.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"操縦: {values['d']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_e.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"知覚: {values['e']}", font=font, fill=text_color)
    y_pos += font.size + margin + 50

    # 技量グループ
    text_color = "white"
    draw.text((margin, y_pos), f"【技量】{values['v']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_f.get():
        text_color = "orange"
    draw.text((margin + 5, y_pos), f"★射撃: {values['f']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_g.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"医療: {values['g']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_h.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"隠密: {values['h']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_i.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"工作: {values['i']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_j.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"捜査: {values['j']}", font=font, fill=text_color)
    y_pos += font.size + margin + 50

    # 心魂グループ
    text_color = "white"
    draw.text((margin, y_pos), f"【心魂】{values['w']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_k.get():
        text_color = "orange"
    draw.text((margin + 5, y_pos), f"★呪法: {values['k']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_l.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"意志: {values['l']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_m.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"看破: {values['m']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_n.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"芸能: {values['n']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_o.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"伝承: {values['o']}", font=font, fill=text_color)
    y_pos += font.size + margin + 50

    # 社会グループ
    text_color = "white"
    draw.text((margin, y_pos), f"【社会】{values['x']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_p.get():
        text_color = "orange"
    draw.text((margin + 5, y_pos), f"★策謀: {values['p']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_q.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"教養: {values['q']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_r.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"交渉: {values['r']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_s.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"電脳: {values['s']}", font=font, fill=text_color)
    y_pos += font.size + margin

    text_color = "white"
    if var_t.get():
        text_color = "orange"
    draw.text((x_pos, y_pos), f"容姿: {values['t']}", font=font, fill=text_color)

    # ファイル名を取得
    filename = filename_entry.get()

    # 拡張子を追加
    filename = filename

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

# pyinstallerに格納
def resource_path(relative_path):
    """リソースパスを取得（PyInstallerで同梱時のパスを解決）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstallerで実行されている場合
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

Config.load_config()

# メインウィンドウの作成
root = tk.Tk()
root.title("ツクモツムギ-能力値/技能-画像出力 Ver3.0.0")
root.geometry("520x260+2000+650")
root.resizable(False, False)
icon_path = resource_path(Config.ICONPATH)
try:
    root.iconbitmap(icon_path)
except tk.TclError:
    print("アイコンファイルが見つからないため、デフォルトアイコンを使用") 


# ステータスバー用の文字列変換を実装
status_var = tk.StringVar()
status_var.set("キャラ分類、能力値、技能取得チェック、キャラ名を入力して画像作成してください")

# ステータスバー用のラベルを作成
status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor="w")
status_label.grid(row=8, column=0, columnspan=15, sticky="ew", pady=(5, 0))

def update_status(message, is_error=False):
    """ステータスバーの更新"""
    status_var.set(message)
    # if is_error:
    #     logging.error(message)
    # else:
    #     logging.info(message)

# 能力値をまとめるフレーム
ability_skill_frame = tk.Frame(root, width=520, height=285)
ability_skill_frame.grid(row=0, rowspan=7, column=0, columnspan=15, sticky="ew")

# 身体
label_u = tk.Label(ability_skill_frame, text="【身体】")
label_u.grid(row=0, column=0, columnspan=2, pady=(10, 0))
entry_u = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_u.grid(row=0, column=2, sticky="w", pady=(10, 0)) 
entry_u.bind("<KeyRelease>", update_entries)

# 技量
label_v = tk.Label(ability_skill_frame, text="【技量】")
label_v.grid(row=0, column=4, columnspan=2, pady=(10, 0))
entry_v = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_v.grid(row=0, column=6, sticky="w", pady=(10, 0)) 
entry_v.bind("<KeyRelease>", update_entries)

# 心魂
label_w = tk.Label(ability_skill_frame, text="【心魂】")
label_w.grid(row=0, column=8, columnspan=2, pady=(10, 0))
entry_w = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_w.grid(row=0, column=10, sticky="w", pady=(10, 0)) 
entry_w.bind("<KeyRelease>", update_entries)

# 社会
label_x = tk.Label(ability_skill_frame, text="【社会】")
label_x.grid(row=0, column=12, columnspan=2, pady=(10, 0))
entry_x = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_x.grid(row=0, column=14, sticky="w", pady=(10, 0)) 
entry_x.bind("<KeyRelease>", update_entries)

# 横線を追加
separator = ttk.Separator(ability_skill_frame, orient="horizontal")
separator.grid(row=1, column=0, columnspan=15, sticky="ew", padx=(5, 5), pady=(10, 0))

# 白兵
var_a = tk.BooleanVar()
check_button_a = Checkbutton(ability_skill_frame, text="★白兵：", variable=var_a, command=lambda: increment_value(var_a, entry_a, check_button_a))
check_button_a.grid(row=2, column=0, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_a = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_a.grid(row=2, column=2, pady=(5, 0))

# 運動
var_b = tk.BooleanVar()
check_button_b = Checkbutton(ability_skill_frame, text="　運動：", variable=var_b, command=lambda: increment_value(var_b, entry_b, check_button_b))
check_button_b.grid(row=3, column=0, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_b = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_b.grid(row=3, column=2, pady=(5, 0))

# 頑健
var_c = tk.BooleanVar()
check_button_c = Checkbutton(ability_skill_frame, text="　頑健：", variable=var_c, command=lambda: increment_value(var_c, entry_c, check_button_c))
check_button_c.grid(row=4, column=0, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_c = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_c.grid(row=4, column=2, pady=(5, 0))

# 操縦
var_d = tk.BooleanVar()
check_button_d = Checkbutton(ability_skill_frame, text="　操縦：", variable=var_d, command=lambda: increment_value(var_d, entry_d, check_button_d))
check_button_d.grid(row=5, column=0, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_d = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_d.grid(row=5, column=2, pady=(5, 0))

# 知覚
var_e = tk.BooleanVar()
check_button_e = Checkbutton(ability_skill_frame, text="　知覚：", variable=var_e, command=lambda: increment_value(var_e, entry_e, check_button_e))
check_button_e.grid(row=6, column=0, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_e = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_e.grid(row=6, column=2, pady=(5, 0))

# 線を追加
separator = ttk.Separator(ability_skill_frame, orient="vertical")
separator.grid(row=0, column=3, rowspan=7, sticky="ns", padx=(10, 5))

# 射撃
var_f = tk.BooleanVar()
check_button_f = Checkbutton(ability_skill_frame, text="★射撃：", variable=var_f, command=lambda: increment_value(var_f, entry_f, check_button_f))
check_button_f.grid(row=2, column=4, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_f = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_f.grid(row=2, column=6, pady=(5, 0))

# 医療
var_g = tk.BooleanVar()
check_button_g = Checkbutton(ability_skill_frame, text="　医療：", variable=var_g, command=lambda: increment_value(var_g, entry_g, check_button_g))
check_button_g.grid(row=3, column=4, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_g = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_g.grid(row=3, column=6, pady=(5, 0))

# 隠密
var_h = tk.BooleanVar()
check_button_h = Checkbutton(ability_skill_frame, text="　隠密：", variable=var_h, command=lambda: increment_value(var_h, entry_h, check_button_h))
check_button_h.grid(row=4, column=4, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_h = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_h.grid(row=4, column=6, pady=(5, 0))

# 工作
var_i = tk.BooleanVar()
check_button_i = Checkbutton(ability_skill_frame, text="　工作：", variable=var_i, command=lambda: increment_value(var_i, entry_i, check_button_i))
check_button_i.grid(row=5, column=4, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_i = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_i.grid(row=5, column=6, pady=(5, 0))

# 捜査
var_j = tk.BooleanVar()
check_button_j = Checkbutton(ability_skill_frame, text="　捜査：", variable=var_j, command=lambda: increment_value(var_j, entry_j, check_button_j))
check_button_j.grid(row=6, column=4, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_j = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_j.grid(row=6, column=6, pady=(5, 0))

# 線を追加
separator = ttk.Separator(ability_skill_frame, orient="vertical")
separator.grid(row=0, column=7, rowspan=7, sticky="ns", padx=(10, 5))

# 呪法
var_k = tk.BooleanVar()
check_button_k = Checkbutton(ability_skill_frame, text="★呪法：", variable=var_k, command=lambda: increment_value(var_k, entry_k, check_button_k))
check_button_k.grid(row=2, column=8, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_k = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_k.grid(row=2, column=10, pady=(5, 0))

# 意志
var_l = tk.BooleanVar()
check_button_l = Checkbutton(ability_skill_frame, text="　意志：", variable=var_l, command=lambda: increment_value(var_l, entry_l, check_button_l))
check_button_l.grid(row=3, column=8, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_l = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_l.grid(row=3, column=10, pady=(5, 0))

# 看破
var_m = tk.BooleanVar()
check_button_m = Checkbutton(ability_skill_frame, text="　看破：", variable=var_m, command=lambda: increment_value(var_m, entry_m, check_button_m))
check_button_m.grid(row=4, column=8, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_m = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_m.grid(row=4, column=10, pady=(5, 0))

# 芸能
var_n = tk.BooleanVar()
check_button_n = Checkbutton(ability_skill_frame, text="　芸能：", variable=var_n, command=lambda: increment_value(var_n, entry_n, check_button_n))
check_button_n.grid(row=5, column=8, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_n = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_n.grid(row=5, column=10, pady=(5, 0))

# 伝承
var_o = tk.BooleanVar()
check_button_o = Checkbutton(ability_skill_frame, text="　伝承：", variable=var_o, command=lambda: increment_value(var_o, entry_o, check_button_o))
check_button_o.grid(row=6, column=8, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_o = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_o.grid(row=6, column=10, pady=(5, 0))

# 線を追加
separator = ttk.Separator(ability_skill_frame, orient="vertical")
separator.grid(row=0, column=11, rowspan=7, sticky="ns", padx=(10, 5))

# 策謀
var_p = tk.BooleanVar()
check_button_p = Checkbutton(ability_skill_frame, text="★策謀：", variable=var_p, command=lambda: increment_value(var_p, entry_p, check_button_p))
check_button_p.grid(row=2, column=12, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_p = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_p.grid(row=2, column=14, padx=(0, 10), pady=(5, 0))

# 教養
var_q = tk.BooleanVar()
check_button_q = Checkbutton(ability_skill_frame, text="　教養：", variable=var_q, command=lambda: increment_value(var_q, entry_q, check_button_q))
check_button_q.grid(row=3, column=12, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_q = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_q.grid(row=3, column=14, padx=(0, 10), pady=(5, 0))

# 交渉
var_r = tk.BooleanVar()
check_button_r = Checkbutton(ability_skill_frame, text="　交渉：", variable=var_r, command=lambda: increment_value(var_r, entry_r, check_button_r))
check_button_r.grid(row=4, column=12, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_r = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_r.grid(row=4, column=14, padx=(0, 10), pady=(5, 0))

# 電脳
var_s = tk.BooleanVar()
check_button_s = Checkbutton(ability_skill_frame, text="　電脳：", variable=var_s, command=lambda: increment_value(var_s, entry_s, check_button_s))
check_button_s.grid(row=5, column=12, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_s = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_s.grid(row=5, column=14, padx=(0, 10), pady=(5, 0))

# 容姿
var_t = tk.BooleanVar()
check_button_t = Checkbutton(ability_skill_frame, text="　容姿：", variable=var_t, command=lambda: increment_value(var_t, entry_t, check_button_t))
check_button_t.grid(row=6, column=12, columnspan=2, sticky="e", pady=(5, 0), padx=(5, 0))
entry_t = tk.Entry(ability_skill_frame, validate="key", validatecommand=(root.register(validate_input), '%P'), width=5)
entry_t.grid(row=6, column=14, padx=(0, 10), pady=(5, 0))

# 出力関連パラメーターをまとめる
output_frame = tk.Frame(root)
output_frame.grid(row=7, column=0, columnspan=15, sticky="ew")

# 巫覡か付喪神か
charactor_type_var = tk.BooleanVar(value=False)
tk.Radiobutton(output_frame, text="巫覡", variable=charactor_type_var, value=False).grid(row=0, column=0, pady=(10, 5))
tk.Radiobutton(output_frame, text="付喪神", variable=charactor_type_var, value=True).grid(row=0, column=1, pady=(10, 5))

# ファイル名
label = tk.Label(output_frame, text="キャラ名:")
label.grid(row=0, column=2, pady=(10, 5), padx=(10, 0), sticky="e")
filename_entry = tk.Entry(output_frame, width=25)
filename_entry.grid(row=0, column=3, columnspan=5, padx=(0, 15), pady=(10, 5), sticky="w")

# 画像作成ボタン
button = tk.Button(output_frame, text="画像作成", command=create_image)
button.grid(row=0, column=13, padx=(0, 15), pady=(10, 5))

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

# リセットボタン
reset_button = tk.Button(output_frame, text="リセット", command=clear_all)
reset_button.grid(row=0, column=14, pady=(10, 5), padx=(0, 10), sticky="w")

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
        window_height = 430
        
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
        ttk.Button(icon_frame, text="アイコンファイル", command=icon_file).pack(anchor="e")

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
        
        # 保存ボタン
        def save_settings():
            Config.FONTPATH = font_path.get()
            Config.ICONPATH = icon_path.get()
            Config.SHEETPATH = sheet_path.get()
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


# メインループ
root.mainloop()
