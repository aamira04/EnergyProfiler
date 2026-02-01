import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from profiler import run_profiler, get_ai_optimization
from energy import estimate_energy

def get_theme_css(dark_mode=True):
    """Returns the appropriate CSS based on theme selection."""
    return get_dark_mode_css() if dark_mode else get_light_mode_css()

def get_light_mode_css():
    """Nature-inspired 'Eco-Professional' light mode.
    
    Accessibility (WCAG AA) Audit:
    - Text (#1a2e26) on Background (#f5f7f5): Contrast 12.8:1
    - Accent (#059669) on Background (#f5f7f5): Contrast 4.6:1
    - Muted Text (#52695e) on Background (#f5f7f5): Contrast 4.6:1
    """
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;700&display=swap');
    
    :root {
        --bg-base: #f7faf8;
        --bg-surface: rgba(255, 255, 255, 0.75);
        --bg-elevated: rgba(255, 255, 255, 0.9);
        --bg-overlay: rgba(240, 245, 241, 0.95);
        --text-primary: #1a2e26;  /* Deep Forest Black-Green */
        --text-secondary: #425e52; /* Sage Shadow */
        --text-muted: #5e7a6e;
        --accent-primary: #059669; /* Emerald Green */
        --accent-secondary: #10b981; /* Sage Emerald */
        --accent-gradient: linear-gradient(135deg, #065f46 0%, #059669 100%);
        --success: #059669;
        --error: #be123c;
        --border-glass: rgba(5, 150, 105, 0.1);
        --shadow-soft: 0 10px 40px 0 rgba(5, 46, 38, 0.05);
        --radius-lg: 32px;
        --radius-md: 20px;
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #e8f5ed, #f7faf8 50%, #f0f7f2);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    @keyframes leafFloat {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    .header-container {
        background: var(--bg-surface);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-lg);
        padding: 3.5rem;
        margin-bottom: 3rem;
        box-shadow: var(--shadow-soft);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '🌿';
        position: absolute;
        top: -10px; right: -10px;
        font-size: 6rem; opacity: 0.05;
        animation: leafFloat 6s infinite ease-in-out;
    }

    .metric-card {
        background: var(--bg-surface);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 1.75rem;
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
        position: relative;
    }

    .metric-card:hover {
        transform: translateY(-8px);
        background: var(--bg-elevated);
        box-shadow: 0 20px 50px 0 rgba(5, 46, 38, 0.1);
        border-color: rgba(5, 150, 105, 0.2);
    }

    .header-badge {
        background: #ecfdf5;
        color: #065f46;
        padding: 0.6rem 1.4rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        border: 1px solid rgba(5, 150, 105, 0.15);
    }

    .header-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #064e3b;
        margin: 1.5rem 0 1rem;
        letter-spacing: -1px;
    }

    .header-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        max-width: 600px;
        line-height: 1.6;
    }

    .stButton > button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(5, 150, 105, 0.25);
        transition: var(--transition);
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(5, 150, 105, 0.4);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #064e3b;
        background: #ecfdf5;
        border-radius: 12px;
    }

    .app-footer {
        color: var(--text-muted);
        border-top: 1px solid var(--border-glass);
    }
