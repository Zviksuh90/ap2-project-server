import webapp2
import json
import datetime
import urllib
from google.appengine.api import urlfetch
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
	def __init__(self, messages, link):
		self.messages = messages
		self.change_server = link

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ChannelWithMems:
        def __init__(self, id, member):
                self.id = id
		self.members = member

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
		self.channel_id = iden
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

class ChannelShortJas:
        def __init__(self, channel_id):
		self.channel_id = channel_id

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
    to_who = ndb.StringProperty()

class ChannelMember(ndb.Model):
    id = ndb.StringProperty()
    channel_id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    mine = ndb.StringProperty()

class Server(ndb.Model):
    id = ndb.StringProperty()
    link = ndb.StringProperty()

class ServerMember(ndb.Model):
    id = ndb.StringProperty()
    user = ndb.StringProperty()
    link = ndb.StringProperty()

class ChannelToSwitch(ndb.Model):
    link = ndb.StringProperty()
    channel_id = ndb.StringProperty()

class Save_Message(webapp2.RequestHandler):
     def post(self):
         #try:
             user = users.get_current_user()
             if user:
                 user = users.get_current_user().nickname()
             else:
                 user = self.request.get('user')
             #user = users.get_current_user().nickname()
             #user = self.request.get('user')
             dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
             query = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :chan AND mine =:t """, chan = self.request.get('channel_id'), t = "true")
             for member in query:      
                     message = Message(id = self.request.get('text'), user_id = user, channel_id = self.request.get('channel_id'), text = self.request.get('text'), latitude = float(self.request.get('latitude')), longtitude = float(self.request.get('longtitude')),  date_time = dateTime, to_who = member.user_id)
                     message.put()
             #memb = messageShort (self.request.get('channel_id'), self.request.get('text') ,self.request.get('latitude'), self.request.get('longtitude'))

             commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
             data = "{\"channel\":\"" + self.request.get('channel_id') + "\",\"text\":\"" + self.request.get('text') + "\",\"longtitude\":" + str(self.request.get('longtitude')) + ",\"latitude\":" + str(self.request.get('latitude')) + "}"
             self.response.out.write(user)
             self.response.out.write(data)
             form_fields = {'user': user, 'action': 3, 'data': data}
             query = ndb.gql("""SELECT * FROM Server""")
             for current in query:
                    url = "http://" + current.link + "/update"
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                    self.response.out.write(result.content)
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
  
         #except (RuntimeError, TypeError, NameError, ValueError):
             mesStat = AddMessageStatus (0 , 'missing a tag')
             self.response.out.write(mesStat.to_JSON())

class Get_Updates(webapp2.RequestHandler):
     def get(self):
         self.response.headers['Content-Type'] = 'application/json'
         chanRemove = "None"
         link = "None"
         chanToSwitch = None
         allMessages = []
         count = 0
         user = users.get_current_user()
         if user:
                 user = users.get_current_user().nickname()
         else:
                 user = self.request.get('user')
         #user = self.request.get('user')
         finalMessage = "{\"messages\":["
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE user_id = :name""", name = user)
         
         for channel in query:
             query2 = ndb.gql("""SELECT * FROM Message WHERE channel_id = :chan AND to_who =:us""", chan = channel.channel_id, us = user)
             for message in query2:
                 if count != 0:
                         finalMessage = finalMessage + ","
                 finalMessage = finalMessage + "{\"channel_id\":\"" + message.channel_id + "\",\"user_id\":\"" + message.user_id + "\",\"text\":\"" + message.text + "\",\"date_time\":\"" + message.date_time + "\",\"longtitude\":" + str(message.longtitude) + ",\"latitude\":" + str(message.latitude) + "}"
                 count += 1
                 message.key.delete()
                 #feed = messages(message.channel_id, message.user_id, message.text, message.date_time, message.latitude, message.longtitude)
                 #allMessages.append(feed)
             query3 = ndb.gql("""SELECT * FROM ChannelToSwitch WHERE channel_id = :chan""", chan = channel.channel_id)
             for server in query3:
                chanRemove = server.channel_id
                link = server.link
                chanToSwitch = server
         finalMessage = finalMessage + "],\"change_server\":\""
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE id = :iden""", iden = user + chanRemove)
         counter = 0
         for member in query:
             member.key.delete()
         query2 = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :name""", name = chanRemove)
         for current in query2:
             counter += 1
         if counter == 0:
             query3 = ndb.gql("""SELECT * FROM Channel WHERE id = :name""", name = chanRemove)
             for current in query3:
                 current.key.delete()
                 chanToSwitch.key.delete()
         finalMessage = finalMessage + "\"}"
         #feeds = Feeds(allMessages, link)
         #self.response.out.write(feeds.to_JSON())
         self.response.out.write(finalMessage)

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
         try:
                 user = users.get_current_user()
                 if user:
                         user = users.get_current_user().nickname()
                 else:
                         user = self.request.get('user')
                 #user = users.get_current_user().nickname()
                 #user = self.request.get('user')
                 
                 self.response.headers['Content-Type'] = 'application/json'
                 counter = 0
                 query = ndb.gql("""SELECT * FROM Channel WHERE id = :iden""", iden = self.request.get('id'))
                 for channel in query:
                         counter += 1
                 if counter == 0:
                         channel = Channel(id = self.request.get('id'), name = self.request.get('name'), icon = self.request.get('icon'))
                         channel.put()
                        
                         chan = ChannelJas (self.request.get('id'), self.request.get('name') ,self.request.get('icon'))
                         commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
                         form_fields = {'user': user, 'action': 4, 'data': chan.to_JSON()}
                         query = ndb.gql("""SELECT * FROM Server""")
                         for current in query:
                                url = 'http://' + current.link + '/update'
                                form_data = urllib.urlencode(form_fields)
                                result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                                self.response.out.write(result.content)
                                


                         #user = users.get_current_user().nickname()
                         #user = self.request.get('user')       
                         channel = self.request.get('id')
                         channel = ChannelMember(id = user + channel, user_id = user, channel_id = channel, mine = "true")
                         channel.put()

                         chanMem = ChannelShortJas (self.request.get('id'))
                         temp = chanMem.to_JSON()

                         commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
                         form_fields = {"user": user, "action": 5, "data": temp}
                         query = ndb.gql("""SELECT * FROM Server""")
                         for current in query:
                                 url = "http://" + current.link + "/update"
                                 form_data = urllib.urlencode(form_fields)
                                 result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)

                         queryS = ndb.gql("""SELECT * FROM Server""")
                         for server in queryS:
                           url = "http://" + server.link + "/getMyChannels"
                           result = urlfetch.fetch(url)
                           if result.status_code == 200:
                             j = json.loads(result.content)
                             channels = j['channels']
                             for channel in channels:
                                     disqualify = 0
                                     queryMem = ndb.gql("""SELECT * FROM ChannelMember WHERE mine = :t AND channel_id = :name""", name = channel, t = "true")
                                     for member in queryMem:
                                             queryMemChannels = ndb.gql("""SELECT * FROM ChannelMember WHERE user_id = :name""", name = member.user_id)
                                             for item in queryMemChannels:
                                                 if item.channel_id not in channels:
                                                     disqualify = 1
                                                     break
                                     if disqualify == 0:
                                             channelToSwitch = ChannelToSwitch(link = server.link, channel_id = channel)
                                             channelToSwitch.put()
                                             break
                             
                         mesStat = AddMessageStatus (1 , 'success')
                         self.response.out.write(mesStat.to_JSON())
                 else:
                         mesStat = AddMessageStatus (0 , 'already exists')
                         self.response.out.write(mesStat.to_JSON())
         except (RuntimeError, TypeError, NameError, ValueError):
                 mesStat = AddMessageStatus (0 , 'problem detected')
                 self.response.out.write(mesStat.to_JSON())

