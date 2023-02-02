import pydivert

# Capture only TCP packets to port 80, i.e. HTTP requests.
w = pydivert.WinDivert("tcp.DstPort == 80 and tcp.PayloadLength > 0")

w.open()  # packets will be captured from now on

packet = w.recv()  # read a single packet
print(packet)
w.send(packet)  # re-inject the packet into the network stack

w.close()  