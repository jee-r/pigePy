FROM python:3.11-alpine

LABEL name="pigepy" \
      maintainer="Jee jee@jeer.fr" \
      description="PigePY is an archiving audio stream python script " \
      url="https://github.com/jee-r/pigepy" \
      org.label-schema.vcs-url="https://github.com/jee-r/pigepy" \
      org.opencontainers.image.source="https://github.com/jee-r/pigepy"
      
COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY entrypoint.sh .

WORKDIR /app

STOPSIGNAL SIGQUIT
ENTRYPOINT ["/entrypoint.sh"]