class Join_Channel(webapp2.RequestHandler):
     def post(self):
         self.response.headers['Content-Type'] = 'application/json'
         try: 
             user = users.get_current_user()
             if user:
                 user = users.get_current_user().nickname()
             else:
                 user = self.request.get('user')
             #user = users.get_current_user().nickname()
             #user = self.request.get('user')
             channel = self.request.get('id')
             counter = 0
             query = ndb.gql("""SELECT * FROM ServerMember WHERE user = :name""", name = user)
             for serverMem in query:
                     counter += 1
             if counter > 0:
                     channel = ChannelMember(id = user + channel, user_id = user, channel_id = channel, mine = "true")
             else:
                     channel = ChannelMember(id = user + channel, user_id = user, channel_id = channel, mine = "false")
             channel.put()

             chanMem = ChannelShortJas (self.request.get('id'))
             temp = chanMem.to_JSON()

             commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
             form_fields = {"user": user, "action": 5, "data": temp}
             query = ndb.gql("""SELECT * FROM Server""")
             for current in query:
                    url = "http://" + current.link + "/update"
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)

             '''
             commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
             form_fields = {}
             url = "http://ap2chatserver.appspot.com/loadBalancing"
             form_data = urllib.urlencode(form_fields)
             self.response.out.write(555)
             result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
             self.response.out.write(result.content)
             self.response.out.write(666)
             '''
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
         except (RuntimeError, TypeError, NameError, ValueError):
             mesStat = AddMessageStatus (0 , 'missing a tag')
             self.response.out.write(mesStat.to_JSON())


