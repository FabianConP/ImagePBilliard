# File for testing in base64 coding
# Related files: images/stop.png
#                b10_b64.txt
#                test.py
import base64

jpgtxt = base64.encodestring(open("../images/billiard/b10.jpg","rb").read())

f = open("b10_b64.txt", "w")
f.write(jpgtxt)
f.close()