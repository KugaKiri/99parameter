import streamlit as st

input_num = st.number_input('Input a number', value=0)

result = input_num ** 2
st.write('Result: ', result)
st.title("Sample calculator")
st.divider()
st.set_page_config(page_title="Sample Calculator")
