FROM ubuntu:24.10


RUN apt-get update && apt-get install -y sysstat procps

COPY start.sh /usr/src/app/start.sh
RUN chmod +x /usr/src/app/start.sh

WORKDIR /usr/src/app

CMD ["sh", "/usr/src/app/start.sh"]