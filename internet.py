import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

# Read in the data
df_raw = load_data(path="data/share-of-individuals-using-the-internet.csv")
df_int = deepcopy(df_raw)

# Create df with only the most recent data of every country

countries = []
mr_year = []

for grp, df in df_int.groupby("Code"):
    countries.append(grp)
    mr_year.append(df["Year"].max())

df_years = pd.DataFrame({"Code": countries, "most_recent_year": mr_year})

df_rec = pd.merge(df_years, df_int)
df_rec = df_rec[df_rec["Year"] == df_rec["most_recent_year"]]

# Add title and header
st.title("Share of individuals using the Internet")

# Setting up columns
# left_column, middle_column, right_column = st.columns([3, 1, 1])

# Widgets

st.subheader("Global map with development per year:")

if st.checkbox("Show map"):

    year_sel = st.slider("Choose year: (2017 has most complete data)",
                          min_value=df_rec["Year"].min(),
                          max_value=df_rec["Year"].max(),
                          value=2017,
                          #step=None,
                          #format=None,
                          #key=None,
                          #help=None,
                          #on_change=None,
                          #args=None,
                          #kwargs=None,
                          #*,
                          #disabled=False,
                          #label_visibility="visible"
                        )

    # Plotting
    df_sel = df_int[df_int["Year"] == year_sel]

    fig = px.choropleth(
        df_sel,
        locations="Code",
        color="Individuals using the Internet (% of population)",
        #width=850,
        height=450,
        labels={"Individuals using the Internet (% of population)":"% of Population",
               "Year":"Year"},
        hover_name="Entity",
        hover_data={"Code": False,
                    "Year": True,
                    "Individuals using the Internet (% of population)":":.2f"
                   },
        #title="<b>Percentage of Population Using the Internet</b>",
        #color_continuous_scale="Viridis",
    )

    fig.update_traces(marker={"opacity":0.7})

    fig.update_layout(margin={"r":20,"t":50,"l":0,"b":5},
                      #font_family="Rockwell",
                      hoverlabel={"bgcolor":"white",
                                  "font_size":12,
                                  #"font_family":"Rockwell"
                                  },
                      title={"font_size":20,
                             "xanchor":"left", "x":0.01,
                             "yanchor":"top"},
                      geo={"resolution":50,
                           "showlakes":True, "lakecolor":"lightblue",
                           "showocean":True, "oceancolor":"aliceblue"
                          }
    )

    st.plotly_chart(fig)

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)

st.subheader("Global map with most recent share per country:")

if st.checkbox("Show map", key=1):

    # Plotting

    fig2 = px.choropleth(
        df_rec,
        locations="Code",
        color="Individuals using the Internet (% of population)",
        #width=850,
        height=450,
        labels={"Individuals using the Internet (% of population)":"% of Population",
               "Year":"Year"},
        hover_name="Entity",
        hover_data={"Code": False,
                    "Year": True,
                    "Individuals using the Internet (% of population)":":.2f"
                   },
        #title="<b>Percentage of Population Using the Internet</b>",
        #color_continuous_scale="Viridis",
    )

    fig2.update_traces(marker={"opacity":0.7})

    fig2.update_layout(margin={"r":20,"t":50,"l":0,"b":5},
                      #font_family="Rockwell",
                      hoverlabel={"bgcolor":"white",
                                  "font_size":12,
                                  #"font_family":"Rockwell"
                                  },
                      title={"font_size":20,
                             "xanchor":"left", "x":0.01,
                             "yanchor":"top"},
                      geo={"resolution":50,
                           "showlakes":True, "lakecolor":"lightblue",
                           "showocean":True, "oceancolor":"aliceblue"
                          }
    )

    st.plotly_chart(fig2)

if st.checkbox("Show dataframe", key=2):
    st.dataframe(data=df_rec)