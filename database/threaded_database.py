from database.database import Database
from queue import Queue
import threading


class ThreadedDatabase(Database):

    def __init__(self):
        Database.__init__(self)
        self.running = False
        self.query_queue = Queue()
        self.reply_queue = Queue()

    def _query_and_wait_for_reply(self, query):
        self.query_queue.put(query)
        return self.reply_queue.get()

    def __getitem__(self, url):
        query = {
            "func": "__getitem__",
            "kwargs": {"url": url}
        }
        return self._query_and_wait_for_reply(query)

    @property
    def accounts(self):
        query = {
            "func": "_get_accounts"
        }
        return self._query_and_wait_for_reply(query)

    @property
    def aliases(self):
        query = {
            "func": "_get_aliases"
        }
        return self._query_and_wait_for_reply(query)

    def add_alias(self, alias):
        query = {
            "func": "add_alias",
            "kwargs": {"alias": alias}
        }
        return self._query_and_wait_for_reply(query)

    def add_account(self, account):
        query = {
            "func": "add_account",
            "kwargs": {"account": account}
        }
        return self._query_and_wait_for_reply(query)

    def load(self, dump):
        query = {
            "func": "load",
            "kwargs": {"dump": dump}
        }
        return self._query_and_wait_for_reply(query)

    def save(self):
        query = {
            "func": "save"
        }
        return self._query_and_wait_for_reply(query)


    def run(self):
        self.running = True
        self.connect()
        while self.running:
            query = self.query_queue.get()
            if query == None:
                break

            method = getattr(super(), query["func"])
            if "kwargs" in query:
                result = method(**(query["kwargs"]))
            else:
                result = method()

            self.reply_queue.put(result)

    def start(self):        
        threading.Thread(target=self.run).start()

    def stop(self):
        self.running = False
        self.query_queue.put(None)
