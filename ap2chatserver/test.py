import unittest
import webapp2
import main
import os
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util  # noqa
import sys
sys.path.append('C:\Program Files\Google\Cloud SDK\google-cloud-sdk')
import dev_appserver
dev_appserver.fix_sys_path()

class HelloWorldTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Create a consistency policy that will simulate the High Replication
        # consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        # Initialize memcache stub too, since ndb also uses memcache
        self.testbed.init_memcache_stub()
        # Clear in-context cache before each test.
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()
    '''
    def setCurrentUser(email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

    def logoutCurrentUser():
        setCurrentUser(None, None)
    '''

    def testGetChannels(self):
        request = webapp2.Request.blank('/getChannels')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('channels', response.body)

    def testGetServers(self):
        request = webapp2.Request.blank('/getServers')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('server', response.body)

    def testGetNetwork(self):
        request = webapp2.Request.blank('/getNetwork')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('channels', response.body)

    def testAddChannel(self):
        #add channel 1
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        id = '123'
        name = 'fox'
        icon = 'icon1'
        params = {'id':id, 'name':name, 'icon':icon}
        #setCurrentUser('djblinick@gmail.com', 'test', False)
        request = webapp2.Request.blank('/addChannel', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
    
    def testGetUpdates(self):
        #getUpdate
        #setCurrentUser('djblinick@gmail.com', 'test', False)
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        request = webapp2.Request.blank('/getUpdates')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('change_server', response.body)
        self.assertIn('messages', response.body)

    def testSendMessage(self):
        channel_id = '123'
        text = 'noice'
        longtitude = '10'
        latitude = '20'
        #setCurrentUser('djblinick@gmail.com', 'test', False)
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        params = {'channel_id': channel_id, 'text':text, 'longtitude': longtitude, 'latitude': latitude}
        request = webapp2.Request.blank('/sendMessage', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)

            
    def testJoinChannel(self):
        channel_id = '123'
        params = {'id': channel_id}
        #setCurrentUser('djblinick@gmail.com', 'test', False)
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        request = webapp2.Request.blank('/joinChannel', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
    
    def testRegister(self):
        link = 'https://practice-server.appspot.com'
        params = {'link': link}
        request = webapp2.Request.blank('/register', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
    
    def testUnRegister(self):
        link = 'https://practice-server.appspot.com'
        params = {'link': link}
        request = webapp2.Request.blank('/unRegister', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)

    def testUpdate(self):   
        user = 'djblinick'
        action = 5
        data = '{"channel_id": "123"}'
        params = {'user': user, 'action': action, 'data': data}
        request = webapp2.Request.blank('/update', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
    
    def testLogin(self):
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        request = webapp2.Request.blank('/login')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
    
    def testLogout(self):
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        request = webapp2.Request.blank('/logout')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 0', response.body)
        
    def testLeaveChannel(self):
        channel_id = '123'
        params = {'id': channel_id}
        #setCurrentUser('djblinick@gmail.com', 'test', False)
        os.environ['USER_EMAIL'] = 'djblinick@gmail.com' or ''
        os.environ['USER_ID'] = 'test' or ''
        os.environ['USER_IS_ADMIN'] = '0'
        request = webapp2.Request.blank('/leaveChannel', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
    
    def testNumOfClients(self):
        channel_id = '123'
        params = {'id': channel_id}
        request = webapp2.Request.blank('/getNumOfClients', POST=params)
        request.method = 'GET'
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, '0')
    
    def testMyChannels(self):
        request = webapp2.Request.blank('/getMyChannels')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
        self.assertIn('channels', response.body)
    
    def testChangeChannels(self):
        remove = ['123','1234']
        linkToServer = 'https://practice-server.appspot.com'
        params = {'remove': remove, 'linkToServer' : linkToServer}
        request = webapp2.Request.blank('/changeChannels', POST=params)
        request.method = 'POST'
        response = request.get_response(main.app)
        
        self.assertEqual(response.status_int, 200)
        self.assertIn('"status": 1', response.body)
      

if __name__ == '__main__':    unittest.main()
