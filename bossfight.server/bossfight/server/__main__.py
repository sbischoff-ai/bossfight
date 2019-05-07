# -*- coding: utf-8 -*-
"""
Main script of bossfight.server package.

- `bossfight.server` will run a local server on an arbitrary free port
- `bossfight.server ip_address` will start a server on an arbitrary free port
bound to the given IP address.
- `bossfight.server ip_address port` will run a server on the specified port
and IP address.

In either case the server process will give the following output on stdout
directly after starting the server:

`ip_address\\n

port\\EOF`

To shutdown the server, write a line containing `shutdown` to the processes
*stdin* channel.
"""

import time
import sys
from pygase import Server, GameStateStore, GameState
from bossfight.server.game_loop import BFStateMachine

SHARED_GAME_STATE = GameState(npcs=dict(), players=dict())
GAME_STATE_STORE = GameStateStore(SHARED_GAME_STATE)
SERVER = Server(GAME_STATE_STORE)
GAME_STATE_MACHINE = BFStateMachine(GAME_STATE_STORE, SERVER)

SERVER_ADDRESS = None
if len(sys.argv) == 1:
    SERVER_ADDRESS = ("localhost", 0)
elif len(sys.argv) == 2:
    SERVER_ADDRESS = (sys.argv[1], 0)
else:
    SERVER_ADDRESS = (sys.argv[1], int(sys.argv[2]))

GAME_STATE_MACHINE.run_game_loop_in_thread()
SERVER.run_in_thread(SERVER_ADDRESS[1], SERVER_ADDRESS[0], GAME_STATE_MACHINE)
time.sleep(0.1)
print(SERVER.hostname)
print(SERVER.port)
sys.stdout.close()

while not sys.stdin.readline().__contains__("shutdown"):
    pass
SERVER.shutdown()
