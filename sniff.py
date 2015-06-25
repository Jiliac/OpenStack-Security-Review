#!/usr/bin/python2
from scapy.all import *
import json
from analyze import *

def process(packets):
    packets_to_analyze = []
    packets_to_analyze_index = []
    packet_index = 0
    for packet in packets:
        if Raw in packet:
            packets_to_analyze.append(packet[Raw].load)
            packets_to_analyze_index.append(packet_index)
        packet_index += 1
    strings_to_analyze = [''] * len(packets_to_analyze)
    index = -1
    for load in packets_to_analyze:
        first_char = ord(load[0])
        if first_char < 20 and load.find("json") != -1:
            index += 1
            strings_to_analyze[index] = load
        else:
            string = strings_to_analyze[index]
            string += load
            strings_to_analyze[index] = string
    token = -2
    for load in strings_to_analyze:
        tmp_token = analyze(load)
        if tmp_token > 0:
            token = tmp_token
    if token > 0:
        for packet in packets:
            if Raw in packet:
                str_token = hex(token)[2:len(hex(token))-1]
                token += 1
                str_token_plus = hex(token)[2:len(hex(token))-1]
                packet[Raw].load = packet[Raw].load.replace(str_token, str_token_plus)
    #for packet in packets:
    #    sendp(packet)

#while(True):
#    capture = sniff(iface="bridge0", timeout=0.1)
#    packets = []
#    for packet in capture:
#        if TCP in packet and (packet[TCP].sport == 5672 or packet[TCP].dport == 5672):
#            packets.append(packet)
##        else:
##            sendp(packet)
#    process(packets)

pack = rdpcap('openstack_adduser.cap')
packets = []
for packet in pack:
    if TCP in packet and (packet[TCP].sport == 5672 or packet[TCP].dport == 5672):
        packets.append(packet)
process(packets)
