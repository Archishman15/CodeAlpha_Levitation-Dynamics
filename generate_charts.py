import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from matplotlib.backends.backend_pdf import PdfPages
import scipy.stats as stats
import matplotlib.patheffects as path_effects

# ==========================================
# CONFIGURATION & THEME SETUP
# ==========================================
plt.style.use('dark_background')
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'figure.facecolor': '#0a0a0a',
    'axes.facecolor': '#0a0a0a',
    'savefig.facecolor': '#0a0a0a',
    'axes.edgecolor': '#444444',
    'axes.labelcolor': '#ffffff',
    'text.color': '#ffffff',
    'xtick.color': '#ffffff',
    'ytick.color': '#ffffff',
    'grid.color': '#222222',
    'grid.alpha': 0.5,
    'figure.figsize': (12, 7),
    'figure.dpi': 300
})

ACCENT_COLOR = '#00d4ff'
WATERMARK_TEXT = "CodeAlpha | Levitation Dynamics Research"

def add_watermark(fig):
    fig.text(0.95, 0.02, WATERMARK_TEXT,
             fontsize=12, color='gray',
             ha='right', va='bottom', alpha=0.5,
             path_effects=[path_effects.withSimplePatchShadow(alpha=0.2, offset=(1, -1))])

def save_and_add_to_pdf(fig, filename, pdf, caption=None):
    add_watermark(fig)
    if caption:
        fig.text(0.5, 0.01, caption, ha='center', va='bottom', fontsize=10, color='#aaaaaa', wrap=True)
        fig.subplots_adjust(bottom=0.15)
    else:
        fig.subplots_adjust(bottom=0.1)
    
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

# ==========================================
# DATA LOADING
# ==========================================
print("Loading data...")
df = pd.read_csv('levitation_cleaned_experiments.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Create a PDF object
pdf_pages = PdfPages('visualization_report.pdf')

# ==========================================
# CHART 1 — Levitation Altitude Distribution
# ==========================================
print("Generating Chart 1...")
fig, ax = plt.subplots()
sns.histplot(df['Levitation_Altitude_m'], kde=True, ax=ax, 
             color='#1f77b4', edgecolor='black', linewidth=1) # Blue

# Creating a gradient-like effect for histogram bars using standard plot (difficult in seaborn directly, so we just use standard styling)
# Getting the patches
for p in ax.patches:
    p.set_alpha(0.8)

mean_val = df['Levitation_Altitude_m'].mean()
median_val = df['Levitation_Altitude_m'].median()
ax.axvline(mean_val, color='#ff7f0e', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}m')
ax.axvline(median_val, color='#2ca02c', linestyle='-', linewidth=2, label=f'Median: {median_val:.2f}m')

ax.set_title("Distribution of Levitation Altitude Across Experiments", fontsize=16, fontweight='bold', color=ACCENT_COLOR, pad=20)
ax.set_xlabel("Levitation Altitude (meters)")
ax.set_ylabel("Frequency")
ax.legend()
ax.text(0.01, 1.02, "Source: Task 2 EDA Cleaned Data", transform=ax.transAxes, fontsize=8, color='gray')

save_and_add_to_pdf(fig, 'altitude_distribution.png', pdf_pages, 
                    caption="Chart 1: Histogram showing the distribution of achieved levitation altitudes.")

# ==========================================
# CHART 2 — Material vs Average Altitude
# ==========================================
print("Generating Chart 2...")
mat_avg = df.groupby('Material_Type')['Levitation_Altitude_m'].mean().sort_values(ascending=True)

fig, ax = plt.subplots()
bars = ax.barh(mat_avg.index, mat_avg.values, color='#333333')

# Custom palette for top 3 (they are at the end of the ascending list)
if len(bars) >= 3:
    bars[-1].set_color('#FFD700') # Gold
    bars[-2].set_color('#C0C0C0') # Silver
    bars[-3].set_color('#CD7F32') # Bronze

for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}m', 
            ha='left', va='center', color='white', fontweight='bold')

ax.set_title("Average Levitation Height by Material Type", fontsize=16, fontweight='bold', color=ACCENT_COLOR, pad=20)
ax.set_xlabel("Average Altitude (meters)")
ax.set_ylabel("Material Type")
ax.text(0.01, 1.02, "Source: Task 2 EDA Cleaned Data", transform=ax.transAxes, fontsize=8, color='gray')
# Remove top and right spines
sns.despine(ax=ax, top=True, right=True)

save_and_add_to_pdf(fig, 'material_altitude_bar.png', pdf_pages, 
                    caption="Chart 2: Horizontal bar chart ranking materials by average levitation altitude achieved.")

# ==========================================
# CHART 3 — Correlation Heatmap
# ==========================================
print("Generating Chart 3...")
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='RdYlGn', 
            center=0, square=True, linewidths=.5, cbar_kws={"shrink": .8}, ax=ax)

ax.set_title("Feature Correlation Matrix — Levitation Dynamics Parameters", fontsize=16, fontweight='bold', color=ACCENT_COLOR, pad=20)
ax.text(0.01, 1.02, "Source: Task 2 EDA Cleaned Data", transform=ax.transAxes, fontsize=8, color='gray')

save_and_add_to_pdf(fig, 'correlation_heatmap.png', pdf_pages, 
                    caption="Chart 3: Correlation matrix of experimental variables, masked for clean visualization.")

# ==========================================
# CHART 4 — Power vs Altitude Scatter Plot
# ==========================================
print("Generating Chart 4...")
fig, ax = plt.subplots()

