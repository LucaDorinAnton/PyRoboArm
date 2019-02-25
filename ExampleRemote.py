from machine import Pin
from machine import ADC
import time

from funcs import connect
from funcs import pin_out
from funcs import pin_in
from funcs import pot
from funcs import noralise_vals

n_name = 'ESP-Robot-ARM-x'

out = pin_out(13)
out.on()

lst = []
vals = [0,0,0,0]
d1 = pin_in(34)
u1 = pin_in(35)

d2 = pin_in(32)
u2 = pin_in(33)

d3 = pin_in(25)
u3 = pin_in(26)

d4 = pin_in(27)
u4 = pin_in(14)

first = (d1, u1)

second = (d2, u2)

third = (d3, u3)

fourth = (d4, u4)

lst = [first, second, third, fourth]

def main():
  print("Trying to connect!")
  connect(n_name)
  while True:
    for i in range(4):
      for j in range(2):
        if lst[i][j].value() == 1:
          if j== 1:
            vals[i] += 1
          else:
            vals[i] -= 1
    vals = normalise_vals(vals)
    print(vals)
    send_cmd(vals)
    time.sleep_ms(50)

main()
