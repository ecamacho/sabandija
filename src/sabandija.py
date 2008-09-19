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

#Domain model
class Jar( db.Model ):    
    jar_name   = db.StringProperty( multiline=False )
class Clazz( db.Model ):    
    class_name   = db.StringProperty( multiline=False )
    jar          = db.ReferenceProperty( Jar, collection_name='classes' )    
class Artifact( db.Model ):    
    url          = db.StringProperty( multiline=False ) 
    jar_name     = db.StringProperty( multiline=False )
    artifactId   = db.StringProperty( multiline=False ) 
    groupId      = db.StringProperty( multiline=False )
    modelVersion = db.StringProperty( multiline=False )
    version      = db.StringProperty( multiline=False )
    size         = db.StringProperty( multiline=False )
    md5          = db.StringProperty( multiline=False )
    sha1         = db.StringProperty( multiline=False )
    jar          = db.ReferenceProperty( Jar, collection_name='artifacts' )


    

#Controllers    
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
        artifacts = searchClazz( keyword )
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write( json.write( artifacts ) )
    
  def post( self ):
    # We use the webapp framework to retrieve the keyword
    keyword = self.request.get( 'keyword' )
    
    template_values = {  }
    if  search:      
      clazzes = self.searchClazz( keyword )
     
      jars    = self.searchJar( keyword )
      template_values = {  'clazzes'      : clazzes,
                           'jars'         : jars,
                       #    'jar_count'    : self.leniter( jars ),
                       #    'clazzes_count': self.leniter( clazzes ), 
                           'keyword'      : keyword  
                        }
    
    path = os.path.join( os.path.dirname(__file__), 'index.html' )
    self.response.out.write( template.render( path, template_values ) )

  def leniter(self, iterator):
    """leniter(iterator): return the length of an iterator,
    consuming it."""
    if hasattr(iterator, "__len__"):
        return len(iterator)
    nelements = 0
    for _ in iterator:
        nelements += 1
    return nelements
  
  def searchJar( self, keyword ):
    jar_query = search.SearchableQuery( 'Jar' )
    jar_query.Search( keyword )
    
    jar_results = jar_query.Run()    
    return jar_results
  
  def searchClazz( self, keyword ):
    # Search the 'Clazz' Entity based on our keyword
    class_query = search.SearchableQuery( 'Clazz' )
    class_query.Search( keyword )
    
    class_results = class_query.Run()
    return class_results    
    #artifacts = []
    #for result in class_results:
        #get the associated artifact for the class
    #    key      = result[ 'jar' ]       
    #    jar = db.get( key )        
    #    if jar:      
    #        arts = jar.artifacts
    #        for art in arts:       
    #            item = { 
    #                    'name' : result[ 'className' ],
    #                    'url'  : art.url 
    #                }
    #            artifacts.append( item )
    #return artifacts;        
      

class SearchJar( webapp.RequestHandler ):
  def get( self ):
    # We use the webapp framework to retrieve the keyword
    keyword = self.request.get( 'jar' )
    template_values = {}        
    if  keyword:      
        #jar   = db.get( db.Key(  keyword.decode() ) )
        query     = db.GqlQuery("SELECT * FROM Jar " + 
                                "WHERE jar_name = :1" ,
                                keyword)
        results   = query.run() 
        if query.count() > 0:
            jar       = results.next()            
            artifacts = jar.artifacts
            template_values = {  'jar'      : jar,
                             'artifacts': artifacts                         
                          }    
    path = os.path.join( os.path.dirname(__file__), 'jar.html' )
    self.response.out.write( template.render( path, template_values ) )

class SearchClass( webapp.RequestHandler ):
  def get( self ):
    # We use the webapp framework to retrieve the keyword
    keyword = self.request.get( 'clazz' )
    template_values = {}        
    if  keyword:      
        #jar   = db.get( db.Key(  keyword.decode() ) )
        query     = db.GqlQuery("SELECT * FROM Clazz " + 
                                "WHERE class_name = :1" ,
                                keyword)
        results   = query.run() 
        template_values = {  'clazzes'      : results,
                             'keyword'        : keyword                         
                          }            
                
    path = os.path.join( os.path.dirname(__file__), 'clazz.html' )
    self.response.out.write( template.render( path, template_values ) )


def main():
  application = webapp.WSGIApplication( [ 
                                          ( '/'      , MainPage ), 
                                          ( '/search', SearchPage ), 
                                          ( '/jar'   , SearchJar ),
                                          ( '/clazz'   , SearchClass )
                                        ],
                                        debug = True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
