#!/usr/bin/env python


import os,sys, time, commands
import requests
import urllib
import json
import urllib2
import oauth2
import xml.etree.ElementTree as ET
import io

class Yelp(object):
    """Represents a yelp server connection"""
    def __init__(self,url,path):
        """Stores information about the server   
        url : the URL of the highrise server
        private_token: the user private token
        email: the user email/login
        password: the user password (associated with email)
        """   
        self._url = '%s/%s' % (url,path)
	self._host = 'api.yelp.com'
	self._path = '/v2/search'
	self._consumer_key= 'D332LLsTfuEj1i5ldjdx4A'
	self._consumer_secret= 'T1nwv87blFaGfHA2JBnEQx9j0pU'
	self._token = 'FQAXrhUX8CCgyrkb5AW-RpbDxxTSnx43'
	self._token_secret= 'YSnPVKpO4le8FdqjfG7HEzdv7v8'

       
    def search(self,term, location, offset_limit=20):
	url = 'http://{0}{1}?'.format(self._host, urllib.quote(self._path.encode('utf8')))
   	url_params = {
        	'term': term.replace(' ', '+'),
	        'location': location.replace(' ', '+'),
		'limit' : 20,
		'offset': offset_limit
	}

	consumer = oauth2.Consumer(self._consumer_key,self._consumer_secret)
    	oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    	oauth_request.update(
           {
            	'oauth_nonce': oauth2.generate_nonce(),
            	'oauth_timestamp': oauth2.generate_timestamp(),
            	'oauth_token': self._token,
            	'oauth_consumer_key': self._consumer_key
           }
    	)
    	token = oauth2.Token(self._token, self._token_secret)
    	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    	signed_url = oauth_request.to_url()
    
    	print u'Querying {0} ...'.format(url)

    	conn = urllib2.urlopen(signed_url, None)
    	try:
        	response = json.loads(conn.read())
    	finally:
        	conn.close()

    	return response


    def createList(self,output,filename="result"):
	try:
		for each in output['businesses']:
			print each['name']
			print "\n"
			fileObj = io.open("%s%s" %(filename,each['rating']), 'a', encoding='utf8')
			fileObj.write("%s |  %s    %s" % (each['name'], " ".join(each['location']['display_address']), each['display_phone']))
			fileObj.write(u'\n')
			fileObj.close()
	except:
		pass
	


if __name__=='__main__':
    
    yelpObject = Yelp('http://api.yelp.com', '/v2/search/')
    term = sys.argv[1]
    location = sys.argv[2]

    for i in range(20,2000,20):
	    result =  yelpObject.search(term,location,offset_limit=i) 
	    yelpObject.createList(result)
