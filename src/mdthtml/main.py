import yaml
import json
from importlib import resources
from collections.abc import Sequence
from typing import Any, ClassVar, Protocol

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml, unescapeAll
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from mdit_py_plugins.anchors import anchors_plugin
#from mdit_py_plugins.attrs import attrs_plugin
#from mdit_py_plugins.attrs import attrs_block_plugin
#from mdit_py_plugins.container import container_plugin
from markdown_it.tree import SyntaxTreeNode

from mdthtml import assets
from mdthtml.plugins.links import links_plugin
from markdown_it.rules_core import StateCore

class Edict(dict):
    """Dictionary subclass. returns an empty string in key is missing.
    """
    def __missing__(self, key):
        return ''

class MyRenderer(RendererHTML):
    """Subclass of markdown_it.renderer.RendererHTML.
    """
    def __init__(self, parser: Any = None):
        super().__init__()

    def code_block(self, tokens, idx, options, env,) -> str:
        content = escapeHtml(tokens[idx].content).split('\n')
        c = 0
        while c < len(content):
            if content[c][0:2] in ['# ', '$ ']:
                content[c] = '<span class="prompt">' + content[c][0:2] + '</span>' + content[c][2:]
            elif content[c][0:4] == '----':
                content[c] = '<hr>'
            c += 1
        return '<pre><code>' + '\n'.join(content) + '</pre></code>\n'

class MarkdownHTML:
    """Render HTML from commonmark markdown with various additions.

    Usage example:

        > from mdthtml import MarkdownHTML

        > mdhtml = MarkdownHTML()
        > text = '# heading\n\nsome text'
        > mdhtml.parse(text)
        > print(mdhtml.html)
    """

    def __init__(self, template=None) -> None:

        """Initialize parser, takes an optional template string: a format_map
        string with keywords {head} and {body}.
        """

        # add target="_blank" to external links:
        def render_link_open(self, tokens, idx, options, env):
            if tokens[idx].attrGet('href')[0:6] in ['http:/', 'https:']:
                tokens[idx].attrSet("target", "_blank")
            return self.renderToken(tokens, idx, options, env)

        self.reset()
        self.template = template
        if type(template) != str or template == '':
            with (resources.files(assets) / 'template.txt').open("r") as f:
                self.template = f.read()
        self.mdit = MarkdownIt('commonmark', renderer_cls=MyRenderer)
        self.mdit.enable('table')
        self.mdit.add_render_rule("link_open", render_link_open)
        #self.mdit.use(anchors_plugin)
        #self.mdit.use(links_plugin)
        #self.mdit.use(attrs_plugin)
        #self.mdit.use(attrs_block_plugin)
        #self.mdit.use(container_plugin)

    def reset(self):
        # TODO: combine instance vars into some dicts
        self.html = ''
        self.json = None
        self.meta = {}
        self.parts = Edict({'metadata': '', 'content': ''})
        self.text = ''
        self.tokens = None
        self.tree = None

    def parse(self, text:str, css_path=None, title=None) -> None:
        """Render HTML from text and optional title.
        """
        self.reset()
        self.text = text

        # extract metadata from front matter:
        lines = text.splitlines()
        front_matter = ''
        i = 0
        if lines[i] == '---':
            i += 1
            while lines[i] != '---' and i < len(lines):
                front_matter += f'{lines[i]}\n'
                i += 1
            self.text = '\n'.join(lines[i+1:])
        self.meta = yaml.safe_load(front_matter)
        if self.meta is None:
            self.meta = {}

        # set metadata from arguments:
        if css_path is not None:
            self.meta['css'] = css_path
        if title is not None:
            self.meta['title'] = title

        self.tokens = self.mdit.parse(self.text)

        # add ids to headings:
        headings = []
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].type == "heading_open":
                content = self.tokens[i+1].children[0].content
                self.tokens[i].attrSet('id', content)
                headings += [[self.tokens[i].tag, content]]
                i += 1
            i += 1

        # TODO: parse more data out before passing to renderer:
        self.parts['content'] = self.mdit.renderer.render(self.tokens, self.mdit.options, {})
        # TODO: add metadata to tree and json output somehow?
        self.tree = SyntaxTreeNode(self.tokens).pretty(show_text=True)
        self.json = json.dumps([t.as_dict() for t in self.tokens])

        # parse metadata:
        meta = []
        if 'title' in self.meta:
            meta += [f'<title>{self.meta["title"]}</title>']
        for key in ['author', 'description', 'keywords']:
            if key in self.meta:
                meta += [f'<meta name="{key}" content="{self.meta[key]}">']
        if 'css' in self.meta:
            meta += [f'<link rel="stylesheet" href="{self.meta["css"]}">']
        self.parts['metadata'] = '\n'.join(meta)

        # build html from template and parts:
        self.html = self.template.format_map(self.parts).rstrip()
