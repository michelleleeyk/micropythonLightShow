from machine import Pin
from neopixel import NeoPixel
import time

np = NeoPixel(Pin(4), 8)

def demo(np):
    n = np.n

    while True:
        # cycle - 1 coloured pixel moving only
        for i in range(4 * n):

            # set all pixels to be blank (no colour)
            for j in range(n):
                np[j] = (0, 0, 0)

            # let each position take turns to be coloured
            # eg (1 % 8 = 1) --> (2 % 8 = 2) --> ...
            np[i % n] = (255, 255, 255)
            np.write()

            # defines how fast the effect is
            time.sleep_ms(25)

        # bounce - 1 blank pixel moving among coloured pixels
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 128)
            if (i // n) % 2 == 0:
                np[i % n] = (0, 0, 0)
            else:
                np[n - 1 - (i % n)] = (0, 0, 0)
            np.write()
            time.sleep_ms(60)

        # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                np[j] = (val, 0, 0)
            np.write()

        # rainbow cycle - distribute the rainbow across the LEDs.
        for j in range(255):
            for i in range(n):
                rc_index = (i * 256 // n) + j
                np[i] = wheel(rc_index & 255)
            np.write()
            time.sleep_ms(4)

        # clear
        for i in range(n):
            np[i] = (0, 0, 0)
        np.write()

# generates the rainbow spectrum
# by varying each colour parameter between 0 - 255
def wheel(pos):
  # The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)