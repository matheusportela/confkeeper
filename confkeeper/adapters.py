import os


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

class VimAdapter(ProgramAdapter):
    def name(self):
        return 'vim'

    def paths(self):
        return [
            '~/.vimrc',
        ]