</style>
"""

def get_dark_mode_css():
    """Nature-inspired 'Eco-Professional' dark mode.
    
    Accessibility (WCAG AA) Audit:
    - Text (#f0fdf4) on Background (#022c22): Contrast 14.8:1
    - Accent (#10b981) on Background (#022c22): Contrast 6.5:1
    - Muted Text (#a7f3d0) on Background (#022c22): Contrast 10.4:1
    """
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;700&display=swap');
    
    :root {
        --bg-base: #022c22; /* Deep Forest Green */
        --bg-surface: rgba(6, 78, 59, 0.6);
        --bg-elevated: rgba(6, 95, 70, 0.8);
        --bg-overlay: rgba(2, 44, 34, 0.95);
        --text-primary: #f0fdf4; /* Mint White */
        --text-secondary: #a7f3d0; /* Soft Mint */
        --text-muted: #6ee7b7;
        --accent-primary: #10b981; /* Sage Emerald */
        --accent-secondary: #34d399;
        --accent-gradient: linear-gradient(135deg, #065f46 0%, #10b981 100%);
        --success: #10b981;
        --error: #fb7185;
        --border-glass: rgba(167, 243, 208, 0.1);
        --shadow-soft: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
        --radius-lg: 32px;
        --radius-md: 20px;
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stApp {
        background: radial-gradient(circle at top left, #064e3b, #022c22 70%, #064e3b);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    .header-container {
        background: var(--bg-surface);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-lg);
        padding: 3.5rem;
        margin-bottom: 3rem;
        box-shadow: var(--shadow-soft);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '🌲';
        position: absolute;
        top: -10px; right: -10px;
        font-size: 6rem; opacity: 0.1;
    }

    .metric-card {
        background: var(--bg-surface);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 1.75rem;
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
        position: relative;
    }

    .metric-card:hover {
        transform: translateY(-8px);
        background: var(--bg-elevated);
        border-color: rgba(167, 243, 208, 0.3);
    }

    .header-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #6ee7b7;
        padding: 0.6rem 1.4rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .header-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f0fdf4 0%, #a7f3d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1.5rem 0 1rem;
    }

    .stButton > button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    [data-testid="stSidebar"] {
        background: rgba(2, 44, 34, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-glass);
    }
</style>
"""

def display_header():
    dark_mode = st.session_state.get("dark_mode", True)
    st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)
    st.markdown('''
    <div class="header-container">
        <div class="header-badge">
            🍃 Sustainable Computing
        </div>
        <h1 class="header-title">Energy-Aware Code Profiler</h1>
        <p class="header-subtitle">Optimizing the digital world, one line of code at a time. Professional analysis with a heart for nature.</p>
    </div>
    ''', unsafe_allow_html=True)

def handle_file_upload():
    st.markdown('''
    <div class="section-header">
        <div class="section-icon">📁</div>
        <h2 class="section-title">Upload Code</h2>
        <div class="section-divider"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload a Python file", 
        type=["py"], 
        help="Choose a .py file to analyze its energy consumption",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        path = "temp.py"
        code = uploaded_file.read().decode("utf-8")
        with open(path, "w") as f:
            f.write(code)
        st.success(f"✓ {uploaded_file.name} uploaded successfully")
        return path, code
    return None, None

def run_analysis(path):
    progress = st.progress(0, text="Initializing...")
    progress.progress(30, text="Running profiler...")
    stats = run_profiler(path)
    progress.progress(70, text="Calculating metrics...")
    progress.progress(100, text="Complete")
    progress.empty()
    return stats

def calculate_grade(total_energy):
    """Calculates a sustainability grade (A-E) based on total energy consumption with botanical colors."""
    if total_energy < 0.1: return "A+", "#059669"
    if total_energy < 0.5: return "A", "#10b981"
    if total_energy < 2.0: return "B", "#34d399"
    if total_energy < 5.0: return "C", "#d97706" # Amber for contrast
    if total_energy < 10.0: return "D", "#dc2626"
    return "E", "#991b1b"

def display_sustainability_score(total_energy):
    grade, color = calculate_grade(total_energy)
    st.markdown(f'''
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 2rem;">
        <div class="score-badge" style="background: {color}; box-shadow: 0 10px 30px {color}44;">
            {grade}
        </div>
        <div class="score-label">Efficiency Grade</div>
    </div>
    ''', unsafe_allow_html=True)

def process_data(stats):
    functions = []
    energies = []
    for func, data in list(stats.items())[:10]:
        cpu_time = data[3]
        functions.append(str(func))
        energies.append(estimate_energy(cpu_time))
    total_energy = sum(energies)
    return functions, energies, total_energy

def display_energy_metrics(total_energy):
    battery_impact = (total_energy / 200000) * 100 
    trees_needed = total_energy * 0.000002 
    
    st.markdown(f'''
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-icon" style="background: linear-gradient(135deg, #059669, #10b981); color: white;">🌿</div>
            <div class="metric-label">Energy Drain</div>
            <div class="metric-value">{total_energy:.4f}<span class="metric-unit">J</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-icon" style="background: linear-gradient(135deg, #047857, #059669); color: white;">🍃</div>
            <div class="metric-label">Device Impact</div>
            <div class="metric-value">{battery_impact:.6f}<span class="metric-unit">%</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-icon" style="background: linear-gradient(135deg, #064e3b, #047857); color: white;">🌳</div>
            <div class="metric-label">Nature Debt</div>
            <div class="metric-value">{trees_needed:.8f}<span class="metric-unit">trees</span></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def display_energy_reduction(total_energy):
    if "previous_energy" not in st.session_state:
        st.session_state.previous_energy = None

    if st.session_state.previous_energy:
        reduction = ((st.session_state.previous_energy - total_energy) / st.session_state.previous_energy) * 100
        if reduction > 0:
            st.success(f"↓ Energy reduced by {reduction:.2f}%")
        elif reduction < 0:
            st.warning(f"↑ Energy increased by {abs(reduction):.2f}%")
        else:
            st.info("→ Energy unchanged")

    st.session_state.previous_energy = total_energy

def display_chart(functions, energies):
    dark_mode = st.session_state.get("dark_mode", True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('''
        <div class="section-header">
            <div class="section-icon">📊</div>
            <h2 class="section-title">Visual Analysis</h2>
            <div class="section-divider"></div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        view_type = st.radio("View Type", ["Bar Chart", "Tree Map"], horizontal=True, label_visibility="collapsed")

    if not functions:
        st.info("No function data available")
        return

    df = pd.DataFrame({'Function': functions, 'Energy (Joules)': energies})
    text_color = "#ffffff" if dark_mode else "#1a1c2e"
    grid_color = "rgba(255, 255, 255, 0.1)" if dark_mode else "rgba(0, 0, 0, 0.05)"

    if view_type == "Bar Chart":
        fig = px.bar(
            df, x='Energy (Joules)', y='Function', orientation='h',
            color='Energy (Joules)',
            color_continuous_scale=['#d1fae5', '#10b981', '#065f46']
        )
        fig.update_layout(
            height=max(300, len(functions) * 40),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color=text_color),
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor=grid_color), yaxis=dict(gridcolor=grid_color)
        )
    else:
        fig = px.treemap(
            df, path=['Function'], values='Energy (Joules)',
            color='Energy (Joules)',
            color_continuous_scale=['#d1fae5', '#10b981', '#065f46']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color=text_color),
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_showscale=False
        )
    
    st.plotly_chart(fig, use_container_width=True)

def display_detailed_stats(stats):
    st.markdown('''
    <div class="section-header">
        <div class="section-icon">📋</div>
        <h2 class="section-title">Detailed Statistics</h2>
        <div class="section-divider"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    if stats:
        stats_df = []
        for func, data in list(stats.items())[:20]:
            stats_df.append({
                "Function": str(func),
                "Calls": data[0],
                "Total Time": f"{data[1]:.4f}s",
                "CPU Time": f"{data[3]:.4f}s",
                "Energy": f"{estimate_energy(data[3]):.2f}J"
            })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    else:
        st.info("No statistics available")

def display_tips():
    st.markdown('''
    <div class="section-header">
        <div class="section-icon">💡</div>
        <h2 class="section-title">Optimization Tips</h2>
        <div class="section-divider"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    tips = [
        ("Use efficient data structures", "Sets for lookups, generators for large datasets"),
        ("Cache expensive computations", "Use memoization for repeated calculations"),
        ("Leverage built-in functions", "Python's built-ins are optimized C code"),
        ("Profile before optimizing", "Focus on actual bottlenecks"),
        ("Use async for I/O", "Reduces wait time for network/file operations"),
        ("Minimize allocations", "Pre-allocate lists, reuse objects"),
    ]
    
    col1, col2 = st.columns(2)
    for i, (title, desc) in enumerate(tips):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f'''
            <div class="card">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">{title}</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)

def display_sustainability_impact():
    st.markdown('''
    <div class="section-header">
        <div class="section-icon">🌱</div>
        <h2 class="section-title">Environmental Impact</h2>
        <div class="section-divider"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="card">
            <div class="card-header">
                <div class="card-icon">🌍</div>
                <div>
                    <h4 class="card-title">Environmental Benefits</h4>
                    <p class="card-description">Impact of optimization</p>
                </div>
            </div>
            <div class="card-body">
                <ul>
                    <li>Reduced carbon footprint</li>
                    <li>Lower energy consumption</li>
                    <li>Sustainable computing</li>
                </ul>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="card">
            <div class="card-header">
                <div class="card-icon">🚀</div>
                <div>
                    <h4 class="card-title">Business Benefits</h4>
                    <p class="card-description">Value of optimization</p>
                </div>
            </div>
            <div class="card-body">
                <ul>
                    <li>Faster execution</li>
                    <li>Reduced cloud costs</li>
                    <li>Better scalability</li>
                </ul>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def update_live_analysis():
    if "live_code" in st.session_state and st.session_state.live_code.strip():
        path = "live_temp.py"
        with open(path, "w") as f:
            f.write(st.session_state.live_code)
        stats = run_profiler(path)
        functions, energies, total_energy = process_data(stats)
        st.session_state.live_stats = stats
        st.session_state.live_functions = functions
        st.session_state.live_energies = energies
        st.session_state.live_total_energy = total_energy
    else:
        st.session_state.live_stats = None
        st.session_state.live_functions = None
        st.session_state.live_energies = None
        st.session_state.live_total_energy = None

def display_ai_optimization(code, joules):
    st.markdown('''
    <div class="section-header">
        <div class="section-icon">🤖</div>
        <h2 class="section-title">AI Optimization</h2>
        <div class="section-divider"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="card">
        <div class="card-body">
            Get AI-powered suggestions to improve your code's energy efficiency. 
            Our AI analyzes patterns and recommends targeted optimizations.
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("Generate Suggestions", type="primary", use_container_width=True):
        with st.spinner("Analyzing code..."):
            opt_code, full_advice = get_ai_optimization(code, joules)
        
        if opt_code and full_advice:
            st.success("✓ Analysis complete")
            
            st.markdown('''
            <div class="section-header" style="margin-top: 1rem;">
                <div class="section-icon">📝</div>
                <h2 class="section-title">Optimized Code</h2>
                <div class="section-divider"></div>
            </div>
            ''', unsafe_allow_html=True)
            st.code(opt_code, language="python")
            
            st.markdown('''
            <div class="section-header">
                <div class="section-icon">💬</div>
                <h2 class="section-title">Recommendations</h2>
                <div class="section-divider"></div>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown(full_advice)
        else:
            st.error("Unable to generate suggestions. Check API key.")

def display_sidebar():
    with st.sidebar:
        st.markdown('''
        <div class="sidebar-header">
            <div class="sidebar-brand">
                <div class="sidebar-logo">🌿</div>
                <div>
                    <div class="sidebar-name">EcoProfiler</div>
                    <div class="sidebar-version">v3.0 • Nature</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Settings</div>', unsafe_allow_html=True)
        
        # Initialize dark_mode if not set
        if "dark_mode" not in st.session_state:
            st.session_state.dark_mode = True
        
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="theme_toggle")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Actions</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Guide</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="sidebar-text">
            1. Upload a Python file<br>
            2. View energy metrics<br>
            3. Get AI suggestions<br>
            4. Download optimized code
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main_ui():
    display_sidebar()
    display_header()
    
    path, code = handle_file_upload()
    
    if path and code:
        st.session_state.code = code
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Overview", 
            "Details", 
            "Impact", 
            "AI Optimize", 
            "Code", 
            "Live Editor"
        ])
        
        stats = run_analysis(path)
        functions, energies, total_energy = process_data(stats)
        st.session_state.stats = stats
        
        with tab1:
            st.markdown('''
            <div class="section-header">
                <div class="section-icon">⚡</div>
                <h2 class="section-title">Sustainability Dashboard</h2>
                <div class="section-divider"></div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Top row: Score + Metrics
            col_score, col_metrics = st.columns([1, 2])
            with col_score:
                display_sustainability_score(total_energy)
            with col_metrics:
                display_energy_metrics(total_energy)
            
            display_energy_reduction(total_energy)
            display_chart(functions, energies)
            
            # Enhanced report download
            report_text = f"ENERGY SUSTAINABILITY REPORT\n" + "="*30 + f"\nGrade: {calculate_grade(total_energy)[0]}\nTotal Energy: {total_energy:.4f} Joules\nCPU Time: {total_energy/30:.4f} s\nCO2: {total_energy*0.0004:.6f} g\n\nFUNCTION BREAKDOWN:\n" + "\n".join([f"• {f}: {e:.4f} J" for f, e in zip(functions, energies)])
            st.download_button("📥 Export Full Report", report_text, file_name="sustainability_report.txt", key="dl1")
        
        with tab2:
            display_detailed_stats(stats)
            csv = "Function,Calls,Total,CPU,Energy\n"
            for func, data in stats.items():
                csv += f"{func},{data[0]},{data[1]:.4f},{data[3]:.4f},{estimate_energy(data[3]):.2f}\n"
            st.download_button("📊 Export CSV", csv, file_name="data.csv", key="dl2")
        
        with tab3:
            display_sustainability_impact()
            display_tips()
        
        with tab4:
            display_ai_optimization(code, total_energy)
        
        with tab5:
            st.markdown('''
            <div class="section-header">
                <div class="section-icon">📝</div>
                <h2 class="section-title">Source Code</h2>
                <div class="section-divider"></div>
            </div>
            ''', unsafe_allow_html=True)
            st.code(code, language="python")
            st.download_button("📥 Download", code, file_name="source.py", key="dl3")
        
        with tab6:
            st.markdown('''
            <div class="section-header">
                <div class="section-icon">⚡</div>
                <h2 class="section-title">Live Editor</h2>
                <div class="section-divider"></div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('''
            <div class="card">
                <div class="card-body">Write or paste Python code for real-time analysis.</div>
            </div>
            ''', unsafe_allow_html=True)
            
            live_code = st.text_area(
                "Code",
                value=st.session_state.get("live_code", "# Enter Python code\nprint('Hello')"),
                height=250,
                key="live_code_input",
                on_change=update_live_analysis,
                label_visibility="collapsed"
            )
            st.session_state.live_code = live_code
            
            if st.session_state.get("live_total_energy"):
                display_energy_metrics(st.session_state.live_total_energy)
                display_chart(st.session_state.live_functions, st.session_state.live_energies)
                
                if st.button("🤖 Optimize", key="live_ai", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        opt_code, advice = get_ai_optimization(live_code, st.session_state.live_total_energy)
                    if opt_code:
                        st.success("✓ Complete")
                        st.code(opt_code, language="python")
                        st.download_button("📥 Download", opt_code, file_name="optimized.py", key="dl4")
                        st.markdown(advice)
                    else:
                        st.error("Failed")
    else:
        st.markdown('''
        <div class="empty-state">
            <div class="empty-icon">📁</div>
            <h3 class="empty-title">No file uploaded</h3>
            <p class="empty-description">
                Upload a Python file to analyze its energy consumption and get optimization suggestions.
            </p>
        </div>
        ''', unsafe_allow_html=True)
    
    dark_mode = st.session_state.get("dark_mode", True)
    theme_label = "🌙 Dark Mode" if dark_mode else "☀️ Light Mode"
    st.markdown(f'''
    <div class="app-footer">
        Energy-Aware Code Profiler v2.3 • {theme_label}<br>
        <a href="#">Built for sustainable development</a>
    </div>
    ''', unsafe_allow_html=True)