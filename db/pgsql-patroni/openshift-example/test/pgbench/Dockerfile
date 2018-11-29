FROM postgres:10

COPY run.sh test.sh /
RUN chmod +x ./run.sh

ENTRYPOINT [ "/run.sh" ]