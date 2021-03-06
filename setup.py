#!/usr/bin/env python
''' TODO
add a way to update the shell file instead of overwriting it
'''


from argparse import ArgumentParser
from datetime import datetime
import json
import os
import sys


here = os.path.abspath(os.path.dirname(__file__))
ALIAS_PATH = os.path.join(here, 'aliases.json')
EDITOR_CONFIG_PATH = os.path.join(here, 'editorconfig')
VIM_DIR_PATH = os.path.join(here, 'vim')
VIMRC_PATH = os.path.join(VIM_DIR_PATH, 'vimrc')
TMUX_PATH = os.path.join(here, 'tmux.conf')

PS1 = '\\[\033[1;34m\\]\\u\\[\033[1;36m\\]@\\[\033[1;35m\\]\\W\\[\033[1;32m\\] $ \\[\033[0m\\]'
with open(ALIAS_PATH) as f:
    ALIASES = json.load(f)

VUNDLE_REPO = 'https://github.com/VundleVim/Vundle.vim.git'
PYENV_REPO = 'https://github.com/yyuu/pyenv.git'
PYENV_VIRTUALENV_REPO = 'https://github.com/yyuu/pyenv-virtualenv.git'


def configure_shell_file(install_dir, shell_file):
    with open(shell_file, 'a') as f:
        # set vim keybindings
        f.write('\nset -o vi\n')

        # install terminal prompt (PS1)
        f.write('\nPS1="{}"\n'.format(PS1))

        # install aliases
        for alias_type, aliases in ALIASES.items():
            f.write('\n# {} aliases\n'.format(alias_type))
            for alias in aliases:
                f.write('alias {}\n'.format(alias))


def install_vim(install_dir, shell_file):
    vim_dir_target = os.path.join(install_dir, '.vim')
    os.system('ln -s %s %s' % (VIM_DIR_PATH, vim_dir_target))

    vimrc_target = os.path.join(install_dir, '.vimrc')
    os.system('ln -s %s %s' % (VIMRC_PATH, vimrc_target))

    vundle_target = os.path.join(vim_dir_target, 'bundle', 'Vundle.vim')
    if not os.path.exists(vundle_target):
        os.system('git clone %s %s' % (VUNDLE_REPO, vundle_target))


def install_tmux(install_dir, shell_file):
    tmux_target = os.path.join(install_dir, '.tmux.conf')
    os.system('ln -s %s %s' % (TMUX_PATH, tmux_target))


def install_pyenv(install_dir, shell_file):
    pyenv_target = os.path.join(install_dir, '.pyenv')
    os.system('git clone %s %s' % (PYENV_REPO, pyenv_target))

    pyenv_virtualenv_target = os.path.join(pyenv_target, 'plugins', 'pyenv-virtualenv')
    os.system('git clone %s %s' % (PYENV_VIRTUALENV_REPO, pyenv_virtualenv_target))

    with open(shell_file, 'a') as f:
        f.write('\n# pyenv + pyenv-virtualenv\n')
        f.write('export PYENV_ROOT="%s"\n' % pyenv_target)
        f.write('export PATH="$PYENV_ROOT/bin:$PATH"\n')
        f.write('eval "$(pyenv init -)"\n')
        f.write('eval "$(pyenv virtualenv-init -)"\n')


def install(install_dir, shell_file):
    ''' Install .vim/ + .vimrc
    Install editorconfig
    Install .tmux.conf
    Setup pyenv + pyenv-virtualenv
    '''

    if not os.path.isdir(install_dir):
        print('install directory %s does not exist. exiting' % install_dir)
        sys.exit(1)

    install_dir = os.path.realpath(install_dir)
    shell_file = os.path.join(install_dir, shell_file)
    if not os.path.isfile(shell_file):
        with open(shell_file, 'w+') as f:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write('# file generated by denv at %s\n' % now)

    editor_config_target = os.path.join(install_dir, '.editorconfig')
    os.system('ln -s %s %s' % (EDITOR_CONFIG_PATH, editor_config_target))

    configure_shell_file(install_dir, shell_file)
    install_vim(install_dir, shell_file)
    install_tmux(install_dir, shell_file)
    install_pyenv(install_dir, shell_file)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-i', '--install-dir', type=str,
        help='specify the install directory')
    arg_parser.add_argument('-s', '--shell-file', type=str,
        help='specify the shell file')
    args = arg_parser.parse_args()

    install_dir = args.install_dir or os.environ['HOME']
    shell_file = args.shell_file or '.bashrc'
    install(install_dir, shell_file)

