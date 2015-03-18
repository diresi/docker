FROM ehazlett/logstash

EXPOSE 5000
ENTRYPOINT ["/opt/logstash/bin/logstash", "-f", "/etc/logstash.conf.sample"]
ADD logstash.conf.sample /etc/logstash.conf.sample
