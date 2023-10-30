# pigePy

pigePy is a python script whose purpose is to record one audio stream per segment.

I wrote this script voluntarily for [Radio Quetsch](https://radio-quetsch.eu).

## Requirements

- [python3](https://www.python.org/)
- [APScheduler](https://apscheduler.readthedocs.io/en/stable/)

## Install

First you need clone the project 

```
git clone https://github.com/jee-r/pigePy.git
```

### VirtualEnv (recommended)

```
cd pigePy
python3 -m virtualenv -p python3 ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Docker

`docker-compose`

```yaml
version: '3'
services:
  pige:
    image: pigepy:latest
    container_name: pigepy
    build:
      context: .
    environment:
      - TZ=Europe/Paris
    volumes: 
      - storagebox_pige:/data
      - /etc/localtime:/etc/localtime:ro
    command: >
      --stream https://my_radio.eu/stream.mp3
      --base-path /data/
      --interval "{'minutes': 1}"
      --file-format "%Y-%m-%d_%Hh-%Mm-%Ss" 
      --directory-format "%Y-%m"
      --align-minute
      --no-subdir
      --timezone Europe/Paris
      --chunk-size 512
      --log-level info
      --healthcheck-url https://healthcheck.io/ping/example_token
      --heathcheck-interval "{'minutes': 10}"

volumes:
  storagebox_pige:
    driver: rclone
    driver_opts:
      remote: 'storagebox_pige:'
      allow_other: 'true'
      vfs_cache_mode: full
      poll_interval: 0
```

For more details about Rclone Docker Volume Plugin see [rclone official doc](https://rclone.org/docker/)

## Usage

```
usage: pigepy [-h] --stream STREAM --base-path BASEPATH [--directory-format DIRECTORYFORMAT]
              [--file-format FILENAMEFORMAT] [--no-subdir] [--prune] [--prune-retention PRUNERETENTION]
              [--prune-interval PRUNEINTERVAL] [--interval INTERVAL] [--align-hour] [--align-minute]
              [--directory-delta DIRECTORYDELTA] [--timezone SCHEDULERTIMEZONE] [--chunk-size CHUNKSIZE]
              [--healthcheck-url HEALTHCHECKURL] [--heathcheck-interval HEALTHCHECKINTERVAL] [--log-level LOGLEVEL]

PigePy is a script for recording audio stream

options:
  -h, --help            show this help message and exit
  --stream STREAM, -s STREAM
                        specify a stream url
  --base-path BASEPATH, -b BASEPATH
                        Base destination directory absolute path.
  --directory-format DIRECTORYFORMAT, -df DIRECTORYFORMAT
                        sub directories structure in strftime format (default: "%Y/%m/%d")
  --file-format FILENAMEFORMAT, -ff FILENAMEFORMAT
                        filename format can contain strftime format (default: "%Hh-%Mm-%Ss")
  --no-subdir, -ns      Don't Create a subdir based on directory format
  --prune               Remove old files and directories in days (default: False)
  --prune-retention PRUNERETENTION, --retention PRUNERETENTION
                        prune retention (aka how many files keep) in kwargs format (default: {"days": 90})
  --prune-interval PRUNEINTERVAL
                        prune interval in kwargs format {"days": int, "hours": int, "minutes": int} (default:
                        {"days": 1})
  --interval INTERVAL, -i INTERVAL
                        Audio files length kwargs format (default: {"minutes": 60})
  --align-hour          automatcally align next record to hour hh:00:00
  --align-minute        automatcally align next record to hour hh:mm:00
  --directory-delta DIRECTORYDELTA, -dd DIRECTORYDELTA
                        directory creating delta, kwargs format (default: {"days": 1})
  --timezone SCHEDULERTIMEZONE, -tz SCHEDULERTIMEZONE
                        APScheduler timezone (default: utc)
  --chunk-size CHUNKSIZE, -cz CHUNKSIZE
                        How much data in octet will be stored in memory before it's write in the file. Must an
                        integer multiple of 1024 eg 1024*512 = 0.5Mo (default: 1024 = 1Mo)
  --healthcheck-url HEALTHCHECKURL
                        Provide a healthcheck url to enable healthcheck monitoring (see https://healthchecks.io/ for
                        more infos default: False)
  --heathcheck-interval HEALTHCHECKINTERVAL
                        healthcheck interval (aka ping interval) kwargs format (default: {"minutes": 10})
  --log-level LOGLEVEL  Set loggin output level (possible values DEBUG,INFO,WARNING,CRITICAL default: INFO)
```
### Limitations 

- The --directory-format (-df) argument allows you to specify the subdirectory structure using the strftime format. However, it does not support the use of the same format specifier multiple times. For example, if the directory format is set to "%Y/%m/%d", the --file-format (-ff) argument cannotinclude the format specifiers %Y, %m, or %d. **Ensure that the file format does not contain the same format specifiers as the directory format** to avoid conflicts and unintended behavior.

## Roadmap

- [ ] healthcheck for each task
- [x] start next record at precise time eg : if script start at 11h43 then next scheduled record should be started at 12h00 instead at 12h43
- [x] Dockerfile and docker-compose
- [ ] github CI

## License




