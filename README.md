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
usage: main.py [-h] --stream STREAM --base-path BASEPATH [--directory-format DIRECTORYFORMAT] [--file-format FILENAMEFORMAT] [--interval INTERVAL]

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

```

## Roadmap

## Contribution

## License

## Credit


