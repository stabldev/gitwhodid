# gitwhodid

> Who did that? A CLI to reveal Git history by file.

![demo](assets/demo.png)

## Overview

`gitwhodid` helps you find out who contributed to a specific file in your Git repo - how much, how recently, and with what kind of commits. (it's a fun weekend project)

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

### Git Integration (Optional)

Add this alias to your Git config to run `gitwhodid` as a Git subcommand:

```bash
git config --global alias.whodid '!gitwhodid'
# now you can use it like
git whodid <file>
```

## License

[MIT](https://github.com/stabldev/gitwhodid/blob/main/LICENSE) Copyright (c) [stabldev](https://github.com/stabldev)
