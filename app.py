import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
import base64
from datetime import datetime

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Now import from src
try:
    from data_loader import ClinicalDataLoader
    from data_integrator import DataIntegrator
    from multi_study_loader import MultiStudyClinicalDataLoader
    from cross_study_analyzer import CrossStudyAnalyzer
    from study_comparator import StudyComparator
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please make sure you have src/__init__.py file")
    st.stop()

# ============================================
# CREATE OUTPUT FOLDER
# ============================================
output_folder = "outputs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ============================================
# BACKGROUND IMAGE FUNCTION (IMPROVED - 50% VISIBILITY)
# ============================================
def add_bg_from_local(image_file, opacity=0.5):
    """Add background image to the app with adjustable opacity"""
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    
    # Calculate rgba color for overlay
    overlay_opacity = 1 - opacity
    
    bg_image = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, {overlay_opacity}), 
                         rgba(255, 255, 255, {overlay_opacity})), 
                         url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-blend-mode: overlay;
    }}
    
    /* Make content areas more visible */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin-top: 1.5rem;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(0, 0, 0, 0.1);
    }}
    
    /* Improve text visibility */
    .stMarkdown, .stText, .stDataFrame, .metric-value {{
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

def add_bg_from_url(url, opacity=0.5):
    """Add background image from URL with adjustable opacity"""
    overlay_opacity = 1 - opacity
    
    bg_image = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, {overlay_opacity}), 
                         rgba(255, 255, 255, {overlay_opacity})), 
                         url("{url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-blend-mode: overlay;
    }}
    
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin-top: 1.5rem;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(0, 0, 0, 0.1);
    }}
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

# ============================================
# THEME FUNCTIONS WITH IMPROVED TEXT VISIBILITY
# ============================================
def apply_theme(theme_name):
    """Apply different color themes with better text color contrast"""
    themes = {
        "Default Blue": {
            "primary": "#3B82F6",
            "secondary": "#1E40AF",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#DC2626",
            "background": "#FFFFFF",
            "text_primary": "#111827",  # Darker text for better visibility
            "text_secondary": "#374151",  # Darker secondary text
            "card_bg": "#FFFFFF",
            "chart_bg": "#FFFFFF"
        },
        "Medical Green": {
            "primary": "#059669",
            "secondary": "#047857",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#DC2626",
            "background": "#F0FDF4",
            "text_primary": "#064E3B",  # Dark green text
            "text_secondary": "#065F46",
            "card_bg": "#FFFFFF",
            "chart_bg": "#FFFFFF"
        },
        "Dark Mode": {
            "primary": "#8B5CF6",
            "secondary": "#7C3AED",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#EF4444",
            "background": "#0F172A",
            "text_primary": "#F1F5F9",  # Light text for dark background
            "text_secondary": "#CBD5E1",
            "card_bg": "#1E293B",
            "chart_bg": "#1E293B"
        },
        "Warm Orange": {
            "primary": "#F97316",
            "secondary": "#EA580C",
            "success": "#22C55E",
            "warning": "#EAB308",
            "danger": "#EF4444",
            "background": "#FFFBEB",
            "text_primary": "#431407",  # Very dark orange/brown text
            "text_secondary": "#7C2D12",
            "card_bg": "#FFFFFF",
            "chart_bg": "#FFFFFF"
        },
        "Professional Purple": {
            "primary": "#7C3AED",
            "secondary": "#6D28D9",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#DC2626",
            "background": "#FAF5FF",
            "text_primary": "#4C1D95",  # Dark purple text
            "text_secondary": "#5B21B6",
            "card_bg": "#FFFFFF",
            "chart_bg": "#FFFFFF"
        }
    }
    
    theme = themes.get(theme_name, themes["Default Blue"])
    
    theme_css = f"""
    <style>
    /* Global text colors with high contrast */
    .stMarkdown, .stText, .stDataFrame, p, h1, h2, h3, h4, h5, h6, div, span {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Metric values with strong contrast */
    .metric-value, .stMetric {{
        color: {theme['text_primary']} !important;
        font-weight: 700 !important;
    }}
    
    /* Dataframes and tables */
    .stDataFrame, .dataframe {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Main header with enhanced styling */
    .main-header {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem !important;
        padding-bottom: 1rem !important;
        border-bottom: 3px solid {theme['primary']};
    }}
    
    /* Subheaders with better contrast */
    .stSubheader, h2, h3 {{
        color: {theme['secondary']} !important;
        border-left: 4px solid {theme['primary']};
        padding-left: 1rem;
        margin-top: 2rem !important;
        font-weight: 700 !important;
    }}
    
    /* Metric cards with theme colors */
    .metric-card {{
        background: {theme['card_bg']};
        border: 1px solid rgba(0,0,0,0.1);
    }}
    
    .metric-card.critical {{ 
        border-left-color: {theme['danger']} !important;
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, {theme['card_bg']} 100%);
    }}
    .metric-card.warning {{ 
        border-left-color: {theme['warning']} !important;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, {theme['card_bg']} 100%);
    }}
    .metric-card.good {{ 
        border-left-color: {theme['success']} !important;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, {theme['card_bg']} 100%);
    }}
    .metric-card.info {{ 
        border-left-color: {theme['primary']} !important;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, {theme['card_bg']} 100%);
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white !important;
        font-weight: 600;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, {theme['secondary']} 0%, {theme['primary']} 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }}
    
    /* Tabs */
    .stTabs [aria-selected="true"] {{
        background-color: {theme['primary']} !important;
        color: white !important;
    }}
    
    /* Background for the app */
    .stApp {{
        background-color: {theme['background']};
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {theme['card_bg']};
    }}
    
    /* Links and interactive elements */
    a {{
        color: {theme['primary']} !important;
        font-weight: 600 !important;
    }}
    
    /* Alert boxes */
    .stAlert.success {{
        background-color: rgba(16, 185, 129, 0.1);
        border-left-color: {theme['success']};
        color: {theme['text_primary']} !important;
    }}
    .stAlert.warning {{
        background-color: rgba(245, 158, 11, 0.1);
        border-left-color: {theme['warning']};
        color: {theme['text_primary']} !important;
    }}
    .stAlert.error {{
        background-color: rgba(220, 38, 38, 0.1);
        border-left-color: {theme['danger']};
        color: {theme['text_primary']} !important;
    }}
    .stAlert.info {{
        background-color: rgba(59, 130, 246, 0.1);
        border-left-color: {theme['primary']};
        color: {theme['text_primary']} !important;
    }}
    
    /* Plotly chart backgrounds */
    .js-plotly-plot {{
        background-color: {theme['chart_bg']} !important;
    }}
    
    /* Selectbox and input fields */
    .stSelectbox, .stTextInput, .stNumberInput {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Radio buttons */
    .stRadio label {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Expander headers */
    .streamlit-expanderHeader {{
        color: {theme['text_primary']} !important;
        font-weight: 600 !important;
    }}
    </style>
    """
    
    st.markdown(theme_css, unsafe_allow_html=True)
    return theme

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Integrated Trial Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True

if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "Default Blue"

if 'bg_opacity' not in st.session_state:
    st.session_state.bg_opacity = 0.5

if 'custom_bg_path' not in st.session_state:
    st.session_state.custom_bg_path = None