sns.scatterplot(data=df, x='Power_Consumption_W', y='Levitation_Altitude_m', 
                hue='Material_Type', size='Success_Rate_Percent', sizes=(20, 200),
                alpha=0.7, ax=ax, palette='viridis')

# Regression line
sns.regplot(data=df, x='Power_Consumption_W', y='Levitation_Altitude_m', 
            scatter=False, ax=ax, color=ACCENT_COLOR, line_kws={'linestyle':'--'})

slope, intercept, r_value, p_value, std_err = stats.linregress(df['Power_Consumption_W'], df['Levitation_Altitude_m'])
r2 = r_value ** 2
eq_text = f"y = {slope:.4f}x + {intercept:.2f}\nR² = {r2:.3f}"
ax.text(0.05, 0.95, eq_text, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='#222222', alpha=0.8))

ax.set_title("Power Consumption vs Levitation Altitude", fontsize=16, fontweight='bold', color=ACCENT_COLOR, pad=20)
ax.set_xlabel("Power Consumption (Watts)")
ax.set_ylabel("Levitation Altitude (meters)")
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax.text(0.01, 1.02, "Source: Task 2 EDA Cleaned Data", transform=ax.transAxes, fontsize=8, color='gray')

save_and_add_to_pdf(fig, 'power_vs_altitude_scatter.png', pdf_pages, 
                    caption="Chart 4: Scatter plot demonstrating the relationship between power and altitude.")

# ==========================================
# CHART 5 — Experiment Success Rate Over Time
# ==========================================
print("Generating Chart 5...")
monthly_success = df.groupby('Month_Year')['Success_Rate_Percent'].mean().reset_index()
monthly_success['Date_Idx'] = pd.to_datetime(monthly_success['Month_Year'] + '-01')
monthly_success = monthly_success.sort_values('Date_Idx')
monthly_success['Rolling_3M'] = monthly_success['Success_Rate_Percent'].rolling(window=3, min_periods=1).mean()

fig, ax = plt.subplots()
ax.plot(monthly_success['Date_Idx'], monthly_success['Success_Rate_Percent'], 
        color='#008080', label='Monthly Avg', alpha=0.5) # Teal
ax.fill_between(monthly_success['Date_Idx'], monthly_success['Success_Rate_Percent'], 
                color='#008080', alpha=0.2)
ax.plot(monthly_success['Date_Idx'], monthly_success['Rolling_3M'], 
        color=ACCENT_COLOR, linewidth=2, label='3-Month Rolling Avg')

ax.set_title("Monthly Experiment Success Rate Trend", fontsize=16, fontweight='bold', color=ACCENT_COLOR, pad=20)
ax.set_xlabel("Date (Month-Year)")
ax.set_ylabel("Success Rate (%)")
ax.legend()
ax.text(0.01, 1.02, "Source: Task 2 EDA Cleaned Data", transform=ax.transAxes, fontsize=8, color='gray')

save_and_add_to_pdf(fig, 'success_rate_trend.png', pdf_pages, 
                    caption="Chart 5: Trend of experiment success rates over time with area fill.")

# ==========================================
# CHART 6 — Lab Performance Comparison
# ==========================================
print("Generating Chart 6...")
fig, ax = plt.subplots()

sns.boxplot(data=df, x='Lab_ID', y='Levitation_Altitude_m', ax=ax,
            palette='mako', flierprops={"marker": "x", "markerfacecolor": "red", "markeredgecolor": "red"})

ax.set_title("Levitation Performance Distribution by Lab", fontsize=16, fontweight='bold', color=ACCENT_COLOR, pad=20)
ax.set_xlabel("Laboratory ID")
ax.set_ylabel("Levitation Altitude (meters)")
ax.text(0.01, 1.02, "Source: Task 2 EDA Cleaned Data", transform=ax.transAxes, fontsize=8, color='gray')

save_and_add_to_pdf(fig, 'lab_comparison_boxplot.png', pdf_pages, 
                    caption="Chart 6: Box plot comparing altitude distributions across different laboratories.")

pdf_pages.close()
print("Saved visualization_report.pdf")

# ==========================================
# CHART 8 — 3D Visualization (Plotly)
# ==========================================
print("Generating Chart 8...")
fig3d = px.scatter_3d(df, x='Power_Consumption_W', y='Temperature_K', z='Levitation_Altitude_m',
                      color='Material_Type', size='Success_Rate_Percent',
                      title="3D Parameter Space of Levitation Dynamics Experiments",
                      template="plotly_dark",
                      color_discrete_sequence=px.colors.qualitative.Bold)

# Update layout for better dark theme and aesthetics
fig3d.update_layout(
    scene=dict(
        xaxis_title='Power (W)',
        yaxis_title='Temperature (K)',
        zaxis_title='Altitude (m)',
        xaxis=dict(backgroundcolor="#111111", gridcolor="#333"),
        yaxis=dict(backgroundcolor="#111111", gridcolor="#333"),
        zaxis=dict(backgroundcolor="#111111", gridcolor="#333")
    ),
    paper_bgcolor='#0a0a0a',
    font=dict(color='#ffffff')
)

fig3d.add_annotation(
    text="Source: Task 2 EDA Cleaned Data<br>" + WATERMARK_TEXT,
    xref="paper", yref="paper",
    x=0, y=0, showarrow=False,
    font=dict(size=10, color="gray")
)

fig3d.write_html('3d_scatter.html')
print("Saved 3d_scatter.html")

print("All charts generated successfully!")
