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
from google.appengine.ext import search
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

#Load custom filters
webapp.template.register_template_library('sabandija_tags')

#Domain model
  
class Jar( search.SearchableModel ):    
    jar_name   = db.StringProperty( multiline=False )
        
class Artifact( db.Model ):            
    jar_name     = db.StringProperty( multiline=False )
    artifactId   = db.StringProperty( multiline=False ) 
    groupId      = db.StringProperty( multiline=False )
    modelVersion = db.StringProperty( multiline=False )
    version      = db.StringProperty( multiline=False )
    size         = db.StringProperty( multiline=False )
    md5          = db.StringProperty( multiline=False )
    sha1         = db.StringProperty( multiline=False )
    mvnModified  = db.StringProperty( multiline=False )   
    jar          = db.ReferenceProperty( Jar, collection_name='artifacts' )

    
class Location( db.Model ):
    url          = db.StringProperty   ( multiline=False )
    repository   = db.StringProperty   ( multiline=False)
    artifact     = db.ReferenceProperty( Artifact, collection_name='locations' )

class Clazz( search.SearchableModel ):    
    class_name   = db.StringProperty( multiline=False )
    jar          = db.ReferenceProperty( Jar, collection_name='classes' )

#Controllers    
class MainPage( webapp.RequestHandler ):
  def get( self ):
    template_values = {
      
      }
  
    path = os.path.join( os.path.dirname(__file__), 'index2.html' )
    self.response.out.write( template.render( path, template_values ) )
          
class SearchPage( webapp.RequestHandler ):
  
  results_limit = 25
    
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
    c_offset = int(self.request.get( 'c_offset' ))
    j_offset = int(self.request.get( 'j_offset' ))
        
    logging.info( 'c_offset: %d', c_offset )    
    template_values    = { }
    if  search:
      more_classes     = False
      more_jars        = False      
      too_many_classes = self.tooManyClazzes( keyword )
      clazzes          = { }
      logging.info( too_many_classes )
      if not too_many_classes:    
          clazzes, more_classes = self.searchClazz( keyword, more_classes, c_offset )
      logging.info( more_classes )
      
      jars, more_jars  = self.searchJar( keyword, more_jars, j_offset )
      template_values  = {  'clazzes'          : clazzes,
                           'jars'             : jars,
                           'c_offset'         : c_offset,  
                           'j_offset'         : j_offset, 
                           'c_more'           : more_classes,
                           'j_more'           : more_jars,
                           'keyword'          : keyword,
                           'too_many_classes' :too_many_classes  
                        }
    
    path = os.path.join( os.path.dirname(__file__), 'index2.html' )
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
  
  def searchJar( self, keyword, more, offset = 0 ):    
    jar_query = Jar.all().search( keyword )
    
    offset = self.calculateOffset( offset )
    
    jar_query.fetch( self.results_limit, offset +1 )
    more = jar_query.count() > self.results_limit
    
    jar_results = jar_query.fetch( self.results_limit, offset )
         
    return jar_results, more
  
  def tooManyClazzes( self, keyword ):
      class_query = Clazz.all().search( keyword )
      return class_query.count() >= 1000
      
  def searchClazz( self, keyword, more, offset = 0 ):
    
    # Search the 'Clazz' Entity based on our keyword
    #class_query = search.SearchableQuery( 'Clazz' )
    #class_query.Search( keyword )
    class_query = Clazz.all().search( keyword )
    offset = self.calculateOffset( offset )
        
    #Try to see if there are more registers after the offset
    class_query.fetch( self.results_limit, offset + 1 )
    more = class_query.count() > self.results_limit
    
    #Retrieve only 25 objects    
    class_results = class_query.fetch( self.results_limit, offset )
    return class_results, more    
      
  def calculateOffset( self, offset ):
     #adjust the offset to the 25 results per page factor 
    if offset > 0:
        offset -= 1
        offset *= self.results_limit
    return offset
       
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
    
#Class used to autocomplete the search input field
class AutocompleteClass( webapp.RequestHandler ):
    def get( self ):
        keyword = self.request.get( 'q' )
        if keyword:
            q = Clazz.all().search( keyword )
            results = q.fetch( 25 )
            artifacts = ""
            for r in results:
                artifacts += r.class_name +'\n'
            #self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(  artifacts  )
            

class DeleteAll( webapp.RequestHandler ):
  def get( self ):
    q = db.GqlQuery("SELECT * FROM Artifact")
    #total = q.count()
    results = q.fetch(250)
    db.delete(results)
    
    print 'Content-Type: text/plain'
    print ''
    #print 'Total -> ', total
    print ' se borraron 250'
          

def main():
  application = webapp.WSGIApplication( [ 
                                          ( '/'             , MainPage ), 
                                          ( '/search'       , SearchPage ), 
                                          ( '/jar'          , SearchJar ),
                                          ( '/clazz'        , SearchClass ),
                                          ( '/autocomplete' , AutocompleteClass ),
                                          ( '/borrartodo'   , DeleteAll )
                                        ],
                                        debug = True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
