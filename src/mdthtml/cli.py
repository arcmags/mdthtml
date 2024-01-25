#!/usr/bin/env python3

"""NAME
    md2html - convert markdown to html

USAGE
    md2html [OPTION...] [FILE...]

DESCRIPTION
    Convert commonmark flavored markdown (plus some extras) to html. Outputs
    to stdout, use the `-o` or `-O` options to save to a file.

OPTIONS
    -c, --css <PATH>
        Add link to css stylesheet. PATH does not necessarily need to exist.

    -R, --relative
        Calculate css path relative to first FILE.

    -f, --template-file <FILE>
        Template file.

    -o, --output <FILE>
        Output to file.

    -O, --auto
        Output to last filename given replacing the file extention.

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
"""

# TODO: allow this script to run on it's own, relative imports? add to path?

import argparse
import os
import sys
from importlib import resources
from textwrap import indent

from mdthtml import MarkdownHTML
from mdthtml import __version__
from mdthtml import assets

def print_help():
    print(__doc__)
    print('DEFAULT TEMPLATE')
    try:
        with (resources.files(assets) / 'template.txt').open("r") as f:
            print(indent(f.read(), '    '))
    except:
        msg_warn('file error: template.txt\n')
    print('VERSION')
    print('    ' + __version__)

def str_ask(msg='', prompt='[y/N]') -> str:
    return '\033[1;38;5;12m:: \033[0;38;5;15m' + msg + '? ' + prompt + '\033[0m '

def msg_error(msg='') -> None:
    print('\033[1;38;5;9mE: \033[0;38;5;15m' + msg + '\033[0m', file=sys.stderr)

def msg_warn(msg='') -> None:
    print('\033[1;38;5;11mW: \033[0;38;5;15m' + msg + '\033[0m', file=sys.stderr)

class CustomHelpFormatter(argparse.HelpFormatter):
    """Subclass of argparse.HelpFormatter. Widens command
    column to 32 characters and shortens command documentation:
        '-o ARG, --opt ARG'  ->  '-o, --opt ARG'
    """
    def __init__(self, prog, indent=2, max_help=32, width=None):
        super().__init__(prog, indent, max_help, width)
    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            parts = [str(p) for p in self._metavar_formatter(action, default)(1)]
        else:
            parts = [', '.join(action.option_strings)]
            if action.nargs != 0:
                default = self._get_default_metavar_for_optional(action)
                parts += [self._format_args(action, default)]
        return ' '.join(parts)

def main() -> int:
    files = []
    markdown = ''
    template = ''
    output_ext = 'html'
    parser = argparse.ArgumentParser(add_help=False, formatter_class=CustomHelpFormatter)
    parser.add_argument('-c', '--css', metavar='PATH', help='path to css stylesheet')
    parser.add_argument('-R', '--relative', action='store_true', help='calculate relative css path')
    parser.add_argument('-f', '--template-file', metavar='FILE', help='template file')
    parser.add_argument('-o', '--output', metavar='FILE', help='output file')
    parser.add_argument('-O', '--auto', action='store_true', help='output to auto-named file')
    parser.add_argument('-t', '--title', metavar='TITLE', help='html title')
    parser.add_argument('-B', '--body-only', action='store_true', help='output body content only')
    parser.add_argument('-M', '--meta-only', action='store_true', help='output meta content only')
    parser.add_argument('-J', '--json', action='store_true', help='output json')
    parser.add_argument('-T', '--tree', action='store_true', help='output syntax tree')
    parser.add_argument('-Y', '--yes', action='store_true', help='overwrite output file')
    parser.add_argument('-h', action='help', help='display short help')
    parser.add_argument('-H', '--help', action='store_true', help='display help')
    parser.add_argument("files", metavar='FILES', nargs="*", help="list of files to convert")
    args = parser.parse_args()

    # print help:
    if args.help:
        print_help()
        return 0

    # get markdown from stdin:
    if not sys.stdin.isatty():
        markdown = ''.join(line for line in sys.stdin)
    # get markdown from files:
    else:
        for file in args.files:
            try:
                with open(file) as f:
                    markdown += f.read()
            except:
                msg_warn('file error: ' + file)

    # set plain template:
    if args.body_only:
        template = '{content}'
    if args.meta_only:
        template = '{metadata}'
    # set template from file:
    else:
        if args.template_file is not None:
            try:
                with open(args.template_file) as f:
                    template = f.read()
            except:
                msg_warn('file error: ' + args.template_file)

    # TODO: allow blank markdown?
    # exit if markdown is blank:
    if markdown == '':
        msg_warn('blank/no markdown')
        return 0

    # calculate relative css_path (from first file to css file):
    dir_file = os.getcwd()
    css_path = None
    if args.css is not None:
        css_path = args.css
    if len(args.files) > 0 and args.relative:
        css_path = os.path.relpath(args.css, os.path.dirname(args.files[0]))

    # generate html:
    mdhtml = MarkdownHTML(template=template)
    mdhtml.parse(markdown, css_path=css_path, title=args.title)
    output_text = mdhtml.html

    # TODO: check mdhtml.metadata for output file/additional instructions

    if args.json:
        output_text = mdhtml.json
        output_ext = 'json'
    elif args.tree:
        output_text = mdhtml.tree
        output_ext = 'txt'

    if args.auto:
        if len(args.files) > 0:
            args.output = f'{os.path.splitext(args.files[-1])[0]}.{output_ext}'
        else:
            args.output = f'stdout.{output_ext}'

    # check for existing output file, exit if exists and not overwriting:
    if args.output is not None and os.path.exists(args.output) and not args.yes:
        reply = input(str_ask('overwrite ' + args.output)).strip().lower()
        if reply not in ['y', 'yes']:
            return 0

    # output to stdout:
    if args.output is None:
        print(output_text)

    # write to output file:
    else:
        with open(args.output, 'w') as w:
            w.write(output_text)

    return 0

if __name__ == '__main__':
    sys.exit(main())
