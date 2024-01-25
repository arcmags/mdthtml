---
title: mdthtml
author: Chris Magyar
description: Commonmark-plus flavored markdown to html parser.
css: css/main.css
---

Markdown parser with extras built in. This project is a bunch of additions to
[markdown-it-py](https://github.com/executablebooks/markdown-it-py). It's kind
of hacky right now because that's the way I generally do things.

# Installation

This is beta-alpha right now so it ain't on pip yet!

Clone the repo and use make to build and install into a venv:

    $ make venv

Or install into a pipx managed venv:

    $ make pipx

# Usage

## Python API Usage

``` python
from mdthtml import MarkdownHTML

text = ("""---
title: Test Document
author: mags
---

# Heading

Some code:

    sudo mount /dev/sda2 /mnt/nas
""")

mdhtml = MarkdownHTML()
mdhtml.parse(text)
print(mdhtml.html)
```

## Command Line Usage

Accepts stdin and/or a list of files. Outputs to stdout or a single file.

    mdthtml [OPTION...] [FILE...]

### Options

    -c, --css <PATH>
        Add link to css stylesheet. PATH does not necessarily need to exist.

    -R, --relative

        Calculate css path relative to first FILE.

    -f, --template-file <FILE>
        Template file.

    -o, --output <FILE>
        Output to file.

    -O, --auto
        Automatically name output file based on last file supplied.

    -t, --title <TITLE>
        Title to include in head, overrides any metadata in document.

    -B, --body-only
        Output html body content only. ('{content}' as template string)

    -M, --meta-only
        Output html meta content only. ('{metatdata}' as template string)

    -J, --json
        Output json.

    -T, --tree
        Output token tree.

    -Y, --yes
        Overwrite output file.

    -h
        Print short help.

    -H, --help
        Print help.

# Features

Commonmark standard (gfm tables) as parsed by *markdown-it-py* plus some hacky
additions:

- add id tags to every heading element
- parse front-matter for metadata (without *front_matter* plugin)
- customized code blocks (make PS1 prompt its own span for styling)

## Features Roadmap

- table of contents (customized names, not just a copy of heading content)
- reference links/variables in bottom-matter substituted in
- syntax highlighting
- images, galleries
- maybe build plugins rather than hacking straight on the source as much
