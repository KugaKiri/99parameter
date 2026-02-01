import streamlit as st
import matplotlib.pyplot as plt

st.title("Sample App")

num = st.number_input("Input a number", value=0)
result = num ** 2
st.write("Result:", result)

if st.button("画像として保存"):
    fig, ax = plt.subplots()
    ax.text(0.5, 0.6, f"Input: {num}", ha="center", fontsize=14)
    ax.text(0.5, 0.4, f"Result: {result}", ha="center", fontsize=14)
    ax.axis("off")

    file_name = "result.png"
    fig.savefig(file_name)

    with open(file_name, "rb") as f:
        st.download_button(
            label="画像をダウンロード",
            data=f,
            file_name=file_name,
            mime="image/png"
        )
