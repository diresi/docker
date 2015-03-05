FROM dockerfile/ubuntu

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractve apt-get install -y gearman

EXPOSE 4730
CMD ["gearmand", "--verbose", "DEBUG"]
