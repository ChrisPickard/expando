import msgpackrpc
from core.expando import ExpandoServer


ADDR = SERVER = THREAD = None
(ADDR, SERVER, THREAD) = ExpandoServer().serve()

client = msgpackrpc.Client(ADDR, unpack_encoding='utf-8')
client.call('add_expansion', u'esc', u'a vim user I see')
action = client.call('expand', u'esc')

print(action)
