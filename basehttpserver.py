from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import boto3
import json



class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")      

    def do_GET(self):
        self._set_headers()
        self.send_header('Access-Control-Allow-Origin', '*')
        data = open('flightForm.html', 'rb')
        print(data)
        self.wfile.write(data)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self.send_header('Access-Control-Allow-Origin', '*')
	content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1><pre>" + post_data + "</pre></body></html>")
	print post_data # <-- Print post data

	bucket='securebooking'
	s3 = boto3.resource('s3')

        mybucket = s3.Bucket(bucket)

        ##sanity show all bookings in db

        
        for object in mybucket.objects.all():
            print(object.key)

        data = json.loads(post_data)

        print('\n')
        print(data)
        
        s3.Bucket('securebooking').put_object(Key='newbooking', Body=post_data)

        for object in mybucket.objects.all():
            print(object.key)

        

        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
