# `gitwhodid`

> Who did that? A CLI to reveal Git history by file.

`gitwhodid` helps you find out who contributed to a specific file in your Git repo - how much, how recently, and with what kind of commits.

## Features

- Shows top contributors to a file with percentage breakdown
- Last seen info for each contributor
- Notable commit messages from each contributor
- Friendly, colorful output powered by [`Rich`](https://github.com/Textualize/rich)

## Installation

```bash
pipx install gitwhodid
```

Or clone the repo and run directly:

```bash
git clone https://github.com/stabldev/gitwhodid
cd gitwhodid
uv sync
uv run gitwhodid <file>
```

## Why?

Sometimes you just want to know who touched this file - either out of curiosity, blame, or celebration. `gitwhodid` makes it easy (and a little fun).

## License

[MIT](https://github.com/stabldev/gitwhodid/blob/main/LICENSE) Copyright (c) [stabldev](https://github.com/stabldev)
