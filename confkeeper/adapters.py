import json
import os


CONFIG = {
    'bash': [
        '~/.bash_profile',
        '~/.bashrc',
        '~/.profile'
    ],
    'zsh': [
        '~/.zshrc',
        '~/.zlogin'
    ],
    'oh my zsh': [
        '~/.oh-my-zsh/custom/aliases.zsh',
        '~/.oh-my-zsh/templates/zshrc.zsh-template'
    ],
    'vim': [
        '~/.vimrc'
    ],
    'git': [
        '~/.gitconfig'
    ],
    'sublime': [
        '~/Library/Application Support/Sublime Text 3/Packages/User/Package Control.sublime-settings',
        '~/Library/Application Support/Sublime Text 3/Packages/User/Preferences.sublime-settings'
    ],
    'vs code': [
        '~/Library/Application Support/Code/User/settings.json',
        '~/Library/Application Support/Code/User/keybindings.json',
        '~/Library/Application Support/Code/User/extensions.json',
        '~/Library/Application Support/Code/User/tasks.json'
    ]
}


class ProgramAdapter:
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths

    def export_files(self):
        result = []

        for path in self.paths:
            content = self.export_file(path)
            if content:
                result.append((path, content))

        return result

    def export_file(self, path):
        try:
            with open(os.path.expanduser(path)) as f:
                content = f.read()
        except FileNotFoundError:
            content = None

        return content

# All registered adapters
adapters = []

# Register adapter class (not instance) to "adapters" list
def register_adapter(adapter):
    adapters.append(adapter)

def build_adapters(config):
    for name, paths in config.items():
        adapter = ProgramAdapter(name, paths)
        register_adapter(adapter)

build_adapters(CONFIG)
