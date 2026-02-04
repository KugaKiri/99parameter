import streamlit as st
import os

# --- 設定 ---
FIXED_WIDTH_PX = 600 # ★ここを変更して全体の幅を調整★

GOOGLE_FONTS_URL = "https://fonts.googleapis.com"
standard_fonts = ["Noto Sans JP"]
google_fonts = [
    "Noto Serif JP", "Dela Gothic One", "DotGothic16", "Hachi Maru Pop", "Kaisei Tokumin", 
    "Kosugi Maru", "M PLUS Rounded 1c", "Reggae One", "WDXL Lubrifont JP N", 
    "Yuji Mai", "Zen Kurenaido", "Zen Maru Gothic"
]
all_fonts = standard_fonts + google_fonts

# --- スタイル定義 (CSS注入) ---
st.markdown(f"""
    <style>
    @import url('{GOOGLE_FONTS_URL}');
    @font-face {{
        font-family: 'Noto Sans JP';
        src: url('assets/fonts/NotoSansJP-Regular.ttf');
    }}

    /* 全体を囲むラッパーの最大幅を固定し、中央寄せする */
    .main-tool-wrapper {{
        max-width: {FIXED_WIDTH_PX}px; 
        margin: 0 auto; /* 画面の中央に配置 */
    }}

    /* プレビュー表示用の共通スタイル */
    .preview-container {{
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 80px;
        display: flex;
        align-items: center;
        text-align: left;
    }}

    /* 以下、既存の微調整CSS */
    div[data-baseweb="select"] > div {{
        height: 50px !important; min-height: 50px !important; align-items: center;
    }}
    .preview-container p {{
        margin: 0 !important; padding: 0 10px !important; width: 100%;
    }}

    /* ★ここから修正：水平方向中央寄せ用のスタイル★ */
    .highlight-center {{
        text-align: center; /* これで中の要素が水平中央揃えになる */
        width: 100%; /* 親コンテナの幅いっぱいを使う */
    }}
    /* カラーピッカー本体（インライン要素）を中央に配置 */
    .highlight-center div[data-testid="stColorPicker"] {{
        display: inline-block;
    }}

    </style>
    """, unsafe_allow_html=True)


# --- UI レイアウト ---
st.title("🔠 プレビュー")

# --- ここからラッパー開始：全体の幅が制限される ---
st.markdown(f'<div class="main-tool-wrapper">', unsafe_allow_html=True)

# --- 設定エリア（ラッパーの幅に制限される） ---
col_font, col_color, col_highlight = st.columns([2, 1, 1], gap="small")

with col_font:
    selected_font = st.selectbox("フォントを選択", all_fonts)

with col_color:
    font_color = st.color_picker("文字色", "#333333")

with col_highlight:
    # ★ここに中央寄せラッパーを適用★
    st.markdown('<div class="highlight-center">', unsafe_allow_html=True)
    highlight_color = st.color_picker("ハイライト色", "#FF0000")
    st.markdown('</div>', unsafe_allow_html=True)

# --- プレビューエリア（ラッパーの幅に制限される） ---

sample_text = "吾輩は猫である。"
font_size = 24 

base_color = font_color
display_html = sample_text.replace("猫", f'<span style="color:{highlight_color};">猫</span>')
    
st.markdown(f"""
    <div class="preview-container">
        <p style="font-family: '{selected_font}', sans-serif; 
                  font-size: {font_size}px; 
                  color: {base_color}; 
                  line-height: 1.0;">
            {display_html}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # --- ラッパー終了 ---

# おまけ情報はラッパーの外に配置
if selected_font in google_fonts:
    st.caption(f"💡 現在 {selected_font} (Google Fonts) を表示中")
else:
    st.caption(f"🏠 現在 {selected_font} (ローカルTTF) を表示中")

