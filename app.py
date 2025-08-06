import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("Cleaned_Bird_Observation_Data.xls")

df = load_data()

# Sidebar - Filters
st.sidebar.header("📊 Filter the Data")
years = sorted(df['Year'].dropna().unique())
habitats = df['Habitat'].dropna().unique()
observers = df['Observer'].dropna().unique()
seasons = df['Season'].dropna().unique()

year_filter = st.sidebar.multiselect("Year", options=years, default=years)
habitat_filter = st.sidebar.multiselect("Habitat", options=habitats, default=habitats)
observer_filter = st.sidebar.multiselect("Observer", options=observers, default=observers)
season_filter = st.sidebar.multiselect("Season", options=seasons, default=seasons)

# Filtered DataFrame
filtered_df = df[
    (df['Year'].isin(year_filter)) &
    (df['Habitat'].isin(habitat_filter)) &
    (df['Observer'].isin(observer_filter)) &
    (df['Season'].isin(season_filter))
]

# Title
st.title("🦜 Bird Species Observation Dashboard")
st.markdown("Explore forest and grassland bird sightings across time, habitat, and conservation metrics.")

# 1. Observations per Year
st.subheader("1. Observations per Year")
year_counts = filtered_df['Year'].value_counts().sort_index().reset_index()
year_counts.columns = ['Year', 'Count']
fig1 = px.bar(year_counts, x='Year', y='Count', title='Bird Observations per Year')
st.plotly_chart(fig1)

# 2. Top 10 Bird Species
st.subheader("2. Top 10 Bird Species")
top_species = filtered_df['Common_Name'].value_counts().head(10).reset_index()
top_species.columns = ['Species', 'Count']
fig2 = px.bar(top_species, x='Species', y='Count', title='Top 10 Observed Bird Species')
st.plotly_chart(fig2)

# 3. Observations by Season
st.subheader("3. Seasonal Trends")
season_counts = filtered_df['Season'].value_counts().reset_index()
season_counts.columns = ['Season', 'Count']
fig3 = px.pie(season_counts, names='Season', values='Count', title='Bird Observations by Season')
st.plotly_chart(fig3)

# 4. Habitat-wise Species Diversity
st.subheader("4. Unique Species per Habitat")
habitat_species = filtered_df.groupby('Habitat')['Scientific_Name'].nunique().reset_index()
fig4 = px.bar(habitat_species, x='Habitat', y='Scientific_Name',
              title='Unique Bird Species per Habitat',
              labels={'Scientific_Name': 'Unique Species'})
st.plotly_chart(fig4)

# 5. Temperature vs Observations
st.subheader("5. Observations vs Temperature")
temp_counts = filtered_df.groupby('Temperature').size().reset_index(name='Count')
fig5 = px.line(temp_counts, x='Temperature', y='Count', markers=True, title='Bird Observations vs Temperature')
st.plotly_chart(fig5)

# 6. Most Active Observers
st.subheader("6. Most Active Observers")
top_obs = filtered_df['Observer'].value_counts().head(10).reset_index()
top_obs.columns = ['Observer', 'Count']
fig6 = px.bar(top_obs, x='Observer', y='Count', title='Top 10 Most Active Observers')
st.plotly_chart(fig6)

# 7. Flyover Behavior
st.subheader("7. Flyover Behavior")
flyover_counts = filtered_df['Flyover_Observed'].astype(str).str.upper().replace({'TRUE': 'Flyover', 'FALSE': 'Not Flyover'}).value_counts().reset_index()
flyover_counts.columns = ['Flyover Status', 'Count']
fig7 = px.pie(flyover_counts, values='Count', names='Flyover Status', title='Flyover Behavior Distribution')
st.plotly_chart(fig7)

# 8. Watchlist Species
st.subheader("8. Conservation Focus - Watchlist Species")
watchlist_df = filtered_df[filtered_df['PIF_Watchlist_Status'] == True]
watchlist_top = watchlist_df['Common_Name'].value_counts().head(10).reset_index()
watchlist_top.columns = ['Species', 'Count']
fig8 = px.bar(watchlist_top, x='Species', y='Count', title='Top 10 Watchlist Bird Species')
st.plotly_chart(fig8)

# Footer
st.markdown("**Data Source:** Forest & Grassland Bird Monitoring Dataset")
st.caption("🚀 Built using Streamlit and Plotly | Developed by [You]")
