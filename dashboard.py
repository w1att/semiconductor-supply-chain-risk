import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="U.S. Semiconductor Import Risk Dashboard", layout="wide")

st.title("U.S. Semiconductor Import Concentration Risk")
st.markdown("Tracking supplier concentration risk in U.S. semiconductor imports (HS 8542), 2015-2023, using UN Comtrade data.")

# Load data
df = pd.read_csv('semiconductor_hhi_trend_expanded.csv')

# --- HHI Trend Chart ---
st.subheader("Import Concentration (HHI) Over Time")

fig_hhi = go.Figure()
fig_hhi.add_trace(go.Scatter(x=df['year'], y=df['hhi'], mode='lines+markers', name='HHI', line=dict(width=3)))
fig_hhi.add_hline(y=2500, line_dash="dash", line_color="red", annotation_text="High concentration threshold (2500)")
fig_hhi.add_hline(y=1500, line_dash="dash", line_color="orange", annotation_text="Moderate concentration threshold (1500)")
fig_hhi.update_layout(xaxis_title="Year", yaxis_title="HHI", height=450)

st.plotly_chart(fig_hhi, use_container_width=True)

# --- Country Share Chart ---
st.subheader("Import Share by Country")

countries = ['Malaysia', 'Other Asia, nes', 'Rep. of Korea', 'China', 'Viet Nam', 'Thailand']
fig_countries = go.Figure()
for country in countries:
    fig_countries.add_trace(go.Scatter(x=df['year'], y=df[country], mode='lines+markers', name=country))
fig_countries.update_layout(xaxis_title="Year", yaxis_title="Share of U.S. Imports (%)", height=450)

st.plotly_chart(fig_countries, use_container_width=True)

# --- Key Stats ---
st.subheader("Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Peak HHI (2020)", f"{df.loc[df['year']==2020, 'hhi'].values[0]:.0f}", "Highly concentrated")
col2.metric("2023 HHI", f"{df.loc[df['year']==2023, 'hhi'].values[0]:.0f}", "Unconcentrated")
col3.metric("Malaysia Share Change", f"{df.loc[df['year']==2023, 'Malaysia'].values[0] - df.loc[df['year']==2015, 'Malaysia'].values[0]:.1f} pts", "2015→2023")

# --- Data Table ---
st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)
