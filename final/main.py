import pyb
import math
import sensor
import image
import time

enable_lens_corr = False  # turn on for straighter lines...
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

uart = pyb.UART(3, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)

f_x = (2.8 / 3.984) * 160  # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120  # find_apriltags defaults to this if not set
c_x = 160 * 0.5  # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5  # find_apriltags defaults to this if not set (the image.h * 0.5)

flag = 1

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr:
        img.lens_corr(1.8)  # for 2.8mm lens...
    '''uart.write("/goStraight/run -30 \n".encode())
    time.sleep(2)
    uart.write("/stop/run \n".encode())
    time.sleep(1)
    uart.write("/turn/run -30 0.01 \n".encode())
    time.sleep(0.7)
    uart.write("/stop/run \n".encode())
    time.sleep(1)
    uart.write("/turn/run -30 -0.01 \n".encode())
    time.sleep(0.7)
    uart.write("/stop/run \n".encode())
    time.sleep(1)'''
    # `merge_distance` controls the merging of nearby lines. At 0 (the default), no
    # merging is done. At 1, any line 1 pixel away from another is merged... and so
    # on as you increase this value. You may wish to merge lines as line segment
    # detection produces a lot of line segment results.

    # `max_theta_diff` controls the maximum amount of rotation difference between
    # any two lines about to be merged. The default setting allows for 15 degrees.

    for l in img.find_line_segments(merge_distance=0, max_theta_diff=5):
        # region = l[0] > 70 and l[0] < 130 and l[2] > 70 and l[2] < 130 and (l[1] < 40 or l[3] < 40) and (l[6] < 20 or l[6] > 160)
        if l.magnitude() > 21 and (l.y1() < 40 and l.y2() < 40) and flag:
            #uart.write(("x1 %d\r\n" % l.x1()).encode())
            #uart.write(("x2 %d\r\n" % l.x2()).encode())
            #uart.write(("y1 %d\r\n" % l.y1()).encode())
            #uart.write(("y2 %d\r\n" % l.y2()).encode())
          # img.draw_line(l.line(), color = (255, 0, 0))
            # uart.write(("theta %d\r\n" % l.theta()).encode())
            if l[6] < 10 or l[6] > 170:
                uart.write("/goStraight/run -30 \n".encode())
                time.sleep(0.3)
            elif l[6] > 10 and l[6] < 90:
                uart.write("/turn/run -30 0.01 \n".encode())
            elif l[6] < 170 and l[6] > 90:
                uart.write("/turn/run -30 -0.01 \n".encode())
            time.sleep(0.3)
            uart.write("/stop/run \n".encode())
            #time.sleep(0.2)
    # uart.write(("FPShaha %f\r\n" % clock.fps()).encode())
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y):
        uart.write(("%d\n" %tag.id()).encode())
        uart.write("/stop/run \n".encode())
        uart.write("\n".encode())
        flag = 0




