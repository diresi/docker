FROM dockerfile/ubuntu

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        openjdk-7-jre-headless

RUN wget http://tweedo.com/mirror/apache/kafka/0.8.2.0/kafka_2.10-0.8.2.0.tgz
RUN tar xf kafka*tgz -C /opt/


ENV KAFKA_DIR /opt/kafka_2.10-0.8.2.0
EXPOSE 9092
ADD run.sh /run.sh
CMD ["/run.sh"]
