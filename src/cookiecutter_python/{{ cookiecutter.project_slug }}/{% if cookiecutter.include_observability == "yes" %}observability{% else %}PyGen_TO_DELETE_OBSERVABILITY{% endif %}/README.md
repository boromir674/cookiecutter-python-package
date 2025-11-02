# 📊 {{ cookiecutter.project_name }} - Observability Stack

This directory contains the observability infrastructure for **{{ cookiecutter.project_name }}**, providing log aggregation and visualization capabilities.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Port 3000 available on host for Grafana web interface

### Start Observability Stack

```bash
# Start all observability services
cd observability
docker-compose -f docker-compose.observability.yml up -d

# Check services are running
docker-compose -f docker-compose.observability.yml ps
```

### Access Grafana Dashboard

- **URL**: http://localhost:3000
- **Username**: `admin`
- **Password**: `admin123`

## 📈 What's Included

### Services
- **Grafana** (port 3000): Web-based visualization and dashboards
- **Loki** (port 3100): Log aggregation and storage
- **Promtail**: Log collection agent

### Log Sources
- **Application Logs**: JSON structured logs from {{ cookiecutter.pkg_name }}
- **Test Logs**: Plain text logs from pytest, tox, and other tools

## 📊 Using the Dashboard

### Viewing Logs
1. Open Grafana at http://localhost:3000
2. Navigate to **Explore** in the sidebar
3. Select **Loki** as the data source
4. Use these queries to get started:

```logql
# All application logs
{job="{{ cookiecutter.pkg_name }}-logs"}

# Error logs only
{job="{{ cookiecutter.pkg_name }}-logs",level="ERROR"}

# Log rate by level (logs per minute)
sum by (level) (rate({job="{{ cookiecutter.pkg_name }}-logs"}[1m]))
```

### Creating Dashboards
1. Click **"+"** → **Dashboard** → **Add new panel**
2. Select **Loki** as data source
3. Enter LogQL queries to visualize your data
4. Customize visualization type (time series, logs, stat, etc.)

## 📝 Generating Logs

### Application Logs (JSON Format)
```python
import json
import logging

# Configure JSON logging
def setup_logging():
    logging.basicConfig(
        format='{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s","component":"{{ cookiecutter.pkg_name }}"}',
        level=logging.INFO
    )

# Generate sample logs
logger = logging.getLogger(__name__)
logger.info("Application started")
logger.warning("Configuration deprecated")
logger.error("Processing failed")
```

### Quick Test Logs
```bash
# Generate sample logs for testing
mkdir -p logs
echo '{"timestamp":"2024-01-01T12:00:00Z","level":"INFO","message":"Application started","component":"{{ cookiecutter.pkg_name }}"}' >> logs/app.log
echo '{"timestamp":"2024-01-01T12:00:01Z","level":"ERROR","message":"Something went wrong","component":"validator"}' >> logs/app.log

# Run tests to generate test logs
python -m pytest -v 2>&1 | tee logs/pytest.log
```

## 🛠️ Configuration

### Loki Configuration
- **File**: `loki/loki-config.yml`
- **Storage**: Local filesystem storage
- **Retention**: Configurable in limits_config

### Promtail Configuration
- **File**: `promtail/promtail-config.yml`
- **Watched Paths**: 
  - `/logs/*.log` (application logs)
  - `/workspace/logs/*.log` (test logs)
- **Log Parsing**: Automatic JSON and regex-based level extraction

### Grafana Configuration
- **Data Sources**: Auto-provisioned Loki connection
- **Dashboards**: Configurable dashboard provisioning
- **Persistence**: Data persisted in Docker volumes

## 🔧 Customization

### Adding Custom Log Sources
Edit `promtail/promtail-config.yml` to add new log file patterns:

```yaml
scrape_configs:
  - job_name: "my-custom-logs"
    static_configs:
      - targets: [localhost]
        labels:
          job: "custom"
          __path__: "/path/to/my/logs/*.log"
```

### Creating Custom Dashboards
1. Create dashboards in Grafana UI
2. Export dashboard JSON
3. Save to `grafana/dashboards/` directory
4. Restart Grafana service to load automatically

## 🚨 Troubleshooting

### Services Not Starting
```bash
# Check service logs
docker-compose -f docker-compose.observability.yml logs grafana
docker-compose -f docker-compose.observability.yml logs loki
docker-compose -f docker-compose.observability.yml logs promtail
```

### No Logs Appearing
1. Check if log files exist in `logs/` directory
2. Verify Promtail is reading files: `docker logs {{ cookiecutter.project_slug }}-promtail`
3. Check Loki is receiving data: http://localhost:3100/metrics

### Port Conflicts
If port 3000 is in use, edit `docker-compose.observability.yml`:
```yaml
grafana:
  ports:
    - "3001:3000"  # Use port 3001 instead
```

## 🎯 Next Steps

1. **Create Custom Dashboards**: Build visualizations specific to your application
2. **Set Up Alerts**: Configure Grafana alerts for critical log patterns
3. **Add Metrics**: Consider adding Prometheus for application metrics
4. **Production Setup**: Configure proper authentication and security for production use

For more information, visit the [Grafana Documentation](https://grafana.com/docs/) and [Loki Documentation](https://grafana.com/docs/loki/).