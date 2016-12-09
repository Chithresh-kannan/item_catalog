from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#import CRUD operations
from database_setup import base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#create session and connect to db
engine = create_engine('sqlite:///restaurantmenu.db')
base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new'>Make a new restaurant here</a></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/edit'>Edit</a></br>"%restaurant.id
                    output += "<a href = '/restaurants/%s/delete'>Delete</a></br></br>" %restaurant.id
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                rid = self.path.split("/")[2]
                editquery = session.query(Restaurant).filter_by(id = rid).one()
                if editquery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s<h1>"%editquery.name
                    output += "<form method = 'post' enctype = 'multipart/form-data' action = '/restaurants/%s/edit'>" %rid
                    output += "<input name = 'newrestaurantname' type = 'text' placeholder = '%s'>" %editquery.name
                    output += "<input type = 'submit' value = 'rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                rid = self.path.split("/")[2]
                deletequery = session.query(Restaurant).filter_by(id = rid).one()
                if rid !=[]:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Are you sure you want to delete %s?</h2>"%deletequery.name
                    output += "<form method = 'post' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>"%rid
                    output += "<input type = 'submit' value = 'delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Make a new restaurant <h1>"
                output += "<form method = 'post' enctype = 'multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newrestaurantname' type = 'text' placeholder = 'new restaurant name'>"
                output += "<input type = 'submit' value = 'create'>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('newrestaurantname')

            newRestaurant = Restaurant(name = messagecontent[0])
            session.add(newRestaurant)
            session.commit()

        if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('newrestaurantname')
            rid = self.path.split("/")[2]
            editquery = session.query(Restaurant).filter_by(id = rid).one()
            if rid != []:
                editquery.name = messagecontent[0]
                session.add(editquery)
                session.commit()
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()

        if self.path.endswith("/delete"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            rid = self.path.split("/")[2]
            deletequery = session.query(Restaurant).filter_by(id = rid).one()
            if deletequery != []:
                session.delete(deletequery)
                session.commit()
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()
                
            
##        try:
##            self.send_response(301)
##            self.send_header('Content-type', 'text/html')
##            self.end_headers()
##            ctype, pdict = cgi.parse_header(
##                self.headers.getheader('content-type'))
##            if ctype == 'multipart/form-data':
##                fields = cgi.parse_multipart(self.rfile, pdict)
##                messagecontent = fields.get('message')
##            output = ""
##            output += "<html><body>"
##            output += " <h2> Okay, how about this: </h2>"
##            output += "<h1> %s </h1>" % messagecontent[0]
##            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
##            output += "</body></html>"
##            self.wfile.write(output)
##            print output
##        except:
##            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
