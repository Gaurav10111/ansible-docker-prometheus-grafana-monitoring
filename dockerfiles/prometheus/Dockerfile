
FROM rockylinux:8

# Install required tools
RUN dnf install -y wget tar && \
    useradd -m prometheus && \
    cd /opt && \
    wget https://github.com/prometheus/prometheus/releases/download/v2.52.0/prometheus-2.52.0.linux-amd64.tar.gz && \
    tar -xzf prometheus-2.52.0.linux-amd64.tar.gz && \
    mv prometheus-2.52.0.linux-amd64 prometheus && \
    chown -R prometheus:prometheus /opt/prometheus && \
    rm -f prometheus-2.52.0.linux-amd64.tar.gz

COPY prometheus.yml /opt/prometheus/prometheus.yml

WORKDIR /opt/prometheus
USER prometheus
EXPOSE 9090
CMD ["./prometheus", "--config.file=prometheus.yml", "--storage.tsdb.path=./data"]


