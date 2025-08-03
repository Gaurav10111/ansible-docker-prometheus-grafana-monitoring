FROM rockylinux:8

RUN dnf install -y wget tar && \
    useradd -m grafana && \
    mkdir -p /opt/grafana && \
    cd /opt/grafana && \
    wget https://dl.grafana.com/oss/release/grafana-11.1.0.linux-amd64.tar.gz && \
    tar --strip-components=1 -xzf grafana-11.1.0.linux-amd64.tar.gz && \
    chown -R grafana:grafana /opt/grafana && \
    rm -f grafana-11.1.0.linux-amd64.tar.gz

WORKDIR /opt/grafana
USER grafana
EXPOSE 3000
CMD ["./bin/grafana-server", "--homepath", "/opt/grafana"]

