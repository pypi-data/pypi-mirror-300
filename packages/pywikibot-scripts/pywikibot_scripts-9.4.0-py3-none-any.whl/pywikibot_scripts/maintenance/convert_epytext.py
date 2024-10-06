#!/usr/bin/python3
"""Convert epytext docstrings to reST (Sphinx) format."""
import codecs
import glob
import os
import re
import sys

import pywikibot

TOKENS_WITH_PARAM = [
    # sphinx
    'param',
    'parameter',
    'arg',
    'argument',
    'key',
    'keyword',
    'type',
    'raises',
    'raise',
    'except',
    'exception',
    'var',
    'ivar',
    'cvar',
    'vartype',
    'meta',
    # epytext
    'todo',
]

TOKENS = [
    # sphinx
    'return',
    'returns',
    'rtype',
    # epytext
    'attention',
    'author',
    'bug',
    'change',
    'changed',
    'contact',
    'copyright',
    '(c)',
    'deprecated',
    'invariant',
    'license',
    'note',
    'organization',
    'org',
    'permission',
    'postcondition',
    'postcond',
    'precondition',
    'precond',
    'requires',
    'require',
    'requirement',
    'see',
    'seealso',
    'since',
    'status',
    'summary',
    'todo',
    'version',
    'warn',
    'warning',
]


def process_docstring(lines):
    """
    Process the docstring for a given python object.

    Note that the list 'lines' is changed in this function. Sphinx
    uses the altered content of the list.
    """
    result = []
    for line in lines:
        line = re.sub(r'(\A *)@({}) '.format('|'.join(TOKENS_WITH_PARAM)),
                      r'\1:\2 ', line)  # tokens with parameter
        line = re.sub(r'(\A *)@({}):'.format('|'.join(TOKENS)), r'\1:\2:',
                      line)  # short token
        line = re.sub(r'(\A *)@(?:kwarg|kwparam) ', r'\1:keyword ',
                      line)  # keyword
        line = re.sub(r'(\A| )L\{([^}]*)\}', r'\1:py:obj:`\2`', line)  # Link
        line = re.sub(r'(\A| )B\{([^}]*)\}', r'\1**\2**', line)  # Bold
        line = re.sub(r'(\A| )I\{([^}]*)\}', r'\1*\2*', line)  # Italic
        line = re.sub(r'(\A| )C\{([^}]*)\}', r'\1``\2``', line)  # Code
        line = re.sub(r'(\A| )U\{([^}]*)\}', r'\1\2', line)  # Url
        result.append(line)
    return result


MAX_DEPTH_RECUR = 50
""" The maximum depth to reach while recursively exploring sub folders."""


def get_files_from_dir(path, recursive=True, depth=0, file_ext='.py'):
    """Retrieve the list of files from a folder.

    :param path: file or directory where to search files
    :param recursive: if True will search also sub-directories
    :param depth: if explore recursively, the depth of sub directories to
        follow
    :param file_ext: the files extension to get. Default is '.py'
    :returns: the file list retrieved. if the input is a file then a one
        element list.

    """
    file_list = []
    if os.path.isfile(path) or path == '-':
        return [path]
    if path[-1] != os.sep:
        path = path + os.sep
    for f in glob.glob(path + "*"):
        if os.path.isdir(f):
            if depth < MAX_DEPTH_RECUR:  # avoid infinite recursive loop
                file_list.extend(get_files_from_dir(f, recursive, depth + 1))
            else:
                continue
        elif f.endswith(file_ext):
            file_list.append(f)
    return file_list


def run(files=[]):
    """Run conversion for given files."""
    for f in files:
        with codecs.open(f, 'r', 'utf8') as file:
            old_script = file.readlines()
            new_script = process_docstring(old_script)
        if old_script != new_script:
            with codecs.open(f, 'w', 'utf8') as file:
                pywikibot.info(f'Converting {f}')
                file.writelines(new_script)


def main(*args):
    """Process conversion."""
    for arg in pywikibot.handle_args():
        opt, _, value = arg.partition(':')
        if opt == '-path':
            files = get_files_from_dir(value)
            if not files:
                sys.exit(f'No files were found matching {value}')
            run(files)


if __name__ == '__main__':
    main()
