import http.server
import json
import pyodbc

# Establish connection to SQL Server database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost.;DATABASE=ACT3;UID=SA;PWD=Password123')

# Create cursor object
cursor = conn.cursor()

class APIServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/notes':
            cursor.execute("SELECT * FROM notes")
            notes = cursor.fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/notes':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_note = json.loads(post_data.decode())
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (new_note['title'], new_note['content']))
            conn.commit()
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_note).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, APIServer)
    print('Starting server...')
    httpd.serve_forever()
