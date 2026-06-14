# 🌌 Levitation Dynamics Research Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75)

Welcome to the **Levitation Dynamics Research Dashboard** project! This repository contains a complete suite for simulating, visualizing, and analyzing advanced levitation dynamics experiments. It transforms raw experimental data into publication-quality insights through an interactive Streamlit dashboard and a beautifully styled static HTML hub.

## ✨ Features

- **Interactive Streamlit Dashboard (`app.py`)**: A modern, dark-themed dashboard allowing users to filter experimental data by date and material type. Features dynamic KPI cards, interactive Plotly charts, and a 3D scatter plot.
- **Static Visualization Hub (`index.html`)**: A premium HTML dashboard with glassmorphism design and micro-animations to elegantly present static research findings and link to interactive charts.
- **Data Generation Engine (`generate_mock_data.py`)**: A configurable script to simulate robust levitation experimental datasets, generating features such as Power Consumption, Temperature, Levitation Altitude, Material Type, and Success Rates.
- **Automated Reporting (`generate_charts.py`)**: A powerful visualization script that utilizes `seaborn`, `matplotlib`, and `plotly` to automatically output high-DPI PNGs, an interactive 3D HTML plot, and a consolidated PDF report of the findings.

## 🗂️ Project Structure

```text
├── app.py                             # Main Streamlit dashboard application
├── index.html                         # Beautiful static HTML visualization hub
├── generate_mock_data.py              # Script to simulate the levitation dataset
├── generate_charts.py                 # Script to create static images, PDF, and 3D HTML plot
├── levitation_cleaned_experiments.csv # The core dataset
├── requirements.txt                   # Python dependencies
└── *.png, *.pdf, *.html               # Generated outputs (Charts, Report, 3D scatter)
```

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/levitation-dynamics.git
   cd levitation-dynamics
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage Guide

### 1. Generate the Dataset
If you want to generate a fresh dataset from scratch, run:
```bash
python generate_mock_data.py
```
*This will create the `levitation_cleaned_experiments.csv` file.*

### 2. Generate Visualizations & Reports
To generate all the high-resolution charts, the correlation matrix, the 3D scatter plot, and the comprehensive PDF report:
```bash
python generate_charts.py
```
*Outputs: Several `.png` files, `visualization_report.pdf`, and `3d_scatter.html`.*

### 3. Run the Streamlit Dashboard
Launch the interactive dashboard to explore the data dynamically:
```bash
streamlit run app.py
```
*The app will automatically open in your default web browser.*

### 4. View the Static Web Hub
Simply open `index.html` in any web browser to view the premium dashboard containing all the static charts and a gateway to the interactive 3D visualization.

## 💻 Tech Stack
- **Frontend/Dashboard:** Streamlit, HTML, CSS (Glassmorphism design)
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Plotly Express, Plotly Graph Objects, Seaborn, Matplotlib
- **Statistical Analysis:** SciPy, Statsmodels

