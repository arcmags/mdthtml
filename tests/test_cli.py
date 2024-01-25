import sys
from unittest.mock import patch
from mdthtml import cli

def test_cli_title(capsys):
    args = [
        'prog',
        '-t', '0000',
        '-f', 'tests/files/temp_meta.txt',
        'tests/files/md_meta.md'
    ]
    target = '<title>0000</title>'
    out, err = '', ''
    with patch.object(sys, 'argv', args):
        cli.main()
        out, err = capsys.readouterr()
    assert out.splitlines()[0] == target, 'cli -t <TITLE> not passed'

def test_cli_css(capsys):
    args = [
        'prog',
        '-c', 'DIR/CSS',
        '-f', 'tests/files/temp_meta.txt',
        'tests/files/md_meta.md'
    ]
    target = '<link rel="stylesheet" href="DIR/CSS">'
    out, err = '', ''
    with patch.object(sys, 'argv', args):
        cli.main()
        out, err = capsys.readouterr()
    assert out.splitlines()[-1] == target, 'cli -c <PATH> not passed'

def test_cli_css_relative(capsys):
    args = [
        'prog', '-R',
        '-c', 'DIR/CSS',
        '-f', 'tests/files/temp_meta.txt',
        'tests/files/md_meta.md'
    ]
    target = '<link rel="stylesheet" href="../../DIR/CSS">'
    out, err = '', ''
    with patch.object(sys, 'argv', args):
        cli.main()
        out, err = capsys.readouterr()
    assert out.splitlines()[-1] == target, 'cli -c <PATH> not passed'
