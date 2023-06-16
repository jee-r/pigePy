#!/bin/sh

# python3 /app/pigepy --help

python3 /app/pigepy --align-minute\
  --stream https://radioquetsch.out.airtime.pro/radioquetsch_a \
  --base-path /data/ \
  --interval "{'minutes': 1}" \
  --timezone Europe/Paris \
  --chunk-size 512 \
  --log-level info \
  --healthcheck-url https://cron.roflcopter.fr/ping/Erl8iLe5lZYoGF-JGYRGeQ/main \
  --heathcheck-interval "{'minutes': 10}" \
