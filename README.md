# confkeeper
Easily export and import configuration files

## Requirements
- Python 3
- `pip`

## Install

```bash
$ git clone https://github.com/matheusportela/confkeeper.git
$ cd confkeeper
$ pip install .
```

## Usage

```bash
$ confkeeper -h
```

**Exporting configuration files:**
```bash
$ confkeeper export > configs.json
$ confkeeper export -o configs.json
$ confkeeper export -f pickle -o configs.pickle
```

**Import configuration files:**
```bash
$ cat configs.json | confkeeper import
$ confkeeper import -i configs.json
$ confkeeper import -f pickle -i configs.pickle
```
