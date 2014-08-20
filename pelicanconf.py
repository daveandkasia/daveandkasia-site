from __future__ import unicode_literals

PLUGINS = ['pelican-smugpy']
SMUGMUG_API_KEY = 'ChOHIeuSvpYEMeU5gtLb0ISPxszAQ0oS'

SITENAME = 'runcible.industries'
SITESUBTITLE = 'Kasia and Dave'

SITEURL = 'http://runcible.industries'
RELATIVE_URLS = True 

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'en_US'
DEFAULT_DATE = 'fs'

# Location for content
PAGE_PATHS = ['content/pages']
ARTICLE_PATHS = ['content/posts']
EXTRA_TEMPLATES_PATHS = ['templates']
DIRECT_TEMPLATES = ['index', 'archives', 'tags', 'categories']

# Specific templates to render without underlying page or post content
#TEMPLATE_PAGES = {'templates/some-categories.html': 'some-categories.html'}

# Static files to copy
EXTRA_PATH_METADATA = {}
STATIC_PATHS = ()

def add_static_path(src_path, dst_path, ext=None):
    import os
    from fnmatch import filter
    from sets import Set
    
    global STATIC_PATHS, EXTRA_PATH_METADATA
    
    # Helper function to update EXTRA_PATH_METADATA
    add_epm = lambda x, y: EXTRA_PATH_METADATA.update({x: {'path': y} })

    # Handle individual files
    if not os.path.isdir(src_path) and ext is None:
        src_path, ext = os.path.split(src_path)

    # Turn single extensions into lists of extensions  
    ext_match = lambda files: files
    if ext:
        ext = isinstance(ext, (list, tuple, Set) ) and ext or (ext,)
        ext_match = lambda files: Set([fn for e in ext for fn in filter(files, e) ])

    # Traverse src_path looking for files that match ext glob(s)
    for root, dirs, files in os.walk(src_path):
        for file in ext_match(files):
            src = os.path.join(root, file)
            dst = os.path.join(dst_path, root[len(src_path)+1:], file)

            STATIC_PATHS += (src,)
            add_epm(src, dst)

add_static_path('extra/robots.txt', 'robots.txt')
add_static_path('extra/CNAME', 'CNAME')
add_static_path('extra/custom.css', 'assets/css/custom.css')
add_static_path('lib/blueimp-gallery', 'assets', 'jquery.blueimp-gallery.min.js')
add_static_path('lib/blueimp-gallery', 'assets', 'blueimp-gallery.min.css')
add_static_path('lib/blueimp-gallery/img', 'assets/img')
add_static_path('lib/bootstrap-gallery', 'assets', 'bootstrap-image-gallery.min.css')
add_static_path('lib/bootstrap-gallery', 'assets', 'bootstrap-image-gallery.min.js')
add_static_path('lib/bootstrap-gallery/img', 'assets/img')

# Theme/UI settings
THEME = 'lib/pelican-bootstrap3'
BOOTSTRAP_THEME = 'flatly'
HIDE_SIDEBAR = False 
BOOTSTRAP_NAVBAR_INVERSE = False
DISPLAY_BREADCRUMBS = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = False
TYPOGRIFY = True

CUSTOM_CSS = 'assets/css/custom.css'
FAVICON = None

MENUITEMS = (
  ('Ride', '/ride/'),
  ('Row', '/row/'),
  ('Relate', '/some-categories.html'),
)
del MENUITEMS

# Blogroll
LINKS =  (
  ('Pelican', 'http://getpelican.com/'),
  ('Python.org', 'http://python.org/'),
  ('Jinja2', 'http://jinja.pocoo.org/'),
  ('You can modify those links in your config file', '#'),
)
del LINKS

# Usage tracking keys
GOOGLE_ANALYTICS = None
GOOGLE_ANALYTICS_UNIVERSAL = 'UA-51964066-5'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'daveandkasia'

DEFAULT_PAGINATION = 20
DEFAULT_ORPHANS = 2
PAGINATION_PATTERNS = (
  (1, '{base_name}/', '{base_name}/index.html'),
  (2, '{base_name}/{number}/', '{base_name}/{number}/index.html'),
)

# RESTish URL setup, relies heavily on index.html handling

CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
ARTICLE_LANG_URL = '{category}/{slug}/{lang}/'
ARTICLE_LANG_SAVE_AS = '{category}/{slug}/{lang}/index.html'

DRAFT_URL = 'draft/' + ARTICLE_URL
DRAFT_SAVE_AS = 'draft/' + ARTICLE_SAVE_AS
DRAFT_LANG_URL = 'draft/' + ARTICLE_LANG_URL
DRAFT_LANG_SAVE_AS = 'draft/' + ARTICLE_LANG_SAVE_AS

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
PAGE_LANG_URL = '{slug}/{lang}/'
PAGE_LANG_SAVE_AS = '{slug}/{lang}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tag/'
TAGS_SAVE_AS = 'tag/index.html'

AUTHOR_URL = 'author/{author}/'
AUTHOR_SAVE_AS = 'author/{author}/index.html'
AUTHORS_URL = 'author/'
AUTHORS_SAVE_AS = 'author/index.html'

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
