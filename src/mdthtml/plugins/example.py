## example.py ::

# Perhaps every customization I want to make could be done through plugins
# rather than subclassing MarkdownIt. ...so I'm going through all the plugins
# in mdit-py-plugins to better understand how to do this.

# adomn:
# Uses block.ruler.before as well as add_render_rule a couple times.
# Looks like add_render_rule can be pretty generic, adding tags, classes, etc
# automatically

# anchors:
# Builds function to add to core rules via core.ruler.push

# attrs:
# Takes a bool argument (spans) to determine whether to use inline.ruler.after or
# inline.ruler.push

# container:
# Uses block.ruler.before as well as add render_rule a couple times.

from typing import Callable, List, Optional, Set

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

# Main function that's added to MarkdownIt instance via `use(example_plugin)`.
# May take args passed in via `use(example_plugin, opt=arg, ...)`
# Purpose of this function is to add actual rule and rule function(s) to parser.
def example_plugin(md: MarkdownIt) -> None:

    # this adds a core rule to MarkdownIt instance:
    md.core.ruler.push(
        "example_core",
        _example_plugin_core,
    )

# Function that's actually added to parser rules.
def _example_plugin_core(state: StateCore) -> None:
    for idx, token in enumerate(state.tokens):
        #print(f'{token}\n')
        pass
