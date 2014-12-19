# https://dev.twitter.com/overview/api/tweets
from TwitterAPI import TwitterAPI
from read_csv_to_dict import read_csv, write_csv
from threading import Timer
import time

twitter_account = read_csv('../twitter_account.csv')
CONSUMER_KEY = twitter_account[0]['CONSUMER_KEY']
CONSUMER_SECRET = twitter_account[0]['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = twitter_account[0]['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = twitter_account[0]['ACCESS_TOKEN_SECRET']
api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)
handles = []
results = {}
result_list = []
handles_csv = read_csv('HouseofReps_twitterhandles.csv')
for each in handles_csv:
	if each['HAgComm'] == 'yes':
		handles.append(each)

for each in handles:
	SEARCH_TERM = each['Twitter_Handle']
	NAME = each['Name']
	output = NAME + '.csv'
	max_ids = []
	for i in range(0, 32):
		print "max_ids", max_ids
		if len(max_ids) == 0:
			r = api.request('statuses/user_timeline', {'screen_name': SEARCH_TERM, 'count': 200, 'include_rts': 0, 'exclude_replies': "true"})
			results = {}
			try:
				code = r.status_code
				if code == 429:
					time.sleep(900)
					r = api.request('statuses/user_timeline', {'screen_name': SEARCH_TERM, 'count': 200, 'include_rts': 1, 'exclude_replies': "false"})
					print "id works!", code
				elif code == 88:
					time.sleep(900)
					r = api.request('statuses/user_timeline', {'screen_name': SEARCH_TERM, 'count': 200, 'include_rts': 1, 'exclude_replies': "flase"})
					for item in r:
						max_ids.append(item['id'])
				elif code==404:
					break
				else:	
					print "???"
					print "code:", code
					for item in r:
						max_ids.append(item['id'])
			except:
				print "except one!", r.status_code
				for item in r:	
					max_ids.append(item['id'])
			finally:
				for item in r:
					results = {}
					try:
						results.update({'text': item['text'].encode("utf-8")})
						results.update({'round': i})
						results.update({'id': str(item['id']).encode("utf-8")})
						results.update({'created_at': str(item['created_at']).encode("utf-8")})
						results.update({'favorite_count': str(item['favorite_count']).encode("utf-8")})
						results.update({'retweet_count': str(item['retweet_count']).encode("utf-8")})
						results.update({'in_reply_to_screen_name': str(item['in_reply_to_screen_name']).encode("utf-8")})
						results.update({'retweeted': str(item['retweeted']).encode("utf-8")})
						results.update({'coordinates': str(item['coordinates'])})
						results.update({'user_screen_name': str(item['user']['screen_name']).encode("utf-8")})
						results.update({'user_statuses_count': str(item['user']['statuses_count']).encode("utf-8")})
					except:
						pass
					finally:
						result_list.append(results)
		else:
			max_id = min(max_ids)
			r = api.request('statuses/user_timeline', {'screen_name': SEARCH_TERM, 'count': 200, 'include_rts': 1, 'exclude_replies': "false", 'max_id': max_id})
			results = {}
			try:
				code = r.status_code
				if (code == 88) or (code == 429):
					time.sleep(900)
					r = api.request('statuses/user_timeline', {'screen_name': SEARCH_TERM, 'count': 200, 'include_rts': 0, 'exclude_replies': "false", 'max_id': max_id})
					for item in r:
						max_ids.append(item['id'])
				elif code==404:
					break
				else:
					print "???"
					print "code:", code	
					for item in r:
						max_ids.append(item['id'])
			except:
				for item in r:
					max_ids.append(item['id'])

			finally:
				for item in r:
					results = {}

					try:
						print item
						results.update({'created_at': str(item['created_at']).encode("utf-8")})
						results.update({'text': item['text'].encode("utf-8")})
						results.update({'round': i})
						results.update({'id': str(item['id']).encode("utf-8")})
						results.update({'favorite_count': str(item['favorite_count']).encode("utf-8")})
						results.update({'retweet_count': str(item['retweet_count']).encode("utf-8")})
						results.update({'in_reply_to_screen_name': str(item['in_reply_to_screen_name']).encode("utf-8")})
						results.update({'retweeted': str(item['retweeted']).encode("utf-8")})
						results.update({'coordinates': str(item['coordinates'])})
						results.update({'user_screen_name': str(item['user']['screen_name']).encode("utf-8")})
						results.update({'user_statuses_count': str(item['user']['statuses_count']).encode("utf-8")})
					except:
						pass
					finally:
						result_list.append(results)
			

	try:
		write_csv(result_list, output)
	except Exception, e:
		print "e", e, "Exception", Exception
		pass