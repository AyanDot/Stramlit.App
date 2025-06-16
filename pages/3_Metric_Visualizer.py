import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="Metric Visualizer – QuantiveFlow™", layout="wide")

# Security check
if not st.session_state.get("logged_in"):
    st.error("🔒 Access Denied: Please login first via the main page")
    st.stop()

# Modern CSS styling
st.markdown("""
<style>
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .control-panel {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #2c3e50 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 2rem;
        border: 1px solid #34495e;
    }

    .control-panel h3 {
        color: white !important;
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border: 1px solid #e1e5e9;
        margin: 0.5rem 0;
    }

    .trend-up { color: #28a745; font-weight: bold; }
    .trend-down { color: #dc3545; font-weight: bold; }
    .trend-stable { color: #6c757d; font-weight: bold; }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .stat-item {
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        display: block;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
current_market = st.session_state.get('selected_market', 'GBPJPY')
st.title("📈 Advanced Metric Visualizer")
st.markdown(f"**Current Market:** {current_market}")

# Market availability check
if current_market != 'GBPJPY':
    st.error(f"🚫 {current_market} market data is not accessible. Please switch to GBP/JPY for full functionality.")
    st.stop()

# File paths
raw_metrics_file = "data/RawMetrics.csv"

# Load data function
@st.cache_data
def load_metrics_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error(f"Metrics file not found: {os.path.basename(file_path)}")
        return pd.DataFrame()

# Load data
raw_df = load_metrics_data(raw_metrics_file)

if raw_df.empty:
    st.warning("No metrics data available.")
    st.stop()

# Control panel - Fixed version
st.markdown("""
<div class="control-panel">
    <h3>🎛️ Analysis Controls</h3>
</div>
""", unsafe_allow_html=True)

# Add negative margin to bring controls closer to the panel
st.markdown("""
<style>
    .control-panel + div {
        margin-top: -1rem;
        padding: 0 1.5rem 1.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #2c3e50 100%);
        border-radius: 0 0 12px 12px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    timeframe_map = {"1TF": 1, "3TF": 3, "5TF": 5, "10TF": 10, "15TF": 15, "20TF": 20}
    selected_tf = st.selectbox("📅 Timeframe", list(timeframe_map.keys()),
                              help="Select analysis timeframe")
    selected_days = timeframe_map[selected_tf]

with col2:
    latest_n = st.slider("📆 Days to Analyze", 5, 100, 30,
                        help="Number of recent days to visualize")

with col3:
    chart_type = st.selectbox("📊 Chart Type",
                             ["Line Chart", "Area Chart", "Candlestick", "Multi-Axis"],
                             help="Select visualization style")

with col4:
    if st.button("🔄 Refresh Data", help="Update all metric data"):
        st.cache_data.clear()
        st.success("Data refreshed!")

# Filter data
filtered_df = raw_df[raw_df["Days"] == selected_days].copy()
filtered_df = filtered_df.sort_values("Date", ascending=True)

if filtered_df.empty:
    st.warning(f"No data available for {selected_tf} timeframe.")
    st.stop()

# Get recent data
df_to_plot = filtered_df.tail(latest_n).copy()

# Available metrics
exclude_cols = ["Date", "Days"]
metric_columns = [col for col in df_to_plot.columns if col not in exclude_cols]

# Main visualization tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Interactive Charts", "📈 Comparative Analysis", "🔍 Correlation Matrix", "📋 Statistical Summary"])

with tab1:
    st.markdown("### 📊 Interactive Metric Visualization")

    # Metric selection
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_metrics = st.multiselect(
            "Select metrics to visualize:",
            metric_columns,
            default=["POC", "VAH", "VAL"] if all(m in metric_columns for m in ["POC", "VAH", "VAL"]) else metric_columns[:3],
            help="Choose metrics for visualization"
        )

    with col2:
        show_ma = st.checkbox("📈 Show Moving Average", help="Add moving average overlay")
        if show_ma:
            ma_period = st.number_input("MA Period", 3, 20, 5)

    if not selected_metrics:
        st.warning("Please select at least one metric.")
    else:
        fig = go.Figure()

        if chart_type == "Line Chart":
            for metric in selected_metrics:
                fig.add_trace(go.Scatter(x=df_to_plot["Date"], y=df_to_plot[metric],
                                         mode='lines+markers', name=metric))

        elif chart_type == "Area Chart":
            for metric in selected_metrics:
                fig.add_trace(go.Scatter(x=df_to_plot["Date"], y=df_to_plot[metric],
                                         mode='lines', name=metric, fill='tozeroy'))

        elif chart_type == "Candlestick" and all(col in selected_metrics for col in ["Open", "High", "Low", "Close"]):
            fig = go.Figure(data=[go.Candlestick(
                x=df_to_plot['Date'],
                open=df_to_plot['Open'],
                high=df_to_plot['High'],
                low=df_to_plot['Low'],
                close=df_to_plot['Close'],
                name="Price"
            )])
        elif chart_type == "Multi-Axis" and len(selected_metrics) >= 2:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=df_to_plot["Date"], y=df_to_plot[selected_metrics[0]],
                                     name=selected_metrics[0]), secondary_y=False)
            fig.add_trace(go.Scatter(x=df_to_plot["Date"], y=df_to_plot[selected_metrics[1]],
                                     name=selected_metrics[1]), secondary_y=True)
        else:
            st.info("📌 For Candlestick, you must select Open, High, Low, Close. For Multi-Axis, select at least two metrics.")
            st.stop()

        # Add moving average
        if show_ma:
            for metric in selected_metrics:
                if df_to_plot[metric].dtype in [np.float64, np.int64]:
                    ma = df_to_plot[metric].rolling(window=ma_period).mean()
                    fig.add_trace(go.Scatter(x=df_to_plot["Date"], y=ma,
                                             mode='lines', name=f"{metric} MA ({ma_period})",
                                             line=dict(dash='dash')))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Metric Value",
            legend_title="Metrics",
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Tab 2: Comparative Analysis
# ----------------------------
with tab2:
    st.markdown("### 📈 Comparative Metric Lines")
    selected = st.multiselect("Select metrics for comparative plotting:", metric_columns, default=metric_columns[:3])
    if selected:
        fig = px.line(df_to_plot, x="Date", y=selected)
        st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Tab 3: Correlation Matrix
# ----------------------------
with tab3:
    st.markdown("### 🔍 Correlation Matrix")
    corr = df_to_plot[selected_metrics].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Tab 4: Summary Statistics
# ----------------------------
with tab4:
    st.markdown("### 📋 Statistical Summary")
    st.dataframe(df_to_plot[selected_metrics].describe().T.style.format(precision=2), use_container_width=True)