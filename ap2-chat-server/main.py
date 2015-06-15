import webapp2
import json
from google.appengine.api import users
from google.appengine.ext import ndb

class AddMessageStatus:
        def __init__(self, status, message):
                self.status = status
                self.message = message

        def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class messages:
	def __init__(self, channel_id, user_id, text, date_time, latitude, longtitude):
                self.channel_id = channel_id
                self.user_id = user_id
                self.text = text
                self.date_time = date_time
		self.latitude = latitude
		self.longtitude = longtitude
 

class Feeds:
	def __init__(self, messages):
		self.messages = messages

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class AllChannels:
	def __init__(self, channel):
		self.channels = channel

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ChannelJas:
	def __init__(self, iden, name, icon):
		self.id = iden
		self.name = name
		self.icon = icon

class ChannelMemberJas:
	def __init__(self, link):
		self.id = iden
		self.user_id = user_id
		self.channel_id = channel_id

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ServerJas:
        def __init__(self, server):
		self.server = server

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
		
class Channel(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    icon = ndb.StringProperty()
    
class Sender(ndb.Model):
    name = ndb.StringProperty()
    lattitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()

class Message(ndb.Model):
    user_id = ndb.StringProperty()
    channel_id = ndb.StringProperty()
    text = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longtitude = ndb.FloatProperty()
    date_time = ndb.StringProperty()

class ChannelMember(ndb.Model):
    id = ndb.StringProperty()
    channel_id = ndb.StringProperty()
    user_id = ndb.StringProperty()

class Server(ndb.Model):
    id = ndb.StringProperty()
    link = ndb.StringProperty()

class Save_Message(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         try:
             message = Message(id = self.request.get('date'), user_id = self.request.get('user'), channel_id = self.request.get('chan'), text = self.request.get('text'), latitude = float(self.request.get('lat')), longtitude = float(self.request.get('long')),  date_time = self.request.get('date'))
             message.put()
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
         except (RuntimeError, TypeError, NameError, ValueError):
             mesStat = AddMessageStatus (0 , 'missing a tag')
             self.response.out.write(mesStat.to_JSON())
         
         
class Retrieve_Message(webapp2.RequestHandler):
     def get(self):
        key = ndb.Key('Message', self.request.get('chan'))
        message = key.get()
        self.response.headers['Content-Type'] = 'application/json'
	feed1 = messages(message.channel_id, message.user_id, message.text, message.date_time, message.latitude, message.longtitude)
	feeds = Feeds([feed1])
	self.response.out.write(feeds.to_JSON())

class Get_Updates(webapp2.RequestHandler):
     def get(self):

         self.response.headers['Content-Type'] = 'application/json'
         allMessages = []

         query = ndb.gql("""SELECT * FROM ChannelMember WHERE user_id = :name""", name = self.request.get('user'))
         
         for channel in query:
             query2 = ndb.gql("""SELECT * FROM Message WHERE channel_id = :chan""", chan = channel.channel_id)
             for message in query2:
                 feed = messages(message.channel_id, message.user_id, message.text, message.date_time, message.latitude, message.longtitude)
                 allMessages.append(feed)    
         feeds = Feeds(allMessages)
         self.response.out.write(feeds.to_JSON())

class Get_Channels(webapp2.RequestHandler):
     def get(self):
         query = ndb.gql("""SELECT * FROM Channel""")
         self.response.headers['Content-Type'] = 'application/json'
         allChannels = []
         for channel in query:
             feed = ChannelJas(channel.id, channel.name, channel.icon)
             allChannels.append(feed)
         feeds = AllChannels(allChannels)
         self.response.out.write(feeds.to_JSON())
         
         
class Add_Channel(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         try:
             channel = Channel(id = self.request.get('name'), name = self.request.get('name'), icon = self.request.get('icon'))
             channel.put()
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
         except (RuntimeError, TypeError, NameError, ValueError):
             mesStat = AddMessageStatus (0 , 'missing a tag')
             self.response.out.write(mesStat.to_JSON())

class Join_Channel(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         try:
             channel = ChannelMember(id = self.request.get('chan'), user_id = self.request.get('user'), channel_id = self.request.get('chan'))
             channel.put()
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
         except (RuntimeError, TypeError, NameError, ValueError):
             mesStat = AddMessageStatus (0 , 'missing a tag')
             self.response.out.write(mesStat.to_JSON())
        
class Add_Server(webapp2.RequestHandler):
     def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            server = Server(id = self.request.get('name'), link = self.request.get('link'))
            server.put()
            mesStat = AddMessageStatus (1 , 'success')
            self.response.out.write(mesStat.to_JSON())
        except (RuntimeError, TypeError, NameError, ValueError):
            mesStat = AddMessageStatus (0 , 'missing a tag')
            self.response.out.write(mesStat.to_JSON())

class Get_Servers(webapp2.RequestHandler):
     def get(self):
        query = ndb.gql("""SELECT * FROM Server""")
        self.response.headers['Content-Type'] = 'application/json'
        allServers = []
        for current in query:
            feed = current.link
            allServers.append(feed)
        feeds = ServerJas(allServers)
        self.response.out.write(feeds.to_JSON())

class Register(webapp2.RequestHandler):
     def get(self):
        url = self.request.get('link') + "/Add_Server?name=chat_server&link=http://ap2-chat-server.appspot.com"
             
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            self.response.out.write(result.content)        

class login(webapp2.RequestHandler):
     def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        if user:
            greeting = ('%s,%s,%s' % (user.email(),user.user_id(),user.nickname()))
            mesStat = AddMessageStatus (1 , 'success')
            self.response.out.write(mesStat.to_JSON())
        else:
            mesStat = AddMessageStatus (0 , 'not logged in')
            self.response.out.write(mesStat.to_JSON())


app = webapp2.WSGIApplication([('/Save_Message', Save_Message), ('/Add_Channel', Add_Channel), ('/Join_Channel', Join_Channel), ('/Get_Servers', Get_Servers),
 ('/login', login),('/Get_Updates', Get_Updates), ('/Get_Channels', Get_Channels),('/Retrieve_Message', Retrieve_Message), ('/Add_Server', Add_Server)
], debug=True)
