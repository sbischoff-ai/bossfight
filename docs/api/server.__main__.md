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