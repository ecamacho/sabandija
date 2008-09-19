from google.appengine.api import datastore
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
import datetime
import logging
from sabandija import Jar, Artifact

class ArtifactLoader( bulkload.Loader ):
  def __init__( self ):    
    bulkload.Loader.__init__( self, 'Artifact',
                              [ ( 'url'         , str ),
                                ( 'jar_name'    , str ), 
                                ( 'modelVersion', str ),
                                ( 'groupId'     , str ),                                
                                ( 'artifactId'  , str ),                                                                                                
                                ( 'version'     , str ),                                                            
                                ( 'size'        , str ),
                                ( 'md5'         , str ),
                                ( 'sha1'        , str ),
                                ( 'mvnModified' , str ),  #lambda x: datetime.datetime.strptime( x, '%d-%m-%Y %H:%M' ) ),
                                #( 'className'   , str )
                               # ( 'sbjModified' , str )
                              ] )

  def HandleEntity( self, entity ):
                  
    j_name = entity[ 'jar_name' ]    
    jar    = datastore.Query( 'Jar', { 'jar_name' : j_name } ).Get( 1 )
    is_new = False  
    if len( jar ) == 0:
        
        jar               = datastore.Entity( 'Jar', 
                                              name = j_name                                     
                                            )                     
        jar[ 'jar_name' ] = j_name
        jar               = search.SearchableEntity( jar )
        is_new            = True
    else:
        jar = jar[ 0 ]
    
    artifact = Artifact(
                        name         = entity[ 'url' ],
                        url          = entity[ 'url' ],
                        jar_name     = entity[ 'jar_name' ],
                        artifactId   = entity[ 'artifactId' ],
                        groupId      = entity[ 'groupId' ],
                        modelVersion = entity[ 'modelVersion' ],
                        version      = entity[ 'version' ],
                        size         = entity[ 'size' ],
                        md5          = entity[ 'md5' ],
                        sha1         = entity[ 'sha1' ],
                        mvnModified  = entity[ 'mvnModified' ],
                        jar          = jar.key()
                       )                
    artifact.put()            
    if is_new:
        return jar    

if __name__ == '__main__':
  bulkload.main( ArtifactLoader() )