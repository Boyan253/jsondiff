# jsondiff

> Deep diff two JSON files and print added, removed and changed paths.

## Why

`diff a.json b.json` is useless when the formatting or key order changes.
`jsondiff` compares the parsed documents and tells you which *paths* moved.

## Usage

```
python jsondiff.py before.json after.json
python jsondiff.py before.json after.json --exit-code   # exit 1 if different
```
