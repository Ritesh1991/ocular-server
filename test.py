from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import cv2
import numpy as np
from ocular import ocular
from ocular.glasses import Glasses


if __name__ == "__main__":
    # load a dummy set of glasses
    dummy = Glasses()
    dummy.load_pieces_from_directory('img/dummy')

    # start video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        faces = ocular.get_facial_keypoints_from_frame(frame)
        for (i, face) in enumerate(faces):
            pieces = dummy.place_glasses(face)
            for piece in pieces.itervalues():
                x, y, h, w = piece['loc']
                alpha_s = piece['data'][:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in xrange(0, 3):
                    frame_slice = np.round((alpha_s * piece['data'][:, :, c] + 
                                            alpha_l * frame[x:x+h, y:y+w, c]))
                    frame[x:x+h, y:y+w, c] = frame_slice.astype(np.uint8)

                for (x, y) in face['keypoints']:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()