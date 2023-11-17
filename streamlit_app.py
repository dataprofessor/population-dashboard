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

# 6rem 1rem 10rem
st.markdown("""
<style>

[data-testid="block-container"] {
    padding: 3rem 2rem 1rem;
}

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
df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')

# Plots

# Heatmap
heatmap = alt.Chart(df_reshaped).mark_rect().encode(
        y=alt.Y('year:O', axis=alt.Axis(title="Year", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X('states:O', axis=alt.Axis(title="", titleFontSize=16, titlePadding=15, titleFontWeight=900)),
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
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=70, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  )
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=38, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=70, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  )
  return plot_bg + plot + text
    

# Row 1
row_0_col = st.columns((1,4,1.5))
row_1_col = st.columns((1,4,1.5))

with row_0_col[2]:
    year_list = list(df_reshaped.year.unique())
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)
    

with row_1_col[0]:
    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

    st.altair_chart(make_donut(25, 'Text', 'orange'), use_container_width=True)
    
with row_1_col[1]:
    st.altair_chart(heatmap, use_container_width=True)

with row_1_col[2]:
    st.dataframe(df_selected_year_sorted,
                 column_order=("states", "population"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "states": st.column_config.TextColumn(
                        "States",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        width="medium",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.population),
                     )}
                 )




# Row 2
#row_2_col = st.columns(2)

#with row_2_col[0]:
#    st.write('6')
#with row_2_col[1]:
#    st.write('7')

