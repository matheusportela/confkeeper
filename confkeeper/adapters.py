import os


adapters = [] # All registered adapters

# Register adapter class (not instance) to "adapters" list
def register_adapter(adapter):
    adapters.append(adapter)


class ProgramAdapter:
    def name(self):
        raise NotImplementedError(f'{self.__class__.__name__} must implement "name"')

    def paths(self):
        raise NotImplementedError(f'{self.__class__.__name__} must implement "paths"')

    def export_files(self):
        result = []

        for path in self.paths():
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


class ZshAdapter(ProgramAdapter):
    def name(self):
        return 'zsh'

    def paths(self):
        return [
            '~/.zshrc',
        ]
register_adapter(ZshAdapter)

class VimAdapter(ProgramAdapter):
    def name(self):
        return 'vim'

    def paths(self):
        return [
            '~/.vimrc',
        ]
register_adapter(VimAdapter)

class SublimeTextAdapter(ProgramAdapter):
    def name(self):
        return 'sublime'

    def paths(self):
        return [
            '~/Library/Application Support/Sublime Text 3/Packages/User/Package Control.sublime-settings',
            '~/Library/Application Support/Sublime Text 3/Packages/User/Preferences.sublime-settings',
        ]
register_adapter(SublimeTextAdapter)
