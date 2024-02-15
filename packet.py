import socket
import struct
import textwrap

def main():
    # Create a raw socket and bind it to the network interface
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    try:
        while True:
            raw_data, addr = conn.recvfrom(65536)
            dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
            print('\nEthernet Frame:')
            print(f'Destination: {dest_mac}, Source: {src_mac}, Protocol: {eth_proto}')

            # IP packets
            if eth_proto == 8:
                version, header_length, ttl, proto, src, target, data = ipv4_packet(data)
                print(f'IPv4 Packet:')
                print(f'  Version: {version}, Header Length: {header_length}, TTL: {ttl}')
                print(f'  Protocol: {proto}, Source: {src}, Target: {target}')

                # ICMP
                if proto == 1:
                    icmp_type, code, checksum, data = icmp_packet(data)
                    print('ICMP Packet:')
                    print(f'  Type: {icmp_type}, Code: {code}, Checksum: {checksum}')
                    print(f'  Data:')
                    print(format_multi_line('\t', data))

                # TCP
                elif proto == 6:
                    src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = tcp_packet(data)
                    print('TCP Segment:')
                    print(f'  Source Port: {src_port}, Destination Port: {dest_port}')
                    print(f'  Sequence: {sequence}, Acknowledgment: {acknowledgment}')
                    print('  Flags:')
                    print(f'    Urgent: {flag_urg}, Acknowledgment: {flag_ack}, Push: {flag_psh}, Reset: {flag_rst}, Syn: {flag_syn}, Fin: {flag_fin}')
                    print(f'  Data:')
                    print(format_multi_line('\t', data))

                # UDP
                elif proto == 17:
                    src_port, dest_port, length, data = udp_packet(data)
                    print('UDP Segment:')
                    print(f'  Source Port: {src_port}, Destination Port: {dest_port}, Length: {length}')
                    print(f'  Data:')
                    print(format_multi_line('\t', data))

                # Other IPv4
                else:
                    print('Other IPv4 Data:')
                    print(format_multi_line('\t', data))

            else:
                print('Non-IPv4 Ethernet Frame:')
                print(format_multi_line('\t', data))

    except KeyboardInterrupt:
        print('Packet sniffing stopped.')

# Unpack Ethernet frame
def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.ntohs(proto), data[14:]

# Return properly formatted MAC address (AA:BB:CC:DD:EE:FF)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

# Unpack IPv4 packet
def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

# Returns properly formatted IPv4 address (192.168.1.1)
def ipv4(addr):
    return '.'.join(map(str, addr))

# Unpack ICMP packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]

# Unpack TCP segment
def tcp_packet(data):
    src_port, dest_port, sequence, acknowledgment, offset_reserved_flags = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    return src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

# Unpack UDP segment
def udp_packet(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, size, data[8:]

# Format multi-line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

main()
