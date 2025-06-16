import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="QuantiveFlow™ - Where Price Meets Value",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    .login-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid #e1e5e9;
        max-width: 400px;
        margin: 0 auto;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        display: block;
    }

    .stat-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }

    .feature-list {
        background: #1e1e1e;
        color: #fff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .feature-item {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }

    .success-animation {
        animation: slideIn 0.5s ease-out;
    }

    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .stSelectbox > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "login_attempts" not in st.session_state:
    st.session_state["login_attempts"] = 0
if "selected_market" not in st.session_state:
    st.session_state["selected_market"] = "GBPJPY"

# Market selection (always visible)
st.markdown('<h1 class="main-header">QuantiveFlow™</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Where Price Meets Value</p>', unsafe_allow_html=True)

# Market selector
markets = ["GBPJPY", "EURUSD", "USDJPY", "XAUUSD", "NAS100", "BTCUSD", "ETHUSD"]
selected_market = st.selectbox(
    "🌍 Select Trading Market:",
    markets,
    index=markets.index(st.session_state["selected_market"]),
    help="Currently, full data is available for GBP/JPY only"
)
st.session_state["selected_market"] = selected_market

# Market availability notice
if selected_market != "GBPJPY":
    st.warning(f"⚠️ {selected_market} market data is not accessible. Please select GBP/JPY for full functionality.")

if not st.session_state["logged_in"]:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.markdown("### 🔐 Secure Access Portal")

    # Quick stats display
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-number">6</span>
            <span class="stat-label">Timeframes</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login form
    password = st.text_input("🔑 Access Password", type="password", placeholder="Enter your secure password")

    col1, col2 = st.columns(2)
    with col1:
        login_btn = st.button("🚀 Login", use_container_width=True)
    with col2:
        st.button("❓ Help", use_container_width=True, help="Contact admin for password")

    if login_btn and password:
        if password == "qfpass123":
            st.session_state["logged_in"] = True
            st.session_state["login_attempts"] = 0
            st.markdown('<div class="success-animation">', unsafe_allow_html=True)
            st.success("✅ Login Successful! Redirecting...")
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        else:
            st.session_state["login_attempts"] += 1
            st.error(f"❌ Incorrect Password (Attempt {st.session_state['login_attempts']})")
            if st.session_state["login_attempts"] >= 3:
                st.warning("🔒 Multiple failed attempts detected. Contact administrator.")

    # Features showcase
    st.markdown("""
    <div class="feature-list">
        <h4>🎯 Platform Features</h4>
        <div class="feature-item">📊 Real-time Market Profile Analysis</div>
        <div class="feature-item">🔥 Z-Score Anomaly Detection</div>
        <div class="feature-item">📈 Interactive Flow Visualizations</div>
        <div class="feature-item">⚡ Custom Metric Calculations</div>
        <div class="feature-item">🎨 Professional UI/UX Design</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Success state
    st.markdown('<div class="success-animation">', unsafe_allow_html=True)
    st.success(f"✅ Welcome! You are logged in and analyzing {selected_market}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick navigation
    st.markdown("### 🧭 Quick Navigation")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Summary Dashboard", use_container_width=True):
            st.switch_page("pages/1_Summary_Tab.py")

    with col2:
        if st.button("🔥 Z-Score Heatmap", use_container_width=True):
            st.switch_page("pages/2_Z-Score_Heatmap.py")

    with col3:
        if st.button("📈 Metric Visualizer", use_container_width=True):
            st.switch_page("pages/3_Metric_Visualizer.py")

    # Market status
    st.info(f"🎯 Current Market: **{selected_market}** | Status: {'🟢 Active Data' if selected_market == 'GBPJPY' else '🔴 Limited Data'}")

    # Logout option
    if st.button("🚪 Logout", help="Return to login screen"):
        st.session_state["logged_in"] = False
        st.rerun()