from mdthtml import MarkdownHTML

def test_render_paragraph():
    target = '<p>XXXX</p>'
    mdhtml = MarkdownHTML(template='{content}')
    mdhtml.parse('XXXX\n')
    assert mdhtml.html == target, 'paragraph rendering error'

def test_render_link_local():
    target = '<p><a href="YYYY">XXXX</a></p>'
    mdhtml = MarkdownHTML(template='{content}')
    mdhtml.parse('[XXXX](YYYY)\n')
    assert mdhtml.html == target, 'local link rendering error'

def test_render_link_external():
    target = '<p><a href="https://YYYY" target="_blank">XXXX</a></p>'
    mdhtml = MarkdownHTML(template='{content}')
    mdhtml.parse('[XXXX](https://YYYY)\n')
    assert mdhtml.html == target, 'external link rendering error'
