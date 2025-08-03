FROM rockylinux:8

RUN dnf install -y wget tar && \
    useradd -m node_exporter && \
    mkdir -p /opt/node_exporter && \
    cd /opt/node_exporter && \
    wget https://github.com/prometheus/node_exporter/releases/download/v1.8.1/node_exporter-1.8.1.linux-amd64.tar.gz && \
    tar --strip-components=1 -xzf node_exporter-1.8.1.linux-amd64.tar.gz && \
    chown -R node_exporter:node_exporter /opt/node_exporter && \
    rm -f node_exporter-1.8.1.linux-amd64.tar.gz

WORKDIR /opt/node_exporter
USER node_exporter
EXPOSE 9100
CMD ["./node_exporter"]

