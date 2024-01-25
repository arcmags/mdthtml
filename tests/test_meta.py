from mdthtml import MarkdownHTML

def test_title():
    mdhtml = MarkdownHTML()
    mdhtml.parse('text')
    assert 'title' not in mdhtml.meta, 'title in mdhtml.meta'

def test_title_args():
    mdhtml = MarkdownHTML()
    mdhtml.parse('---\ntitle: XXXX\n---', title='YYYY')
    assert mdhtml.meta['title'] == 'YYYY', 'title not parsed from function args'

def test_title_front_matter():
    mdhtml = MarkdownHTML()
    mdhtml.parse('---\ntitle: XXXX\n---')
    assert mdhtml.meta['title'] == 'XXXX', 'title not parsed from front matter'

def test_css():
    mdhtml = MarkdownHTML()
    mdhtml.parse('text')
    assert 'css' not in mdhtml.meta, 'css in mdhtml.meta'

def test_css_args():
    mdhtml = MarkdownHTML()
    mdhtml.parse('---\ncss: XXXX\n---', css_path='XXXX')
    assert mdhtml.meta['css'] == 'XXXX', 'css not parsed from function args'

def test_css_front_matter():
    mdhtml = MarkdownHTML()
    mdhtml.parse('---\ncss: XXXX\n---')
    assert mdhtml.meta['css'] == 'XXXX', 'css not parsed from front matter'

def test_author_front_matter():
    target = '<meta name="author" content="XXXX">'
    mdhtml = MarkdownHTML()
    mdhtml.parse('---\nauthor: XXXX\n---')
    assert mdhtml.parts['metadata'] == target, 'author not parsed from front matter'
