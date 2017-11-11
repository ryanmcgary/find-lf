# sudo docker build -t finddocker .
# sudo docker run -it -p 18003:8003 -p 11883:1883 -v /path/to/host/data/folder:/data finddocker bash
FROM ubuntu:16.04

# Get basics
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y git wget curl vim

# Add Python stuff

# Install Go
RUN wget https://storage.googleapis.com/golang/go1.9.2.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.9.2.linux-amd64.tar.gz
RUN rm go1.9*
ENV PATH="/usr/local/go/bin:${PATH}"
RUN mkdir /usr/local/work
ENV GOPATH /usr/local/work

# Install FIND
RUN go get github.com/ryanmcgary/find-lf/server
WORKDIR "/usr/local/work/src/github.com/ryanmcgary/find-lf/server"
# RUN rm supervisord.conf
RUN go build -v
RUN mkdir /root/find-lf

# Setup supervisor
RUN apt-get update
RUN apt-get install -y supervisor

# Add supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add Tini
ENV TINI_VERSION v0.13.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Startup
CMD ["/usr/bin/supervisord"]
