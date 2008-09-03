from google.appengine.api import datastore
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
import datetime

class ArtifactLoader( bulkload.Loader ):
  def __init__( self ):    
    bulkload.Loader.__init__( self, 'Artifact',
                              [ ( 'url'         , str ),                                
                                ( 'artifactId'  , str ),
                                ( 'groupId'     , str ),                                  
                                ( 'modelVersion', str ),
                                ( 'version'     , str ),                                                            
                                ( 'size'        , str ),
                                ( 'md5'         , str ),
                                ( 'sha1'        , str ),
                                ( 'mvnModified' , str ),  #lambda x: datetime.datetime.strptime( x, '%d-%m-%Y %H:%M' ) ),
                                #( 'className'   , str )
                               # ( 'sbjModified' , str )
                              ] )

  def HandleEntity( self, entity ):
    newent = datastore.Entity( 'Artifact', name = entity[ 'url']  ) 
    newent.update(entity) 
    #ent = search.SearchableEntity(newent) 
    return newent 

if __name__ == '__main__':
  bulkload.main( ArtifactLoader() )