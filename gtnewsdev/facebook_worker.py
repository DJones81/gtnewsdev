# Facebook Worker

# Facebook worker for shares, likes, comments and clicks 

import requests
import datetime
import json


#cc-nebula.cc.gatech.edu/geonewsapi/articles/?date>=    [datetime.datetime.now()-timedelta(days=7)]


# This function takes in a primary key and a URL from an article, 
# calls facebook's data on that data and then adds all the information
# for that article in the database fields. 
def populateFacebookCounts(pk, url, article):

	# Get Query in correct Format for pulling data

	append = "https://api.facebook.com/method/fql.query?query=select%20total_count,like_count,comment_count,share_count,click_count%20from%20link_stat%20where%20url=%27"
	appendEnd = "%27&format=json"
	query = append + url + appendEnd

	response = requests.get(query).json()[0]

	shareCount = response['share_count']
	likeCount = response['like_count']
	commentCount = response['comment_count']
	clickCount = response['click_count']

	article['facebookcounts'].append({'sharecount': shareCount, 'likecount' : likeCount, 'commentcount' : commentCount, 'clickcount': clickCount})
	article['sharecount'] = shareCount
	# article['likecounts'].append({'likecount': likeCount})
	# article['commentcounts'].append({'commentcount': commentCount})
	# article['clickcounts'].append({'clickcount': clickCount})

def getUrlsAndPk(articles):

	for article in articles:
		populateFacebookCounts(article['pk'], article['url'], article)
		r = requests.put('http://cc-nebula.cc.gatech.edu/geonewsapi/articles/' + str(article['pk'])+'/' , data = json.dumps(article), headers={'content-type':'application/json', 'accept':'application/json'})
		if (r.status_code == 400):
			print("put failed\nr.content\n")


#get back the date 7 days ago in the format specified
date = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

#articles will be an array of article
articles = requests.get('http://cc-nebula.cc.gatech.edu/geonewsapi/articles/?format=json&enddate=' + date).json()

getUrlsAndPk(articles)


# https://api.facebook.com/method/fql.query?query=select%20total_count,like_count,
# comment_count,share_count,click_count%20from%20link_stat%20where%20url=%27
# http://www.nytimes.com/2015/11/06/us/louisiana-police-shooting-marksville.html       -> this is the address appended to the param
# %27&format=json
