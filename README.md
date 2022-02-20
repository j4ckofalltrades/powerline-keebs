# powerline-keebs

[![PyPI](https://img.shields.io/pypi/v/powerline-keebs)](https://pypi.org/project/powerline-keebs/)

A custom [Powerline](https://github.com/powerline/powerline) segment for displaying currently connected keyboards.

Keyboard detection and parsing based off of [pykeeb](https://github.com/j4ckofalltrades/pykeeb).

![](https://res.cloudinary.com/j4ckofalltrades/image/upload/v1645293862/foss/powerline_keebs_hwsshp.png)

## Installation

### Using pip

`$ pip install powerline-keebs`

### Local development

`$ pip install --editable .`

Installing the package in editable mode saves you from having to "re-install" to see the latest changes.

## Configuration

### Colorscheme

Add the following config items to your Powerline colorscheme config file (usually located at `~/.config/powerline/colorschemes/`),
see [Powerline Colorschemes](https://powerline.readthedocs.io/en/master/configuration/reference.html#colorschemes) for more info.

```json
{
  "keebs":           { "fg": "solarized:base3", "bg": "solarized:base01", "attrs": ["bold"] },
  "keebs:divider":   { "fg": "gray4",           "bg": "solarized:base02", "attrs": [] }
}
```

### Segment

Add the following config item to your Powerline segments config file,
see [Powerline Segment reference](https://powerline.readthedocs.io/en/master/configuration/segments.html#segment-reference) for more info.

Note: Dongles (or wireless receivers) are included by default -- to exclude them add the "args" config from the example below.

```json
{
  "function": "powerline_keebs.keebs",
  "priority": 30,
  "args": {
    "no_dongles": true
  }
}
```

- If adding the segment to the shell, edit `~/.config/powerline/themes/shell/default.json`.
- If adding the segment to the tmux status line, edit `~/.config/powerline/themes/tmux/default.json`.

### Toggle visibility

Toggle entire segment or specific section's visibility with the following environment variables:

- `POWERLINE_KEEBS_SHOW`

```shell
# toggle segment visibility
$ POWERLINE_KEEBS_SHOW=0 powerline-daemon --replace # hide powerline-keebs segment
$ POWERLINE_KEEBS_SHOW=1 powerline-daemon --replace # show powerline-keebs segment (default)
```

Alternatively you can add the following function to your shell for easier toggling:

```shell
toggle_powerline_keebs() {
  case "$1" in
      # toggle segment visibility
      if [[ "${POWERLINE_KEEBS_SHOW:-1}" -eq 1 ]]; then
        export POWERLINE_KEEBS_SHOW=0
      else
        export POWERLINE_KEEBS_SHOW=1
      fi
    ;;
  esac
}
```
