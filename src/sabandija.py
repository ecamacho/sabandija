import cgi
import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import search
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template



class MainPage( webapp.RequestHandler ):
  def get( self ):
    template_values = {
      
      }
  
    path = os.path.join( os.path.dirname(__file__), 'index.html' )
    self.response.out.write( template.render( path, template_values ) )
          
class SearchPage( webapp.RequestHandler ):
  def post( self ):
    # We use the webapp framework to retrieve the keyword
    keyword = self.request.get( 'keyword' )

    #self.response.headers[ 'Content-Type' ] = 'text/plain'
    #self.response.out.write('%s' % keyword)
    template_values = {  }
    if  keyword:      
      # Search the 'Artifact' Entity based on our keyword
      query = search.SearchableQuery( 'Artifact' )
      query.Search(keyword)
      results = query.Run()
      template_values = { 'artifacts': results, 
                          'keyword'  : keyword  
                        }
    
    path = os.path.join( os.path.dirname(__file__), 'index.html' )
    self.response.out.write( template.render( path, template_values ) )
     # for result in query.Run():
      #   self.response.out.write('%s' % result['jarName'] + ".jar")
       
def main():
  application = webapp.WSGIApplication( [ 
                                          ( '/', MainPage ), 
                                          ( '/search', SearchPage ) 
                                        ],
                                        debug = True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
