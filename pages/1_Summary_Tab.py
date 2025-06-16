import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Summary Dashboard – QuantiveFlow™", layout="wide")

# Security check
if not st.session_state.get("logged_in"):
    st.error("🔒 Access Denied: Please login first via the main page")
    st.stop()

# Modern CSS styling
st.markdown("""
<style>
    .metric-card {
        background: #1f1f1f;
        color: #fff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }

    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .flow-positive { color: #28a745; font-weight: bold; }
    .flow-negative { color: #dc3545; font-weight: bold; }
    .flow-neutral { color: #6c757d; font-weight: bold; }

    .refresh-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .badge-bullish { background: #d4edda; color: #155724; }
    .badge-bearish { background: #f8d7da; color: #721c24; }
    .badge-neutral { background: #e2e3e5; color: #383d41; }
</style>
""", unsafe_allow_html=True)

# Header with market info
current_market = st.session_state.get('selected_market', 'GBPJPY')
st.title("📊 Summary Dashboard")
st.markdown(f"**Current Market:** {current_market}")

# Market availability check
if current_market != 'GBPJPY':
    st.error(f"🚫 {current_market} market data is not accessible. Please switch to GBP/JPY for full functionality.")
    st.stop()

# File paths
# File paths
market_condition_file = "data/MarketCondition.csv"
ri_qc_file = "data/RI&QC.csv"
raw_metrics_file = "data/RawMetrics.csv"
tf_files = {f"{i}TF": f"data/{i}TF Net Table.csv" for i in [1,3,5,10,15,20]}

# Refresh button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🔄 Refresh Data", help="Update all market data"):
        st.cache_data.clear()
        st.success("Data refreshed!")
        st.rerun()

with col2:
    auto_refresh = st.checkbox("⚡ Live Mode", help="Enable for frequent updates")

