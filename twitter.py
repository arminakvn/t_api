import pycurl, urllib, urllib2, json, time
import oauth2 as oauth


# check this out for seting the oath parameters correctly:
# https://github.com/simplegeo/python-oauth2

# check out this one, a readly to use library
# https://github.com/geduldig/TwitterAPI
# example for using the above
# http://nbviewer.ipython.org/github/furukama/Mining-the-Social-Web-2nd-Edition/blob/master/ipynb/Chapter%201%20-%20Mining%20Twitter.ipynb
# and https://github.com/sixohsix/twitter




REQUEST_URI = 'https://api.twitter.com/1.1/statuses/user_timeline.json'


OAUTH_KEYS = {'consumer_key': 'ZvJpzvD5QQnvnxIHwC7iWImIQ',
              'consumer_secret': 'MvlMo4JUIpLaGhxN8OkiUJl6yEdE1ab06McwaZScTba65dg5pY',
              'access_token_key': '399546099-9gp6yS27rihI8nXsJR98fpYu2hZAI1jBbKhhp89a',
              'access_token_secret': 'G396dozy7c6zATPMSCPGNcRqX9yvwSADNF5qfMjC6Q6ez'}


POST_PARAMS = {'screen_name': 'SenShelby'	}

class twitterPy:
	def __init__(self):
		self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
		self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
		self.conn = None
		self.buffer = ''
		self.setup_connection()

	def setup_connection(self):
		print "insid the setup and this is self:", self
		if self.conn:
			self.conn.close()
			self.buffer = ''
		self.conn = pycurl.Curl()
		self.conn.setopt(pycurl.URL, REQUEST_URI)
		# self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
		self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
		self.conn.setopt(pycurl.POST, 1)
		self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
		self.conn.setopt(pycurl.HTTPHEADER, ['Host: api.twitter.com', 'Authorization: %s' % self.get_oauth_header()])
		self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)
	
	def get_oauth_header(self):
		print "here it gets the oauth headers"
		params = {'oauth_version': '1.0', 'oauth_nonce': oauth.generate_nonce(), 'oauth_timestamp': int(time.time())}
		req = oauth.Request(method='GET', parameters=params, url='%s?%s' % (REQUEST_URI, urllib.urlencode(POST_PARAMS)))
		req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
		return req.to_header()['Authorization'].encode('utf-8')



	def start(self):
		self.setup_connection()
		self.conn.perform()
	def handle_tweet(self, data):
		print "data:", data
		self.buffer += data
		if data.endswith('\r\n') and self.buffer.strip():
			message = json.loads(self.buffer)
			self.buffer = ''
			msg = ''
			if message.get('limit'):
				print 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
			elif message.get('disconnect'):
				raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
			elif message.get('warning'):
				print 'Got warning: %s' % message['warning'].get('message')
			else:
				print 'Got tweet with text: %s' % message.get('text')

if __name__ == '__main__':
    ts = twitterPy()
    ts.setup_connection()
    ts.start()

# def getUserData():
# 	c = pycurl.Curl()
# 	c.setopt(pycurl.URL, 'https://api.github.com/users/braitsch')
# 	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
# 	c.setopt(pycurl.VERBOSE, 0)
# 	c.setopt(pycurl.USERPWD, 'username:userpass')
# 	c.perform()


# def githubPost():
# 	postData =  '{"name" : "sample-repo", "description" : "repo-description"}'
# 	c = pycurl.Curl()
# 	c.setopt(pycurl.URL, 'https://api.github.com/user/repos')
# 	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
# 	c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
# 	c.setopt(pycurl.POST, 1)
# 	c.setopt(pycurl.POSTFIELDS, postData)
# 	c.setopt(pycurl.USERPWD, 'username:userpass')
# 	c.perform()


# def getUserData():
# 	# first encode the username & password 
# 	userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
# 	# create a new Urllib2 Request object	
# 	req = urllib2.Request('https://api.github.com/users/braitsch')
# 	# add any additional headers you like 
# 	req.add_header('Accept', 'application/json')
# 	req.add_header("Content-type", "application/x-www-form-urlencoded")
# 	# add the authentication header, required
# 	req.add_header('Authorization', userData)
# 	# make the request and print the results
# 	res = urllib2.urlopen(req)
# 	print res.read()
