# negative number -> clock is faster than real time
# positive number -> clock is slower than real time
# time given in milliseconds
# time server: time.cloudflare.com

DEVICE_TIME_OFFSET = {
    "1": -468,
    "2": -3570,
    "3": -1929,
    "4": -37,
    "5": 209,
    "6": -3050,
    "7": 663,
    "8": -3343,
    "9": -976,
}
#
# !Cam is connected with personal phone and it also create some delay (set aproxymately to 1 sec)
CAM_PHONE_DELAY = 1000
PHONE_OFFSET = 680
CAM_OFFSET = CAM_PHONE_DELAY + PHONE_OFFSET
# ? need to be modified every time?
