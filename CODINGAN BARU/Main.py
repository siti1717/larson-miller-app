import streamlit as st

st.set_page_config(page_title="Larson-Miller Parameter", layout="wide")

st.title("🔬 Larson–Miller Parameter Calculator")
st.markdown("""
Welcome to the **Larson–Miller Parameter** application built with Streamlit.

Use the **menu on the left sidebar** to select the calculation method:
- Mean 1 1/4 Cr - 1/2 Mo-Si Steel
- Mean 2 1/4 Cr - 1 Mo Steel 
- Minimal 1 1/4 Cr - 1/2 Mo-Si Steel 
- Minimal 2 1/4 Cr - 1 Mo Steel 

Upload a CSV file containing the **Stress (ksi)** column to start the calculation.
""")
