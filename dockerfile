FROM ubuntu:24.10


RUN apt-get update && \
    apt-get install -y sysstat procps fuse libfuse2 ssh openssh-server jsvc libxml2-utils wget && \
    wget http://www.opendedup.org/downloads/sdfs_3.10.8_amd64.deb && \
    dpkg -i sdfs_3.10.8_amd64.deb

    

COPY start.sh /usr/src/app/start.sh
RUN chmod +x /usr/src/app/start.sh

WORKDIR /usr/src/app

CMD ["sh", "/usr/src/app/start.sh"]