# TO DO:
# 1. List out all categories and relavent items
# 2. add create new category function
# 3. add edite delete to each items
# 4. add create new category function
# 5. add edit to the category for user
# 6. add delete option to category for user

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Import CRUD operations from Lesson 1
from database_setup import Base, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()


class webserverHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:

			if self.path.endswith("/catalog/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Category</h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/catalog/new'>"
				output += "<input name = 'newCategoryName' type = 'text' placeholder = 'New Category Name' > "
				output += "<input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return

			if self.path.endswith("/edit"):
				itemIDPath = self.path.split("/")[2]
				myitemQuery = session.query(CategoryItem).filter_by(id=itemIDPath).one()
				if myitemQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<html><body>"
					output += "<h1>"
					output += myitemQuery.name
					output += "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action = '/catalog/%s/edit' >" % itemIDPath
					output += "<input name = 'newitemName' type='text' placeholder = '%s' >" % myitemQuery.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)

			if self.path.endswith("/delete"):
				itemIDPath = self.path.split("/")[2]
				myitemQuery = session.query(CategoryItem).filter_by(id=itemIDPath).one()
				if myitemQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<html><body>"
					output += "<h1>Are you sure you want to delete %s ?" % myitemQuery.name
					output += "<form method='POST' enctype='multipart/form-data' action = '/catalog/%s/delete' >" % itemIDPath
					output += "<input type = 'submit' value = 'Delete'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)

			if self.path.endswith("/catalog"):
				categories = session.query(Category).all()
				items = session.query(CategoryItem).all()
				output = ""

				output += "<a href = '/catalog/new' > Make a New Category Here </a></br></br>"
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output += "<html><body>"

				for category in categories:
					output += category.name
					output += "</br></br></br>"

				for item in items:
					output += "<a href = '#'>%s</a>" % item.name
					output += "</br>"
					output += item.description
					output += "</br></br>"

					output += "<a href ='/catalog/%s/edit'>Edit</a>" % item.id
					output += "</br>"
					output += "<a href ='/catalog/%s/delete'>Delete</a>" % item.id
					output += "</br></br>"

				output += "</body></html>"
				# send message back to client
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File Not Found: %s" % self.path)

	def do_POST(self):
		try:

			if self.path.endswith("/delete"):
				itemIDPath = self.path.split("/")[2]
				myitemQuery = session.query(CategoryItem).filter_by(id=itemIDPath).one()
				if myitemQuery:
					session.delete(myitemQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/catalog')
					self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newCategoryName')
					itemIDPath = self.path.split("/")[2]

					myitemQuery = session.query(CategoryItem).filter_by(id=itemIDPath).one()
					if myitemQuery != []:
						myitemQuery.name = messagecontent[0]
						session.add(myitemQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/catalog')
						self.end_headers()

			if self.path.endswith("/catalog/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newCategoryName')

					# Create new Category Object
					newCategory = Category(name=messagecontent[0])
					session.add(newCategory)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/catalog')
					self.end_headers()

		except:
			pass

def main():
	try:
		port = 8888
		server = HTTPServer(('',port),webserverHandler)
		print "web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server"
		server.socket.close()

if __name__ == '__main__':
	main()