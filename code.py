import time
import board
import digitalio
import analogio
import pwmio
import audiomp3
import audiopwmio
import neopixel
from rainbowio import colorwheel
from adafruit_motor import servo

YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 40, 0)
CYAN = (0, 250, 250)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
GREY = (30, 30, 30)
WHITE = (250, 250, 250) # better not to use
TEAL = (0, 255, 120)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
BLACK = (0, 0, 0) # black or off
GOLD = (255, 222, 30)
PINK = (242, 90, 255)
AQUA = (50, 255, 255)
JADE = (0, 255, 40)
AMBER = (255, 100, 0)
RED = (255,  0,  0)
RED2 = (200,  0,  0)
RED3 = (150,  0,  0)
RED4 = (100,  0,  0)
RED5 = (30,  0,  0)

num_pixels = 1
pixels_pin = board.GP2
pixels_color = [BLACK, BLACK, BLACK]
pixels_speed = [10 for i in pixels_color] # up to 255
if len(pixels_color) < num_pixels:
    for i in range (num_pixels - len(pixels_color)):
        pixels_color.append(GREY)

pixels = neopixel.NeoPixel(pixels_pin, num_pixels, auto_write=False)
pixels.brightness = 1
# Audio setup
audio = audiopwmio.PWMAudioOut(board.GP0)
# Servo setup
pwm_servo = pwmio.PWMOut(board.GP3, duty_cycle=2 ** 15, frequency=50)
servo1 = servo.Servo(
    pwm_servo, min_pulse=750, max_pulse=2250
)  # tune pulse for specific servo
crt_angle = 80
tgt_angle = 80
srv_speed = 0.1

# 레인보우 효과
def rainbow(speed):
    ebreak = False
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(pixel_index & 255)
            pixels.show()
            time.sleep(speed)

def pixeltarget(index):
    tgt_color = []
    speed = pixels_speed[index]
    for i in range(3):
        if pixels[index][i] > pixels_color[index][i]:
            tgt_color.append(max(pixels[index][i] - speed ,pixels_color[index][i]))
        elif pixels[index][i] < pixels_color[index][i]:
            #pixels[index][i] = max(pixels_color[index][i] - (abs(pixels[index][i] - pixels_color[index][i]))*speed//255 , pixels_color[index][i])
            tgt_color.append(min(pixels[index][i] + speed , pixels_color[index][i]))
        else:
            tgt_color.append(pixels_color[index][i])
    #print(index, tgt_color)
    pixels[index] = tgt_color

def playbgm(mp3file):
    mp3 = open(mp3file, "rb")
    decoder = audiomp3.MP3Decoder(mp3)
    if not audio.playing:
        audio.play(decoder)

def servo_easyout():
    global tgt_angle, crt_angle, srv_speed
    crt_angle += (tgt_angle - crt_angle) * srv_speed
    servo1.angle = crt_angle


# Servo smooth test
def servo_smooth_test():
    print("servo smooth test: 180 - 0, -1º steps")
    for angle in range(170, 10, -1):  # 180 - 0 degrees, -1º at a time.
        servo1.angle = angle
        time.sleep(0.02)
    time.sleep(1)
    print("servo smooth test: 0 - 180, 1º steps")
    for angle in range(10, 170, 1):  # 0 - 180 degrees, 1º at a time.
        servo1.angle = angle
        time.sleep(0.02)
    time.sleep(1)

# "led",인덱스,목표밝기, 전환속도(1000), 지연시간
# "mp3",파일명,지연시간
intro = [
    ['mp3','Standby.mp3',0],
    ['led', 0, 65535,40,1],
    ]

anms = [
    ['servo',90,0.1,0],
    ['led', 0, BLACK,1,3],
    ['mp3','zaku01.mp3',0],
    ['led', 0, AMBER,20,0.2],
    ['led', 0, RED5,1,2.5],
    ['servo',140,0.05,0],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['servo',40,0.05,0],
    ['led', 0, RED,8,0.5],
    ['mp3','engine02.mp3',0],
    ['led', 0, BLACK,50,0.2],
    ['servo',10,0.2,0],
    ['led', 0, RED5,2,1.5],
    ['servo',40,0.5,0],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],#10초
    ['servo',120,0.2,0],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['servo',70,0.3,0],

    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
   ['servo',160,0.1,0],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],#20초

    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],
    ['led', 0, RED,8,0.5],
    ['led', 0, RED5,2,1.5],#30초
    ['led', 0, RED,8,0.5],
    ['led', 0, BLACK,1,0],
    ]

last_move = time.monotonic()
anm_num = 0
anm_wait = 0
introloop = False
#while introloop:
#    if time.monotonic() - last_move > anm_wait:
#        if intro[anm_num][0] == "led":
#            leds_brightness[intro[anm_num][1]] = intro[anm_num][2]
#            leds_speed[intro[anm_num][1]] = intro[anm_num][3]
#            anm_wait = intro[anm_num][4]
#        elif intro[anm_num][0] == "mp3":
#            playbgm(intro[anm_num][1])
#            anm_wait = intro[anm_num][2]
#        last_move = time.monotonic()
#        if anm_num < len(intro)-1 :
#            anm_num = anm_num+1
#        else:
#            anm_num = 0
#            anm_wait = 0
#            introloop = False
#    for j, led in enumerate(leds):
#        pixeltarget(j)
#    time.sleep(0.01)
# main loop

while True:
#    if not button.value:
#        if not audio.playing:
#            playbgm(mp3files[0])
    if time.monotonic() - last_move > anm_wait:
        if anms[anm_num][0] == "led":
            pixels_color[anms[anm_num][1]] = anms[anm_num][2]
            pixels_speed[anms[anm_num][1]] = anms[anm_num][3]
            anm_wait = anms[anm_num][4]
        elif anms[anm_num][0] == "mp3":
            playbgm(anms[anm_num][1])
            anm_wait = anms[anm_num][2]
        elif anms[anm_num][0] == "servo":
            tgt_angle = anms[anm_num][1]
            srv_speed = anms[anm_num][2]
            anm_wait = anms[anm_num][3]
        last_move = time.monotonic()
        anm_num = anm_num+1 if anm_num < len(anms)-1 else 0
    servo_easyout()
    #print (crt_angle,tgt_angle)
    for j in range(num_pixels):
        pixeltarget(j)
    #print(pixels_color[2])
    pixels.show()

    time.sleep(0.01)
