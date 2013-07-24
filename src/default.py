import webapp2
import logging
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write('Hello, webapp World!')
        
        #directory = os.path.dirname(__file__)
        #path = os.path.join(directory, os.path.join('templates', template_name))
        self.response.out.write(template.render('templates/index.html', {}))
        
class ToolsPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write('Hello, webapp World!')
        
        #directory = os.path.dirname(__file__)
        #path = os.path.join(directory, os.path.join('templates', template_name))
        self.response.out.write(template.render('templates/tools.html', {}))
        
def handle_404(request, response, exception):
    logging.exception(exception)
    response.out.write(template.render('templates/404.html', {}))
    response.set_status(404)

app = webapp2.WSGIApplication([('/', MainPage),('/tools', ToolsPage)], debug=True)
app.error_handlers[404] = handle_404

""" Old code:
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
"""