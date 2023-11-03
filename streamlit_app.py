import streamlit as st

st.set_page_config(
    page_title="Snowboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
<style>
.grid-container {
  display: grid;
  grid-template-columns: auto auto auto;
  background-color: #2196F3;
  padding: 10px;
}
.grid-item {
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.8);
  padding: 20px;
  font-size: 30px;
  text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f'''
<div class="grid-container">
  <div class="grid-item">{st.write("1")}</div>
  <div class="grid-item">2</div>
  <div class="grid-item">3</div>  
  <div class="grid-item">4</div>
  <div class="grid-item">5</div>
  <div class="grid-item">6</div>  
  <div class="grid-item">7</div>
  <div class="grid-item">8</div>
  <div class="grid-item">9</div>  
</div>
''', unsafe_allow_html=True)


#col = st.columns(5)

#with col[0]:
#    st.write('1')
#with col[1]:
#    st.write('2')
#with col[2]:
    #st.write('3')
#    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
#with col[3]:
#    st.write('4')
#with col[4]:
#    st.write('5')
