import redis
import time
import cv2
import numpy as np
r = redis.Redis(host='localhost', port=6379)


vid = cv2.VideoCapture(0)

while True:
    if vid.isOpened():
        empty, frame = vid.read()
        data = cv2.imencode('.jpg', frame)[1].tostring()
        r.set('pose_frame', data)
        # Intermediary socket stuffs
        # data = r.get('pose_frame')
        # nparr = np.fromstring(data, np.uint8)
        # newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow("s", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()

r.set('pose_frame', 'stop')


