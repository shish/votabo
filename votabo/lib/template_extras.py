import re
from webhelpers.html import literal

_bbp_clink = re.compile(">>(\d+)((#c?\d+)?)")  # >>[digit], >>[digit]c[digit]
_bbp_quote = re.compile("^>>([^\d].+)")        # >>[non-digit][anything]
_bbp_wiki1 = re.compile("\[\[([^\]\|]+)\]\]")
_bbp_wiki2 = re.compile("\[\[([^\|]+)\|([^\]]+)\]\]")
_bbp_site = re.compile("site://([a-zA-Z0-9/]+)")

def _bbcode_extra(bbcode):
    """
    Pure text-manipulation BBCode extras:

    >>> _bbcode_extra(">>123")
    '<a class="shm-clink" data-clink-sel="" href="site://post/123">&gt;&gt;123</a>'
    >>> _bbcode_extra(">>123#c456")
    '<a class="shm-clink" data-clink-sel="#c456" href="site://post/123#c456">&gt;&gt;123#c456</a>'

    >>> _bbcode_extra(">>bob says hi")
    '<blockquote>bob says hi</blockquote>'
    >>> _bbcode_extra("rar >>bob says hi")
    'rar >>bob says hi'

    >>> _bbcode_extra("[[cake]]")
    '<a href="site://wiki/cake">cake</a>'
    >>> _bbcode_extra("[[cake|The Cake]]")
    '<a href="site://wiki/cake">The Cake</a>'
    """
    bbcode = _bbp_clink.sub('<a class="shm-clink" data-clink-sel="\\2" href="site://post/\\1\\2">&gt;&gt;\\1\\2</a>', bbcode)
    bbcode = _bbp_quote.sub('<blockquote>\\1</blockquote>', bbcode)
    bbcode = _bbp_wiki1.sub('<a href="site://wiki/\\1">\\1</a>', bbcode)
    bbcode = _bbp_wiki2.sub('<a href="site://wiki/\\1">\\2</a>', bbcode)
    bbcode = bbcode.replace("[ul]", "").replace("[/ul]", "")
    bbcode = bbcode.replace("[ol]", "").replace("[/ol]", "")
    return bbcode

def bbcode_extra(request, bbcode):
    """
    >>> import mock
    >>> r = mock.Mock(u

    """
    bbcode = _bbcode_extra(bbcode)
    bbcode = _bbp_site.sub(request.route_path("home") + "\\1", bbcode)
    return literal(bbcode)
