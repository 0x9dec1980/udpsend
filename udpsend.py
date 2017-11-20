"""
	udpsend
	
	Copyright (C) 2017  0x9dec1980 0x9dec1980@gmail.com

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import socket
import sys
import argparse
from random import randint

def hexdump(src, length=8):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(['%0*X' % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b'%04X   %-*s   %s' % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)

def send_raw_udp(remote_ip, remote_port, local_port, data, silent):
    try:
        remote_address = (remote_ip, remote_port)
        local_ip = "0.0.0.0" 
        # open raw socket
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        s.bind((local_ip, local_port))
        s.connect(remote_address)
        # add the local port (source port) to the UDP header
        packet = '%0*X' % (4, local_port)
        # add the remote port (dest port) to the UDP header
        packet += '%0*X' % (4, remote_port)
        # add the length field of UDP header
        raw_data = ''.join(x.encode('hex') for x in data)
        length = len(raw_data) / 2 + 8
        packet += '%0*X' % (4,length)
        # add a fake UDP checksum field with zeros
        checksum = 0;
        packet += '%0*X' % (4,checksum)
        # add the data of the datagram
        packet += raw_data
        # print info
        if silent == False:
            print ' '       
            print 'Sending UDP datagram %s:%s -> %s:%s' %(local_ip, local_port, remote_ip, remote_port)
            print ' '                   
            print hexdump(packet.decode('hex'), 8)
        # send the datagram         
        s.send(packet.decode('hex'))
    except socket.error as msg:
        print 'Caught exception socket.error : %s' % msg

def main():
    parser = argparse.ArgumentParser(description='Sends UDP datagrams through a raw socket in Windows XPSP2 or later')
    
    parser.add_argument('-rp', '--remote-port', dest='remotePort', type=int, help='Destination UDP port (remote port)', metavar='port')
    parser.add_argument('-lp', '--local-port', dest='localPort', type=int, help='Source UDP port (local port)', metavar='port')
    parser.add_argument('-n', dest='count', default=1, type=int, help='Number of datagrams to send', metavar='count')
    parser.add_argument('-s', '--silent', action='store_true', dest='silent', default=False, help='Silent mode, do not print datagrams')       
    parser.add_argument('-m', '--message', dest='msg',  help='Send non-default message', metavar='msg') 
    parser.add_argument(dest='remoteIp', help='Reachable destination address (remote IPv4)',  metavar='address')

    args = parser.parse_args()

    for i in range(args.count):
            # use random UDP ports unless user wants specific ports
            remote_ip = args.remoteIp           
            remote_port = args.remotePort if (args.remotePort != None) else randint(0, 0xFFFF)
            local_port = args.localPort if (args.localPort != None) else randint(0, 0xFFFF)
            silent = args.silent
            data = args.msg if (args.msg != None) else 'HELLO, THIS IS AN UDP DATAGRAM SENT THROUGH A RAW SOCKET IN WINDOWS'
            send_raw_udp(remote_ip, remote_port, local_port, data, silent)

if __name__ == '__main__':
    main()      