class LoadBalance(webapp2.RequestHandler):
     def post(self):
         queryS = ndb.gql("""SELECT * FROM Server""")
         finish = 0
         for server in queryS:
             '''
             url = server.link + "/getMyChannels"
             result = urlfetch.fetch(url)
             if result.status_code == 200:
                 j = json.loads(result.content)
                 self.response.out.write(result.content)
                 channels = j['channels']
                 for channel in channels:
                     disqualify = 0
                     queryMC = ndb.gql("""SELECT * FROM Channel WHERE mine = :t AND id = :name""", name = channel, t = "true")
                     self.response.out.write(111)
                     for current in queryMC:
                         queryMem = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :name""", name = channel)
                         self.response.out.write(222)
                         for member in queryMem:
                             queryMemOfUs = ndb.gql("""SELECT * FROM ServerMember WHERE user = :name""", name = member.user_id)
                             self.response.out.write(333)
                             for myMember in queryMemOfUs:
                                 queryMemChannels = ndb.gql("""SELECT * FROM ChannelMember WHERE user_id = :name""", name = member.user_id)
                                 self.response.out.write(333)
                                 for item in queryMemChannels:
                                     if item.channel_id not in channels:
                                         disqualify = 1
                                         break
                     if disqualify == 0:
                         self.response.out.write(444)
                         channelToSwitch = ChannelToSwitch(link = server.link, channel_id = channel)
                         channelToSwitch.put()
                         finish = 1
                         break
             if finish == 1:
                 break
             '''
                                     
                             
class register(webapp2.RequestHandler):
     def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        try:
            server = Server(id = self.request.get('link'), link = self.request.get('link'))
            server.put()
            mesStat = AddMessageStatus (1 , 'success')
            self.response.out.write(mesStat.to_JSON())
        except (RuntimeError, TypeError, NameError, ValueError):
            mesStat = AddMessageStatus (0 , 'missing a tag')
            self.response.out.write(mesStat.to_JSON())

class unRegister(webapp2.RequestHandler):
     def post(self):
        try:
            query = ndb.gql("""SELECT * FROM Server WHERE link = :name""", name = self.request.get('link'))
            self.response.headers['Content-Type'] = 'application/json'
            for current in query:
                    current.key.delete()
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