# Helper functions
@st.cache_data
def load_csv_safe(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.warning(f"Data file not found: {os.path.basename(file_path)}")
        return pd.DataFrame()

def flow_color_class(val):
    if isinstance(val, str): return ""
    if val > 0: return "flow-positive"
    elif val < 0: return "flow-negative"
    else: return "flow-neutral"

def format_flow_value(val):
    if isinstance(val, str): return val
    return f"{val:+.2f}" if abs(val) >= 0.01 else f"{val:+.4f}"

# Load all data
market_df = load_csv_safe(market_condition_file)
ri_df = load_csv_safe(ri_qc_file)
metrics_df = load_csv_safe(raw_metrics_file)

# Main dashboard layout
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Overview", "📈 Flow Analysis", "🧮 Custom Metrics", "🔄 Flow Deltas"])

with tab1:
    if not market_df.empty:
        # Market Condition Overview
        st.markdown("""
        <div class="metric-card">
              <h3 class="metric-title">📍 Market Condition Overview</h3>
        </div>
        """, unsafe_allow_html=True)

        market_df = market_df.sort_values("Date", ascending=False)
        latest_condition = market_df.iloc[0]

        cols = ["1D", "3D", "5D", "10D", "15D", "20D"]
        condition_data = []

        for tf in cols:
            condition_data.append({
                "Timeframe": tf,
                "Condition": latest_condition[tf],
                "Distributions": latest_condition[f"{tf}_NumDists"],
                "Upper Limit": f"{latest_condition[f'{tf}_D1_Upper']:.4f}",
                "Lower Limit": f"{latest_condition[f'{tf}_D1_Lower']:.4f}"
            })

        condition_df = pd.DataFrame(condition_data)
        st.dataframe(condition_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # RI & QC Overview
        if not ri_df.empty:
            st.markdown("""
        <div class="metric-card">
              <h3 class="metric-title">📈 RI and QC Overview</h3>
        </div>
        """, unsafe_allow_html=True)

            ri_df = ri_df.sort_values("Date", ascending=False)
            latest_ri = ri_df.iloc[0]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("RI (4D)", f"{latest_ri['RI_4']:.3f}")
            with col2:
                st.metric("RI (8D)", f"{latest_ri['RI_8']:.3f}")
            with col3:
                st.metric("QC (4D)", latest_ri['RI_4_QC'])
            with col4:
                st.metric("QC (8D)", latest_ri['RI_8_QC'])

            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    # Flow Tables Analysis
    st.markdown("### 🌊 Flow Analysis by Timeframe")

    # Load all flow tables
    net_tables = {}
    for tf, file_path in tf_files.items():
        df = load_csv_safe(file_path)
        if not df.empty:
            df = df.sort_values("Date", ascending=False).reset_index(drop=True)
            net_tables[tf] = df

    if net_tables:
        # Timeframe selector
        selected_tf = st.selectbox("📅 Select Timeframe", list(net_tables.keys()), key="flow_tf")

        if selected_tf in net_tables:
            flow_df = net_tables[selected_tf]

            # Current flow metrics
            latest_flow = flow_df.iloc[0]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Direction", format_flow_value(latest_flow["Dir"]),
                         delta=f"{latest_flow['Dir'] - flow_df.iloc[1]['Dir']:+.3f}" if len(flow_df) > 1 else None)
            with col2:
                st.metric("Activity", format_flow_value(latest_flow["Act"]),
                         delta=f"{latest_flow['Act'] - flow_df.iloc[1]['Act']:+.3f}" if len(flow_df) > 1 else None)
            with col3:
                st.metric("Net Flow", format_flow_value(latest_flow["Net"]),
                         delta=f"{latest_flow['Net'] - flow_df.iloc[1]['Net']:+.3f}" if len(flow_df) > 1 else None)
            with col4:
                st.metric("3D Net", format_flow_value(latest_flow["3D Net"]),
                         delta=f"{latest_flow['3D Net'] - flow_df.iloc[1]['3D Net']:+.3f}" if len(flow_df) > 1 else None)

            # Flow history chart
            if len(flow_df) >= 10:
                chart_df = flow_df.head(10)
                fig = go.Figure()

                fig.add_trace(go.Scatter(x=chart_df['Date'], y=chart_df['Net'],
                                       mode='lines+markers', name='Net Flow',
                                       line=dict(color='#667eea', width=3)))
                fig.add_trace(go.Scatter(x=chart_df['Date'], y=chart_df['3D Net'],
                                       mode='lines+markers', name='3D Net',
                                       line=dict(color='#764ba2', width=2)))

                fig.update_layout(title=f"Flow Trend - {selected_tf}", height=400,
                                hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)

            # Detailed flow table
            with st.expander("📊 Detailed Flow Data"):
                st.dataframe(flow_df.head(10), use_container_width=True, hide_index=True)

with tab3:
    # Custom Metrics Analysis
    if not metrics_df.empty:
        st.markdown("### 🧮 Custom Auction Metric Analysis")

        # Timeframe selector for metrics
        tf_options = sorted(metrics_df['Days'].unique())
        selected_days = st.selectbox("📅 Select Analysis Period", tf_options, key="metrics_tf")

        filtered_df = metrics_df[metrics_df["Days"] == selected_days].reset_index(drop=True)

        if len(filtered_df) >= 2:
            row0, row1 = filtered_df.iloc[0], filtered_df.iloc[1]

            # Custom calculations
            custom_metrics = {
                "Value Area Position": (
                    "Higher" if row0["VAL"] >= row1["VAL"] and row0["VAH"] >= row1["VAH"] else
                    "Lower" if row0["VAL"] <= row1["VAL"] and row0["VAH"] <= row1["VAH"] else
                    "OL Higher" if row0["VAL"] >= row1["VAH"] else
                    "OL Lower" if row0["VAH"] <= row1["VAL"] else
                    "Inside" if row0["VAL"] <= row1["VAH"] and row0["VAH"] >= row1["VAL"] else
                    "Outside"
                ),
                "POC Movement": "POC Up" if row0["POC"] > row1["POC"] else "POC Down" if row0["POC"] < row1["POC"] else "Unchanged",
                "POC to Prev VA": (
                    "Below VA" if row0["POC"] < row1["VAL"] else
                    "Above VA" if row0["POC"] > row1["VAH"] else
                    "Inside VA"
                ),
                "Range Expansion": (
                    "Both Sides Expand" if row0["Low"] < row1["Low"] and row0["High"] > row1["High"] else
                    "Lower Break" if row0["Low"] < row1["Low"] else
                    "Upper Break" if row0["High"] > row1["High"] else
                    "Inside Day"
                ),
                "Close-V.A": (
                    "Below VA" if row0["Close"] < row0["VAL"] else
                    "Above VA" if row0["Close"] > row0["VAH"] else
                    "Inside VA"
                ),
                "TPO Imbalance": (
                    "Top-Weighted" if row0["TPO Ab. POC"] > row0["TPO Bl. POC"] else
                    "Bottom-Weighted" if row0["TPO Bl. POC"] > row0["TPO Ab. POC"] else
                    "Balanced"
                )
            }

            # Display custom metrics in cards
            col1, col2 = st.columns(2)
            metrics_items = list(custom_metrics.items())

            with col1:
                for i in range(0, len(metrics_items), 2):
                    metric, value = metrics_items[i]
                    badge_class = "badge-bullish" if "Higher" in value or "Up" in value or "Above" in value else "badge-bearish" if "Lower" in value or "Down" in value or "Below" in value else "badge-neutral"
                    st.markdown(f'**{metric}:** <span class="status-badge {badge_class}">{value}</span>', unsafe_allow_html=True)

            with col2:
                for i in range(1, len(metrics_items), 2):
                    if i < len(metrics_items):
                        metric, value = metrics_items[i]
                        badge_class = "badge-bullish" if "Higher" in value or "Up" in value or "Above" in value else "badge-bearish" if "Lower" in value or "Down" in value or "Below" in value else "badge-neutral"
                        st.markdown(f'**{metric}:** <span class="status-badge {badge_class}">{value}</span>', unsafe_allow_html=True)

            # Key metrics visualization
            key_metrics = ['POC', 'VAH', 'VAL', 'High', 'Low', 'Close']
            if all(col in filtered_df.columns for col in key_metrics):
                chart_data = filtered_df.head(10)[['Date'] + key_metrics]

                fig = go.Figure()
                colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']

                for i, metric in enumerate(key_metrics):
                    fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data[metric],
                                           mode='lines+markers', name=metric,
                                           line=dict(color=colors[i % len(colors)], width=2)))

                fig.update_layout(title=f"Key Metrics Trend ({selected_days}D)", height=400,
                                hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)

