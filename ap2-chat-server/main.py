import webapp2
import json
import datetime
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
 
class messageShort:
	def __init__(self, channel_id,  text, latitude, longtitude):
                self.channel_id = channel_id
                self.text = text
		self.latitude = latitude
		self.longtitude = longtitude

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Feeds:
	def __init__(self, messages):
		self.messages = messages

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ChannelWithMems:
        def __init__(self, id, member):
                self.id = id
		self.member = member

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
class Member:
        def __init__(self, member):
                self.member = member

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

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

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
    mine = ndb.StringProperty()
    
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
    id = ndb.IntegerProperty()
    link = ndb.StringProperty()

class Save_Message(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         try:
             #user = users.get_current_user().user_id()
             dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             message = Message(id = self.request.get('text'), user_id = self.request.get('user'), channel_id = self.request.get('channel_id'), text = self.request.get('text'), latitude = float(self.request.get('latitude')), longtitude = float(self.request.get('longtitude')),  date_time = dateTime)
             message.put()
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
             '''
             memb = messageShort (self.request.get('channel_id'), self.request.get('text') ,self.request.get('latitude'), self.request.get('longtitude'))
             commandType = {'Content-Type': '/update'}
             form_fields = {"user": self.request.get('user'), "action": 3, "data": memb.to_JSON}
             query = ndb.gql("""SELECT * FROM Server""")
             for current in query:
                    url = current.link
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                    if result.status_code == 200:
                            self.response.out.write(result.content)
             '''               
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
         #user = users.get_current_user().user_id()
         user = self.request.get('user')
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE user_id = :name""", name = user)
         
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
     def post(self):
         self.response.headers['Content-Type'] = 'application/json'
         key = ndb.Key('Channel', self.request.get('id'))
         if key is None:
             try:
                 channel = Channel(id = self.request.get('id'), name = self.request.get('name'), icon = self.request.get('icon'), mine = "true")
                 channel.put()
                 mesStat = AddMessageStatus (1 , 'success')
                 self.response.out.write(mesStat.to_JSON())
                 '''
                 chan = ChannelJas (self.request.get('id'), self.request.get('name') ,self.request.get('icon'))
                 commandType = {'Content-Type': '/update'}
                 form_fields = {"user": self.request.get('user'), "action": 4, "data": chan.to_JSON}
                 query = ndb.gql("""SELECT * FROM Server""")
                 for current in query:
                        url = current.link
                        form_data = urllib.urlencode(form_fields)
                        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                        if result.status_code == 200:
                                self.response.out.write(result.content)
                 '''
             except (RuntimeError, TypeError, NameError, ValueError):
                 mesStat = AddMessageStatus (0 , 'missing a tag')
                 self.response.out.write(mesStat.to_JSON())
         else:
             mesStat = AddMessageStatus (0 , 'channel already exists')
             self.response.out.write(mesStat.to_JSON())

class Join_Channel(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         try: 
             #user = users.get_current_user().user_id()
             user = self.request.get('user')
             channel = self.request.get('id')
             channel = ChannelMember(id = user + channel, user_id = user, channel_id = channel)
             channel.put()
             '''
             chanMem = ChannelMemberJas (user + channel, user , channel)
             commandType = {'Content-Type': '/update'}
             form_fields = {"user": self.request.get('user'), "action": 5, "data": chanMem.to_JSON}
             query = ndb.gql("""SELECT * FROM Server""")
             for current in query:
                    url = current.link
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                    if result.status_code == 200:
                            self.response.out.write(result.content)
             '''
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
         except (RuntimeError, TypeError, NameError, ValueError):
             mesStat = AddMessageStatus (0 , 'missing a tag')
             self.response.out.write(mesStat.to_JSON())
        
class register(webapp2.RequestHandler):
     def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            server = Server(id = int(self.request.get('id')), link = self.request.get('link'))
            #self.response.out.write(server.key.id())
            server.put()
            mesStat = AddMessageStatus (1 , 'success')
            self.response.out.write(mesStat.to_JSON())
        except (RuntimeError, TypeError, NameError, ValueError):
            mesStat = AddMessageStatus (0 , 'missing a tag')
            self.response.out.write(mesStat.to_JSON())

class unRegister(webapp2.RequestHandler):
     def get(self):
        id = self.request.get('link')
        ndb.Key(Server, int(id)).delete()
        try:
            '''
            query = ndb.gql("""SELECT * FROM Server""")
            self.response.headers['Content-Type'] = 'application/json'
            allServers = []
            for current in query:
                    if current.link == self.request.get('link'):
                            current.key.delete()
            '''
            #server.key = ndb.Key('Server', self.request.get('link'))
            #server.key.delete()
            #self.response.out.write(type(key.get()))
            #self.response.out.write(key.id())
            #key2 = ndb.Key(Server, self.request.get('link'))
            #self.response.out.write(type(key2.get()))
            #self.response.out.write(key2.id())
            #server = key.get()
            '''
            if key is None:
                    mesStat = AddMessageStatus (0 , 'no existing server')
                    self.response.out.write(mesStat.to_JSON())
            else:
                    #server = key.get()
                    #self.response.out.write(server.link)
                    key2.delete()
                    mesStat = AddMessageStatus (1 , 'success')
                    self.response.out.write(mesStat.to_JSON())
            '''        
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

class add_myself(webapp2.RequestHandler):
     def post(self):
        url = self.request.get('link') + "/register?name=chat_server&link=http://ap2-chat-server.appspot.com"
             
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            self.response.out.write(result.content)        

class update(webapp2.RequestHandler):
     def get(self):
             
        alreadySeen = 1
        user = self.request.get('user')
        action = int(self.request.get('action'))
        j = json.loads(self.request.get('data'))
        #j = json.loads(info)
        
        if action == 3:
                key = ndb.Key('Message', j['text'])
                if key is None:
                        alreadySeen = 0
                        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message = Message(id = j['text'], user_id = self.request.get('user'), channel_id = j['channel'], text = j['text'], latitude = float(j['latitude']), longtitude = float(j['longtitude']), date_time = dateTime)
                        message.put()
        elif action == 4:
                key = ndb.Key('Channel', j['channel_id'])
                if key is None:
                        alreadySeen = 0
                        channel = Channel(id = j['channel_id'], name = j['name'], icon = j['icon'], mine = "false")
                        channel.put()
        elif action == 5:
                key = ndb.Key('Channel', j['channel_id'])
                if key is None:
                        alreadySeen = 1
                else: 
                        user = self.request.get('user')
                        channel = j['channel_id']
                        key2 = ndb.Key('ChannelMember',  user + channel)
                        if key2 is None:
                                alreadySeen = 0
                                channel = ChannelMember(id = user + channel, user_id = user, channel_id = channel)
        elif action == 6:
                key = ndb.Key('Channel', j['channel_id'])
                if key is None:
                        alreadySeen = 1
                else:
                        user = self.request.get('user')
                        channel = j['channel_id']
                        key2 = ndb.Key('ChannelMember',  user + channel)
                        if key2 is None:
                               alreadySeen = 1
                        else:
                                key2.delete()
        elif action == 7:
                key = ndb.Key('Channel', j['channel_id'])
                if key is None:
                        alreadySeen = 1
                else:
                        key.delete()
        '''              
        if !alreadySeen:
                commandType = {'Content-Type': '/update'}
                form_fields = {"user": self.request.get('user'), "action": action, "data": self.request.get('data')}
                query = ndb.gql("""SELECT * FROM Server""")
                for current in query:
                    #url = current.link + "/Add_Server?name=chat_server&link=http://ap2-chat-server.appspot.com"
                    #result = urlfetch.fetch(url)
                    
                    url = current.link
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                    if result.status_code == 200:
                            self.response.out.write(result.content)
                mesStat = AddMessageStatus (1 , 'success')
                self.response.out.write(mesStat.to_JSON())
        else:
                mesStat = AddMessageStatus (0 , 'something went wrong')
                self.response.out.write(mesStat.to_JSON())
 '''       

class login(webapp2.RequestHandler):
     def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
            mesStat = AddMessageStatus (1 , 'success')
            self.response.out.write(mesStat.to_JSON())
        else:
            self.redirect(users.create_login_url(self.request.uri))
            mesStat = AddMessageStatus (0 , 'not logged in')
            self.response.out.write(mesStat.to_JSON())

class logoff(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url(self.request.uri))

class Leave_Channel(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         #user = users.get_current_user().user_id()
         user = self.request.get('user')
         channel = self.request.get('id')
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE id = :chan""", chan = user + channel)
         for user in query:
                 user.key.delete()
         '''
         key = ndb.Key('ChannelMember', user + channel)
		 
         if key is None:
            mesStat = AddMessageStatus (0 , 'channel does not exist')
            self.response.out.write(mesStat.to_JSON())
         else:
            key.delete()
         '''
         '''
            chanMem = ChannelMemberJas (user + channel, user , channel)
            commandType = {'Content-Type': '/update'}
            form_fields = {"user": self.request.get('user'), "action": 6, "data": chanMem.to_JSON}
            query = ndb.gql("""SELECT * FROM Server""")
            for current in query:
                    url = current.link
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                    if result.status_code == 200:
                            self.response.out.write(result.content)
            counter = 0
            query = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :name""", name = channel)
            for current in query:
                    counter += 1
            if counter == 0:
                    key = ndb.Key('Channel', channel)
                    chan = key.get()
                    chan = ChannelJas (chan.id, chan.name ,chan.icon)
                    commandType = {'Content-Type': '/update'}
                    form_fields = {"user": self.request.get('user'), "action": 4, "data": chan.to_JSON}
                    query = ndb.gql("""SELECT * FROM Server""")
                    for current in query:
                           url = current.link
                           form_data = urllib.urlencode(form_fields)
                           result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                           if result.status_code == 200:
                                   self.response.out.write(result.content)

                    key.delete() 
         '''
         mesStat = AddMessageStatus (1 , 'success')
         self.response.out.write(mesStat.to_JSON())

