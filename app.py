import streamlit as st
from ui import main_ui

# Initialize theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.set_page_config(
    page_title="Energy-Aware Code Profiler",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': 'Energy-Aware Code Profiler - Optimize your Python code for better energy efficiency!'
    }
)

# Custom CSS for better styling
if st.session_state.dark_mode:
    css = """
<style>
    .stApp {
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    .main-header {
        color: #4CAF50 !important;
    }
    .sub-header {
        color: #81C784 !important;
    }
    .metric-card {
        background-color: #333333 !important;
        border-color: #555555 !important;
        color: #ffffff !important;
    }
    .tab-content {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    .sidebar-content {
        background-color: #2e2e2e !important;
        color: #ffffff !important;
    }
    .footer {
        color: #cccccc !important;
    }
    .footer a {
        color: #81C784 !important;
    }
    /* Streamlit specific */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e1e1e !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #333333 !important;
        color: #ffffff !important;
    }
    .stMarkdown, .stText, .stCodeBlock, .stAlert {
        color: #ffffff !important;
    }
    .stSidebar {
        background-color: #2e2e2e !important;
    }
    .stSidebar .stMarkdown {
        color: #ffffff !important;
    }
</style>
"""
else:
    css = """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4682B4;
        margin-bottom: 0.5rem;
        animation: fadeIn 1.5s ease-in;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #add8e6;
        margin: 0.5rem 0;
        animation: slideIn 0.5s ease-out;
    }
    .tab-content {
        padding: 1rem;
        background-color: #fafafa;
        border-radius: 5px;
        margin: 0.5rem 0;
        animation: fadeIn 1s ease-in;
    }
    .sidebar-content {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 5px;
        animation: slideInLeft 0.5s ease-out;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
        font-size: 0.8rem;
        animation: fadeIn 2s ease-in;
    }
    .footer a {
        color: #4682B4;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

if __name__ == "__main__":
    main_ui()
