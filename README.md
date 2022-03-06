# pigePy

[pigePy](https://jeer.fr/projects/pigePy) is a python script whose purpose is to record one audio stream per segment.

I wrote this script voluntarily for [Radio Quetsch](https://radio-quetsch.eu),   

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
TODO

### Kubernetes
TODO

## Usage

```
usage: pigepy [-h] --stream STREAM --base-path BASEPATH [--directory-format DIRECTORYFORMAT] [--file-format FILENAMEFORMAT] [--interval INTERVAL] [--directory-delta DIRECTORYDELTA]
              [--timezone SCHEDULERTIMEZONE] [--chunk-size CHUNKSIZE] [--healthcheck-url HEALTHCHECKURL] [--heathcheck-interval HEALTHCHECKINTERVAL] [--log-level LOGLEVEL]

PigePy is a script for recording audio stream

optional arguments:
  -h, --help            show this help message and exit
  --stream STREAM, -s STREAM
                        specify a stream url
  --base-path BASEPATH, -b BASEPATH
                        Base destination directory absolute path.
  --directory-format DIRECTORYFORMAT, -df DIRECTORYFORMAT
                        sub directories structure in strftime format (default: "%Y/%m/%d")
  --file-format FILENAMEFORMAT, -ff FILENAMEFORMAT
                        filename format can contain strftime format (default: "%Hh-%Mm-%Ss")
  --interval INTERVAL, -i INTERVAL
                        Audio files length kwargs format (default: {"minutes": 60})
  --align-hour          automatcally align next record to hour hh:00:00
  --align-minute        automatcally align next record to hour hh:mm:00

  --directory-delta DIRECTORYDELTA, -dd DIRECTORYDELTA
                        directory creating delta, kwargs format (default: {"days": 1})
  --timezone SCHEDULERTIMEZONE, -tz SCHEDULERTIMEZONE
                        APScheduler timezone (default: utc)
  --chunk-size CHUNKSIZE, -cz CHUNKSIZE
                        How much data in octet will be stored in memory before it's write in the file. Must an integer multiple of 1024 eg 1024*512 = 0.5Mo (default: 1024 = 1Mo)
  --healthcheck-url HEALTHCHECKURL
                        Provide a healthcheck url to enable healthcheck monitoring (see https://healthchecks.io/ for more infos default: False)
  --heathcheck-interval HEALTHCHECKINTERVAL
                        healthcheck interval (aka ping interval) kwargs format (default: {"minutes": 10})
  --log-level LOGLEVEL  Set loggin output level (possible values DEBUG,INFO,WARNING,CRITICAL default: INFO)
```

## Roadmap

- [ ] healthcheck for each task
- [x] start next record at precise time eg : if script start at 11h43 then next scheduled record should be started at 12h00 instead at 12h43
- [ ] Dockerfile and docker-compose
- [ ] github CI

## Contribution

## License

## Credit


