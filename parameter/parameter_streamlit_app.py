import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import json
import re
import io

st.set_page_config(layout="wide")

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
                    cls.ICONSUBPATH = config.get('ICONSUBPATH', cls.DEFAULT_CONFIG['ICONSUBPATH'])
            else:
                cls.FONTPATH = cls.DEFAULT_CONFIG['FONTPATH']
                cls.ICONPATH = cls.DEFAULT_CONFIG['ICONPATH']
                cls.SHEETPATH = cls.DEFAULT_CONFIG['SHEETPATH']
                cls.ICONSUBPATH = cls.DEFAULT_CONFIG['ICONSUBPATH']
        except Exception as e:
            st.error(f"設定ファイルの読み込みに失敗しました: {e}")
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
            st.error(f"設定ファイルの保存に失敗しました: {e}")

def validate_input(input_string):
    """
    入力が数字のみで構成されているかを確認する関数。
    数字のみの場合はTrueを返し、それ以外の場合はFalseを返す。
    """
    if re.match("^[0-9]*$", input_string):
        return True
    else:
        return False

def create_image(values, checks, filename, charactor_type, uploaded_file):
    """
    入力された値とチェック状態から画像を生成する関数
    左側：アップロード画像、分類、キャラ名
    右側：能力値情報
    """
    # グループ定義
    groups = {
        'u': {
            'name': '身体',
            'skills': [('a', '★白兵'), ('b', '運動'), ('c', '頑健'), ('d', '操縦'), ('e', '知覚')]
        },
        'v': {
            'name': '技量',
            'skills': [('f', '★射撃'), ('g', '医療'), ('h', '隠密'), ('i', '工作'), ('j', '捜査')]
        },
        'w': {
            'name': '心魂',
            'skills': [('k', '★呪法'), ('l', '意志'), ('m', '看破'), ('n', '芸能'), ('o', '伝承')]
        },
        'x': {
            'name': '社会',
            'skills': [('p', '★策謀'), ('q', '教養'), ('r', '交渉'), ('s', '電脳'), ('t', '容姿')]
        }
    }
    
    # 全体の寸法設定
    left_width = 310    # 左側（アップロード画像 + キャラ情報）
    right_width = 600   # 右側（能力値情報）
    total_width = left_width + right_width
    
    # 各セクションの高さ
    img_target_height = 430      # 画像の高さ
    char_info_height = 90        # 分類とキャラ名の高さ
    content_height = 520         # 能力値情報の高さ
    
    # 左側全体の高さ
    left_total_height = img_target_height + char_info_height
    
    # 全体の高さ = 左右で大きい方
    total_img_height = max(left_total_height, content_height)
    
    # アップロード画像の処理
    if uploaded_file:
        uploaded_img = Image.open(uploaded_file)
        # アスペクト比を保持して、高さを430pxに合わせる
        aspect_ratio = uploaded_img.width / uploaded_img.height
        target_width = int(img_target_height * aspect_ratio)
        
        # 幅が左側の幅を超える場合は制限
        if target_width > left_width:
            target_width = left_width
        
        uploaded_img = uploaded_img.resize((target_width, img_target_height), Image.Resampling.LANCZOS)
    else:
        uploaded_img = None
    
    # 全体の画像を作成
    img = Image.new('RGBA', (total_width, total_img_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # フォント設定
    try:
        font_large = ImageFont.truetype(Config.FONTPATH, 40)
        font_medium = ImageFont.truetype(Config.FONTPATH, 35)
        font_small = ImageFont.truetype(Config.FONTPATH, 28)
        font_tiny = ImageFont.truetype(Config.FONTPATH, 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # 左側にアップロード画像を配置（中央揃え）
    if uploaded_img:
        left_x = (left_width - uploaded_img.width) // 2
        img.paste(uploaded_img, (left_x, 0))
    
    # 左側の下部にキャラクター情報を表示
    info_y = img_target_height + 10
    
    # キャラクター分類を表示
    charactor_type_str = "巫覡" if not charactor_type else "付喪神"
    draw.text((20, info_y), f"{charactor_type_str}", font=font_small, fill="black")
    
    # キャラ名を表示
    char_name = filename if filename else "No Name"
    char_name_text = f"{char_name}"
    
    # テキスト幅をチェック
    text_bbox = draw.textbbox((0, 0), char_name_text, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]
    
    # 利用可能な幅（左側のスペース）
    available_width = left_width - 40
    
    if text_width > available_width:
        # フォントサイズを縮小
        draw.text((20, info_y + 40), char_name_text, font=font_tiny, fill="black")
    else:
        draw.text((20, info_y + 40), char_name_text, font=font_small, fill="black")
    
    # 右側に能力値情報を描画
    y_pos = 30
    line_height = 60
    right_start_x = left_width + 20
    
    for group_key in ['u', 'v', 'w', 'x']:
        group_data = groups[group_key]
        # グループタイトル: 【身体】：数値
        group_value = values.get(group_key, '')
        group_title = f"【{group_data['name']}】：{group_value}"
        draw.text((right_start_x, y_pos), group_title, font=font_large, fill="black")
        y_pos += line_height
        
        # スキル一覧を1行で表示
        x_offset = right_start_x
        for skill_key, skill_name in group_data['skills']:
            is_checked = checks.get(skill_key, False)
            text_color = (255, 165, 0) if is_checked else (0, 0, 0)  # オレンジまたは黒
            
            draw.text((x_offset, y_pos), skill_name, font=font_medium, fill=text_color)
            # 次のスキル位置を計算
            text_bbox = draw.textbbox((0, 0), skill_name, font=font_medium)
            text_width = text_bbox[2] - text_bbox[0]
            x_offset += text_width + 40
        
        y_pos += line_height
    
    # ファイル名がない場合はデフォルト
    if not filename:
        filename = "output"
    
    # メモリ上に画像を保存（BytesIO）
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes, filename

# Streamlitアプリ
st.title("ツクモツムギ-能力値/技能-画像出力 Ver3.0.0")

Config.load_config()

# セッションステートの初期化
st.session_state.setdefault('values', {key: '' for key in 'abcdefghijklmnopqrstuvwx'})
st.session_state.setdefault('checks', {key: False for key in 'abcdefghijklmnopqrst'})
st.session_state.setdefault('filename', '')
st.session_state.setdefault('charactor_type', "巫覡")  # 初期値: 巫覡

def get_skill_value(key):
    group_key = {'a':'u', 'b':'u', 'c':'u', 'd':'u', 'e':'u',
                 'f':'v', 'g':'v', 'h':'v', 'i':'v', 'j':'v',
                 'k':'w', 'l':'w', 'm':'w', 'n':'w', 'o':'w',
                 'p':'x', 'q':'x', 'r':'x', 's':'x', 't':'x'}[key]
    base = int(st.session_state.get(group_key, 0) or 0)
    if st.session_state.get(f'check_{key}', False):
        return str(base + 1)
    else:
        return str(base)

# サイドバーで設定
with st.sidebar:
    st.header("設定")
    font_path = st.text_input("フォントパス", Config.FONTPATH)
    icon_path = st.text_input("アイコンパス", Config.ICONPATH)
    sheet_path = st.text_input("シートパス", Config.SHEETPATH)
    if st.button("設定保存"):
        Config.FONTPATH = font_path
        Config.ICONPATH = icon_path
        Config.SHEETPATH = sheet_path
        Config.save_config()
        st.success("設定を保存しました")

# メインコンテンツ
col_img, col1, col2, col3, col4 = st.columns([1.2, 0.9, 0.9, 0.9, 0.9])

with col_img:
    # 画像アップロード
    uploaded_file = st.file_uploader("キャラ立ち絵※一時表示用のため保存されません。　また、300x500以内の画像に限ります。", type=["png", "jpg", "jpeg"], help="PNG, JPG, JPEG形式の画像を選択してください (最大200MB)")
    st.session_state['uploaded_file'] = uploaded_file
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # 高さ上限を500pxとし、幅をアスペクト比で調整
        max_height = 500
        if image.height > max_height:
            aspect_ratio = image.width / image.height
            new_width = int(max_height * aspect_ratio)
            image = image.resize((new_width, max_height))
        st.image(image, caption="アップロードされた画像")

with col1:
    st.subheader("【身体】")
    st.text_input("身体", key='u')
    st.checkbox("★白兵", key='check_a')
    st.text_input("白兵", value=get_skill_value('a'), disabled=True)
    st.checkbox("運動", key='check_b')
    st.text_input("運動", value=get_skill_value('b'), disabled=True)
    st.checkbox("頑健", key='check_c')
    st.text_input("頑健", value=get_skill_value('c'), disabled=True)
    st.checkbox("操縦", key='check_d')
    st.text_input("操縦", value=get_skill_value('d'), disabled=True)
    st.checkbox("知覚", key='check_e')
    st.text_input("知覚", value=get_skill_value('e'), disabled=True)

with col2:
    st.subheader("【技量】")
    st.text_input("技量", key='v')
    st.checkbox("★射撃", key='check_f')
    st.text_input("射撃", value=get_skill_value('f'), disabled=True)
    st.checkbox("医療", key='check_g')
    st.text_input("医療", value=get_skill_value('g'), disabled=True)
    st.checkbox("隠密", key='check_h')
    st.text_input("隠密", value=get_skill_value('h'), disabled=True)
    st.checkbox("工作", key='check_i')
    st.text_input("工作", value=get_skill_value('i'), disabled=True)
    st.checkbox("捜査", key='check_j')
    st.text_input("捜査", value=get_skill_value('j'), disabled=True)

with col3:
    st.subheader("【心魂】")
    st.text_input("心魂", key='w')
    st.checkbox("★呪法", key='check_k')
    st.text_input("呪法", value=get_skill_value('k'), disabled=True)
    st.checkbox("意志", key='check_l')
    st.text_input("意志", value=get_skill_value('l'), disabled=True)
    st.checkbox("看破", key='check_m')
    st.text_input("看破", value=get_skill_value('m'), disabled=True)
    st.checkbox("芸能", key='check_n')
    st.text_input("芸能", value=get_skill_value('n'), disabled=True)
    st.checkbox("伝承", key='check_o')
    st.text_input("伝承", value=get_skill_value('o'), disabled=True)

with col4:
    st.subheader("【社会】")
    st.text_input("社会", key='x')
    st.checkbox("★策謀", key='check_p')
    st.text_input("策謀", value=get_skill_value('p'), disabled=True)
    st.checkbox("教養", key='check_q')
    st.text_input("教養", value=get_skill_value('q'), disabled=True)
    st.checkbox("交渉", key='check_r')
    st.text_input("交渉", value=get_skill_value('r'), disabled=True)
    st.checkbox("電脳", key='check_s')
    st.text_input("電脳", value=get_skill_value('s'), disabled=True)
    st.checkbox("容姿", key='check_t')
    st.text_input("容姿", value=get_skill_value('t'), disabled=True)

st.radio("キャラクター分類", ["巫覡", "付喪神"], key='charactor_type')
st.text_input("キャラ名", key='filename')

if st.button("画像作成"):
    # 最新の値を構築
    values_final = {}
    for group_key in 'uvwx':
        values_final[group_key] = st.session_state.get(group_key, '')
    
    # チェック状態を取得
    checks = {key: st.session_state.get(f'check_{key}', False) for key in 'abcdefghijklmnopqrst'}
    
    # 画像作成
    charactor_type = st.session_state['charactor_type'] == "付喪神"
    img_bytes, filename = create_image(values_final, checks, st.session_state['filename'], charactor_type, st.session_state.get('uploaded_file'))
    
    # 画像を表示
    img_bytes.seek(0)
    st.image(img_bytes, caption="生成された画像")
    
    # ダウンロードボタンを表示
    img_bytes.seek(0)
    st.download_button(
        label="📥 画像をダウンロード",
        data=img_bytes,
        file_name=f"{filename}.png",
        mime="image/png"
    )
    st.success("✅ 画像を生成しました。ダウンロードボタンから保存してください。")