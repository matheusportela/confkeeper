# confkeeper
Easily export and import configuration files

## Install

```bash
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
