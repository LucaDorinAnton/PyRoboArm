import network as nt
import machine
import time
import struct
import usocket

# Create the acces point and set it's name
ap = nt.WLAN(nt.AP_IF)
serversocket = None
n_name = 'ESP-Robot-ARM-1'


# Variables for all the pins and sevos
right = None
rs = None
left = None
ls = None
bottom = None
bs = None
claw = None
cs = None

# Start the acces point
def start_network():
  global ap, n_name
  ap.config(essid=n_name)
  ap.active(True)

# Create pin and servo objects for each servo
def setup_servos():
  global right, rs, left, ls, bottom, bs, claw, cs
  right = machine.Pin(25)
  rs = machine.PWM(right, freq=50)
  left = machine.Pin(33)
  ls = machine.PWM(left,freq=50)
  bottom = machine.Pin(26)
  bs = machine.PWM(bottom, freq=50)
  claw = machine.Pin(32)
  cs = machine.PWM(claw, freq=50)
  # duty for servo is between 30 - 130

# Turn the degree values 0 - 180 into duty cycle
# values (30 - 130)
def transpose(lst):
  res = []
  for i in lst:
    if i < 0:
      i = 0
    if i > 180:
      i = 180
    res.append(int((i/180)*80+ 30))
  return res

# Move the servos to the defined locations
def move(lst):
  goto = transpose(lst)
  rs.duty(goto[0])
  ls.duty(goto[1])
  bs.duty(goto[2])
  cs.duty(goto[3])


# Prepare the network to receive TCP connection requests
# on port 1337
def setup_network():
  global serversocket
  serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
  host = ""
  port = 1337
  serversocket.bind((host, port))
  serversocket.listen(1)

def main():
  setup_servos()
  start_network()
  setup_network()
  while True:
    try:
      # establish a connection
      clientsocket,addr = serversocket.accept()
      print("Got a connection from %s" % str(addr))
      byt = clientsocket.recv(32)
      print(byt)
      # Turn the binary values into integers
      res = struct.unpack("BBBB", byt)
      print(res)
      # close the connection
      clientsocket.close()
      # Move to the specified position
      move(res)
      time.sleep_ms(50)
    except:
      print("I failed!")
      clientsocket.close()
      break


# Run the main Function
main()
