FROM fluent/fluentd:latest
USER root
RUN gem install elasticsearch --no-document --version 8.19.0 && \
    gem install fluent-plugin-elasticsearch --no-document --version 5.4.3
USER fluent
