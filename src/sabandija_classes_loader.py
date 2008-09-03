from google.appengine.api import datastore
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
from google.appengine.ext import db
import logging

class ClazzLoader( bulkload.Loader ):
  def __init__( self ):    
    bulkload.Loader.__init__( self, 'Clazz',
                              [ ( 'url'         , str ),                                                                
                                ( 'className'   , str )
                               # ( 'sbjModified' , str )
                              ] )

  def HandleEntity( self, entity ):
   #Obtain the Artifact entity associated to this model   
   url = entity['url']   
   art = datastore.Query('Artifact', {'url': url}).Get(1)  
   if art[0]:       
       newent = datastore.Entity( 'Clazz' )
       newent[ 'artifact' ] = art[0].key()
       newent[ 'className' ] = entity['className']
       ent = search.SearchableEntity( newent )
       return ent
   else:    
       logging.info("not done :-(")
       
if __name__ == '__main__':
  bulkload.main( ClazzLoader() )