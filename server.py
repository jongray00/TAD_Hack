import csv
import json
import urllib.parse
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonpointer import resolve_pointer, JsonPointerException


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        if not post_data:
            self.send_response(400)
            self.end_headers()
            return

        post_data = json.loads(post_data)

        try:
            # Checking if the SWAIG action is post_conversation
            if resolve_pointer(post_data, "/action") == "post_conversation":
                prompt_data = resolve_pointer(post_data, "/post_prompt_data/parsed/0")

                with open('customer_data.csv', mode='a') as customer_file:
                    fieldnames = ['caller_name', 'phone_number', 'call_summary']
                    writer = csv.DictWriter(customer_file, fieldnames=fieldnames)

                    writer.writerow(prompt_data)

                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.end_headers()
        except JsonPointerException:
            # Skip this call if post_chat action is not found.
            pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MyRequestHandler)
    print("Server started on port 8080")
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()