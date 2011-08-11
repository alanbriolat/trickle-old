import re

import web

# Available template functions
template_functions = dict()

def register(f):
    """Register a function as a template function, keeping its name."""
    template_functions[f.__name__] = f
    return f

def natural_sort(xs):
    """Natural sort of a list

    Sort a list in a case-insensitive way, ordering numbers correctly.  Taken
    from http://stackoverflow.com/questions/4836710#4836734 .
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(xs, key=alphanum_key)

@register
def iterdirs(filetree):
    """Iterate over only the directories of *filetree* in "natural" order."""
    keys = natural_sort(k for k, v in filetree.iteritems() if v['type'] == 'dir')
    return ((k, filetree[k]) for k in keys)

@register
def iterfiles(filetree):
    """Iterate over only the files of *filetree* in "natural" order."""
    keys = natural_sort(k for k, v in filetree.iteritems() if v['type'] != 'dir')
    return ((k, filetree[k]) for k in keys)

@register
def si_size(b):
    """Convert a byte count to a nicely readable SI unit."""
    UNITS = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    index = 0
    while b >= 1024 and index < len(UNITS) - 1:
        b /= 1024.0
        index += 1
    return "%.1f %s" % (b, UNITS[index])

@register
def icon(i, alt=None):
    """Output a named icon image, with alt text defaulting to the icon name."""
    alt = alt or i
    return '<img class="icon" src="/static/icons/%s.png" alt="%s"/>' % (i, alt)

@register
def icon_css(i):
    """Generate CSS style information for an icon as a background image."""
    return 'background-image: url(/static/icons/%s.png);' % (i,)

# Create a template renderer with these template functions available
render = web.template.render('templates/', base='layout', globals=template_functions)
