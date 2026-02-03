import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import re
import io

st.set_page_config(layout="wide")

MAX_WIDTH_PX = 1200

st.markdown(
    f"""
    <style>
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
    </style>
    """,
    unsafe_allow_html=True
)

def resolve_font_path(app_font_path=None):
    """日本語表示を想定したフォントパスを解決する"""
    if app_font_path and os.path.exists(app_font_path):
        return app_font_path

    env_font = os.environ.get("FONT_PATH")
    if env_font and os.path.exists(env_font):
        return env_font

    windows_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    candidates = [
        os.path.join(windows_fonts, "YuGothM.ttc"),
        os.path.join(windows_fonts, "YuGothB.ttc"),
        os.path.join(windows_fonts, "meiryo.ttc"),
        os.path.join(windows_fonts, "meiryo.ttf"),
        os.path.join(windows_fonts, "msgothic.ttc"),
        os.path.join(windows_fonts, "MSMINCHO.TTC"),
        os.path.join(windows_fonts, "AdobeFangsongStd-Regular.otf"),
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/noto/NotoSansJP-Regular.otf",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    ]

    for path in candidates:
        if os.path.exists(path):
            return path
    return None


APP_FONT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "fonts",
    "WDXLLubrifontJPN-Regular.ttf"
)
FONT_PATH = resolve_font_path(APP_FONT_PATH)

def load_font(size):
    if FONT_PATH:
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except OSError:
            pass
    return ImageFont.load_default()

def validate_input(input_string):
    """
    入力が数字のみで構成されているかを確認する関数。
    数字のみの場合はTrueを返し、それ以外の場合はFalseを返す。
    """
    if re.match("^[0-9]*$", input_string):
        return True
    else:
        return False

def create_image(values, checks, filename, charactor_type, uploaded_file, swap_layout=False, bg_color_hex="#FFFFFF", bg_alpha=100, text_color_hex="#000000", learned_color_hex="#FFA500"):
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
    stats_area_width = 580    # 能力値情報の幅
    total_width = image_area_width + stats_area_width
    
    # 各セクションの高さ
    default_img_height = 440    # 画像がない場合の高さ
    char_info_height = 90       # 分類とキャラ名の高さ
    content_height = 500        # 能力値情報の高さ
    
    # アップロード画像の処理
    if uploaded_file:
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
    font_large = load_font(40)
    font_medium = load_font(35)
    font_small = load_font(28)
    font_tiny = load_font(20)
    
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

# Streamlitアプリ
st.title("ツクモツムギ-能力値画像出力-Webアプリ-βテスト版")

if not FONT_PATH:
    st.warning("日本語フォントが見つからないため、既定フォントで描画します。文字化けする場合はアプリ内のフォントファイルを配置するか、環境変数FONT_PATHで指定してください。")

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

    st.radio("キャラクター分類", ["巫覡", "付喪神"], key='charactor_type')
    st.text_input("キャラ名", key='filename')
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
    st.checkbox("画像と能力値を左右入れ替え画像生成(デフォルト：画像|能力値)", key="swap_layout")

with col_img:
    # 画像アップロード
    uploaded_file = st.file_uploader("使用するキャラ立ち絵※一時表示用のためネットワーク上には保存されません。\nまた、300x500以内の画像に限ります。", type=["png", "jpg", "jpeg"], help="PNG, JPG, JPEG形式の画像を選択してください (最大200MB)")
    st.session_state['uploaded_file'] = uploaded_file
    if uploaded_file is not None:
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

st.divider()

if st.button("画像作成"):
    # 最新の値を構築
    values_final = {}
    for group_key in 'uvwx':
        values_final[group_key] = st.session_state.get(group_key, '')
    
    # チェック状態を取得
    checks = {key: st.session_state.get(f'check_{key}', False) for key in 'abcdefghijklmnopqrst'}
    
    # 画像作成
    charactor_type = st.session_state['charactor_type'] == "付喪神"
    img_bytes, filename = create_image(
        values_final,
        checks,
        st.session_state['filename'],
        charactor_type,
        st.session_state.get('uploaded_file'),
        st.session_state.get('swap_layout', False),
        bg_color_hex,
        bg_alpha,
        text_color_hex,
        learned_color_hex
    )
    
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