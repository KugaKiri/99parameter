import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import re
import io
import base64
import hashlib
from functools import lru_cache
from pathlib import Path

st.set_page_config(layout="wide")

MAX_WIDTH_PX = 1200

standard_fonts = ["Noto Sans JP"]
all_fonts = standard_fonts

st.markdown(
    f"""
    <style>
    @font-face {{
        font-family: 'Noto Sans JP';
        src: url('assets/fonts/NotoSansJP-Regular.ttf');
    }}

    /* 全体を囲むラッパーの最大幅を固定し、中央寄せする */
    .main-tool-wrapper {{
        max-width: {MAX_WIDTH_PX}px;
        margin: 0 auto; /* 画面の中央に配置 */
    }}

    /* プレビュー表示用の共通スタイル */
    .preview-container {{
        border: 1px solid #ddd;
        padding: 5px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 60px;
        display: flex;
        align-items: center;
        text-align: left;
    }}

    /* 以下、既存の微調整CSS */
    .block-container {{
        max-width: {MAX_WIDTH_PX}px;
        padding-top: 1.5rem;
    }}
    .skill-row-label {{
        display: flex;
        align-items: center;
        height: 2.4rem;
        line-height: 1.2;
    }}
    .group-header {{
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 0.1rem 0 0.3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 2.2rem;
    }}
    /* 背景色/文字色/習得済色/透過率の行だけギャップを縮小 */
    .color-controls + div[data-testid="stHorizontalBlock"] {{
        gap: 0.2rem !important;
        column-gap: 0.2rem !important;
    }}
    .font-preview-container {{
        border: none;
        padding: 5px;
        border-radius: 10px;
        background-color: transparent;
        box-shadow: none;
        height: 60px;
        display: flex;
        align-items: center;
        text-align: left;
        margin-bottom: 0.8rem;
    }}

    .font-preview-container p {{
        margin: 0 !important;
        padding: 0 10px !important;
        width: 100%;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

ASSETS_FONTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "fonts"
)
APP_FONT_PATH = os.path.join(ASSETS_FONTS_DIR, "NotoSansJP-Regular.ttf")
FONT_PATH = APP_FONT_PATH if os.path.exists(APP_FONT_PATH) else None
FONT_SIZE_OVERRIDES = {
    "DelaGothicOne-Regular": 20,
    "DotGothic16-Regular": 23,
    "HachiMaruPop-Regular": 22,
    "KaiseiTokumin-Regular": 24,
    "KosugiMaru-Regular": 23,
    "MPLUSRounded1c-Regular": 23,
    "NotoSansJP-Regular": 26,
    "NotoSerifJP-Regular": 26,
    "ReggaeOne-Regular": 21,
    "WDXLLubrifontJPN-Regular": 30,
    "YujiMai-Regular": 22,
    "ZenKurenaido-Regular": 26,
    "ZenMaruGothic-Regular": 26,
}
SAMPLE_TEXT_FOR_MEASURE = "あいうえおアイウエオ漢字"
TARGET_FONT_SIZES = [40, 35, 28, 20]

def list_local_fonts(fonts_dir):
    fonts = {}
    fonts_path = Path(fonts_dir)

    if not fonts_path.is_dir():
        return fonts
    
    for font_file in fonts_path.iterdir():
        if font_file.suffix.lower() in {".ttf", ".otf", ".ttc"}:
            display_name = font_file.stem
            fonts[display_name] = str(font_file)

    return dict(sorted(fonts.items(), key=lambda item: item[0].lower()))

LOCAL_FONTS = list_local_fonts(ASSETS_FONTS_DIR)

def load_font(font_path, size):
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            pass
    if FONT_PATH:
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except OSError:
            pass
    return ImageFont.load_default()

def load_specific_font(font_path, size):
    if not font_path or not os.path.exists(font_path):
        return None
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        return None

@lru_cache(maxsize=256)
def get_font_height(font_path, size):
    font = load_specific_font(font_path, size)
    if font is None and FONT_PATH and font_path != FONT_PATH:
        font = load_specific_font(FONT_PATH, size)
    if font is None:
        font = ImageFont.load_default()
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), SAMPLE_TEXT_FOR_MEASURE, font=font)
    height = bbox[3] - bbox[1]
    return max(1, height)

REFERENCE_HEIGHTS = {size: get_font_height(FONT_PATH, size) for size in TARGET_FONT_SIZES}

def compute_normalized_size(font_path, base_size, target_height):
    current_height = get_font_height(font_path, base_size)
    if not current_height:
        return base_size
    scale = target_height / current_height
    return max(1, int(round(base_size * scale)))

def load_normalized_font(font_path, base_size, target_height, font_scale=1.0):
    normalized_size = compute_normalized_size(font_path, base_size, target_height)
    normalized_size = max(1, int(round(normalized_size * font_scale)))
    return load_font(font_path, normalized_size)

def build_font_face_css(font_path, font_family):
    if not font_path or not os.path.exists(font_path):
        return ""
    ext = os.path.splitext(font_path)[1].lower()
    if ext not in {".ttf", ".otf"}:
        return ""
    try:
        with open(font_path, "rb") as font_file:
            font_data = base64.b64encode(font_file.read()).decode("utf-8")
        mime = "font/ttf" if ext == ".ttf" else "font/otf"
        format_name = "truetype" if ext == ".ttf" else "opentype"
        return f"""
        @font-face {{
            font-family: '{font_family}';
            src: url(data:{mime};base64,{font_data}) format('{format_name}');
            font-weight: normal;
            font-style: normal;
        }}
        """
    except OSError:
        return ""

def hex_to_rgba_css(hex_color, alpha_percent):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return "rgba(255,255,255,1)"
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    alpha = max(0, min(100, int(alpha_percent))) / 100
    return f"rgba({r}, {g}, {b}, {alpha})"

def validate_input(input_string):
    """
    入力が数字のみで構成されているかを確認する関数。
    数字のみの場合はTrueを返し、それ以外の場合はFalseを返す。
    """
    if re.match("^[0-9]*$", input_string):
        return True
    else:
        return False

def hash_uploaded_file(uploaded_file):
    """
    アップロードされたファイルのハッシュ値を計算する関数
    キャッシュのキーとして使用
    """
    if uploaded_file is None:
        return None
    uploaded_file.seek(0)
    file_hash = hashlib.md5(uploaded_file.read()).hexdigest()
    uploaded_file.seek(0)  # ハッシュ計算後にシークを戻す
    return file_hash

def create_image(values, checks, filename, charactor_type, uploaded_file, font_path=None, font_scale=1.0, swap_layout=False, bg_color_hex="#FFFFFF", bg_alpha=100, text_color_hex="#000000", learned_color_hex="#FFA500"):
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
    
    # 生成する画像の寸法設定
    image_area_width = 320    # 画像 + キャラ情報の幅
    stats_area_width = 690    # 能力値情報の幅
    total_width = image_area_width + stats_area_width
    
    # 各セクションの高さ
    default_img_height = 440    # 画像がない場合の高さ
    char_info_height = 90       # 分類とキャラ名の高さ
    content_height = 500        # 能力値情報の高さ
    
    # アップロード画像の処理
    if uploaded_file:
        uploaded_file.seek(0)
        uploaded_img = Image.open(uploaded_file)
        # アスペクト比を保持して、幅300px基準でリサイズ（高さ上限415px）
        aspect_ratio = uploaded_img.width / uploaded_img.height
        target_width = image_area_width
        target_height = int(target_width / aspect_ratio)
        max_height = 390
        if target_height > max_height:
            target_height = max_height
            target_width = int(target_height * aspect_ratio)
        uploaded_img = uploaded_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        img_target_height = target_height
    else:
        uploaded_img = None
        img_target_height = default_img_height
    
    # 左側全体の高さ
    left_total_height = img_target_height + char_info_height

    # 全体の高さ = 左右で大きい方
    total_img_height = max(left_total_height, content_height)

    def hex_to_rgba(hex_color, alpha_percent):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = max(0, min(255, int(alpha_percent * 255 / 100)))
        return (r, g, b, a)

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)

    bg_rgba = hex_to_rgba(bg_color_hex, bg_alpha)
    text_rgb = hex_to_rgb(text_color_hex)
    learned_rgb = hex_to_rgb(learned_color_hex)

    # 全体の画像を作成
    img = Image.new('RGBA', (total_width, total_img_height), bg_rgba)
    draw = ImageDraw.Draw(img)

    # フォント設定
    font_large = load_normalized_font(font_path, 40, REFERENCE_HEIGHTS[40], font_scale)
    font_medium = load_normalized_font(font_path, 35, REFERENCE_HEIGHTS[35], font_scale)
    font_small = load_normalized_font(font_path, 28, REFERENCE_HEIGHTS[28], font_scale)
    font_tiny = load_normalized_font(font_path, 20, REFERENCE_HEIGHTS[20], font_scale)
    
    # 左右の配置を決定
    if swap_layout:
        stats_area_x = 0
        image_area_x = stats_area_width
    else:
        image_area_x = 0
        stats_area_x = image_area_width

    # ここでは折り返し計算は行わない

    # 画像エリアにアップロード画像を配置（中央揃え）
    image_area_height = total_img_height - char_info_height
    if uploaded_img:
        # 透過PNGは背景色で合成して透過を防ぐ
        uploaded_img = uploaded_img.convert("RGBA")
        bg_layer = Image.new("RGBA", uploaded_img.size, bg_rgba)
        uploaded_img = Image.alpha_composite(bg_layer, uploaded_img)

        left_x = image_area_x + (image_area_width - uploaded_img.width) // 2
        top_y = max(0, (image_area_height - uploaded_img.height) // 2)
        img.paste(uploaded_img, (left_x, top_y))
    
    # 左側の下部にキャラクター情報を表示
    info_y = image_area_height + 10

    # キャラクター分類を表示
    charactor_type_str = "巫覡" if not charactor_type else "付喪神"
    draw.text((image_area_x + 10, info_y), f"{charactor_type_str}", font=font_small, fill=text_rgb)

    # キャラ名を表示
    char_name = filename if filename else "No Name"
    char_name_text = f"{char_name}"

    # テキスト幅をチェック
    text_bbox = draw.textbbox((0, 0), char_name_text, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]

    # 利用可能な幅（左側のスペース）
    available_width = image_area_width - 40

    if text_width > available_width:
        # フォントサイズを縮小
        draw.text((image_area_x + 15, info_y + 40), char_name_text, font=font_tiny, fill=text_rgb)
    else:
        draw.text((image_area_x + 15, info_y + 40), char_name_text, font=font_small, fill=text_rgb)
    
    # 右側に能力値情報を描画
    y_pos = 20
    line_height = 60
    right_start_x = stats_area_x + 20
    
    for group_key in ['u', 'v', 'w', 'x']:
        group_data = groups[group_key]
        # グループタイトル: 【身体】：数値
        group_value = values.get(group_key, '')
        group_title = f"【{group_data['name']}】：{group_value}"
        draw.text((right_start_x, y_pos), group_title, font=font_large, fill=text_rgb)
        y_pos += line_height
        
        # スキル一覧を1行で表示（各スキルの数値を含む）
        x_offset = right_start_x
        for skill_key, skill_name in group_data['skills']:
            is_checked = checks.get(skill_key, False)
            text_color = learned_rgb if is_checked else text_rgb  # 習得済色または指定色
            
            # 各スキルの数値を計算（グループ値+チェック時+1）
            base_value = int(group_value) if group_value else 0
            skill_value = base_value + 1 if is_checked else base_value
            skill_text = f"{skill_name}:{skill_value}"
            
            draw.text((x_offset, y_pos), skill_text, font=font_medium, fill=text_color)
            # 次のスキル位置を計算
            text_bbox = draw.textbbox((0, 0), skill_text, font=font_medium)
            text_width = text_bbox[2] - text_bbox[0]
            x_offset += text_width + 20
        
        y_pos += line_height
    
    # ファイル名がない場合はデフォルト
    if not filename:
        filename = "output"
    
    # メモリ上に画像を保存（BytesIO）
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes, filename

@st.cache_data(show_spinner="🎨 画像を生成中...")
def create_image_cached(
    _values_tuple,
    _checks_tuple,
    filename,
    charactor_type,
    _uploaded_file_hash,
    font_path,
    font_scale,
    swap_layout,
    bg_color_hex,
    bg_alpha,
    text_color_hex,
    learned_color_hex
):
    """
    キャッシュ対応版の画像生成関数
    辞書をタプルに変換して、キャッシュ可能な形式にする
    """
    # タプルを辞書に戻す
    values = dict(_values_tuple)
    checks = dict(_checks_tuple)
    
    # 元のcreate_image()を呼び出し
    return create_image(
        values, checks, filename, charactor_type,
        st.session_state.get('uploaded_file'),
        font_path, font_scale, swap_layout,
        bg_color_hex, bg_alpha, text_color_hex, learned_color_hex
    )

# Streamlitアプリ
st.title("ツクモツムギ-能力値画像出力-WebAppβテスト版 [⚡キャッシュ版]")

if not FONT_PATH:
    st.warning("日本語フォントが見つからないため、既定フォントで描画します。文字化けする場合はアプリ内のフォントファイルを配置するか、環境変数FONT_PATHで指定してください。")

# サイドバーの情報
with st.sidebar:
    st.markdown("""
    ### ℹ️ 使い方
    1. キャラクターの能力値を入力
    2. 取得している技能にチェックを入れる
    3. キャラクター分類とキャラクター名を入力する
    4. 画像をアップロード（任意）
    5. 使用するフォント、背景色、文字色、ハイライト、透過率を設定する
    6. プレビューを確認
    7. ダウンロードボタンで保存
    
    ### 🔒 プライバシー
    - アップロードされた画像はサーバーに保存されません
    - すべての処理はメモリ上で完了します
    - 個人情報は一切収集しません
    - このアプリはオープンソースであり、コードはGitHubで公開されています
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚡ パフォーマンス")
    if st.button("🗑️ キャッシュをクリア", help="画像生成のキャッシュをクリアします"):
        st.cache_data.clear()
        st.success("キャッシュをクリアしました！")
        st.rerun()
    
    st.markdown("""
    ### ℹ️ キャッシュについて
    - 同じ設定で画像を生成する場合、キャッシュから高速表示されます
    - 設定を変更すると新しく生成されます
    - メモリ使用量が増える場合は、キャッシュをクリアしてください
    """)
    
    st.markdown("---")
    
    # 以下はお好みでコメントを外して使用してください
    # st.markdown("""
    # ### 📖 ツクモツムギとは
    # ツクモツムギは、現代日本を舞台にしたTRPGです。
    # プレイヤーは巫覡（フゲキ）や付喪神（ツクモガミ）となり、
    # 怪異に立ち向かう物語を紡ぎます。
    # """)
    
    # st.markdown("""
    # ### 🔗 リンク
    # - [GitHub リポジトリ](https://github.com/KugaKiri/Streamlit)
    # - [ツクモツムギ 公式サイト](https://example.com)
    # - [お問い合わせ](mailto:your-email@example.com)
    # """)

# セッションステートの初期化
st.session_state.setdefault('values', {key: '' for key in 'abcdefghijklmnopqrstuvwx'})
st.session_state.setdefault('checks', {key: False for key in 'abcdefghijklmnopqrst'})
st.session_state.setdefault('filename', '')
st.session_state.setdefault('charactor_type', "巫覡")  # 初期値: 巫覡
st.session_state.setdefault('font_css_sizes', {})
font_options = list(LOCAL_FONTS.keys())
if not font_options:
    font_options = ["既定フォント"]
default_font_name = "NotoSansJP-Regular" if "NotoSansJP-Regular" in font_options else font_options[0]
st.session_state.setdefault('font_name', default_font_name)

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

def render_skill_row(label, check_key, value_key):
    col_check, col_label, col_value = st.columns([0.5, 1.4, 1.1])
    with col_check:
        st.checkbox(label, key=check_key, label_visibility="collapsed")
    with col_label:
        st.markdown(f"<div class='skill-row-label'>{label}</div>", unsafe_allow_html=True)
    with col_value:
        st.text_input(label, value=get_skill_value(value_key), disabled=True, label_visibility="collapsed")

def render_group_header(title, value_key):
    col_title, col_value = st.columns([1.0, 0.8])
    with col_title:
        st.markdown(f"<div class='group-header'>{title}</div>", unsafe_allow_html=True)
    with col_value:
        st.text_input(title, key=value_key, label_visibility="collapsed")

# メインコンテンツ
col_stats, col_img = st.columns([1.2, 0.9])

with col_stats:
    col1, col2, col3, col4 = st.columns([0.4, 0.4, 0.4, 0.4])

    with col1:
        render_group_header("身体", "u")
        render_skill_row("★白兵", "check_a", "a")
        render_skill_row("運動", "check_b", "b")
        render_skill_row("頑健", "check_c", "c")
        render_skill_row("操縦", "check_d", "d")
        render_skill_row("知覚", "check_e", "e")

    with col2:
        render_group_header("技量", "v")
        render_skill_row("★射撃", "check_f", "f")
        render_skill_row("医療", "check_g", "g")
        render_skill_row("隠密", "check_h", "h")
        render_skill_row("工作", "check_i", "i")
        render_skill_row("捜査", "check_j", "j")

    with col3:
        render_group_header("心魂", "w")
        render_skill_row("★呪法", "check_k", "k")
        render_skill_row("意志", "check_l", "l")
        render_skill_row("看破", "check_m", "m")
        render_skill_row("芸能", "check_n", "n")
        render_skill_row("伝承", "check_o", "o")

    with col4:
        render_group_header("社会", "x")
        render_skill_row("★策謀", "check_p", "p")
        render_skill_row("教養", "check_q", "q")
        render_skill_row("交渉", "check_r", "r")
        render_skill_row("電脳", "check_s", "s")
        render_skill_row("容姿", "check_t", "t")

    
    col_char_type, col_char_name = st.columns([0.3, 0.7], gap="small")
    with col_char_type:
        st.radio("キャラクター分類", ["巫覡", "付喪神"], key="charactor_type", horizontal=True)
    with col_char_name:
        st.text_input("キャラ名", key="filename")
    st.markdown("<div class='color-controls'></div>", unsafe_allow_html=True)
    col_bg_color, col_text_color, col_learned_color, col_bg_alpha = st.columns([0.45, 0.45, 0.55, 1.1], gap="small")
    with col_bg_color:
        bg_color_hex = st.color_picker("背景色", value="#FFFFFF")
    with col_text_color:
        text_color_hex = st.color_picker("文字色", value="#000000")
    with col_learned_color:
        learned_color_hex = st.color_picker("習得済色", value="#FFA500")
    with col_bg_alpha:
        bg_alpha = st.slider("背景透過率(0=完全透明, 100=不透明)", min_value=0, max_value=100, value=100, step=5)

    col_font_select, col_font_preview = st.columns([0.40, 0.6], gap="small")
    with col_font_select:
        selected_font_name = st.selectbox("フォント", font_options, key="font_name")
        selected_font_path = LOCAL_FONTS.get(selected_font_name)
        st.session_state['font_path'] = selected_font_path

    with col_font_preview:
        selected_font_name = st.session_state.get('font_name', font_options[0])
        selected_font_path = st.session_state.get('font_path') or LOCAL_FONTS.get(selected_font_name)
        preview_font_family = f"preview-{selected_font_name}"
        font_face_css = build_font_face_css(selected_font_path, preview_font_family)
        if font_face_css:
            st.markdown(f"<style>{font_face_css}</style>", unsafe_allow_html=True)
        else:
            preview_font_family = selected_font_name

        preview_text = "巫覡と付喪神"
        preview_html = preview_text.replace("付喪", f"<span style='color:{learned_color_hex};'>付喪</span>")
        preview_bg_rgba = hex_to_rgba_css(bg_color_hex, bg_alpha)
        preview_font_size = st.session_state.get('font_css_sizes', {}).get(
            selected_font_name,
            FONT_SIZE_OVERRIDES.get(selected_font_name, 28)
        )
        st.markdown(
            f"""
            <div class="font-preview-container" style="background-color: {preview_bg_rgba};">
                <p style="font-family: '{preview_font_family}', sans-serif; font-size: {preview_font_size}px; color: {text_color_hex};">
                    {preview_html}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with col_img:
    # 画像アップロード
    uploaded_file = st.file_uploader("使用するキャラ立ち絵※一時表示用のためネットワーク上には保存されません。\nまた、300x500以内の10MB以下の画像に限ります。", type=["png", "jpg", "jpeg"], help="PNG, JPG, JPEG形式の画像を選択してください (推奨: 5MB以下)")
    
    # ファイルサイズチェック
    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > 10:
            st.error(f"⚠️ ファイルサイズが大きすぎます（{file_size_mb:.1f}MB）。10MB以下の画像をアップロードしてください。")
            uploaded_file = None
            st.session_state['uploaded_file'] = None
        else:
            st.session_state['uploaded_file'] = uploaded_file
    else:
        st.session_state['uploaded_file'] = uploaded_file
    
    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            # 幅300px基準でアスペクト比を保持（高さ上限415px）
            target_width = 300
            aspect_ratio = image.width / image.height
            new_height = int(target_width / aspect_ratio)
            max_height = 415
            if new_height > max_height:
                new_height = max_height
                target_width = int(new_height * aspect_ratio)
            image = image.resize((target_width, new_height))
            st.image(image, caption="アップロードされた画像")
        except Exception as e:
            st.error(f"❌ 画像の読み込みに失敗しました: {str(e)}")
            st.session_state['uploaded_file'] = None


    # プレビュー（キャッシュ版で画像を生成）
    preview_values = {group_key: st.session_state.get(group_key, '') for group_key in 'uvwx'}
    preview_checks = {key: st.session_state.get(f'check_{key}', False) for key in 'abcdefghijklmnopqrst'}
    preview_charactor_type = st.session_state.get('charactor_type') == "付喪神"
    preview_font_name = st.session_state.get('font_name', font_options[0])
    preview_font_scale = st.session_state.get('font_css_sizes', {}).get(
        preview_font_name,
        FONT_SIZE_OVERRIDES.get(preview_font_name, 28)
    ) / 28
    
    # アップロードファイルのハッシュを計算
    uploaded_file_hash = hash_uploaded_file(st.session_state.get('uploaded_file'))
    
    try:
        # キャッシュ対応関数を呼び出し
        preview_img_bytes, _ = create_image_cached(
            tuple(preview_values.items()),  # 辞書 → タプル
            tuple(preview_checks.items()),  # 辞書 → タプル
            st.session_state.get('filename', ''),
            preview_charactor_type,
            uploaded_file_hash,  # ファイルのハッシュ値
            st.session_state.get('font_path'),
            preview_font_scale,
            st.session_state.get('swap_layout', False),
            bg_color_hex,
            bg_alpha,
            text_color_hex,
            learned_color_hex
        )
        preview_img_bytes.seek(0)
        st.image(preview_img_bytes, caption="プレビュー ⚡")
    except Exception as e:
        st.error(f"❌ プレビュー生成に失敗しました: {str(e)}")
        preview_img_bytes = None

st.checkbox("画像と能力値を左右入れ替え画像生成(デフォルト：画像|能力値)", key="swap_layout")


# ダウンロードボタンを常に表示（50%縮小版）
if preview_img_bytes:
    preview_img_bytes.seek(0)
    download_filename = st.session_state.get('filename', '').strip()
    if not download_filename:
        download_filename = "chara"

    try:
        # ダウンロード用に50%縮小した画像を作成
        preview_img_bytes.seek(0)
        preview_image = Image.open(preview_img_bytes)
        original_width, original_height = preview_image.size
        new_width = int(original_width * 0.5)
        new_height = int(original_height * 0.5)
        resized_image = preview_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # BytesIOに保存
        download_img_bytes = io.BytesIO()
        resized_image.save(download_img_bytes, format='PNG')
        download_img_bytes.seek(0)

        st.download_button(
            label="📥 画像をダウンロード",
            data=download_img_bytes,
            file_name=f"{download_filename}.png",
            mime="image/png"
        )
    except Exception as e:
        st.error(f"❌ ダウンロード用画像の生成に失敗しました: {str(e)}")
else:
    st.info("プレビュー画像を生成してからダウンロードできます。")



# フッター
st.markdown("---")
st.caption("本サイトは「倉樫 澄人、N.G.P.、新紀元社」が権利を有する「[怪異捜査RPG ツクモツムギ](https://r-r.arclight.co.jp/rpg/怪異捜査rpgツクモツムギ/)」の二次創作物です。")
st.caption("プログラミング言語：Python3.13.9｜[GitHub](https://github.com/KugaKiri/Streamlit)｜使用フォント: Google Fonts (OFL)")
# フッターのカスタマイズ例（コメントアウト）:
st.caption("制作者：くがみ | ツクモツムギ-能力値画像ジェネレーター")
