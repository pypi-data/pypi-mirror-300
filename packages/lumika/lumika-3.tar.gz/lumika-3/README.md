# Lumika

Lightweight flexible hybrid terminal for actions and uses specific to some programs.

## How it works

- Lumika is not itself a terminal, it runs *in* your terminal.
- Lumika utilizes "modules" to run as a hybrid.
- Use `cm <module>` to travel to a relative module
- or `cm :<module>` to travel to an absolute module.
- Third-party programs can utilize command line arguments to automatically take the user to a specific module.
- e.g. `lumika python.exe/-m/twine`

## Installation

### `pip install lumika`
### `pip install lumika==<version>`

## Patches

### 1
- Initial update
- PyPI release

### 2
- In-line scripts
- Command history
- Autocomplete
- Colouring
- Former `LUMIKA` text in the main prompt now displays the user's Windows username
- Atomic variables (right now only strings)
- Running commands as verbose
- Reboot
- Screen automatically clears after a command (use in-line scripts to bypass this)
- ETO (Enter To Continue)
- Better error handling
**Highlight**: Non-built in commands now run through the system, and no longer require a subprocess. This also means that output is generated sequentially, and not after the command finishes.

### 3
- User's Windows username in main prompt now displays 'logged in as' before it
- More autocomplete terms
- Credits
- GitHub repo (https://github.com/elemenom/lumika)
- Smart keybindings*
- Bug fixes
**Highlight**: Orbitshell-like structure, allows consecutive commands without in-line scripts

*Smart keybindings:
- RETURN (in the main prompt) --------------------------------------------------- submit (if something is inputted)/next line (if empty)
- CTRL+C (in the main prompt) --------------------------------------------------- terminate current chain
- Hold CTRL+C (in the main prompt) ---------------------------------------------- exit lumika completely
- RETURN (after a command) ------------------------------------------------------ submit a consecutive command
- CTRL+C (after a command) ------------------------------------------------------ terminate current chain
- Hold CTRL+C (after a command) ------------------------------------------------- exit lumika completely