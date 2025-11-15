import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import numpy as np
from collections import deque
import random
import json

# Page config
st.set_page_config(
    page_title="Real-Time Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .alert-banner {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    .alert-success {
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    .pipeline-card {
        background: rgba(107, 91, 149, 0.05);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(107, 91, 149, 0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_points' not in st.session_state:
    st.session_state.data_points = deque(maxlen=200)  # Increased buffer
    st.session_state.pipeline_data = {}  # Multi-pipeline support
    st.session_state.alerts = deque(maxlen=50)
    st.session_state.start_time = datetime.now()
    st.session_state.anomalies_detected = 0

# Header
st.title("📊 Advanced Real-Time Analytics Dashboard")
st.markdown("**Enterprise-grade data pipeline monitoring with anomaly detection and multi-pipeline support**")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Data Source
    data_source = st.selectbox(
        "Data Source",
        ["Simulated Pipeline", "Multi-Pipeline View", "Historical Analysis", "Anomaly Detection Mode"]
    )
    
    # Pipeline Selection (for multi-pipeline)
    if data_source == "Multi-Pipeline View":
        num_pipelines = st.slider("Number of Pipelines", 2, 5, 3)
    else:
        num_pipelines = 1
    
    # Update Settings
    update_interval = st.slider("Update Interval (seconds)", 1, 10, 2)
    auto_refresh = st.checkbox("Auto Refresh", value=True)
    
    # Alert Thresholds
    st.subheader("🚨 Alert Thresholds")
    latency_threshold = st.slider("Latency Alert (ms)", 100, 1000, 400)
    error_threshold = st.slider("Error Rate Alert (%)", 1, 10, 5)
    cpu_threshold = st.slider("CPU Alert (%)", 50, 100, 80)
    
    # Advanced Options
    st.subheader("🔧 Advanced")
    show_anomalies = st.checkbox("Show Anomaly Detection", value=True)
    enable_export = st.checkbox("Enable Data Export", value=True)
    show_heatmap = st.checkbox("Show Correlation Heatmap", value=False)
    
    if st.button("🔄 Reset All Data"):
        st.session_state.data_points = deque(maxlen=200)
        st.session_state.pipeline_data = {}
        st.session_state.alerts = deque(maxlen=50)
        st.session_state.start_time = datetime.now()
        st.session_state.anomalies_detected = 0
        st.rerun()

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_realistic_data_point(pipeline_id=0, base_throughput=500):
    """
    Generate realistic pipeline data with trends, patterns, and occasional anomalies.
    This simulates real-world behavior without needing API keys.
    """
    timestamp = datetime.now()
    
    # Create realistic trends (not just random)
    time_factor = (timestamp - st.session_state.start_time).total_seconds() / 60  # minutes
    
    # Simulate daily patterns (higher during business hours)
    hour = timestamp.hour
    business_hour_factor = 1.0
    if 9 <= hour <= 17:  # Business hours
        business_hour_factor = 1.3
    elif 0 <= hour <= 6:  # Off hours
        business_hour_factor = 0.6
    
    # Add some realistic variation
    trend = np.sin(time_factor / 30) * 0.2  # Slow trend
    noise = random.gauss(0, 0.1)  # Gaussian noise
    
    # Throughput with realistic patterns
    throughput_base = base_throughput * business_hour_factor * (1 + trend + noise)
    throughput = max(50, int(throughput_base))
    
    # Latency correlated with throughput (higher load = higher latency)
    latency_base = 100 + (throughput / 10) + random.gauss(0, 20)
    latency_ms = max(50, int(latency_base))
    
    # Error rate (occasional spikes)
    error_rate = random.uniform(0, 2)
    if random.random() < 0.05:  # 5% chance of error spike
        error_rate = random.uniform(3, 8)
    
    # System resources (correlated with throughput)
    cpu_base = 30 + (throughput / 20) + random.gauss(0, 5)
    cpu_usage = max(10, min(95, cpu_base))
    
    memory_base = 40 + (throughput / 25) + random.gauss(0, 5)
    memory_usage = max(20, min(90, memory_base))
    
    # Active connections
    connections = int(10 + (throughput / 15) + random.gauss(0, 5))
    connections = max(5, min(150, connections))
    
    # Data quality metrics
    data_quality = 100 - random.uniform(0, 3)
    if random.random() < 0.03:  # 3% chance of quality issue
        data_quality = random.uniform(85, 95)
    
    # Processing time
    processing_time = latency_ms + random.randint(-10, 10)
    
    return {
        'timestamp': timestamp,
        'pipeline_id': pipeline_id,
        'throughput': throughput,
        'latency_ms': latency_ms,
        'error_rate': error_rate,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'active_connections': connections,
        'data_quality': data_quality,
        'processing_time_ms': processing_time,
        'records_processed': throughput * update_interval,
        'successful_requests': throughput * (1 - error_rate / 100)
    }

def detect_anomalies(df):
    """Detect anomalies using statistical methods"""
    if len(df) < 10:
        return []
    
    anomalies = []
    
    # Z-score based anomaly detection
    for metric in ['latency_ms', 'error_rate', 'cpu_usage']:
        if metric in df.columns:
            mean = df[metric].mean()
            std = df[metric].std()
            if std > 0:
                z_scores = np.abs((df[metric] - mean) / std)
                anomaly_indices = df[z_scores > 2.5].index
                for idx in anomaly_indices:
                    anomalies.append({
                        'timestamp': df.loc[idx, 'timestamp'],
                        'metric': metric,
                        'value': df.loc[idx, metric],
                        'severity': 'high' if z_scores.loc[idx] > 3 else 'medium'
                    })
    
    return anomalies

def check_alerts(data_point, latency_threshold, error_threshold, cpu_threshold):
    """Check if current metrics trigger alerts"""
    alerts = []
    
    if data_point['latency_ms'] > latency_threshold:
        alerts.append({
            'type': 'warning',
            'message': f"High Latency: {data_point['latency_ms']:.0f}ms (threshold: {latency_threshold}ms)",
            'timestamp': data_point['timestamp']
        })
    
    if data_point['error_rate'] > error_threshold:
        alerts.append({
            'type': 'danger',
            'message': f"High Error Rate: {data_point['error_rate']:.1f}% (threshold: {error_threshold}%)",
            'timestamp': data_point['timestamp']
        })
    
    if data_point['cpu_usage'] > cpu_threshold:
        alerts.append({
            'type': 'warning',
            'message': f"High CPU Usage: {data_point['cpu_usage']:.1f}% (threshold: {cpu_threshold}%)",
            'timestamp': data_point['timestamp']
        })
    
    return alerts

# ============================================================================
# DATA COLLECTION
# ============================================================================

# Generate data based on selected mode
if data_source == "Multi-Pipeline View":
    for i in range(num_pipelines):
        base_throughput = 300 + (i * 100)
        data = generate_realistic_data_point(pipeline_id=i, base_throughput=base_throughput)
        if i not in st.session_state.pipeline_data:
            st.session_state.pipeline_data[i] = deque(maxlen=200)
        st.session_state.pipeline_data[i].append(data)
        st.session_state.data_points.append(data)
        
        # Check alerts
        alerts = check_alerts(data, latency_threshold, error_threshold, cpu_threshold)
        for alert in alerts:
            st.session_state.alerts.append(alert)
else:
    data = generate_realistic_data_point()
    st.session_state.data_points.append(data)
    
    # Check alerts
    alerts = check_alerts(data, latency_threshold, error_threshold, cpu_threshold)
    for alert in alerts:
        st.session_state.alerts.append(alert)

# ============================================================================
# METRICS CALCULATION
# ============================================================================

if len(st.session_state.data_points) > 0:
    df = pd.DataFrame(list(st.session_state.data_points))
    
    # Calculate comprehensive metrics
    metrics = {
        'total_requests': len(st.session_state.data_points),
        'avg_latency': df['latency_ms'].mean(),
        'p95_latency': df['latency_ms'].quantile(0.95),
        'p99_latency': df['latency_ms'].quantile(0.99),
        'success_rate': 100 - df['error_rate'].mean(),
        'throughput': df['throughput'].mean(),
        'total_records': df['records_processed'].sum(),
        'avg_cpu': df['cpu_usage'].mean(),
        'avg_memory': df['memory_usage'].mean(),
        'data_quality': df['data_quality'].mean(),
        'uptime_minutes': (datetime.now() - st.session_state.start_time).total_seconds() / 60
    }
    
    # Detect anomalies
    if show_anomalies:
        anomalies = detect_anomalies(df)
        st.session_state.anomalies_detected = len(anomalies)
else:
    metrics = {}
    df = pd.DataFrame()

# ============================================================================
# ALERTS DISPLAY
# ============================================================================

if len(st.session_state.alerts) > 0:
    st.subheader("🚨 Active Alerts")
    recent_alerts = list(st.session_state.alerts)[-5:]  # Show last 5
    
    for alert in reversed(recent_alerts):
        alert_class = alert['type']
        st.markdown(
            f'<div class="alert-banner alert-{alert_class}">'
            f'<strong>{alert["timestamp"].strftime("%H:%M:%S")}</strong> - {alert["message"]}'
            f'</div>',
            unsafe_allow_html=True
        )

# ============================================================================
# KEY METRICS ROW
# ============================================================================

if len(df) > 0:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Requests",
            f"{metrics['total_requests']:,}",
            delta=f"+{len(st.session_state.data_points)}"
        )
    
    with col2:
        p95_delta = f"P95: {metrics['p95_latency']:.0f}ms"
        st.metric(
            "Avg Latency",
            f"{metrics['avg_latency']:.0f}ms",
            delta=p95_delta
        )
    
    with col3:
        st.metric(
            "Success Rate",
            f"{metrics['success_rate']:.1f}%",
            delta=f"Quality: {metrics['data_quality']:.1f}%"
        )
    
    with col4:
        st.metric(
            "Throughput",
            f"{metrics['throughput']:.0f}/s",
            delta=f"Total: {metrics['total_records']:,.0f}"
        )
    
    with col5:
        anomaly_badge = f"⚠️ {st.session_state.anomalies_detected}" if st.session_state.anomalies_detected > 0 else "✓ 0"
        st.metric(
            "Anomalies",
            anomaly_badge,
            delta=f"Uptime: {metrics['uptime_minutes']:.1f}m"
        )

# ============================================================================
# ADVANCED VISUALIZATIONS
# ============================================================================

if len(df) > 0:
    # Row 1: Main Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Throughput & Latency Trend")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['throughput'],
                name="Throughput",
                line=dict(color='#667eea', width=2)
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['latency_ms'],
                name="Latency",
                line=dict(color='#ff6b6b', width=2)
            ),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Throughput (req/s)", secondary_y=False)
        fig.update_yaxes(title_text="Latency (ms)", secondary_y=True)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Performance Distribution")
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=df['latency_ms'],
            name='Latency (ms)',
            boxmean='sd',
            marker_color='#667eea'
        ))
        
        fig.add_trace(go.Box(
            y=df['error_rate'],
            name='Error Rate (%)',
            boxmean='sd',
            marker_color='#764ba2'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: System Resources & Error Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖥️ System Resources")
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['cpu_usage'],
            name='CPU',
            fill='tozeroy',
            line=dict(color='#667eea'),
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['memory_usage'],
            name='Memory',
            fill='tozeroy',
            line=dict(color='#764ba2'),
            fillcolor='rgba(118, 75, 162, 0.2)'
        ))
        
        # Add threshold lines
        fig.add_hline(y=cpu_threshold, line_dash="dash", line_color="red", 
                     annotation_text=f"CPU Alert ({cpu_threshold}%)")
        
        fig.update_layout(
            title="CPU & Memory Usage Over Time",
            xaxis_title="Time",
            yaxis_title="Usage (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Error Rate & Data Quality")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['error_rate'],
                name="Error Rate",
                fill='tozeroy',
                line=dict(color='#ff6b6b'),
                fillcolor='rgba(255, 107, 107, 0.3)'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['data_quality'],
                name="Data Quality",
                line=dict(color='#28a745', width=2)
            ),
            secondary_y=True
        )
        
        # Add threshold line
        fig.add_hline(y=error_threshold, line_dash="dash", line_color="orange",
                     annotation_text=f"Error Alert ({error_threshold}%)", secondary_y=False)
        
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Error Rate (%)", secondary_y=False)
        fig.update_yaxes(title_text="Data Quality (%)", secondary_y=True)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Row 3: Multi-Pipeline View or Advanced Analytics
    if data_source == "Multi-Pipeline View" and len(st.session_state.pipeline_data) > 1:
        st.subheader("🔀 Multi-Pipeline Comparison")
        
        fig = go.Figure()
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
        
        for pipeline_id, pipeline_df in st.session_state.pipeline_data.items():
            if len(pipeline_df) > 0:
                pipeline_df_clean = pd.DataFrame(list(pipeline_df))
                fig.add_trace(go.Scatter(
                    x=pipeline_df_clean['timestamp'],
                    y=pipeline_df_clean['throughput'],
                    name=f'Pipeline {pipeline_id + 1}',
                    line=dict(color=colors[pipeline_id % len(colors)], width=2)
                ))
        
        fig.update_layout(
            title="Throughput Comparison Across Pipelines",
            xaxis_title="Time",
            yaxis_title="Throughput (req/s)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Heatmap
    if show_heatmap and len(df) > 10:
        st.subheader("🔥 Metric Correlation Heatmap")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Metric", y="Metric", color="Correlation"),
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Gauge Charts for Key Metrics
    st.subheader("🎯 Performance Gauges")
    gauge_col1, gauge_col2, gauge_col3, gauge_col4 = st.columns(4)
    
    with gauge_col1:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = metrics['success_rate'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Success Rate"},
            delta = {'reference': 95},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 90], 'color': "lightgray"},
                    {'range': [90, 100], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with gauge_col2:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = metrics['avg_latency'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Avg Latency (ms)"},
            gauge = {
                'axis': {'range': [None, 500]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 200], 'color': "lightgreen"},
                    {'range': [200, 400], 'color': "yellow"},
                    {'range': [400, 500], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': latency_threshold
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with gauge_col3:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = metrics['avg_cpu'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CPU Usage (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': cpu_threshold
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with gauge_col4:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = metrics['data_quality'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Data Quality (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 90], 'color': "lightgray"},
                    {'range': [90, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# DATA EXPORT
# ============================================================================

if enable_export and len(df) > 0:
    with st.expander("📥 Export Data", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name=f"pipeline_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="📄 Download JSON",
                data=json_data,
                file_name=f"pipeline_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ============================================================================
# DATA TABLE
# ============================================================================

with st.expander("📋 Recent Data Points", expanded=False):
    if len(df) > 0:
        display_df = df[['timestamp', 'throughput', 'latency_ms', 'error_rate', 
                         'cpu_usage', 'memory_usage', 'data_quality']].tail(30)
        st.dataframe(
            display_df.style.format({
                'throughput': '{:.0f}',
                'latency_ms': '{:.0f}',
                'error_rate': '{:.2f}',
                'cpu_usage': '{:.1f}',
                'memory_usage': '{:.1f}',
                'data_quality': '{:.1f}'
            }),
            use_container_width=True,
            hide_index=True
        )

# ============================================================================
# FOOTER & INFO
# ============================================================================

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Built with Streamlit | Enterprise Data Pipeline Monitoring**")

with col2:
    st.markdown(f"**Status:** {'🟢 Running' if auto_refresh else '⏸️ Paused'} | "
                f"**Data Points:** {len(st.session_state.data_points)} | "
                f"**Mode:** {data_source}")

# Info about data source
with st.expander("ℹ️ About This Dashboard", expanded=False):
    st.markdown("""
    ### 📊 Data Source Explanation
    
    **This dashboard uses simulated data** - no API keys required!
    
    The data generation includes:
    - ✅ **Realistic patterns**: Business hour variations, trends, correlations
    - ✅ **Statistical noise**: Gaussian distributions for natural variation
    - ✅ **Anomaly simulation**: Occasional spikes and issues (5% chance)
    - ✅ **Multi-metric correlation**: Metrics influence each other realistically
    
    ### 🔌 Adding Real Data Sources
    
    To connect real APIs, replace the `generate_realistic_data_point()` function:
    
    ```python
    # Example: GitHub API
    def fetch_github_data():
        response = requests.get(
            "https://api.github.com/users/yourusername/events",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
        # Process and return metrics
        return processed_data
    
    # Example: Database connection
    def fetch_pipeline_metrics():
        conn = psycopg2.connect(DATABASE_URL)
        # Query your pipeline metrics table
        return metrics
    ```
    
    See `README.md` for detailed integration examples!
    """)

# Auto-refresh
if auto_refresh:
    time.sleep(update_interval)
    st.rerun()