if 'ai_responses' not in st.session_state:
    st.session_state.ai_responses = {}

# Initialize multi-study session states
if 'multi_loader' not in st.session_state:
    st.session_state.multi_loader = None
if 'studies_discovered' not in st.session_state:
    st.session_state.studies_discovered = []

# ============================================
# CUSTOM CSS (UPDATED WITH BETTER VISIBILITY)
# ============================================
st.markdown("""
<style>
    /* Enhanced Main header */
    .main-header {
        font-size: 3.2rem !important;
        text-align: center;
        margin-bottom: 2.5rem !important;
        padding: 1.5rem;
        font-weight: 900 !important;
        letter-spacing: -1px !important;
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 25%;
        width: 50%;
        height: 4px;
        border-radius: 2px;
    }
    
    /* Enhanced Metric cards */
    .metric-card {
        padding: 1.8rem !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12) !important;
        margin: 0.8rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 140px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Dataframe styling with better visibility */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.85rem 2.2rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Sidebar toggle button */
    .sidebar-toggle {
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 9999 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
        border: 2px solid white !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    
    .sidebar-toggle:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }
    
    /* Hide hamburger menu */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Enhanced expander */
    .streamlit-expanderHeader {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 1rem 1.5rem !important;
        margin: 0.5rem 0 !important;
        color: #111827 !important;
    }
    
    /* Chart containers with better visibility */
    .js-plotly-plot {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1) !important;
        padding: 1rem !important;
        background: white !important;
    }
    
    /* Plotly text color fixes */
    .gtitle, .xtitle, .ytitle, .legendtext {
        fill: #111827 !important;
        color: #111827 !important;
    }
    
    /* Text input enhancement */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.75rem 1rem !important;
        color: #111827 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Selectbox enhancement */
    .stSelectbox > div > div {
        border-radius: 10px !important;
    }
    
    /* Radio button enhancement */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }
    
    .stRadio label {
        color: #111827 !important;
        font-weight: 500 !important;
    }
    
    /* Badge styling for status */
    .status-badge {
        display: inline-block !important;
        padding: 0.25rem 0.75rem !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Floating action button */
    .fab {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        z-index: 1000 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
        font-size: 1.5rem !important;
    }
    
    .fab:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
    }
    
    /* Table text color fix */
    table {
        color: #111827 !important;
    }
    
    /* Strong text for better visibility */
    strong, b {
        color: #111827 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR TOGGLE BUTTON
# ============================================
toggle_html = f"""
<div class="sidebar-toggle" onclick="toggleSidebar()">
    {'◀' if st.session_state.sidebar_visible else '▶'}
</div>

<script>
function toggleSidebar() {{
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    const event = new CustomEvent('toggleSidebar');
    if (sidebar) {{
        if (sidebar.style.display === 'none') {{
            sidebar.style.display = 'block';
        }} else {{
            sidebar.style.display = 'none';
        }}
    }}
    window.dispatchEvent(event);
}}
</script>
"""

st.markdown(toggle_html, unsafe_allow_html=True)

# ============================================
# SIDEBAR (CONDITIONAL)
# ============================================
if st.session_state.sidebar_visible:
    with st.sidebar:
        # Logo with enhanced styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("/Users/aquib/Downloads/Integrated Trial Monitor/assets/images/logo.png", width=500)
        
        st.markdown("---")
        
        # Enhanced title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #1E40AF; font-weight: 800; margin-bottom: 0.5rem;">📊 NAVIGATION</h2>
            <p style="color: #6B7280; font-size: 0.9rem;">Clinical Trial Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        sections = [
            "📊 Dashboard Overview",
            "👥 Patient Analytics",
            "🔬 Multi-Study Analytics",
            "📈 Data Quality Metrics",
            "⚠️ Risk Monitoring",
            "🔍 Data Explorer",
            "🤖 AI Insights",
            "⚙️ Settings"
        ]
        
        selected_section = st.radio("", sections, label_visibility="collapsed")
        
        st.markdown("---")
        
        # Quick Settings Section
        st.markdown("""
        <div style="text-align: center; margin: 1.5rem 0;">
            <h3 style="color: #1E40AF; font-weight: 700;">⚙️ QUICK SETTINGS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme selector
        theme_options = ["Default Blue", "Medical Green", "Dark Mode", "Warm Orange", "Professional Purple"]
        new_theme = st.selectbox("🎨 Theme", theme_options, 
                                index=theme_options.index(st.session_state.current_theme),
                                label_visibility="collapsed")
        
        if new_theme != st.session_state.current_theme:
            st.session_state.current_theme = new_theme
            st.rerun()
        
        # Hide sidebar button
        if st.button("👁️ Hide Sidebar", use_container_width=True):
            st.session_state.sidebar_visible = False
            st.rerun()
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border-radius: 10px;">
            <p style="color: #4B5563; font-weight: 600; margin-bottom: 0.5rem;">Integrated Trial Monitor</p>
            <p style="color: #6B7280; font-size: 0.8rem; margin: 0;">v2.0 • Clinical Excellence</p>
        </div>
        """, unsafe_allow_html=True)
else:
    selected_section = st.session_state.get('last_section', "📊 Dashboard Overview")
    
    # Show a minimal header when sidebar is hidden
    col1, col2 = st.columns([1, 20])
    with col1:
        if st.button("▶", help="Show Sidebar", use_container_width=True):
            st.session_state.sidebar_visible = True
            st.rerun()
    with col2:
        st.markdown(f"### 🏥 {selected_section}")

# Store the selected section
st.session_state.last_section = selected_section

# ============================================
# APPLY SELECTED THEME
# ============================================
current_theme = apply_theme(st.session_state.current_theme)

# ============================================
# ENHANCED TITLE (ONLY SHOW WHEN SIDEBAR IS VISIBLE)
# ============================================
if st.session_state.sidebar_visible:
    st.markdown("""
    <div style="text-align: center; padding: 0.1rem 0 0.3rem 0;">
        <h1 class="main-header">INTEGRATED TRIAL MONITOR</h1>
        <p style="font-size: 1.2rem; color: #6B7280; max-width: 800px; margin: 0 auto; line-height: 1.6;">
            Advanced Clinical Trial Analytics & Monitoring Platform • Real-time Insights • AI-Powered Decision Support
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTION (UPDATED)
# ============================================
@st.cache_resource(show_spinner=False)
def load_and_process_data():
    """Load and process clinical trial data"""
    try:
        # Initialize loader
        loader = ClinicalDataLoader("data")
        
        # Load data
        with st.spinner("📂 Loading data from Excel files..."):
            data = loader.load_all_data()
        
        # Initialize integrator
        integrator = DataIntegrator(loader)
        
        # Process data
        with st.spinner("🔧 Processing and integrating data..."):
            patient_data = integrator.create_unified_patient_view()
            patient_metrics = integrator.calculate_patient_metrics()
            summary_stats = integrator.get_summary_stats()
        
        return {
            'loader': loader,
            'integrator': integrator,
            'data': data,
            'patient_data': patient_metrics,
            'summary': summary_stats,
            'success': True
        }
    
    except FileNotFoundError as e:
        st.error(f"❌ Data folder error: {str(e)}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return {'success': False, 'error': str(e)}

# ============================================
# MULTI-STUDY DASHBOARD SECTION (FIXED)
# ============================================
def render_multi_study_dashboard():
    """Render multi-study comparison dashboard"""
    st.header("🔬 Multi-Study Analytics Dashboard")
    
    # Initialize multi-study loader
    if st.session_state.multi_loader is None:
        with st.spinner("Discovering studies..."):
            try:
                multi_loader = MultiStudyClinicalDataLoader("data")
                studies = multi_loader.studies  # Fixed: Use studies attribute instead of discover_studies()
                st.session_state.multi_loader = multi_loader
                st.session_state.studies_discovered = list(studies.keys())
                st.success(f"✅ Discovered {len(studies)} studies")
            except Exception as e:
                st.error(f"❌ Failed to discover studies: {str(e)}")
                return
    
    multi_loader = st.session_state.multi_loader
    
    if not multi_loader.studies:
        st.warning("No studies found in the data folder. Please ensure studies are organized in subdirectories.")
        return
    
    # Study selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_studies = st.multiselect(
            "Select Studies to Analyze",
            options=st.session_state.studies_discovered,
            default=st.session_state.studies_discovered[:3] if len(st.session_state.studies_discovered) >= 3 else st.session_state.studies_discovered
        )
    
    with col2:
        if st.button("📊 Load Selected Studies", type="primary", use_container_width=True):
            if selected_studies:
                with st.spinner(f"Loading {len(selected_studies)} studies..."):
                    for study_id in selected_studies:
                        multi_loader.load_study(study_id)
                    st.success(f"✅ Loaded {len(selected_studies)} studies")
                    st.rerun()
            else:
                st.warning("Please select at least one study")
    
    if selected_studies and all(study_id in multi_loader.study_data for study_id in selected_studies):
        # Create analyzer
        try:
            analyzer = CrossStudyAnalyzer(multi_loader)
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Study Comparison",
                "📈 Metrics Overview",
                "🎯 Performance Analysis",
                "📋 Detailed Reports"
            ])
            
            with tab1:
                st.subheader("Cross-Study Comparison")
                
                # Comparison metric selection
                comparison_metric = st.selectbox(
                    "Select Metric for Comparison",
                    options=['Data_Quality_Score', 'Estimated_Patients', 'Issue_Count', 'SAE_Count']
                )
                
                # Comparison chart
                try:
                    fig = analyzer.compare_studies(comparison_metric)
                    # Update chart text colors for better visibility
                    fig.update_layout(
                        font=dict(color=current_theme['text_primary']),
                        plot_bgcolor=current_theme['chart_bg'],
                        paper_bgcolor=current_theme['chart_bg']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not generate comparison chart: {str(e)}")
                
                # Heatmap
                st.subheader("Metrics Heatmap")
                try:
                    heatmap_fig = analyzer.create_study_heatmap()
                    # Update heatmap text colors
                    heatmap_fig.update_layout(
                        font=dict(color=current_theme['text_primary']),
                        plot_bgcolor=current_theme['chart_bg'],
                        paper_bgcolor=current_theme['chart_bg']
                    )
                    st.plotly_chart(heatmap_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not generate heatmap: {str(e)}")
            
            with tab2:
                st.subheader("Study Metrics Overview")
                
                try:
                    metrics_df = analyzer.calculate_study_metrics()
                    st.dataframe(metrics_df, use_container_width=True, height=400)
                    
                    # Export metrics
                    csv = metrics_df.to_csv(index=False)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"study_metrics_{timestamp}.csv"
                    
                    st.download_button(
                        label="📥 Download Study Metrics",
                        data=csv,
                        file_name=filename,
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Could not calculate study metrics: {str(e)}")
            
            with tab3:
                st.subheader("Performance Analysis")
                
                # Top performers
                top_n = st.slider("Show Top N Studies", 3, 10, 5)
                
                try:
                    top_performers = analyzer.identify_top_performers(top_n)
                    
                    st.write(f"**Top {top_n} Performing Studies:**")
                    st.dataframe(top_performers, use_container_width=True)
                    
                    # Performance insights
                    report = analyzer.generate_cross_study_report()
                    
                    st.subheader("Key Insights")
                    if 'recommendations' in report and report['recommendations']:
                        for insight in report.get('recommendations', []):
                            st.info(insight)
                    else:
                        st.info("No specific recommendations available for the selected studies.")
                except Exception as e:
                    st.error(f"Could not analyze performance: {str(e)}")
            
            with tab4:
                st.subheader("Detailed Study Reports")
                
                for study_id in selected_studies:
                    with st.expander(f"📁 Study: {study_id}", expanded=False):
                        if study_id in multi_loader.study_data:
                            study_data = multi_loader.study_data[study_id]
                            
                            # Study summary
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("📄 Files Loaded", len(study_data['files']))
                            with col2:
                                st.metric("🔍 Status", "Active")
                            with col3:
                                try:
                                    dq_score = analyzer.calculate_study_dq_score(study_data['files'])
                                    st.metric("📊 Data Quality", f"{dq_score:.1f}/100")
                                except:
                                    st.metric("📊 Data Quality", "N/A")
                            
                            # File list
                            st.write("**Files in this study:**")
                            for file_name in study_data['files'].keys():
                                st.write(f"- {file_name}")
                        else:
                            st.warning(f"Study data not available for {study_id}")
            
        except Exception as e:
            st.error(f"Failed to initialize analyzer: {str(e)}")
    else:
        st.info("👈 Select studies and click 'Load Selected Studies' to begin multi-study analysis")
        
        # Show available studies
        if st.session_state.studies_discovered:
            st.write("**Available Studies:**")
            for study in st.session_state.studies_discovered[:10]:  # Show first 10
                st.write(f"- {study}")
            if len(st.session_state.studies_discovered) > 10:
                st.write(f"... and {len(st.session_state.studies_discovered) - 10} more")
        else:
            st.warning("No studies discovered. Check your data folder structure.")

# ============================================
# AI AGENT FUNCTION (UPDATED WITH REAL DATA)
# ============================================
def get_ai_response(query, patient_data, summary, integrator):
    """Get AI response based on query"""
    query_key = query.lower().strip()
    
    # Cache responses
    if query_key in st.session_state.ai_responses:
        return st.session_state.ai_responses[query_key]
    
    response = ""
    
    try:
        if "missing" in query_key or ("data" in query_key and "quality" in query_key):
            # Use actual data quality score from summary
            avg_score = summary.get('avg_data_quality_score', 0)
            total_patients = summary.get('total_patients', 0)
            
            response += f"**📊 Data Quality Analysis:**\n\n"
            response += f"- **Average Data Quality Score**: {avg_score:.1f}/100\n"
            response += f"- **Total Patients Analyzed**: {total_patients}\n"
            response += f"- **Clean Patients**: {summary.get('clean_percentage', 0)}%\n"
            response += f"- **Critical Patients**: {summary.get('critical_patients', 0)}\n\n"
            
            if avg_score < 70:
                response += "**⚠️ Action Required:** Data quality is below target. Consider implementing additional quality checks.\n"
            elif avg_score < 80:
                response += "**📈 Opportunity:** Data quality is acceptable but could be improved with better data entry processes.\n"
            else:
                response += "**✅ Excellent:** Data quality is meeting or exceeding expectations.\n"
        
        elif "critical" in query_key or "urgent" in query_key:
            if 'Patient_Status' in patient_data.columns:
                critical = patient_data[patient_data['Patient_Status'] == 'Critical']
                if len(critical) > 0:
                    response += f"**🚨 Critical Patients ({len(critical)} found):**\n\n"
                    for _, row in critical.head(5).iterrows():
                        response += f"- **Patient {row['Patient_ID']}**: Score: {row.get('Data_Quality_Score', 0):.1f}, Issues: {row.get('Issue_Count', 0)}\n"
                    response += "\n**⚠️ Action Required:** These patients need immediate attention to prevent trial delays."
                else:
                    response += "**✅ No Critical Patients:** All patients are in good standing."
            else:
                response += "**📊 Status Information:** Patient status data not available in current analysis."
        
        elif "sae" in query_key or "safety" in query_key:
            # Try to find SAE data in patient data
            sae_columns = [col for col in patient_data.columns if 'sae' in str(col).lower() or 'adverse' in str(col).lower()]
            if sae_columns:
                sae_count = patient_data[sae_columns[0]].sum() if sae_columns else 0
                response += f"**⚠️ Safety Analysis:**\n\n"
                response += f"- **SAEs Detected**: {sae_count}\n"
                response += "\n**🔍 Recommendation:** Review safety profiles and consider additional monitoring."
            else:
                response += "**📋 Safety Data:** No SAE-specific columns found in the current data analysis."
        
        elif "trend" in query_key or "pattern" in query_key:
            response += "**📈 Data Trends Identified:**\n\n"
            
            # Use actual data if available
            if not patient_data.empty:
                if 'Data_Quality_Score' in patient_data.columns:
                    score_trend = "stable"
                    mean_score = patient_data['Data_Quality_Score'].mean()
                    if mean_score > 80:
                        score_trend = "improving"
                    elif mean_score < 60:
                        score_trend = "declining"
                    
                    response += f"1. **Overall Trend**: Data quality is {score_trend} (average score: {mean_score:.1f}/100)\n"
                
                if 'Issue_Count' in patient_data.columns:
                    avg_issues = patient_data['Issue_Count'].mean()
                    response += f"2. **Issue Pattern**: Average {avg_issues:.1f} issues per patient\n"
            
            response += "3. **Recommendation**: Regular data quality audits can improve overall data integrity\n"
            response += "4. **Insight**: Proactive monitoring reduces data issues by up to 40%\n\n"
            response += "**💡 Next Step**: Consider implementing automated data validation checks"
        
        elif "summary" in query_key or "overview" in query_key:
            response += f"**📊 Study Overview:**\n\n"
            response += f"- **Total Patients**: {summary.get('total_patients', 0)}\n"
            response += f"- **Data Quality Index**: {summary.get('avg_data_quality_score', 0):.1f}/100\n"
            response += f"- **Clean Patients**: {summary.get('clean_percentage', 0)}%\n"
            response += f"- **Critical Patients**: {summary.get('critical_patients', 0)}\n"
            response += f"- **Studies Analyzed**: {summary.get('total_studies', 0)}\n\n"
            
            if summary.get('avg_data_quality_score', 0) > 75:
                response += "**🎯 Status**: Data quality is meeting expectations. Continue current practices."
            else:
                response += "**🎯 Priority**: Focus on improving data quality through training and validation."
        
        elif "recommend" in query_key or "suggestion" in query_key:
            response += "**💡 AI Recommendations:**\n\n"
            
            recommendations = []
            avg_score = summary.get('avg_data_quality_score', 0)
            
            if avg_score < 70:
                recommendations.append("**Implement data quality training** for data entry staff")
            
            if summary.get('critical_patients', 0) > 0:
                recommendations.append("**Establish rapid response team** for critical patient cases")
            
            if summary.get('total_studies', 0) > 5:
                recommendations.append("**Standardize data collection** across all studies")
            
            if len(recommendations) > 0:
                for i, rec in enumerate(recommendations, 1):
                    response += f"{i}. {rec}\n"
            else:
                response += "Current operations are meeting quality standards. Continue current practices."
        
        else:
            # General response for other queries
            response += f"**🤖 AI Analysis for: \"{query}\"**\n\n"
            response += "Based on my analysis of the clinical trial data:\n\n"
            response += "**📈 Key Findings:**\n"
            response += f"- Study has {summary.get('total_patients', 0)} patients with average quality score of {summary.get('avg_data_quality_score', 0):.1f}/100\n"
            response += f"- {summary.get('clean_percentage', 0)}% of patients are in 'Clean' status\n"
            response += f"- {summary.get('critical_patients', 0)} patients require immediate attention\n\n"
            response += "**🎯 Suggested Actions:**\n"
            response += "1. Review patients with 'Critical' status\n"
            response += "2. Implement data quality improvement initiatives\n"
            response += "3. Schedule regular data review meetings\n"
            response += "4. Consider cross-study standardization\n\n"
            response += "**📊 Next Steps:** Ask specific questions about data quality, safety, or trends for detailed insights."
        
        # Cache the response
        st.session_state.ai_responses[query_key] = response
        
    except Exception as e:
        response = f"**⚠️ AI Analysis Error:**\n\nI encountered an error while processing your query: {str(e)}\n\nPlease try rephrasing your question or contact support."
    
    return response

# ============================================
# EXPORT FUNCTION WITH OUTPUT FOLDER
# ============================================
def export_to_csv(data, filename_prefix, section):
    """Export data to CSV in outputs folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{section}_{timestamp}.csv"
    filepath = os.path.join(output_folder, filename)
    
    data.to_csv(filepath, index=False)
    
    # Read file for download
    with open(filepath, 'rb') as f:
        csv_data = f.read()
    
    return csv_data, filename

# ============================================
# LOAD DATA
# ============================================
data_result = load_and_process_data()

if not data_result['success']:
    st.error("Failed to load data. Please check:")
    st.error("1. Ensure 'data' folder exists in project root")
    st.error("2. Ensure Excel files are in the 'data' folder")
    st.error("3. Check file names match expected names")
    st.stop()

# Extract data
loader = data_result['loader']
integrator = data_result['integrator']
patient_data = data_result['patient_data']
summary = data_result['summary']

# ============================================
# BACKGROUND IMAGE SETUP
# ============================================
if st.session_state.custom_bg_path and os.path.exists(st.session_state.custom_bg_path):
    add_bg_from_local(st.session_state.custom_bg_path, opacity=st.session_state.bg_opacity)
else:
    # Try default path, if not found, use no background
    image_path = "/Users/aquib/Downloads/Integrated Trial Monitor/assets/images/dashboard_bg.jpg"
    if os.path.exists(image_path):
        add_bg_from_local(image_path, opacity=st.session_state.bg_opacity)
    else:
        st.info("ℹ️ Background image not found. Using theme colors only.")

# ============================================
# FLOATING ACTION BUTTON FOR QUICK ACTIONS
# ============================================
st.markdown("""
<div class="fab" onclick="showQuickActions()">
    ⚡
</div>

<script>
function showQuickActions() {
    alert('Quick Actions:\\n1. Export Current View\\n2. Refresh Data\\n3. Generate Report\\n4. Contact Support');
}
</script>
""", unsafe_allow_html=True)

# ============================================
# MAIN CONTENT - DASHBOARD OVERVIEW (FIXED)
# ============================================
if selected_section == "📊 Dashboard Overview":
    st.header("📈 Executive Dashboard")
    
    # Summary metrics in a nice grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card info">', unsafe_allow_html=True)
        st.metric("👥 Total Patients", summary.get('total_patients', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card good">', unsafe_allow_html=True)
        clean_pct = summary.get('clean_percentage', 0)
        st.metric("✅ Clean Patients", 
                 f"{summary.get('clean_patients', 0)}",
                 f"{clean_pct}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card warning">', unsafe_allow_html=True)
        critical_pct = summary.get('critical_percentage', 0)
        st.metric("⚠️ Needs Review", 
                 f"{summary.get('needs_review_patients', 0)}",
                 f"{critical_pct}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card critical">', unsafe_allow_html=True)
        st.metric("🚨 Critical Patients", 
                 f"{summary.get('critical_patients', 0)}",
                 delta="-Action Required" if summary.get('critical_patients', 0) > 0 else "All Good")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card info">', unsafe_allow_html=True)
        st.metric("📊 Avg Quality Score", f"{summary.get('avg_data_quality_score', 0):.1f}/100")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card info">', unsafe_allow_html=True)
        st.metric("📚 Total Studies", summary.get('total_studies', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card info">', unsafe_allow_html=True)
        st.metric("📄 Data Files", summary.get('total_dataframes', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        # Calculate issue count based on available data
        if 'Issue_Count' in patient_data.columns:
            total_issues = patient_data['Issue_Count'].sum()
        else:
            total_issues = 0
        
        st.markdown('<div class="metric-card warning">', unsafe_allow_html=True)
        st.metric("📝 Total Issues", int(total_issues))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export dashboard data
    if st.button("📥 Export Dashboard Data", type="primary"):
        csv_data, filename = export_to_csv(patient_data, "dashboard", "overview")
        st.download_button(
            label=f"Download {filename}",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
        st.success(f"✅ Data exported to {output_folder}/{filename}")
    
    # Charts section
    st.subheader("📊 Visual Analytics")
    
    if not patient_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Patient Status Distribution (with safe column check)
            if 'Patient_Status' in patient_data.columns:
                status_counts = patient_data['Patient_Status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                fig1 = px.pie(
                    status_counts,
                    values='Count',
                    names='Status',
                    title="Patient Status Distribution",
                    color='Status',
                    color_discrete_map={
                        'Clean': current_theme['success'],
                        'Needs Review': current_theme['warning'],
                        'Critical': current_theme['danger']
                    },
                    hole=0.4
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                # Update text colors for visibility
                fig1.update_layout(
                    font=dict(color=current_theme['text_primary']),
                    paper_bgcolor=current_theme['chart_bg']
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Patient status data not available for visualization")
        
        with col2:
            # Data Quality Score Distribution (with safe column check)
            if 'Data_Quality_Score' in patient_data.columns:
                fig2 = px.histogram(
                    patient_data,
                    x='Data_Quality_Score',
                    nbins=20,
                    title="Data Quality Score Distribution",
                    color_discrete_sequence=[current_theme['primary']],
                    opacity=0.8
                )
                fig2.update_layout(
                    xaxis_title="Data Quality Score",
                    yaxis_title="Number of Patients",
                    bargap=0.1,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor=current_theme['chart_bg'],
                    font=dict(color=current_theme['text_primary'])
                )
                # Add vertical line for average
                fig2.add_vline(
                    x=summary.get('avg_data_quality_score', 0),
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Avg: {summary.get('avg_data_quality_score', 0):.1f}",
                    annotation_font=dict(color=current_theme['text_primary'])
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Data quality scores not available for visualization")
    
    # Issue Breakdown (simplified based on available data)
    st.subheader("📋 Data Analysis")
    
    if not patient_data.empty:
        # Create analysis based on available columns
        analysis_items = []
        
        if 'Data_Quality_Score' in patient_data.columns:
            avg_score = patient_data['Data_Quality_Score'].mean()
            analysis_items.append(['Average Quality Score', f"{avg_score:.1f}/100", 'Medium'])
        
        if 'Issue_Count' in patient_data.columns:
            total_issues = patient_data['Issue_Count'].sum()
            analysis_items.append(['Total Issues', total_issues, 'High'])
        
        if 'Patient_Status' in patient_data.columns:
            critical_count = (patient_data['Patient_Status'] == 'Critical').sum()
            analysis_items.append(['Critical Patients', critical_count, 'Critical'])
        
        # Add basic metrics
        analysis_items.append(['Total Patients', summary.get('total_patients', 0), 'Info'])
        analysis_items.append(['Studies Analyzed', summary.get('total_studies', 0), 'Info'])
        
        if analysis_items:
            analysis_df = pd.DataFrame(analysis_items, columns=['Metric', 'Value', 'Severity'])
            
            fig3 = px.bar(
                analysis_df,
                x='Metric',
                y='Value',
                color='Severity',
                title="Key Metrics Analysis",
                color_discrete_map={
                    'Critical': current_theme['danger'],
                    'High': current_theme['warning'],
                    'Medium': current_theme['primary'],
                    'Info': current_theme['success']
                },
                text='Value'
            )
            fig3.update_traces(textposition='outside')
            fig3.update_layout(
                xaxis_title="Metric",
                yaxis_title="Value",
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor=current_theme['chart_bg'],
                font=dict(color=current_theme['text_primary'])
            )
            st.plotly_chart(fig3, use_container_width=True)

# ============================================
# MAIN CONTENT - PATIENT ANALYTICS (FIXED)
# ============================================
elif selected_section == "👥 Patient Analytics":
    st.header("👤 Patient-Level Analytics")
    
    if patient_data.empty:
        st.warning("No patient data available")
        st.stop()
    
    # Determine available columns for display
    available_cols = patient_data.columns.tolist()
    
    # Default display columns (only include those that exist)
    default_display_cols = ['Patient_ID', 'Data_Quality_Score', 'Patient_Status', 'Risk_Level']
    
    # Add additional columns if they exist
    optional_cols = ['Record_Count', 'Source_Count', 'Study_Count', 'Issue_Count']
    for col in optional_cols:
        if col in available_cols:
            default_display_cols.append(col)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'Data_Quality_Score' in patient_data.columns:
            min_score = st.slider("🎯 Minimum Data Quality Score", 0, 100, 0)
        else:
            min_score = 0
            st.info("Data quality score not available")
    
    with col2:
        if 'Patient_Status' in patient_data.columns:
            status_options = ['All'] + sorted(patient_data['Patient_Status'].unique().tolist())
            selected_status = st.selectbox("📊 Filter by Status", status_options)
        else:
            selected_status = 'All'
            st.info("Patient status not available")
    
    with col3:
        if 'Risk_Level' in patient_data.columns:
            risk_options = ['All'] + sorted(patient_data['Risk_Level'].unique().tolist())
            selected_risk = st.selectbox("⚠️ Filter by Risk Level", risk_options)
        else:
            selected_risk = 'All'
            st.info("Risk level not available")
    
    # Apply filters
    filtered_data = patient_data.copy()
    
    if 'Data_Quality_Score' in patient_data.columns:
        filtered_data = filtered_data[filtered_data['Data_Quality_Score'] >= min_score]
    
    if selected_status != 'All' and 'Patient_Status' in patient_data.columns:
        filtered_data = filtered_data[filtered_data['Patient_Status'] == selected_status]
    
    if selected_risk != 'All' and 'Risk_Level' in patient_data.columns:
        filtered_data = filtered_data[filtered_data['Risk_Level'] == selected_risk]
    
    # Display stats
    st.subheader(f"📋 Showing {len(filtered_data)} Patients")
    
    if len(filtered_data) > 0:
        # Display as table
        display_cols = [col for col in default_display_cols if col in filtered_data.columns]
        
        # Sort options based on available columns
        available_sort_cols = [col for col in ['Data_Quality_Score', 'Issue_Count', 'Record_Count'] if col in filtered_data.columns]
        if not available_sort_cols:
            available_sort_cols = list(filtered_data.columns)
        
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("🔽 Sort by", available_sort_cols)
        
        with col2:
            sort_order = st.radio("📈 Sort order", ['Ascending', 'Descending'], horizontal=True)
        
        if sort_order == 'Descending':
            filtered_data = filtered_data.sort_values(sort_by, ascending=False)
        else:
            filtered_data = filtered_data.sort_values(sort_by, ascending=True)
        
        # Simple display with formatted numbers
        formatted_df = filtered_data[display_cols].copy()
        if 'Data_Quality_Score' in formatted_df.columns:
            formatted_df['Data_Quality_Score'] = formatted_df['Data_Quality_Score'].map('{:.1f}'.format)
        
        st.dataframe(
            formatted_df,
            use_container_width=True,
            height=400
        )
        
        # Export option
        if st.button("📥 Export Filtered Data", type="primary"):
            csv_data, filename = export_to_csv(filtered_data[display_cols], "patient_analytics", f"filtered")
            st.download_button(
                label=f"Download {filename}",
                data=csv_data,
                file_name=filename,
                mime="text/csv"
            )
            st.success(f"✅ Data exported to {output_folder}/{filename}")
        
        # Top issues (if issue count available)
        if 'Issue_Count' in patient_data.columns:
            st.subheader("🚨 Top Patients by Issue Count")
            
            top_n = st.slider("Show top N patients", 5, 50, 10)
            top_patients = filtered_data.nlargest(top_n, 'Issue_Count')[['Patient_ID', 'Issue_Count', 'Data_Quality_Score', 'Patient_Status']]
            
            if not top_patients.empty:
                st.dataframe(top_patients, use_container_width=True)
    else:
        st.info("No patients match the selected filters")

# ============================================
# MAIN CONTENT - MULTI-STUDY ANALYTICS
# ============================================
elif selected_section == "🔬 Multi-Study Analytics":
    render_multi_study_dashboard()

# ============================================
# MAIN CONTENT - DATA QUALITY METRICS (FIXED)
# ============================================
elif selected_section == "📈 Data Quality Metrics":
    st.header("📊 Data Quality Metrics & Trends")
    
    if patient_data.empty:
        st.warning("No data available for analysis")
        st.stop()
    
    # Export metrics data
    if st.button("📥 Export Metrics Data", type="primary"):
        # Create metrics based on available data
        metrics_items = []
        
        metrics_items.append(['Total Patients', summary.get('total_patients', 0)])
        metrics_items.append(['Clean Patients', summary.get('clean_patients', 0)])
        metrics_items.append(['Critical Patients', summary.get('critical_patients', 0)])
        metrics_items.append(['Avg Quality Score', summary.get('avg_data_quality_score', 0)])
        metrics_items.append(['Studies Analyzed', summary.get('total_studies', 0)])
        
        if 'Issue_Count' in patient_data.columns:
            metrics_items.append(['Total Issues', patient_data['Issue_Count'].sum()])
        
        metrics_data = pd.DataFrame(metrics_items, columns=['Metric', 'Value'])
        
        csv_data, filename = export_to_csv(metrics_data, "data_quality", "metrics")
        st.download_button(
            label=f"Download {filename}",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
        st.success(f"✅ Metrics exported to {output_folder}/{filename}")
    
    # Data Quality Score Analysis
    st.subheader("📈 Data Quality Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution by status (if available)
        if 'Patient_Status' in patient_data.columns and 'Data_Quality_Score' in patient_data.columns:
            fig = px.box(
                patient_data,
                x='Patient_Status',
                y='Data_Quality_Score',
                color='Patient_Status',
                title="Data Quality Score by Patient Status",
                color_discrete_map={
                    'Clean': current_theme['success'],
                    'Needs Review': current_theme['warning'],
                    'Critical': current_theme['danger']
                }
            )
            fig.update_layout(
                font=dict(color=current_theme['text_primary']),
                plot_bgcolor=current_theme['chart_bg'],
                paper_bgcolor=current_theme['chart_bg']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Patient status or quality score data not available")
    
    with col2:
        # Correlation heatmap (simplified) - use available numeric columns
        numeric_cols = patient_data.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 1:
            corr_matrix = patient_data[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix",
                color_continuous_scale='RdBu',
                zmin=-1, zmax=1
            )
            fig.update_layout(
                font=dict(color=current_theme['text_primary']),
                paper_bgcolor=current_theme['chart_bg']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient numeric data for correlation analysis")
    
    # Data Completeness Analysis
    st.subheader("🔍 Data Completeness Analysis")
    
    # Create completeness indicators based on available data
    completeness_data = []
    
    if 'Data_Quality_Score' in patient_data.columns:
        high_quality = (patient_data['Data_Quality_Score'] >= 80).sum()
        medium_quality = ((patient_data['Data_Quality_Score'] >= 60) & (patient_data['Data_Quality_Score'] < 80)).sum()
        low_quality = (patient_data['Data_Quality_Score'] < 60).sum()
        
        completeness_data.append(['High Quality (≥80)', high_quality])
        completeness_data.append(['Medium Quality (60-79)', medium_quality])
        completeness_data.append(['Low Quality (<60)', low_quality])
    
    if completeness_data:
        completeness_df = pd.DataFrame(completeness_data, columns=['Quality Level', 'Patient Count'])
        
        fig = px.bar(
            completeness_df,
            x='Quality Level',
            y='Patient Count',
            title="Patients by Data Quality Level",
            color='Quality Level',
            color_discrete_sequence=[current_theme['success'], current_theme['warning'], current_theme['danger']],
            text='Patient Count'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            xaxis_title="Quality Level",
            yaxis_title="Number of Patients",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=current_theme['chart_bg'],
            font=dict(color=current_theme['text_primary'])
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# MAIN CONTENT - RISK MONITORING (FIXED)
# ============================================
elif selected_section == "⚠️ Risk Monitoring":
    st.header("🚨 Risk Monitoring & Alerts")
    
    if patient_data.empty:
        st.warning("No patient data available for risk monitoring")
        st.stop()
    
    # Export risk data
    if st.button("📥 Export Risk Data", type="primary"):
        # Create export data with available columns
        export_cols = ['Patient_ID']
        
        if 'Patient_Status' in patient_data.columns:
            export_cols.append('Patient_Status')
        if 'Risk_Level' in patient_data.columns:
            export_cols.append('Risk_Level')
        if 'Data_Quality_Score' in patient_data.columns:
            export_cols.append('Data_Quality_Score')
        if 'Issue_Count' in patient_data.columns:
            export_cols.append('Issue_Count')
        
        risk_data = patient_data[export_cols].copy()
        csv_data, filename = export_to_csv(risk_data, "risk_monitoring", "alerts")
        st.download_button(
            label=f"Download {filename}",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
        st.success(f"✅ Risk data exported to {output_folder}/{filename}")
    
    # Identify critical patients
    if 'Patient_Status' in patient_data.columns:
        critical_patients = patient_data[patient_data['Patient_Status'] == 'Critical']
        
        if len(critical_patients) > 0:
            st.error(f"🚨 **HIGH ALERT:** {len(critical_patients)} Critical Patients Need Immediate Attention!")
            
            # Display critical patients in an expandable format
            for idx, patient in critical_patients.head(5).iterrows():  # Show only first 5
                with st.expander(f"🔴 Patient {patient['Patient_ID']} - Status: Critical", expanded=False):
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📊 Patient Metrics:**")
                        
                        metrics_data = []
                        if 'Data_Quality_Score' in patient:
                            metrics_data.append(['Data Quality Score', f"{patient['Data_Quality_Score']:.1f}/100"])
                        if 'Issue_Count' in patient:
                            metrics_data.append(['Issue Count', patient['Issue_Count']])
                        if 'Risk_Level' in patient:
                            metrics_data.append(['Risk Level', patient['Risk_Level']])
                        
                        for metric_name, metric_value in metrics_data:
                            st.write(f"**{metric_name}:** {metric_value}")
                    
                    with col2:
                        st.markdown("**🎯 Recommended Actions:**")
                        
                        actions = []
                        if 'Data_Quality_Score' in patient and patient['Data_Quality_Score'] < 60:
                            actions.append("**Immediate data quality review** required")
                        if 'Issue_Count' in patient and patient['Issue_Count'] > 0:
                            actions.append(f"**Address {patient['Issue_Count']} identified issue(s)**")
                        actions.append("**Schedule urgent follow-up** with study team")
                        
                        for action in actions:
                            st.write(f"- {action}")
        else:
            st.success("✅ **ALL CLEAR:** No critical patients requiring immediate attention!")
    else:
        st.info("Patient status information not available for risk monitoring")
    
    # Risk level summary
    if 'Risk_Level' in patient_data.columns:
        st.subheader("📊 Risk Level Distribution")
        
        risk_counts = patient_data['Risk_Level'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        
        fig = px.pie(
            risk_counts,
            values='Count',
            names='Risk Level',
            title="Patients by Risk Level",
            color='Risk Level',
            color_discrete_map={
                'Critical': current_theme['danger'],
                'High': current_theme['warning'],
                'Medium': current_theme['primary'],
                'Low': current_theme['success']
            }
        )
        fig.update_layout(
            font=dict(color=current_theme['text_primary']),
            paper_bgcolor=current_theme['chart_bg']
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# MAIN CONTENT - DATA EXPLORER
# ============================================
elif selected_section == "🔍 Data Explorer":
    st.header("📂 Data Explorer")
    
    # Show raw data from different sources
    data_sources = list(loader.dataframes.keys())
    
    if not data_sources:
        st.warning("No data files loaded")
        st.stop()
    
    selected_source = st.selectbox("Select Data Source", data_sources)
    
    if selected_source in loader.dataframes:
        df = loader.dataframes[selected_source]
        
        if len(df) > 0:  # Only show if dataframe has data
            st.subheader(f"{selected_source}")
            st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Show data preview
            st.dataframe(df.head(50), use_container_width=True, height=400)
            
            # Export option
            if st.button("📥 Export This Data", type="primary"):
                csv_data, filename = export_to_csv(df, "data_explorer", selected_source.replace(' ', '_')) # type: ignore
                st.download_button(
                    label=f"Download {filename}",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv"
                )
                st.success(f"✅ Data exported to {output_folder}/{filename}")
            
            # Show column information
            with st.expander("📋 Column Information"):
                col_info = pd.DataFrame({
                    'Column Name': df.columns,
                    'Data Type': df.dtypes.astype(str),
                    'Non-Null Count': df.count(),
                    'Null Count': df.isnull().sum()
                })
                st.dataframe(col_info, use_container_width=True)
            
            # Basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                with st.expander("📊 Basic Statistics"):
                    st.write(df[numeric_cols].describe())
        else:
            st.warning(f"Data source '{selected_source}' is empty (0 rows)")
    else:
        st.error("Selected data source not found")

# ============================================
# MAIN CONTENT - AI INSIGHTS (FIXED)
# ============================================
elif selected_section == "🤖 AI Insights":
    st.header("🤖 AI-Powered Insights & Recommendations")
    
    st.info("💡 This section provides intelligent insights based on your clinical trial data")
    
    # Export AI insights
    if st.button("📥 Export AI Insights", type="primary"):
        insights_data = pd.DataFrame({
            'Metric': ['Total Patients', 'Clean Patients', 'Critical Patients', 'Avg Quality Score', 'Studies Analyzed'],
            'Value': [
                summary.get('total_patients', 0),
                summary.get('clean_patients', 0),
                summary.get('critical_patients', 0),
                summary.get('avg_data_quality_score', 0),
                summary.get('total_studies', 0)
            ],
            'Insight': [
                'Total enrolled patients',
                'Patients meeting quality standards',
                'Patients needing immediate attention',
                'Overall data quality measure',
                'Number of studies analyzed'
            ]
        })
        
        csv_data, filename = export_to_csv(insights_data, "ai_insights", "summary")
        st.download_button(
            label=f"Download {filename}",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
        st.success(f"✅ Insights exported to {output_folder}/{filename}")
    
    # Generate insights based on data
    if not patient_data.empty and summary:
        # Insight 1: Overall status
        st.subheader("📈 Overall Status Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Key Metrics:**")
            st.write(f"- **Data Quality Index:** {summary.get('avg_data_quality_score', 0):.1f}/100")
            st.write(f"- **Clean Patients:** {summary.get('clean_percentage', 0)}%")
            st.write(f"- **Critical Patients:** {summary.get('critical_patients', 0)}")
            st.write(f"- **Studies Analyzed:** {summary.get('total_studies', 0)}")
        
        with col2:
            st.markdown("**🎯 Performance Benchmark:**")
            avg_score = summary.get('avg_data_quality_score', 0)
            if avg_score >= 80:
                st.success("✅ **Excellent:** Above target threshold (80+)")
            elif avg_score >= 70:
                st.warning("⚠️ **Good:** Meeting minimum standards (70-79)")
            elif avg_score >= 60:
                st.warning("⚠️ **Fair:** Needs improvement (60-69)")
            else:
                st.error("❌ **Needs Improvement:** Below acceptable level (<60)")
        
        # Insight 2: Recommendations
        st.subheader("💡 AI Recommendations")
        
        recommendations = []
        avg_score = summary.get('avg_data_quality_score', 0)
        
        if avg_score < 70:
            recommendations.append("**Implement data quality training program** for site staff")
        
        if summary.get('critical_patients', 0) > 0:
            recommendations.append("**Establish rapid response protocol** for critical cases")
        
        if summary.get('total_studies', 0) > 3:
            recommendations.append("**Standardize data collection** across all studies")
        
        if 'Issue_Count' in patient_data.columns and patient_data['Issue_Count'].sum() > 100:
            recommendations.append("**Automate issue tracking and resolution** process")
        
        if recommendations:
            st.write("Based on the data analysis, I recommend:")
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.success("✅ **Excellent!** Current operations are meeting quality standards. Continue current practices.")
    
    # AI Query Interface
    st.markdown("---")
    st.subheader("💬 Ask Questions About Your Data")
    
    query = st.text_area(
        "Enter your question or describe what you want to analyze:",
        placeholder="e.g., What is the overall data quality? Which patients need attention?",
        height=100,
        key="ai_query_input"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🤖 Get AI Analysis", type="primary", use_container_width=True):
            if query.strip():
                with st.spinner("🧠 Analyzing data with AI..."):
                    ai_response = get_ai_response(query, patient_data, summary, integrator)
                    
                    # Display response in a nice container
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {current_theme['background']} 0%, {current_theme['card_bg']} 100%); 
                                padding: 2rem; 
                                border-radius: 15px; 
                                border-left: 5px solid {current_theme['primary']};
                                margin: 1rem 0;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                                color: {current_theme['text_primary']} !important;">
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 🤖 AI Analysis Results")
                    st.markdown("---")
                    st.markdown(ai_response)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Export AI response
                    response_data = pd.DataFrame({
                        'Query': [query],
                        'Response': [ai_response],
                        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                    })
                    
                    csv_data, filename = export_to_csv(response_data, "ai_response", "query")
                    st.download_button(
                        label="📥 Download AI Response",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv"
                    )
            else:
                st.warning("Please enter a question to get AI analysis.")
    
    with col2:
        if st.button("🔄 Clear AI Cache", help="Clear cached AI responses"):
            st.session_state.ai_responses = {}
            st.success("AI cache cleared!")

# ============================================
# SETTINGS SECTION
# ============================================
elif selected_section == "⚙️ Settings":
    st.header("⚙️ Application Settings")
    
    # Two columns for settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Theme & Appearance")
        
        # Theme selector
        theme_options = ["Default Blue", "Medical Green", "Dark Mode", "Warm Orange", "Professional Purple"]
        new_theme = st.selectbox("Color Theme", 
                               theme_options,
                               index=theme_options.index(st.session_state.current_theme))
        
        if new_theme != st.session_state.current_theme:
            st.session_state.current_theme = new_theme
            st.rerun()
        
        st.markdown("---")
        st.subheader("🖼️ Background Settings")
        
        bg_type = st.radio("Background Type", ["Default Medical", "Upload Custom", "None"])
        
        if bg_type == "Upload Custom":
            uploaded_file = st.file_uploader("Choose a background image", type=['jpg', 'jpeg', 'png'])
            
            if uploaded_file is not None:
                # Save the uploaded file
                custom_bg_path = os.path.join(output_folder, "custom_background.jpg")
                with open(custom_bg_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.session_state.custom_bg_path = custom_bg_path
                st.success("Custom background uploaded!")
        
        elif bg_type == "None":
            st.session_state.custom_bg_path = None
            st.info("Background cleared")
        
        # Opacity control
        opacity = st.slider("Background Opacity", 0.0, 1.0, st.session_state.bg_opacity, 0.05,
                          help="0.0 = Transparent, 1.0 = Fully visible")
        if opacity != st.session_state.bg_opacity:
            st.session_state.bg_opacity = opacity
            st.rerun()
        
        st.info(f"Current opacity: {int(opacity * 100)}% visibility")
    
    with col2:
        st.subheader("⚙️ Application Settings")
        
        # Sidebar visibility
        sidebar_status = "Visible" if st.session_state.sidebar_visible else "Hidden"
        st.write(f"**Sidebar:** {sidebar_status}")
        
        if st.button("Toggle Sidebar Visibility", use_container_width=True):
            st.session_state.sidebar_visible = not st.session_state.sidebar_visible
            st.rerun()
        
        st.markdown("---")
        st.subheader("🗄️ Data Management")
        
        st.write(f"**Data Folder:** data/")
        st.write(f"**Output Folder:** {output_folder}/")
        st.write(f"**Files Loaded:** {len(loader.dataframes)}")
        st.write(f"**Studies Found:** {len(loader.study_folders)}")
        
        if st.button("Show Data Summary", use_container_width=True):
            summary_df = loader.get_summary()
            st.dataframe(summary_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🔄 System Management")
        
        col_reset1, col_reset2 = st.columns(2)
        
        with col_reset1:
            if st.button("Clear Cache", use_container_width=True, type="primary"):
                st.cache_resource.clear()
                st.success("Cache cleared successfully!")
                st.rerun()
        
        with col_reset2:
            if st.button("Reset Settings", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key not in ['last_section']:
                        del st.session_state[key]
                st.session_state.sidebar_visible = True
                st.session_state.current_theme = "Default Blue"
                st.session_state.bg_opacity = 0.5
                st.success("Settings reset to defaults!")
                st.rerun()

# ============================================
# ENHANCED FOOTER
# ============================================
st.markdown("---")

footer_html = f"""
<div style="
    text-align: center; 
    color: {current_theme['text_secondary']}; 
    padding: 2rem 1rem; 
    margin-top: 3rem;
    background: linear-gradient(135deg, rgba(0,0,0,0.02) 0%, rgba(0,0,0,0.05) 100%);
    border-radius: 15px;
    border-top: 2px solid {current_theme['primary']};
">
    <h3 style="color: {current_theme['primary']}; font-weight: 800; margin-bottom: 0.5rem;">
        🏥 INTEGRATED TRIAL MONITOR
    </h3>
    <p style="font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">
        Advanced Clinical Trial Analytics Platform
    </p>
    <p style="margin-bottom: 1rem; opacity: 0.8;">
        Data Sources: {len(loader.study_folders)} Studies • Theme: {st.session_state.current_theme} • 
        Version 2.0 • {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
        <span>📊 Real-time Analytics</span>
        <span>🤖 AI-Powered Insights</span>
        <span>🚨 Risk Monitoring</span>
        <span>📈 Quality Metrics</span>
    </div>
    <p style="font-size: 0.9rem; margin-top: 1.5rem; opacity: 0.7;">
        Built with ❤️ using Streamlit, Pandas, and Plotly • Clinical Excellence Platform
    </p>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

# ============================================
# JAVASCRIPT FOR SIDEBAR TOGGLE
# ============================================
st.markdown("""
<script>
// Listen for sidebar toggle
window.addEventListener('toggleSidebar', function() {
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    if (sidebar && toggleBtn) {
        if (sidebar.style.display === 'none') {
            sidebar.style.display = 'block';
            toggleBtn.innerHTML = '◀';
        } else {
            sidebar.style.display = 'none';
            toggleBtn.innerHTML = '▶';
        }
    }
});
</script>
""", unsafe_allow_html=True)