import threading
import sys
import struct
import json
import traceback


class FirefoxComInterface(object):

    def __init__(self, identity_handler):
        self.running = False
        self.identity_handler = identity_handler

    def receive(self):
        rawLength = sys.stdin.buffer.read(4)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.buffer.read(messageLength).decode('utf-8')
        with open("temp.txt", "w") as f:
            f.write(str(type(message)))
        return json.loads(message)

    def send(self, message):
        encodedContent = json.dumps(message).encode('utf-8')
        encodedLength  = struct.pack('@I', len(encodedContent))
        sys.stdout.buffer.write(encodedLength)
        sys.stdout.buffer.write(encodedContent)
        sys.stdout.buffer.flush()

    def run(self):
        while self.running:
            message = self.receive()
            try:
                url   = message["URL"]
                email = message["EMAIL"]
                field = message["FIELD"]
                query = message["QUERY"]
                identities = self.identity_handler.identities[url]
                field_value = None
                for account in identities:
                    if field == "email":
                        field_value = account.email
                    elif field == "password":
                        field_value = account.password
                    # if account.alias.email == email:
                    break
            except:
                self.send(str(traceback.format_exc()))
            self.send({"field_value": field_value, "query": query})

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.running = False
