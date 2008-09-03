import cgi
import os
import json
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import search
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class Artifact( db.Model ):    
    url = db.StringProperty(multiline=False)
    artifactId = db.StringProperty(multiline=False)
    groupId = db.StringProperty(multiline=False)
    modelVersion = db.StringProperty(multiline=False)
    version = db.StringProperty(multiline=False)
    size = db.StringProperty(multiline=False)
    md5 = db.StringProperty(multiline=False)
    sha1 = db.StringProperty(multiline=False)


class MainPage( webapp.RequestHandler ):
  def get( self ):
    template_values = {
      
      }
  
    path = os.path.join( os.path.dirname(__file__), 'index.html' )
    self.response.out.write( template.render( path, template_values ) )
          
class SearchPage( webapp.RequestHandler ):
  def get( self ):
    # We use the webapp framework to retrieve the keyword
    keyword = self.request.get( 'keyword' )        
    if  keyword:      
        artifacts = search( keyword )
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( json.write( artifacts ) )
    
  def post( self ):
    # We use the webapp framework to retrieve the keyword
    keyword = self.request.get( 'keyword' )
    
    template_values = {  }
    if  search:      
      artifacts = self.search( keyword )
      template_values = { 'artifacts': artifacts, 
                          'keyword'  : keyword  
                        }
    
    path = os.path.join( os.path.dirname(__file__), 'index.html' )
    self.response.out.write( template.render( path, template_values ) )
    
  
  def search( self, keyword ):
    # Search the 'Clazz' Entity based on our keyword
    query = search.SearchableQuery( 'Clazz' )
    query.Search(keyword)
    results = query.Run()    
    artifacts = []
    for result in results:
        #get the associated artifact for the class
        key = result[ 'artifact' ]       
        artifact = db.get(key)
        if artifact:            
            item = { 
                    'name' : result[ 'className' ],
                    'url'  : artifact.url 
                    }
            artifacts.append( item )
    return artifacts;        
      
  

def main():
  application = webapp.WSGIApplication( [ 
                                          ( '/', MainPage ), 
                                          ( '/search', SearchPage ) 
                                        ],
                                        debug = True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
