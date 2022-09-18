# powerline-keebs

[![PyPI](https://img.shields.io/pypi/v/powerline-keebs)](https://pypi.org/project/powerline-keebs/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/powerline-keebs)

A custom [Powerline](https://github.com/powerline/powerline) segment for displaying currently connected keyboards.

Keyboard detection and parsing based off of [kbdetector](https://github.com/j4ckofalltrades/kbdetector).

![](https://res.cloudinary.com/j4ckofalltrades/image/upload/v1645293862/foss/powerline_keebs_hwsshp.png)

## Installation

### Using pip

`$ pip install powerline-keebs`

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

```json
{
  "function": "powerline_keebs.keebs",
  "priority": 30,
  "args": {
    "no_dongles": true,
    "exclude_list": "comma,separated,keyboard,list"
  }
}
```

- If adding the segment to the shell, edit `~/.config/powerline/themes/shell/default.json`.
- If adding the segment to the tmux status line, edit `~/.config/powerline/themes/tmux/default.json`.

#### Configuration items

| config_item  | description                                     | value                                 |
|--------------|-------------------------------------------------|---------------------------------------|
| no_dongles   | exclude keyboard dongles and/or receivers       | `true` or `false` (defaults to false) |
| exclude_list | exclude pre-defined keyboard(s) from the result | comma-separated string                |

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

## Stats

![Alt](https://repobeats.axiom.co/api/embed/49028c098050f2ec944637634225038be092c693.svg "Repobeats analytics image")
