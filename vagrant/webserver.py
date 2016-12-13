# take advantage of this BaseHTTPServer functionality.
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import common gateway interface
import cgi 

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqllist:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    # handles all get requests our web server recieves.
    # In order to figure out which resource we are trying to access,
    # we will use a simple pattern matching plan that only looks for the ending of our URL path.
    def do_GET(self):
        try:
            # Objective 3 Step 2- Create /restarants/new page
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<intput name = 'newResturantName' type = 'text' placeholder = 'New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></form>"
                self.wfile.write(output)
                return

            # Object 4 step 2 -- looks for slash edit in the URL
            if self.path.endswith("/edit"):
                # first, we need to find a way to grab the ID number out of the URL
                restaurantIDPath = self.path.split("/")[2]
                # grab the restaurant entry 
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            # Object 5
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            # provide a variable path contains the URL sent by the client
            # to the server as a string. the if statement looks for the URL that ends with /hello
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""

                # Objective 3 step 1 - Create a Link to create a new menu item
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br></br></br>"

                    # Objective 2 -- Add Edit and Delete Links
                    # Objective 4 Step 1 -- Replace Edit href
                    # output += "<a href ='#' >Edit</a>"
                    output += "<a href ='/restaurants/%s/edit' >Edit </a>" % restaurant.id
                    output += "</br>"

                    # Object 5 step 1 -- Replace Delete href
                    output += "<a href = '/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br></br></br>"

                # output += "<h1>Hello!</h1>"
                # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # tell the client with the new information I've recieved.
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Objective 3 Step 3 - Make POST method
    def do_POST(self):
        try:
            # Object 5 step 3 -- Make delete post request work
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    
            # Object 4 Step 3 -- Make edit post request work
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                # grab the input from our form again
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    # find the Object with the matching ID
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    # reset the name field to the entry we created in the form.
                    # add the session and commit 
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        # add a redirect to bring us back to our restaurants page
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

# part 2 - section part
def main():
    try:
        port = 10080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s ... open localhost:10080/restaurants in your browser" % port
        # keep it constantly listening until I call CTRL+C or exit the application.
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        # shutdown the server
        server.socket.close()

# immediately run the main method when the Python interpreter executes my script.
if __name__ == '__main__':
    main()


