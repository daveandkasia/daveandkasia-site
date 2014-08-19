from smugpy import SmugMug
from pelican import signals
import logging, re, copy, os.path, urlparse
from sets import Set

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SMUGMUG_API_KEY = 'ChOHIeuSvpYEMeU5gtLb0ISPxszAQ0oS'

class SmugMugClient():

	def __init__(self, api_key=SMUGMUG_API_KEY):
		self._smugmug = SmugMug(api_version='1.3.0',
								app_name='pelican-smugpy',
								api_key=api_key)
		self.users = Set()
		
		self._albums = {}
		self._albums_users = Set()

		logger.debug('Instantiated %s' % self.__class__)

	@property
	def albums(self):
		if self._albums_users != self.users:

			logging.debug('Cache miss, refreshing albums list')
			
			for user in self.users - self._albums_users:

				logging.debug('Requesting albums for user %s' % user)
				albums = self._smugmug.albums_get(NickName=user, Heavy=True)
				for album in albums['Albums']:
					self._albums[album['URL']] = album

				logging.debug('Added %d albums for user %s' % (len(albums['Albums']), 
															   user,))
			# Update cached users list
			self._albums_users = self.users.copy()

		return self._albums

	def _process_album(self, album_url):
		albums = self.albums
		if album_url in albums.keys():
			album = albums[album_url]
		else:
			raise Exception('Cannot locate album: %s' % album_url)

		logging.debug('Requesting images for album {URL}'.format(**album))
		album = self._smugmug.images_get(AlbumID=album['id'],
		                                  AlbumKey=album['Key'],
		                                  Heavy=True)['Album']
		logging.debug('Retrieved metadata for {ImageCount} images in album {URL}'.format(**album))

		return [{
			'thumb': i['ThumbURL'], 
		    'image': i['X2LargeURL'],
		} for i in album['Images']]


	def add_smugmug_article(self, generator):
		for article in generator.articles:
			if not 'smugmug' in article.metadata.keys():
				continue

			self.users.add(_get_user_for_article(generator, article))

			album = self.albums[article.metadata.get('smugmug')]

			article.album = self.albums[article.metadata.get('smugmug')]['Title']
			article.galleryimages = self._process_album(albumname,user)
		
	def add_smugmug_page(self, generator, user):
		pass


if __name__ == '__main__':
	client = SmugMugClient()
	client.users.add('jdleslie')
	#client.users.add('katarzyna')

	for url, album in client.albums.iteritems():
		print album['id'], url
		client._process_album(url)

def _get_user_for_article(generator, article):
	user = None
	with article.metadata as meta:

		# User specified explicitly in article metadata
		if 'smugmug-user' in meta.keys():
			user = meta.get('smugmug-user')

		# User parsed from album URL
		elif re.match(r'^https?://([\w]+)\.smugmug.com/.*', meta.get('smugmug')):
			user = _.group(1)

		# Configured default used
		elif 'SMUGMUG_DEFAULT_USER' in generator.settings.keys():
			logging.debug('Using default user for %s' % meta.get('smugmug'))
			user = generator.settings.get('SMUGMUG_DEFAULT_USER')

		# Raise error if no user can be determined
		else:
			raise Exception('Cannot determine user for %s' % meta.get('smugmug'))

	return user


def _get_album_url(url):
	file = os.path.basename(url)
	file = re.sub(r'([^?]*)\?.*', r'\1', file)
	file = not '.' in file or ''
	return os.path.join(os.path.dirname(url), file)

#re.sub(r'(.*)/(?:([^.]*)|.*)\??.*', r'\1\2', 'http://example.com/a/b/c/d.htm?aaa')


def register():
    signals.article_generator_finalized.connect(add_smugmug_article)
    signals.page_generator_finalized.connect(add_smugmug_page)