with tab4:
    # Flow Delta Analysis
    if net_tables:
        st.markdown("### 🔄 Flow Delta Analysis")

        delta_pairs = [("1TF", "3TF"), ("3TF", "5TF"), ("5TF", "10TF"), ("10TF", "15TF"), ("15TF", "20TF")]
        delta_data = []

        for tf1, tf2 in delta_pairs:
            df1, df2 = net_tables.get(tf1), net_tables.get(tf2)
            if df1 is not None and df2 is not None and not df1.empty and not df2.empty:
                r1, r2 = df1.iloc[0], df2.iloc[0]
                delta_data.append({
                    "Transition": f"{tf1} → {tf2}",
                    "Δ Direction": r1["Dir"] - r2["Dir"],
                    "Δ Activity": r1["Act"] - r2["Act"],
                    "Δ Net Flow": r1["Net"] - r2["Net"],
                    "Δ 3D Net": r1["3D Net"] - r2["3D Net"]
                })

        if delta_data:
            delta_df = pd.DataFrame(delta_data)

            # Delta visualization
            fig = go.Figure()

            fig.add_trace(go.Bar(x=delta_df['Transition'], y=delta_df['Δ Net Flow'],
                               name='Net Flow Delta', marker_color='#667eea'))
            fig.add_trace(go.Bar(x=delta_df['Transition'], y=delta_df['Δ 3D Net'],
                               name='3D Net Delta', marker_color='#764ba2'))

            fig.update_layout(title="Flow Deltas Across Timeframes", height=400,
                            barmode='group', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

            # Delta table
            st.dataframe(delta_df, use_container_width=True, hide_index=True)

        # Flow Consensus Analysis
        st.markdown("### 🧠 Flow Consensus")

        consensus_data = {"Metric": [], "Agreement Count": [], "Consensus": []}
        for metric in ["Dir", "Act", "Net", "3D Net"]:
            signs = []
            for tf in tf_files:
                df = net_tables.get(tf)
                if df is not None and not df.empty:
                    signs.append(np.sign(df.iloc[0][metric]))

            if signs:
                mode_sign = max(set(signs), key=signs.count)
                agreement_count = signs.count(mode_sign)
                consensus = "Bullish" if mode_sign > 0 else "Bearish" if mode_sign < 0 else "Neutral"

                consensus_data["Metric"].append(metric)
                consensus_data["Agreement Count"].append(f"{agreement_count}/{len(signs)}")
                consensus_data["Consensus"].append(consensus)

        consensus_df = pd.DataFrame(consensus_data)

        # Consensus visualization
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(consensus_df, use_container_width=True, hide_index=True)

        with col2:
            # Overall market sentiment
            net_consensus = consensus_df[consensus_df['Metric'] == 'Net']['Consensus'].iloc[0] if not consensus_df.empty else "Neutral"
            sentiment_color = "#28a745" if net_consensus == "Bullish" else "#dc3545" if net_consensus == "Bearish" else "#6c757d"

            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: {sentiment_color}20; border-radius: 12px; border: 2px solid {sentiment_color};">
                <h3 style="color: {sentiment_color}; margin: 0;">Market Sentiment</h3>
                <h2 style="color: {sentiment_color}; margin: 0.5rem 0;">{net_consensus}</h2>
                <p style="margin: 0; opacity: 0.8;">Based on Net Flow Consensus</p>
            </div>
            """, unsafe_allow_html=True)

# Auto-refresh functionality
if auto_refresh:
    time.sleep(30)  # 30-second refresh in live mode
    st.rerun()