# udpsend
Python tool for sending UDP datagrams through a raw socket in Windows XP SP2 or later.

## Usage

![Image of CMD](https://github.com/0x9dec1980/udpsend/blob/master/img/help.png)

###  Example

Sending a datagram forging local UDP port 0, to 1.2.3.4:567

![Image of CMD](https://github.com/0x9dec1980/udpsend/blob/master/img/cmd.png)

Sent datagram in WireShark:

![Image of captured datagram](https://github.com/0x9dec1980/udpsend/blob/master/img/WireShark.png)

###  Limitations on Raw Sockets introduced by Windows XP SP2
 * Users running applications that use raw sockets must be a member of the Administrators group on the local computer.
 * TCP data cannot be sent over raw sockets.
 * UDP datagrams with an invalid source address cannot be sent over raw sockets. The IP source address for any outgoing UDP datagram must exist on a network interface or the datagram is dropped.  
* A call to the bind function with a raw socket for the IPPROTO_TCP protocol is not allowed. 


#### Warning

This is my first script in Python, good luck x)
