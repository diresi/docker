FROM larrycai/gerrit

USER root
ADD ./gerrit.config ${GERRIT_HOME}/gerrit/etc/gerrit.config
ADD ./start.sh ${GERRIT_HOME}/start.sh
RUN chown -R ${GERRIT_USER}:${GERRIT_USER} $GERRIT_HOME

USER ${GERRIT_USER}
EXPOSE 8080 29418
VOLUME ${GERRIT_HOME}
CMD ["/home/gerrit2/start.sh"]
