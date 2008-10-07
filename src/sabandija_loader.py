from google.appengine.api import datastore
from google.appengine.ext import db
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
import datetime
import logging
from sabandija import Jar, Artifact, Location

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
                                ( 'repository' , str )
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
                        name         = entity[ 'jar_name' ],                        
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
    #oldArt = Artifact.get( db.Key(artifact.jar_name) )
    
    oldArt = db.GqlQuery("Select * from Artifact where jar_name = :1", artifact.jar_name).get()
    
    #update the existing one
    if oldArt:        
        oldArt.artifactId   = artifact.artifactId
        oldArt.groupId      = artifact.groupId
        oldArt.modelVersion = artifact.modelVersion
        oldArt.version      = artifact.version
        oldArt.size         = artifact.size
        oldArt.md5          = artifact.md5
        oldArt.sha1         = artifact.sha1
        oldArt.mvnModified  = artifact.mvnModified
        #oldArt.jar          = artifact.jar 
        key            = oldArt.put()
        
        logging.info("updating..")
    #insert the new one    
    else:                          
        key = artifact.put()
        logging.info("inserting..")
    old_location = db.GqlQuery("Select * from Location where url = :1", entity[ 'url' ]).get()
    if not old_location:
        location = Location(
                        name         = entity[ 'url' ],
                        url          = entity[ 'url' ],
                        repository   = entity[ 'repository' ],
                        artifact     = key    
                        )        
        location.put()
    if is_new:
        return jar    

if __name__ == '__main__':
  bulkload.main( ArtifactLoader() )