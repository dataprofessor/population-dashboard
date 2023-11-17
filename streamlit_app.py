import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Snowboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


# CSS styling
# .st-emotion-cache-j5r0tf {
#    width: calc(20% - 1rem);
#    flex: 1 1 calc(20% - 1rem);
#    text-align: center;
#    padding: 80px 0;
#    background-color: #154360;
#}

st.markdown("""
<style>

[data-testid="stMetric"] {
    background-color: #154360;
    text-align: center;
    padding: 25px 0;
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
df = pd.read_csv('data/us-population-2010-2019-reshaped.csv')

# Plots

# Heatmap
heatmap = alt.Chart(df).mark_rect().encode(
        y=alt.Y('year:O', axis=alt.Axis(title="Year", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X('states:O', axis=alt.Axis(title="States", titleFontSize=16, titlePadding=15, titleFontWeight=900)),
        color=alt.Color('max(population):Q',
                         legend=alt.Legend(title=" "),
                         scale=alt.Scale(scheme="blueorange")),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
        #tooltip=[
        #    alt.Tooltip('year:O', title='Year'),
        #    alt.Tooltip('population:Q', title='Population')
        #]
    ).properties(width=900
    #).configure_legend(orient='bottom', titleFontSize=16, labelFontSize=14, titlePadding=0
    #).configure_axisX(labelFontSize=14)
    ).configure_axis(
    labelFontSize=12,
    titleFontSize=12
    )

# Donut chart
def make_donut_chart(input_response, input_text, input_color):

   if input_color == 'blue':
       chart_color = ['#29b5e8', '#155F7A']
   if input_color == 'green':
       chart_color = ['#27AE60', '#12783D']
   if input_color == 'orange':
       chart_color = ['#F39C12', '#875A12']
   if input_color == 'red':
       chart_color = ['#E74C3C', '#781F16']
    
   source = pd.DataFrame({"Topic": ['Other', input_text], "Percent Response": [100-input_response, input_response]})
   source_bg = pd.DataFrame({"Topic": ['Other', input_text],"Percent Response": [100, 0]})
    
   selector = alt.selection_single(on='mouseover')
    
   donut = alt.Chart(source).mark_arc(innerRadius=70, cornerRadius=25).encode(
             theta=alt.Theta(field="Percent Response", type="quantitative", stack=True),
             color=alt.condition(selector, 'Topic', alt.value('#111111'), scale=alt.Scale(domain=[input_text, 'Other'], range=chart_color), legend=None),
             tooltip=['Topic', 'Percent Response']
   ).add_selection(selector).encode(text='Topic')

   #####
   plot = alt.Chart(source).mark_arc(innerRadius=70, cornerRadius=25).encode(
      theta=alt.Theta(field="Percent Response", type="quantitative", stack=True),
      color=alt.condition(selector, 'Topic', alt.value('#111111'), scale=alt.Scale(domain=[input_text, 'Other'], range=chart_color), legend=None),
   )
   #####
    
   plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=70, cornerRadius=20).encode(
             theta=alt.Theta(field="Percent Response", type="quantitative", stack=True),
             color=alt.condition(selector, 'Topic', alt.value('#111111'), scale=alt.Scale(domain=[input_text, 'Other'], range=chart_color), legend=None),
             tooltip=['Topic', 'Percent Response']
   )

   text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=38, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
   return plot_bg + donut + text
    

# Row 1
row_1_col = st.columns((1,4))

with row_1_col[0]:
    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

    make_donut_chart(25, 'Text', 'blue')
    
with row_1_col[1]:
    st.altair_chart(heatmap, use_container_width=True)

# Row 2
#row_2_col = st.columns(2)

#with row_2_col[0]:
#    st.write('6')
#with row_2_col[1]:
#    st.write('7')

