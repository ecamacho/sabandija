from google.appengine.ext import webapp
 
register = webapp.template.create_template_register()
#Custom filters for the application

#Returns the name of a maven repository based on its number
def mvnrepo( value ):
    tag = ""    
    if   value == "1":
            tag = "mvn repo";
    elif value == "2":
            tag = "ibiblio.org"
    elif value == "3":            
            tag = "java.net"     
    return tag

register.filter( mvnrepo )