from google.appengine.api import datastore
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
from google.appengine.ext import db
import logging

class ClazzLoader( bulkload.Loader ):
  def __init__( self ):    
    bulkload.Loader.__init__( self, 'Clazz',
                              [ 
                                ( 'jar_name', str ),                                                                                                
                                ( 'class_name' , str )                               
                              ] 
                            )

  def HandleEntity( self, entity ):
   #Obtain the Jar entity associated to this model   
   j_name = entity[ 'jar_name' ]
   #key    = db.Key(j_name)  
   #jar        = db.get(key)
   jar    = datastore.Query( 'Jar', { 'jar_name': j_name } ).Get( 1 )  
   if jar[0]:       
       newent                = datastore.Entity( 'Clazz' )
       newent[ 'jar' ]       = jar[0].key()
       newent[ 'class_name' ] = entity[ 'class_name' ]
       ent                   = search.SearchableEntity( newent )
       return ent
   else:    
       logging.info("not done :-(")
       
if __name__ == '__main__':
  bulkload.main( ClazzLoader() )