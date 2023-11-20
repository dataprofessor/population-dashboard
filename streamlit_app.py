import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

# Page configuration
st.set_page_config(
    page_title="Population Dashboard",
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
    padding: 1rem 2rem 1rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
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

[data-testid="stMetricDeltaIcon-Down"] {
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

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = previous_year_data.population.sub(selected_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)


# Sidebar
with st.sidebar:
    st.title('Population Dashboard')
    year_list = list(df_reshaped.year.unique())
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)


# Choropleth map
states = alt.topo_feature(data.us_10m.url, 'states')

choropleth_map = alt.Chart(states).mark_geoshape().encode(
    color=alt.Color('population:Q', scale=alt.Scale(scheme="blueorange")),   # scale=color_scale
    stroke=alt.value('#154360')
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_selected_year, 'id', list(df_selected_year.columns))
).properties(
    width=500,
    height=300
).project(
    type='albersUsa'
)




# Row 1
row_1_col = st.columns((1,4,1.5))

with row_1_col[0]:
    st.subheader('Gains/Losses')

    df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)
    
    #first_state_name = df_selected_year_sorted.states.iloc[0]
    #first_state_population = format_number(df_selected_year_sorted.population.iloc[0])

    first_state_name = df_population_difference_sorted.states.iloc[0]
    first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
    first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])

    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    #last_state_name = df_selected_year_sorted.states.iloc[-1]
    #last_state_population = format_number(df_selected_year_sorted.population.iloc[-1])   

    last_state_name = df_population_difference_sorted.states.iloc[-1]
    last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
    last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   

    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    st.altair_chart(make_donut(25, 'Text', 'orange'), use_container_width=True)
    
with row_1_col[1]:
    st.subheader('Annual Population Growth')
    st.altair_chart(heatmap, use_container_width=True)
    #st.altair_chart(choropleth_map, use_container_width=True)

with row_1_col[2]:
    st.subheader('Top States')

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
    with st.expander('Data source'):
        st.write('''
            - [State population data (2010-2019)](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html) obtained from the U.S. Census Bureau.
            ''')


# Row 2
#row_2_col = st.columns(2)

#with row_2_col[0]:
#    st.write('6')
#with row_2_col[1]:
#    st.write('7')


from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout({
'template': 'plotly_dark',
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

with row_1_col[1]:
    st.plotly_chart(fig, use_container_width=True)