class update(webapp2.RequestHandler):
     def post(self):
        self.response.headers['Content-Type'] = 'application/json'     
        alreadySeen = 0
        user = self.request.get('user')
        action = int(self.request.get('action'))
        j = json.loads(self.request.get('data'))
        self.response.out.write(self.request.get('data'))

        if action == 1:
                query = ndb.gql("""SELECT * FROM ServerMember WHERE id = :iden""", iden = user + j['server'])
                for current in query:
                        alreadySeen += 1
                if alreadySeen == 0:
                        serverMemb = ServerMember(id = user + j['server'], user = user, link = j['server'])
                        serverMemb.put()
        elif action == 2:
                query = ndb.gql("""SELECT * FROM ServerMember WHERE id = :iden""", iden = user + j['server'])
                alreadySeen = 1
                for user in query:
                        user.key.delete()
                        alreadySeen -= 1
                if alreadySeen < 0:
                        alreadySeen = 0
        elif action == 3:
                counter = 0
                query = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :chan AND mine =:t """, chan = j['channel'], t = "true")
                for member in query:      
                     counter += 1
                query = ndb.gql("""SELECT * FROM Message WHERE text = :name""", name = j['text'])
                for current in query:
                        alreadySeen += 1
                if alreadySeen == 0 and counter > 0:
                        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message = Message(id = j['text'], user_id = self.request.get('user'), channel_id = j['channel'], text = j['text'], latitude = float(j['latitude']), longtitude = float(j['longtitude']), date_time = dateTime, to_who = users.get_current_user().nickname())
                        message.put()
        elif action == 4:
                query = ndb.gql("""SELECT * FROM Channel WHERE id = :name""", name = j['channel_id'])
                for current in query:
                        alreadySeen += 1
                if alreadySeen == 0:
                        channel = Channel(id = j['channel_id'], name = j['name'], icon = j['icon'])
                        channel.put()

        elif action == 5:
                query = ndb.gql("""SELECT * FROM Channel WHERE id = :name""", name = j['channel_id'])
                channelExists = 0
                for current in query:
                        channelExists += 1
                if channelExists > 0:
                        user = self.request.get('user')
                        channel = j['channel_id']
                        query = ndb.gql("""SELECT * FROM ChannelMember WHERE id = :name""", name = user + channel)
                        for current in query:
                                alreadySeen += 1
                        if alreadySeen == 0:
                                channelMem = ChannelMember(id = user + channel, user_id = user, channel_id = channel, mine = "false")
                                channelMem.put()
        elif action == 6:
                user = self.request.get('user')
                channel = j['channel_id']
                query = ndb.gql("""SELECT * FROM ChannelMember WHERE id = :name""", name = user + channel)
                alreadySeen = 1
                for current in query:
                        current.key.delete()
                        alreadySeen -= 1
                if alreadySeen < 0:
                        alreadySeen = 0
        elif action == 7:
                query = ndb.gql("""SELECT * FROM Channel WHERE id = :name""", name = j['channel_id'])
                alreadySeen = 1
                for current in query:
                        current.key.delete()
                        alreadySeen -= 1
                if alreadySeen < 0:
                        alreadySeen = 0                      

        if alreadySeen == 0:
                commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
                form_fields = {"user": self.request.get('user'), "action": action, "data": self.request.get('data')}
                query = ndb.gql("""SELECT * FROM Server""")
                for current in query:
                    url = "http://" + current.link + "/update"
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
                mesStat = AddMessageStatus (1 , 'success')
                self.response.out.write(mesStat.to_JSON())
        else:
                mesStat = AddMessageStatus (0 , 'something went wrong')
                self.response.out.write(mesStat.to_JSON())
      

class login(webapp2.RequestHandler):
     def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
            name = user.nickname()
            serverLink = "ap2-chat-server.appspot.com"
            serverMemb = ServerMember(id = name + serverLink, user = name, link = serverLink)
            serverMemb.put()

            serverJason = ServerJas (serverLink)
            commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
            form_fields = {"user": name, "action": 1, "data": serverJason.to_JSON()}
            query = ndb.gql("""SELECT * FROM Server""")
            for current in query:
                    url = "http://" + current.link + "/update"
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
            
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
            name = user.nickname()
            serverLink = "ap2-chat-server.appspot.com"
            query = ndb.gql("""SELECT * FROM ServerMember WHERE id = :ser""", ser = name + serverLink)
            for user in query:
                    user.key.delete()
                    
            self.redirect(users.create_logout_url(self.request.uri))
            
            serverJason = ServerJas (serverLink)
            commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
            form_fields = {"user": name, "action": 2, "data": serverJason.to_JSON()}
            query = ndb.gql("""SELECT * FROM Server""")
            for current in query:
                    url = "http://" + current.link + "/update"
                    form_data = urllib.urlencode(form_fields)
                    result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)
            mesStat = AddMessageStatus (1 , 'success')
            self.response.out.write(mesStat.to_JSON())
        else:
            mesStat = AddMessageStatus (0 , 'not logged in')
            self.response.out.write(mesStat.to_JSON())

class Leave_Channel(webapp2.RequestHandler):
     def post(self):
         self.response.headers['Content-Type'] = 'application/json'
         user = users.get_current_user().nickname()
         #user = self.request.get('user')
         channel = self.request.get('id')
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE id = :iden""", iden = user + channel)
         counter = 0
         for member in query:
                 member.key.delete()

         chanMem = ChannelShortJas (channel)
         commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
         form_fields = {"user": user, "action": 6, "data": chanMem.to_JSON()}
         query = ndb.gql("""SELECT * FROM Server""")
         for current in query:
                 url = "http://" + current.link + "/update"
                 form_data = urllib.urlencode(form_fields)
                 result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)

         query2 = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :name""", name = channel)
         for current in query2:
                 counter += 1
         if counter == 0:
                 query3 = ndb.gql("""SELECT * FROM Channel WHERE id = :name""", name = channel)
                 for current in query3:
                         current.key.delete()
                 chanMem = ChannelShortJas (channel)
                 commandType = {'Content-Type': 'application/x-www-form-urlencoded'}
                 form_fields = {"user": user, "action": 7, "data": chanMem.to_JSON()}
                 query = ndb.gql("""SELECT * FROM Server""")
                 for current in query:
                         url = "http://" + current.link + "/update"
                         form_data = urllib.urlencode(form_fields)
                         result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST, headers=commandType)

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
         self.response.headers['Content-Type'] = 'application/json'
         query = ndb.gql("""SELECT * FROM ChannelMember WHERE mine = :t""", t = "true")
         allChannels = []
         for channel in query:
             allChannels.append(channel.channel_id)
         feeds = AllChannels(allChannels)
         self.response.out.write(feeds.to_JSON())

class changeChannels(webapp2.RequestHandler):
     def post(self):
         listOfChannels = self.request.get('remove')
         link = self.request.get('linkToServer')
         for channel in listOfChannels:
             disqualify = 0
             queryMC = ndb.gql("""SELECT * FROM Channel WHERE mine = :t AND id = :name""", t = "true", name = channel)
             for current in queryMC:
                 queryMem = ndb.gql("""SELECT * FROM ChannelMember WHERE channel_id = :name""", name = channel)
                 for member in queryMem:
                     queryMemOfUs = ndb.gql("""SELECT * FROM ServerMember WHERE user_id = :name""", name = member.user_id)
                     for myMember in queryMemOfUs:
                         queryMemChannels = ndb.gql("""SELECT * FROM ChannelMember WHERE user_id = :name""", name = member.user_id)
                         for item in queryMemChannels:
                             if item.channel_id not in channels:
                                 disqualify = 1
                                 break
         if disqualify == 0:
             for channel in listOfChannels:
                 channelToSwitch = ChannelToSwitch(link = link, channel_id = channel)
                 channelToSwitch.put()
             mesStat = AddMessageStatus (1 , 'success')
             self.response.out.write(mesStat.to_JSON())
         else:
             mesStat = AddMessageStatus (0 , 'no can do')
             self.response.out.write(mesStat.to_JSON())


class reset(webapp2.RequestHandler):
     def get(self):
        query = ndb.gql("""SELECT * FROM ChannelMember""")
        for current in query:
                current.key.delete()
        query = ndb.gql("""SELECT * FROM Channel""")
        for current in query:
                current.key.delete()
        query = ndb.gql("""SELECT * FROM Message""")
        for current in query:
                current.key.delete()
        query = ndb.gql("""SELECT * FROM Server""")
        for current in query:
                current.key.delete()
        query = ndb.gql("""SELECT * FROM ServerMember""")
        for current in query:
                current.key.delete()
        query = ndb.gql("""SELECT * FROM ChannelToSwitch""")
        for current in query:
                current.key.delete()
         
             
app = webapp2.WSGIApplication([('/sendMessage', Save_Message), ('/addChannel', Add_Channel), ('/joinChannel', Join_Channel), ('/getServers', Get_Servers),
 ('/login', login),('/getUpdates', Get_Updates), ('/getChannels', Get_Channels), ('/register', register),
 ('/leaveChannel', Leave_Channel), ('/logoff', logoff), ('/update', update), ('/unRegister', unRegister), ('/getNetwork', getNetwork),
 ('/getNumOfClients', getNumOfClients), ('/getMyChannels', getMyChannels), ('/loadBalancing', LoadBalance), ('/changeChannels', changeChannels), ('/reset',reset)
], debug=True)
