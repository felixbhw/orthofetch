
# Orthofetch

A system fetch tool that displays Orthodox Christian daily readings alongside system information.

## Features
- Displays system information using fastfetch
- Shows daily Orthodox readings and commemorations
- Clean, side-by-side display with ASCII art cross
- Multiple display presets (default, epistle)
- Configurable ASCII art logos

## Installation
```bash
pipx install orthofetch
```

Requires `fastfetch` to be installed for system information.

## Usage
Basic usage:
```bash
orthofetch
```

### Options
- `--verse-only`: Show only Bible verses
- `--saints-only`: Show only saints
- `--no-system`: Skip system information
- `--logo`: Select ASCII art logo (choices: calvary_cross, orthodox_cross, dove)
- `--preset`: Select display preset (choices: default, epistle)

### Presets
- `default`: Shows full system information, readings, and commemorations
- `epistle`: Focused view with system time and full epistle reading

## Version
Current version: 0.2

## Dependencies
- Python 3.8+
- fastfetch
- click
- rich
- requests

## License
MIT
```

References to code blocks:
```
src/orthofetch/main.py
startLine: 48
endLine: 56
```

```
setup.py
startLine: 4
endLine: 5
```

```
src/orthofetch/presets/default.py
startLine: 4
endLine: 13
```

```
src/orthofetch/presets/epistle.py
startLine: 4
endLine: 14
```