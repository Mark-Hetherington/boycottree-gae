# Copyright 2013 Mark Hetherington
#
# License to be decided - It is intended to be Open source, but will have to weigh up  
# restrictions on creating closed source forks etc... 

"""An application to track boycotts.

Built in Python on GAE as a learning experience. It's my first experience of Python and GAE.
Hopefully we get to a useful application!
"""

__author__ = 'Mark Hetherington'

import webapp2
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
import os
import models
from datetime import datetime

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class RequestHandlerBase(webapp2.RequestHandler):
    def renderTemplate(self, template_name, template_data={}):
        data = {
          'request': self.request,
          'user': users.get_current_user(),
          'login_url': users.create_login_url(self.request.uri),
          'logout_url': users.create_logout_url(self.request.uri)
        }
        data.update(template_data)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))
        self.response.out.write(template.render(path, data, debug=_DEBUG))
  
    def head(self, *args):
        pass
  
    def get(self, *args):
        pass
    
    def post(self, *args):
        pass

class MainPage(RequestHandlerBase):
    def get(self):
        self.renderTemplate('index.html')
        
class ToolsPage(RequestHandlerBase):
    def get(self):
        self.renderTemplate('tools.html')

class SearchPage(RequestHandlerBase):
    def get(self):        
        #TODO:Generate search data!
        self.renderTemplate('search.html',{ 'query' : self.request.get("q")})
        
class ProductIndex(RequestHandlerBase):
    def get(self):
        self.renderTemplate('products.html')

class CompanyIndex(RequestHandlerBase):
    def get(self):
        self.renderTemplate('companies.html')

class BoycottIndex(RequestHandlerBase):
    def get(self):
        self.renderTemplate('boycotts.html')
        
    def post(self):
        boycott = models.Boycott()
        boycott.name = self.request.get('name')
        boycott.content = self.request.get('content')
        boycott.started = datetime.strptime(self.request.get('started'),'%Y-%M-%d')
        boycott.finished = datetime.strptime(self.request.get('finished'),'%Y-%M-%d')
        boycottId = boycott.put()
        self.redirect('/boycott/' + "%02d" % boycottId.id())

class BoycottPage(RequestHandlerBase):
    def get(self,boycottId):
        boycott = models.Boycott.get_by_id(int(boycottId))
        self.renderTemplate('boycott.html',{'boycott':boycott})
    
    
        
"""    def post(self,boycottId):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')"""

class CountryIndex(RequestHandlerBase):
    def get(self):
        self.renderTemplate('countries.html')
        
def handle_404(request, response, exception):
    logging.exception(exception)
    response.out.write(template.render('templates/404.html', {}))
    response.set_status(404)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/tools', ToolsPage),
                               ('/search',SearchPage),
                               ('/product',ProductIndex),
                               ('/company',CompanyIndex),
                               ('/boycott',BoycottIndex),
                               (r'/boycott/(.*)', BoycottPage),
                               ('/country',CountryIndex)], debug=True)
app.error_handlers[404] = handle_404

""" Old code:
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
"""