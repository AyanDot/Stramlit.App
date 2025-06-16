import streamlit as st

# Page configuration
st.set_page_config(
    page_title="QuantiveFlow™ Home",
    layout="wide",
    page_icon="🌐"
)

# Security check
if not st.session_state.get("logged_in"):
    st.error("🔒 Access Denied: Please login from the main page")
    st.stop()

# Custom CSS for modern home page
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }

    .feature-card {
        background: linear-gradient(135deg, #2c2f36 0%, #1a1d23 100%);
        border-radius: 15px;
        color: white;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-left-color: #764ba2;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }

    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        text-align: center;
    }

    .feature-desc {
        color: #b8c2cc;
        line-height: 1.6;
        text-align: center;
    }

    .stats-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .stat-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        display: block;
    }

    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }

    .quick-tip {
        background: linear-gradient(135deg, #2c2f36 0%, #1a1d23 100%);
        color: white;
        border-left: 4px solid #28a745;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">🌐 QuantiveFlow™</div>
    <div class="hero-subtitle">Where Price Meets Value</div>
    <p>Currently analyzing: <strong>{st.session_state.get('selected_market', 'GBPJPY')}</strong></p>
</div>
""", unsafe_allow_html=True)

# Market status check
current_market = st.session_state.get('selected_market', 'GBPJPY')
if current_market != 'GBPJPY':
    st.warning(f"⚠️ **{current_market}** market data is not accessible. Switch to GBP/JPY for full functionality.")

# Platform statistics
st.markdown("""
<div class="stats-row">
    <div class="stat-box">
        <span class="stat-number">6</span>
        <span class="stat-label">Timeframes</span>
    </div>
    <div class="stat-box">
        <span class="stat-number">15+</span>
        <span class="stat-label">Metrics</span>
    </div>
    <div class="stat-box">
        <span class="stat-number">24/7</span>
        <span class="stat-label">Analysis</span>
    </div>
    <div class="stat-box">
        <span class="stat-number">Real-time</span>
        <span class="stat-label">Updates</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Key features showcase
st.markdown("## ✨ Platform Capabilities")

# Using columns for better layout instead of CSS Grid
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔐</div>
        <div class="feature-title">Secure Access</div>
        <div class="feature-desc">Enterprise-grade security with session management and login attempt tracking for professional trading environments.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧮</div>
        <div class="feature-title">Custom Calculations</div>
        <div class="feature-desc">Dynamic auction metrics including Value Area positioning, POC movement, and range expansion analysis.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Interactive Visualizations</div>
        <div class="feature-desc">Professional-grade charts and heatmaps with real-time data visualization and export capabilities.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Market Profile Analysis</div>
        <div class="feature-desc">Comprehensive flow analysis with directional bias detection across multiple timeframes for informed decision making.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔥</div>
        <div class="feature-title">Z-Score Detection</div>
        <div class="feature-desc">Advanced anomaly detection system to identify market exhaustion points and momentum shifts.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Real-time Updates</div>
        <div class="feature-desc">Live market data processing with refresh controls and automated analysis across all supported timeframes.</div>
    </div>
    """, unsafe_allow_html=True)

# Quick navigation
st.markdown("## 🧭 Navigate to Analysis Tools")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 **Summary Dashboard**", use_container_width=True, help="View comprehensive market analysis"):
        st.switch_page("pages/1_Summary_Tab.py")

with col2:
    if st.button("🔥 **Z-Score Heatmap**", use_container_width=True, help="Detect market anomalies"):
        st.switch_page("pages/2_Z-Score_Heatmap.py")

with col3:
    if st.button("📈 **Metric Visualizer**", use_container_width=True, help="Interactive metric charts"):
        st.switch_page("pages/3_Metric_Visualizer.py")

# Usage instructions
st.markdown("## 📋 Quick Start Guide")

st.markdown("""
<div class="quick-tip">
    <strong>💡 Pro Tip:</strong> Start with the Summary Dashboard to get an overview of market conditions, then dive deeper into specific analysis tools.
</div>
""", unsafe_allow_html=True)

instructions = """
### 🎯 How to Use QuantiveFlow™:

1. **Market Selection**: Choose your desired market from the dropdown (currently optimized for GBP/JPY)
2. **Summary Analysis**: Navigate to the Summary Tab for directional insights and flow consensus
3. **Anomaly Detection**: Use the Z-Score Heatmap to identify unusual market behavior
4. **Metric Deep-Dive**: Explore the Metric Visualizer for detailed technical analysis
5. **Data Refresh**: Use refresh buttons for real-time updates (no automatic refresh for performance)

### 📊 Key Analysis Components:

**Market Condition Overview**: Real-time distribution analysis across 6 timeframes
**RI & QC Metrics**: Regime identification and quadrant classification
**Flow Tables**: Directional, activity, and net flow measurements
**Custom Calculations**: Value Area positioning, POC movement, range analysis
**Flow Consensus**: Cross-timeframe agreement analysis for confidence building
"""

st.markdown(instructions)

# Footer with current session info
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Market", current_market)
with col2:
    st.metric("Session Status", "🟢 Active")
with col3:
    st.metric("Data Access", "🟢 Full" if current_market == "GBPJPY" else "🔴 Limited")
