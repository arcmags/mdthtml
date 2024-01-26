## example.py ::

# Basically, it looks like plugins work by adding/modifying parser rules.
# See markdown_it.ruler for methods.

from typing import Callable, List, Optional, Set

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

# Main function that's added to MarkdownIt instance via `use(example_plugin)`.
# May take args passed in via `use(example_plugin, opt=arg, ...)`
def example_plugin(md: MarkdownIt) -> None:

    # this adds a core rule to MarkdownIt instance:
    md.core.ruler.push(
        "example_core",
        _example_plugin_core,
    )

#
def _example_plugin_core(state: StateCore) -> None:
    for idx, token in enumerate(state.tokens):
        #print(f'{token}\n')
        pass
