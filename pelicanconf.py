from __future__ import unicode_literals

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
EXTRA_PATH_METADATA = {
  'extra/robots.txt': {'path': 'robots.txt'},
}
STATIC_PATHS = ('extra/robots.txt', )

# Theme/UI settings
THEME = 'pelican-bootstrap3'
BOOTSTRAP_THEME = 'flatly'
HIDE_SIDEBAR = False 
BOOTSTRAP_NAVBAR_INVERSE = False
DISPLAY_BREADCRUMBS = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = False
TYPOGRIFY = True

#CUSTOM_CSS = 'custom.css'
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
