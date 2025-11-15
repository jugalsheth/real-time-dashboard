# 📊 Data Source Explanation

## How Does the Dashboard Work Without API Keys?

The dashboard currently uses **simulated data** - sophisticated algorithms that generate realistic pipeline metrics without needing any external APIs or keys.

## 🎲 What Makes It "Realistic"?

### 1. **Pattern-Based Generation** (Not Just Random!)
- **Business Hour Patterns**: Higher throughput during 9 AM - 5 PM
- **Trends**: Slow sine wave patterns simulating daily/weekly cycles
- **Correlations**: Metrics influence each other (high throughput → higher latency)

### 2. **Statistical Realism**
- **Gaussian Noise**: Natural variation using normal distributions
- **Anomaly Injection**: 3-5% chance of error spikes or quality issues
- **Realistic Ranges**: Values stay within production-like bounds

### 3. **Multi-Metric Relationships**
```python
# Example correlations in the code:
- Throughput ↑ → Latency ↑ (realistic!)
- Throughput ↑ → CPU Usage ↑
- Error spikes → Data Quality ↓
- Business hours → Throughput ↑
```

## 🔌 Adding Real Data Sources

### Option 1: GitHub API (Free, No Auth for Public Repos)

```python
import requests

def fetch_github_activity(username="jugalsheth"):
    """Fetch real GitHub activity"""
    url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(url)
    events = response.json()
    
    # Process events into metrics
    return {
        'throughput': len(events),
        'latency_ms': calculate_avg_response_time(events),
        'error_rate': 0,  # GitHub API is reliable
        # ... more metrics
    }
```

### Option 2: Database Connection (PostgreSQL/Snowflake)

```python
import psycopg2
import pandas as pd

def fetch_pipeline_metrics():
    """Connect to your data warehouse"""
    conn = psycopg2.connect(
        host="your-host",
        database="your-db",
        user="your-user",
        password="your-password"
    )
    
    query = """
    SELECT 
        timestamp,
        throughput,
        latency_ms,
        error_rate
    FROM pipeline_metrics
    WHERE timestamp > NOW() - INTERVAL '1 hour'
    ORDER BY timestamp DESC
    """
    
    df = pd.read_sql(query, conn)
    return df.to_dict('records')
```

### Option 3: Kafka/Redis Stream

```python
from kafka import KafkaConsumer
import json

def fetch_kafka_metrics():
    """Consume from Kafka topic"""
    consumer = KafkaConsumer(
        'pipeline-metrics',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    messages = []
    for message in consumer:
        messages.append(message.value)
        if len(messages) >= 10:
            break
    
    return process_messages(messages)
```

### Option 4: REST API Endpoint

```python
import requests

def fetch_custom_api():
    """Call your internal monitoring API"""
    response = requests.get(
        "https://your-api.com/metrics",
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )
    return response.json()
```

## 🔐 Setting Up API Keys (When Needed)

### Streamlit Secrets (Recommended)

1. Create `.streamlit/secrets.toml`:
```toml
[api_keys]
github_token = "your_github_token"
database_url = "postgresql://user:pass@host/db"
custom_api_key = "your_api_key"
```

2. Use in code:
```python
import streamlit as st

github_token = st.secrets["api_keys"]["github_token"]
```

### Environment Variables

```bash
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."
```

Then in Python:
```python
import os
github_token = os.getenv("GITHUB_TOKEN")
```

## 📈 Current Simulation Features

The simulated data includes:

✅ **Realistic Business Patterns**
- Higher activity during business hours
- Lower activity at night
- Gradual trends over time

✅ **Statistical Accuracy**
- Normal distributions for natural variation
- Occasional anomalies (like real systems!)
- Correlated metrics

✅ **Production-Like Metrics**
- Throughput: 50-1000 req/s
- Latency: 50-500ms (with P95/P99)
- Error rates: 0-5% (spikes to 8%)
- CPU/Memory: Realistic usage patterns

## 🚀 Next Steps

1. **Test with Simulated Data** (Current)
   - Perfect for demos and portfolios
   - No setup required
   - Shows all features

2. **Add Real APIs Gradually**
   - Start with public APIs (GitHub, Twitter)
   - Then add database connections
   - Finally, connect to your actual pipelines

3. **Hybrid Approach**
   - Use real data when available
   - Fall back to simulation for missing metrics
   - Best of both worlds!

---

**The simulation is sophisticated enough to demonstrate real-world scenarios without needing actual infrastructure!** 🎯

