import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="Z-Score Heatmap – QuantiveFlow™", layout="wide")

# Security check
if not st.session_state.get("logged_in"):
    st.error("🔒 Access Denied: Please login first via the main page")
    st.stop()

# Modern CSS styling
st.markdown("""
<style>
    .heatmap-container {
        background: #1e1e1e;
        border-radius: 15px;
        color: #fff;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .alert-card {
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid;
    }

    .alert-critical {
        background: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }

    .alert-warning {
        background: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }

    .alert-normal {
        background: #d4edda;
        border-color: #28a745;
        color: #155724;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        display: block;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
current_market = st.session_state.get('selected_market', 'GBPJPY')
st.title("🔥 Z-Score Anomaly Detection")
st.markdown(f"**Current Market:** {current_market}")

# Market availability check
if current_market != 'GBPJPY':
    st.error(f"🚫 {current_market} market data is not accessible. Please switch to GBP/JPY for full functionality.")
    st.stop()

# File paths
zscore_files = {
    "1TF": "data/1tf Z-Score.csv",
    "3TF": "data/3tf Z-Score.csv",
    "5TF": "data/5tf Z-Score.csv",
    "10TF": "data/10tf Z-Score.csv",
    "15TF": "data/15tf Z-Score.csv",
    "20TF": "data/20tf Z-Score.csv",
}

# Controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_tf = st.selectbox("📅 Timeframe", list(zscore_files.keys()),
                              help="Select analysis timeframe")

with col2:
    latest_n = st.slider("📆 Days to View", 1, 20, 10,
                        help="Number of recent days to analyze")

with col3:
    if st.button("🔄 Refresh Data", help="Update Z-Score data"):
        st.cache_data.clear()
        st.success("Data refreshed!")

with col4:
    threshold = st.selectbox("⚠️ Alert Threshold", [1.5, 2.0, 2.5], index=1,
                           help="Z-Score threshold for anomaly alerts")

# Load and process data
@st.cache_data
def load_zscore_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'Date' in df.columns:
            df = df.set_index("Date")
        return df
    except FileNotFoundError:
        st.error(f"Z-Score file not found: {os.path.basename(file_path)}")
        return pd.DataFrame()

# Load selected data
zscore_df = load_zscore_data(zscore_files[selected_tf])

if zscore_df.empty:
    st.warning("No Z-Score data available for the selected timeframe.")
else:
    # Filter recent data
    zscore_df_latest = zscore_df.head(latest_n)

    # Calculate anomaly statistics
    total_values = zscore_df_latest.size
    extreme_values = (np.abs(zscore_df_latest) >= threshold).sum().sum()
    critical_values = (np.abs(zscore_df_latest) >= 2.5).sum().sum()
    anomaly_rate = (extreme_values / total_values * 100) if total_values > 0 else 0

    # Display key metrics
    st.markdown("""
    <div class="metric-grid">
        <div class="metric-box">
            <span class="metric-value">{:.1f}%</span>
            <span class="metric-label">Anomaly Rate</span>
        </div>
        <div class="metric-box">
            <span class="metric-value">{}</span>
            <span class="metric-label">Extreme Values</span>
        </div>
        <div class="metric-box">
            <span class="metric-value">{}</span>
            <span class="metric-label">Critical Alerts</span>
        </div>
        <div class="metric-box">
            <span class="metric-value">{}</span>
            <span class="metric-label">Total Metrics</span>
        </div>
    </div>
    """.format(anomaly_rate, extreme_values, critical_values, total_values), unsafe_allow_html=True)

    # Main visualization tabs
    tab1, tab2, tab3 = st.tabs(["🔥 Interactive Heatmap", "📊 Anomaly Analysis", "📈 Time Series"])

    with tab1:
        st.markdown("""
        <div class="heatmap-container">
              <h3 class="metric-title">Z-Score Heatmap</h3>
        </div>
          """, unsafe_allow_html=True)

        # Create interactive Plotly heatmap
        fig = go.Figure(data=go.Heatmap(
            z=zscore_df_latest.values,
            x=zscore_df_latest.columns,
            y=zscore_df_latest.index,
            colorscale='RdBu_r',
            zmid=0,
            text=zscore_df_latest.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            colorbar=dict(
                title="Z-Score",
                title_side="right"
            )

        ))

        fig.update_layout(
            title=f"Z-Score Heatmap - {selected_tf} ({latest_n} Days)",
            height=max(400, len(zscore_df_latest) * 30),
            xaxis_title="Metrics",
            yaxis_title="Date",
            font=dict(size=12)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Alert summary
        if extreme_values > 0:
            st.markdown(f"""
            <div class="alert-card alert-warning">
                <strong>⚠️ Anomaly Alert:</strong> {extreme_values} metrics showing extreme Z-scores (±{threshold}+)
            </div>
            """, unsafe_allow_html=True)

        if critical_values > 0:
            st.markdown(f"""
            <div class="alert-card alert-critical">
                <strong>🚨 Critical Alert:</strong> {critical_values} metrics showing critical Z-scores (±2.5+)
            </div>
            """, unsafe_allow_html=True)

        if extreme_values == 0:
            st.markdown("""
            <div class="alert-card alert-normal">
                <strong>✅ Normal Conditions:</strong> No significant anomalies detected
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📊 Detailed Anomaly Analysis")

        # Find most extreme values
        flat_values = zscore_df_latest.abs().unstack().sort_values(ascending=False)
        top_anomalies = flat_values.head(10)

        if not top_anomalies.empty:
            anomaly_data = []
            for (metric, date), zscore in top_anomalies.items():
                original_value = zscore_df_latest.loc[date, metric]
                severity = "Critical" if abs(original_value) >= 2.5 else "High" if abs(original_value) >= 2.0 else "Moderate"
                direction = "Positive" if original_value > 0 else "Negative"

                anomaly_data.append({
                    "Date": date,
                    "Metric": metric,
                    "Z-Score": f"{original_value:.3f}",
                    "Severity": severity,
                    "Direction": direction
                })

            anomaly_df = pd.DataFrame(anomaly_data)
            st.dataframe(anomaly_df, use_container_width=True, hide_index=True)

            # Anomaly distribution chart
            severity_counts = anomaly_df['Severity'].value_counts()
            fig_bar = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Anomaly Distribution by Severity",
                color=severity_counts.values,
                color_continuous_scale="Reds"
            )
            fig_bar.update_layout(height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No significant anomalies detected in the current dataset.")

    with tab3:
        st.markdown("### 📈 Z-Score Time Series Analysis")

        # Select metrics for time series
        available_metrics = zscore_df_latest.columns.tolist()
        selected_metrics = st.multiselect(
            "Select metrics to analyze:",
            available_metrics,
            default=available_metrics[:3] if len(available_metrics) >= 3 else available_metrics,
            help="Choose metrics for time series visualization"
        )

        if selected_metrics:
            # Create time series plot
            fig_ts = go.Figure()

            colors = px.colors.qualitative.Set1
            for i, metric in enumerate(selected_metrics):
                fig_ts.add_trace(go.Scatter(
                    x=zscore_df_latest.index,
                    y=zscore_df_latest[metric],
                    mode='lines+markers',
                    name=metric,
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=6)
                ))

            # Add threshold lines
            fig_ts.add_hline(y=threshold, line_dash="dash", line_color="orange",
                           annotation_text=f"Alert Threshold (+{threshold})")
            fig_ts.add_hline(y=-threshold, line_dash="dash", line_color="orange",
                           annotation_text=f"Alert Threshold (-{threshold})")
            fig_ts.add_hline(y=2.5, line_dash="dot", line_color="red",
                           annotation_text="Critical (+2.5)")
            fig_ts.add_hline(y=-2.5, line_dash="dot", line_color="red",
                           annotation_text="Critical (-2.5)")

            fig_ts.update_layout(
                title="Z-Score Time Series Analysis",
                height=500,
                xaxis_title="Date",
                yaxis_title="Z-Score",
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig_ts, use_container_width=True)

            # Statistical summary
            st.markdown("#### 📈 Statistical Summary")
            stats_df = zscore_df_latest[selected_metrics].describe().round(3)
            st.dataframe(stats_df, use_container_width=True)

    # Raw data table (expandable)
    with st.expander("📄 View Raw Z-Score Data"):
        st.dataframe(zscore_df_latest.round(3), use_container_width=True)

# Interpretation guide
st.markdown("---")
st.markdown("### ℹ️ Z-Score Interpretation Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🟢 Normal Range (-1 to +1)**
    - Typical market behavior
    - No immediate concern
    - Regular market conditions
    """)

with col2:
    st.markdown("""
    **🟡 Moderate (±1 to ±2)**
    - Slightly unusual behavior
    - Monitor for continuation
    - Potential setup forming
    """)

with col3:
    st.markdown("""
    **🔴 Extreme (±2+)**
    - Highly abnormal behavior
    - Exhaustion/momentum signals
    - Critical inflection points
    """)
