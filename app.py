import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19 Global Dashboard",
    page_icon="🦠",
    layout="wide"
)

# ─── Title ─────────────────────────────────────────────────────
st.title("🦠 COVID-19 Global Dashboard")
st.markdown("Interactive global COVID-19 data explorer — built by **Dixitha BV**")
st.markdown("---")

# ─── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("covid-data.csv", parse_dates=["Date"])
    df.columns = df.columns.str.strip()
    return df

with st.spinner("Loading COVID-19 data..."):
    df = load_data()

# ─── Sidebar Filters ───────────────────────────────────────────
st.sidebar.header("🔍 Filters")

countries = sorted(df["Country"].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=countries,
    default=["India", "US", "United Kingdom"] if "India" in countries else countries[:3]
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if not selected_countries:
    st.warning("Please select at least one country from the sidebar.")
    st.stop()

# ─── Filter Data ───────────────────────────────────────────────
filtered = df[
    (df["Country"].isin(selected_countries)) &
    (df["Date"] >= pd.Timestamp(start_date)) &
    (df["Date"] <= pd.Timestamp(end_date))
]

# ─── KPI Cards ─────────────────────────────────────────────────
st.subheader("📊 Key Metrics (Latest Data)")

latest = filtered.sort_values("Date").groupby("Country").last().reset_index()

col1, col2, col3, col4 = st.columns(4)

total_cases  = latest["Confirmed"].sum()
total_deaths = latest["Deaths"].sum()
total_recovered = latest["Recovered"].sum()
death_rate   = (total_deaths / total_cases * 100) if total_cases > 0 else 0

col1.metric("🦠 Total Confirmed", f"{total_cases:,.0f}")
col2.metric("💀 Total Deaths",    f"{total_deaths:,.0f}")
col3.metric("💚 Total Recovered", f"{total_recovered:,.0f}")
col4.metric("📉 Death Rate",      f"{death_rate:.2f}%")

st.markdown("---")

# ─── Chart 1: Confirmed Cases Over Time ────────────────────────
st.subheader("📈 Confirmed Cases Over Time")
fig1 = px.line(
    filtered,
    x="Date",
    y="Confirmed",
    color="Country",
    title="Total Confirmed COVID-19 Cases Over Time",
    labels={"Confirmed": "Confirmed Cases", "Date": "Date", "Country": "Country"},
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)

# ─── Chart 2: Deaths Over Time ─────────────────────────────────
st.subheader("💀 Deaths Over Time")
fig2 = px.line(
    filtered,
    x="Date",
    y="Deaths",
    color="Country",
    title="Total COVID-19 Deaths Over Time",
    labels={"Deaths": "Total Deaths", "Date": "Date", "Country": "Country"},
    template="plotly_dark"
)
st.plotly_chart(fig2, use_container_width=True)

# ─── Chart 3: Recovered Over Time ──────────────────────────────
st.subheader("💚 Recovered Cases Over Time")
fig3 = px.line(
    filtered,
    x="Date",
    y="Recovered",
    color="Country",
    title="Total Recovered COVID-19 Cases Over Time",
    labels={"Recovered": "Recovered Cases", "Date": "Date", "Country": "Country"},
    template="plotly_dark"
)
st.plotly_chart(fig3, use_container_width=True)

# ─── Chart 4: Death Rate by Country ────────────────────────────
st.subheader("📉 Death Rate by Country (%)")
latest["Death Rate (%)"] = (latest["Deaths"] / latest["Confirmed"] * 100).round(2)
fig4 = px.bar(
    latest,
    x="Country",
    y="Death Rate (%)",
    color="Country",
    title="Death Rate by Country (%)",
    labels={"Death Rate (%)": "Death Rate (%)", "Country": "Country"},
    template="plotly_dark"
)
st.plotly_chart(fig4, use_container_width=True)

# ─── Chart 5: Confirmed vs Deaths Comparison ───────────────────
st.subheader("📊 Confirmed vs Deaths Comparison")
fig5 = px.bar(
    latest,
    x="Country",
    y=["Confirmed", "Deaths", "Recovered"],
    barmode="group",
    title="Confirmed vs Deaths vs Recovered by Country",
    template="plotly_dark"
)
st.plotly_chart(fig5, use_container_width=True)

# ─── Raw Data Table ─────────────────────────────────────────────
st.subheader("📋 Raw Data")
with st.expander("Click to view raw data table"):
    st.dataframe(
        filtered.sort_values("Date", ascending=False),
        use_container_width=True
    )

# ─── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "Built with ❤️ by **Dixitha BV** | "
    "Data source: [datasets/covid-19](https://github.com/datasets/covid-19) | "
    "[GitHub](https://github.com/DixithaBV)"
)