class getNetwork(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         query = ndb.gql("""SELECT * FROM Channel""")
         allChannels = []
         for channel in query:
                 query2 = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :chan""", chan = channel.id)
                 allUsers = []
                 for user in query2:
                         allUsers.append(user.user_id)
                 feed = ChannelWithMems(channel.id, allUsers)
                 allChannels.append(feed)
         feeds = AllChannels(allChannels)
         self.response.out.write(feeds.to_JSON())
                
class getNumOfClients(webapp2.RequestHandler):
     def get(self):
         counter = 0
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :name""", name = self.request.get('id'))
         for current in query:
                 counter += 1
         self.response.out.write(counter)

class getMyChannels(webapp2.RequestHandler):
     def get(self):
         query = ndb.gql("""SELECT * FROM Channel WHERE mine = true""")
         self.response.headers['Content-Type'] = 'application/json'
         allChannels = []
         for channel in query:
             feed = ChannelJas(channel.id, channel.name, channel.icon)
             allChannels.append(feed)
         feeds = AllChannels(allChannels)
         self.response.out.write(feeds.to_JSON())

             
app = webapp2.WSGIApplication([('/sendMessage', Save_Message), ('/addChannel', Add_Channel), ('/joinChannel', Join_Channel), ('/getServers', Get_Servers),
 ('/login', login),('/getUpdates', Get_Updates), ('/getChannels', Get_Channels),('/Retrieve_Message', Retrieve_Message), ('/register', register),
 ('/leaveChannel', Leave_Channel), ('/logoff', logoff), ('/update', update), ('/unRegister', unRegister), ('/getNetwork', getNetwork),
 ('/getNumOfClients', getNumOfClients), ('/getMyChannels', getMyChannels)
], debug=True)
