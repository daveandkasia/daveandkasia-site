from pelican import signals
from smugpy import SmugMug
import percache
import logging
from sets import Set
from collections import OrderedDict
import os.path, re

SMUGMUG_API_KEY = 'ChOHIeuSvpYEMeU5gtLb0ISPxszAQ0oS'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Persist SmugMug responses to disk between calls (via shelve module)
# TODO: Invalidate stale cache based on mtime
cache = None	

class SmugMugCache(SmugMug):
	"""Caching wrapper for SmugMug API

	Disk cache (percache) avoids API calls during subsequent builds, results cached in 
	memory during run and written to disk when object deleted or on cache.sync()/close()
	"""
	def __init__(self, *args, **kwargs):
		if not 'api_version' in kwargs.keys():
			kwargs['api_version'] = '1.3.0'
		if not 'app_name' in kwargs.keys():
			kwargs['app_name'] = 'pelican-smugpy'

		super(SmugMugCache, self).__init__(*args, **kwargs)

	def __getattr__(self, *args, **kwargs):
		parent = super(SmugMugCache, self).__getattr__(*args, **kwargs)

		@cache
		def cacheable_result(*args, **kwargs):
			logging.debug('Cache miss, calling SmugMug API')
			return parent(*args, **kwargs)

		return cacheable_result

# SmugMug API accessed via this object, frequent and redundant calls are OK due to caching
smugmug = None

# Prioritized dictionary keys match named properties of SmugMug Album objects,
# values contain callable objects that accept to args: target and candidate match values.
# Callable objects should return True if candidate "matches" target and False otherwise.
album_match = OrderedDict([
	('id',
		lambda target, candidate: False),
	('Key',
		lambda target, candidate: target == candidate),
	('URL',
		lambda target, candidate: target in candidate),
	('Title',
		lambda target, candidate: target.strip().lower() == candidate.strip().lower()),
	('NiceName',
		lambda target, candidate: target == candidate),
	('Description',
		lambda target, candidate: False),
])

# Map of SmugMug Image attributes to returned properties of template gallery object
image_attribute_map = {
	'gallery': {
		'thumb': 'ThumbURL',
		'image': 'X2LargeURL',
	}
}

def get_album(username, album):
	# Request user's albums from API
	logging.debug('Requesting albums for user %s' % username)
	albums = smugmug.albums_get(NickName=username, Heavy=True)
	logging.debug('Received %d albums for user %s' % (len(albums['Albums']), username,))
	
	# Reference to specified album, will be updated with reference to API Album object
	# that most closely matches criteria specific in album argument0
	target = None

	# Find album based on album criteria dictionary
	for album_candidate in albums['Albums']:
		for (key, match) in album_match.iteritems():
			if match(album, album_candidate[key]):
				target = album_candidate
				break
		else:
			# Called when album_candidate does not match criteria
			continue
		# Called when album_candidate matches criteria and break called from inner loop
		break
	else:
		# Called when no album_candidate matches criteria
		raise ValueError('Cannot locate album: %s' % repr(album))

	return target

def get_album_with_images(username, album):
	target = get_album(username, album)

	# Request image list for target album from API
	logging.debug('Requesting images for album {URL}'.format(**target))
	images = smugmug.images_get(AlbumID=target['id'], AlbumKey=target['Key'], Heavy=True)
	logging.debug('Received metadata for {ImageCount} images in album {URL}'.format(**images['Album']))

	target['Images'] = images['Album']['Images']
	
	return target

def get_images(username, album, attribute_map=None):
	target = get_album_with_images(username, album)
	images = []

	if attribute_map:
		for image in target['Images']:
			# META: This could be a dictionary comprehension
			images.append({})

			for dst, src in image_attribute_map[attribute_map].iteritems():
				images[-1][dst] = image[src]
	else:
		images = target['Images']
	
	return images

def get_username(settings, item):
	username = None

	if 'smugmug-user' in item.keys():
		# Defined in item metadata
		username = item.get('smugmug-user')
	elif re.match(r'^http://([\w]+)\.smugmug.com/.*', item.get('smugmug')):
		# Implicitly defined in specified URL
		username = _.group(1)
	elif 'SMUGMUG_DEFAULT_USER' in settings.keys():
		# Defined in configuration
		logging.debug('Using default user for %s' % item.get('smugmug'))
		username = settings.get('SMUGMUG_DEFAULT_USER')
	else:
		raise Exception('Cannot determine user for %s' % meta.get('smugmug'))
	
	return username

def add_smugmug_item(generator, item_collection, metadata=None):
	has_smugmug_metadata = lambda item: 'smugmug' in item.metadata.keys()
	print "called item!"
	for item in filter(has_smugmug_metadata, item_collection):
		username = get_username(generator.settings, item.metadata)
		item.metadata['album'] = get_album_with_images(username, item.metadata.get('smugmug'))
		print "hi there!"
		#item.album = album['Title']
		#item.images = get_images(username, album['Key'])

def add_smugmug_album(generator, metadata):
	import copy
	if 'smugmug' in metadata.keys():
		username = get_username(generator.settings, metadata)
		metadata['album'] = get_album_with_images(username, metadata.get('smugmug'))

def persist_api_cache(pelican):
	if cache:
		logging.debug('Closing SmugMug API cache')
		cache.close()

def init_api(pelican):
	global cache, smugmug
	logging.debug('Initializing SmugMug API')
	settings = pelican.settings
	settings.setdefault('SMUGMUG_CACHE', 
						os.path.join(settings['CACHE_PATH'], 'smugmug'))
	cache = percache.Cache(settings['SMUGMUG_CACHE'])

	smugmug = SmugMugCache(api_key=settings['SMUGMUG_API_KEY'])

def register():
	signals.initialized.connect(init_api)
	signals.article_generator_context.connect(add_smugmug_album)
	signals.page_generator_context.connect(add_smugmug_album)
	signals.finalized.connect(persist_api_cache)

if __name__ == '__main__':
	import sys, string

	cache = percache.Cache('cache')
	smugmug = SmugMugCache(api_key=SMUGMUG_API_KEY)

	username = sys.argv[1]
	album_title = string.join(sys.argv[2:])

	# Print list of albums for user
	albums = smugmug.albums_get(NickName=username, Heavy=True)
	for album in albums["Albums"]:
		print("%s, %s" % (album["id"], album["URL"]))

	# Return image metadata for specified album
	if len(album_title):
		for image in get_images(username, album_title, 'gallery'):
			print image

	cache.close()
	sys.exit(0)
