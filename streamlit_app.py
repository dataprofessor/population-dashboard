import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Snowboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

# CSS styling
st.markdown("""
<style>
.st-emotion-cache-j5r0tf {
    width: calc(20% - 1rem);
    flex: 1 1 calc(20% - 1rem);
    text-align: center;
    padding: 80px 0;
    background-color: #154360;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 40%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/dashboard-v3/master/data/us-population-2010-2019.csv')

# Row 1
row_1_col = st.columns(5)

with row_1_col[0]:
    st.write('1')
with row_1_col[1]:
    st.write('2')
with row_1_col[2]:
    #st.write('3')
    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
with row_1_col[3]:
    st.write('4')
with row_1_col[4]:
    st.write('5')

# Row 2
row_2_col = st.columns(2)

with row_2_col[0]:
    st.write('6')
with row_2_col[1]:
    st.write('7')

