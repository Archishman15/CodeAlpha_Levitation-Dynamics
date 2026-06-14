import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

# ==========================================
# STREAMLIT CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="Levitation Dynamics Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Theme & Accent Color
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    .css-1d391kg {
        background-color: #111111;
    }
    h1, h2, h3 {
        color: #00d4ff !important;
    }
    .kpi-card {
        background-color: #1a1a1a;
        border-left: 5px solid #00d4ff;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .kpi-title {
        color: #888888;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('levitation_cleaned_experiments.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Black_hole_-_Messier_87_crop_max_res.jpg/320px-Black_hole_-_Messier_87_crop_max_res.jpg", use_container_width=True)
st.sidebar.title("🌌 Controls")

# Date Range Slider
min_date = df['Date'].min().date()
max_date = df['Date'].min().date() + pd.Timedelta(days=(df['Date'].max() - df['Date'].min()).days)

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Material Type Dropdown
materials = ['All'] + sorted(df['Material_Type'].unique().tolist())
selected_material = st.sidebar.selectbox("Filter by Material Type", materials)

# Apply filters
mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
if selected_material != 'All':
    mask = mask & (df['Material_Type'] == selected_material)

filtered_df = df[mask]

# ==========================================
# MAIN DASHBOARD
# ==========================================
st.title("CodeAlpha | Levitation Dynamics Dashboard")
st.markdown("Interactive exploration of levitation dynamics experimental parameters and outcomes.")

# KPI Cards
if len(filtered_df) > 0:
    total_experiments = len(filtered_df)
    avg_altitude = filtered_df['Levitation_Altitude_m'].mean()
    best_lab = filtered_df.groupby('Lab_ID')['Levitation_Altitude_m'].mean().idxmax()
    top_material = filtered_df.groupby('Material_Type')['Levitation_Altitude_m'].mean().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Experiments</div><div class="kpi-value">{total_experiments}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Avg Altitude (m)</div><div class="kpi-value">{avg_altitude:.2f}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Best Performing Lab</div><div class="kpi-value">{best_lab}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Top Material</div><div class="kpi-value">{top_material}</div></div>', unsafe_allow_html=True)
else:
    st.warning("No data available for the selected filters.")
    st.stop()

st.markdown("---")

# Common Plotly Theme config
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor='#0a0a0a',
    plot_bgcolor='#0a0a0a',
    font=dict(color='#ffffff', family='Arial')
)

# Layout rows
row1_col1, row1_col2 = st.columns(2)

# CHART 1: Altitude Distribution
with row1_col1:
    st.subheader("1. Levitation Altitude Distribution")
    fig1 = px.histogram(filtered_df, x="Levitation_Altitude_m", 
                        marginal="box", nbins=30, 
                        color_discrete_sequence=['#00d4ff'])
    
    mean_val = filtered_df['Levitation_Altitude_m'].mean()
    median_val = filtered_df['Levitation_Altitude_m'].median()
    fig1.add_vline(x=mean_val, line_dash="dash", line_color="#ff7f0e", annotation_text=f"Mean: {mean_val:.1f}")
    fig1.add_vline(x=median_val, line_dash="solid", line_color="#2ca02c", annotation_text=f"Median: {median_val:.1f}")
    fig1.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig1, use_container_width=True)

# CHART 2: Material vs Average Altitude
with row1_col2:
    st.subheader("2. Avg Altitude by Material")
    mat_avg = filtered_df.groupby('Material_Type')['Levitation_Altitude_m'].mean().reset_index()
    mat_avg = mat_avg.sort_values('Levitation_Altitude_m', ascending=True)
    
    fig2 = px.bar(mat_avg, x="Levitation_Altitude_m", y="Material_Type", orientation='h',
                  color="Levitation_Altitude_m", color_continuous_scale="Tealgrn",
                  text="Levitation_Altitude_m")
    fig2.update_traces(texttemplate='%{text:.2f}m', textposition='outside')
    fig2.update_layout(**PLOTLY_THEME, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

# CHART 3: Correlation Heatmap
with row2_col1:
    st.subheader("3. Feature Correlation Matrix")
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    corr = numeric_df.corr().round(2)
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    df_mask = corr.mask(mask)
    
    fig3 = go.Figure(data=go.Heatmap(
        z=df_mask.values, x=df_mask.columns, y=df_mask.index,
        colorscale='RdYlGn', zmin=-1, zmax=1,
        text=df_mask.values, texttemplate="%{text}", textfont={"size":10}
    ))
    fig3.update_layout(**PLOTLY_THEME, height=400)
    st.plotly_chart(fig3, use_container_width=True)

# CHART 4: Power vs Altitude Scatter Plot
with row2_col2:
    st.subheader("4. Power Consumption vs Altitude")
    fig4 = px.scatter(filtered_df, x="Power_Consumption_W", y="Levitation_Altitude_m",
                      color="Material_Type", size="Success_Rate_Percent",
                      trendline="ols", trendline_color_override="#00d4ff",
                      color_discrete_sequence=px.colors.qualitative.Bold)
    fig4.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig4, use_container_width=True)

row3_col1, row3_col2 = st.columns(2)

# CHART 5: Experiment Success Rate Over Time
with row3_col1:
    st.subheader("5. Monthly Success Rate Trend")
    monthly_success = filtered_df.groupby('Month_Year')['Success_Rate_Percent'].mean().reset_index()
    monthly_success['Date_Idx'] = pd.to_datetime(monthly_success['Month_Year'] + '-01')
    monthly_success = monthly_success.sort_values('Date_Idx')
    monthly_success['Rolling_3M'] = monthly_success['Success_Rate_Percent'].rolling(window=3, min_periods=1).mean()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=monthly_success['Date_Idx'], y=monthly_success['Success_Rate_Percent'],
                              mode='lines', line=dict(color='rgba(0, 128, 128, 0.5)'), fill='tozeroy',
                              name='Monthly Avg'))
    fig5.add_trace(go.Scatter(x=monthly_success['Date_Idx'], y=monthly_success['Rolling_3M'],
                              mode='lines', line=dict(color='#00d4ff', width=3),
                              name='3-Month Rolling Avg'))
    fig5.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig5, use_container_width=True)

# CHART 6: Lab Performance Comparison
with row3_col2:
    st.subheader("6. Lab Performance Distribution")
    fig6 = px.box(filtered_df, x="Lab_ID", y="Levitation_Altitude_m", 
                  color="Lab_ID", color_discrete_sequence=px.colors.qualitative.Prism)
    fig6.update_layout(**PLOTLY_THEME, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# CHART 8: 3D Visualization
st.subheader("8. 3D Parameter Space")
fig8 = px.scatter_3d(filtered_df, x='Power_Consumption_W', y='Temperature_K', z='Levitation_Altitude_m',
                      color='Material_Type', size='Success_Rate_Percent',
                      color_discrete_sequence=px.colors.qualitative.Bold)
fig8.update_layout(**PLOTLY_THEME, height=600, 
                   scene=dict(
                       xaxis=dict(backgroundcolor="#111111", gridcolor="#333"),
                       yaxis=dict(backgroundcolor="#111111", gridcolor="#333"),
                       zaxis=dict(backgroundcolor="#111111", gridcolor="#333")
                   ))
st.plotly_chart(fig8, use_container_width=True)

st.caption("© 2026 CodeAlpha | Levitation Dynamics Division")
