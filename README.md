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

## Output

```
+ user.email = "ada@example.com"
- user.legacy_id = 4471
~ user.plan: "free" -> "pro"
~ items[2].qty: 1 -> 3
```

`+` added, `-` removed, `~` changed. Paths are dotted for objects and
bracketed for array indices, so you can paste one straight into `jq`.

## In CI

`--exit-code` makes the tool exit 1 when anything differs, which is enough to
fail a build on unexpected API or config drift:

```
python jsondiff.py schema.committed.json schema.generated.json --exit-code
```

## Tests

```
pip install pytest
pytest
```
