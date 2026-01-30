import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit 表表示サンプル")

# 行数を指定する数値入力フォーム
rows = st.number_input("生成する行数を入力してください", min_value=1, max_value=100, value=10)

# サンプルデータの作成（固定データ4列 + 入力用1列）
df = pd.DataFrame(
    np.random.randn(rows, 4),
    columns=[f'列 {i+1}' for i in range(4)]
)
df['入力値'] = 0.0  # 初期値0の入力用列を追加

# 1. st.dataframe: インタラクティブな表
st.header("1. st.dataframe (推奨)")
st.write("列のソート、リサイズ、検索が可能です。大量のデータ表示に向いています。")
# use_container_width=True で横幅いっぱいに広げられます
st.dataframe(df, use_container_width=True)

# 2. st.table: 静的な表
st.header("2. st.table")
st.write("HTMLのテーブルとしてレンダリングされます。データ量が少ない場合や、固定表示したい場合に適しています。")
st.table(df.head(3)) # 上位3行のみ表示

# 3. st.data_editor: 編集可能な表
st.header("3. st.data_editor")
st.write("一番右の列だけ編集できるように設定しています。")

# 編集不可にする列のリスト（最後の列以外すべて）
disabled_cols = df.columns[:-1]

edited_df = st.data_editor(df, key="editor", disabled=disabled_cols)

# 編集されたデータを確認するボタン
if st.button("編集後のデータを確認"):
    st.write("編集後のデータフレーム:")
    st.dataframe(edited_df)
    st.success("このデータをCSVとして保存したり、計算に使ったりできます。")