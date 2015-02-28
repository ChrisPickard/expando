#!/usr/bin/env python

import pymongo
import msgpackrpc

_client = pymongo.MongoClient()
_db = _client.test_database


class ExpandoServer(object):

    def add_expansion(self, trigger, action, upsert=False):
        """
        Adds expando expansion. Use the upsert flag to override
        any current expansion with that trigger.

        returns whether expansion was successfully added
        """
        document = {"trigger": trigger, "action": action}
        _collection = _db.test_collection
        record = _collection.find_one({"trigger": trigger})
        print(record.get("action"))
        if record and not upsert:
            return False
        else:
            # TODO this doesn't upsert, need to fix that
            _collection.save(document)
            return True

    def expand(self, trigger):
        """
        Gets the expansion for a trigger

        returns the expansion for a trigger
        """
        _collection = _db.test_collection
        return _collection.find_one({"trigger": trigger}).get("action")


def serve_background(server, daemon=False):
    def _start_server(server):
        server.start()
        server.close()

    import threading

    t = threading.Thread(target=_start_server, args=(server,))
    t.setDaemon(daemon)
    t.start()
    return t


def serve(daemon=False):
    """Serve echo server in background on localhost.
    This returns (server, port). port is number in integer.
    To stop, use ``server.shutdown()``
    """
    for port in range(9000, 10000):
        try:
            addr = msgpackrpc.Address('localhost', port)
            server = msgpackrpc.Server(ExpandoServer())
            print(server)
            server.listen(addr)
            thread = serve_background(server, daemon)
            return (addr, server, thread)
        except Exception as err:
            print(err)
            pass

if __name__ == "__main__":
    ADDR = SERVER = THREAD = None
    (ADDR, SERVER, THREAD) = serve(False)

    client = msgpackrpc.Client(ADDR, unpack_encoding='utf-8')
    if not client.call('add_expansion', 'esc', 'ah, a vim user I see'):
        client.call(
            'add_expansion',
            'esc',
            'oh no! a conflict',
            'upsert=True')
    action = client.call('expand', 'esc')
    SERVER.stop()

    print(action)
