from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import cv2
import numpy as np
from ocular import ocular
from ocular.glasses import Glasses


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--glasses-type', type=str, default='demo', help='demo|circular|kanye|thin')
    parser.add_argument('--width-factor', type=float, default=1.75, help='width of glass to eye [default: 1.75]')
    args = parser.parse_args()

    # load a set of glasses
    glasses = Glasses()
    glasses.load_pieces_from_directory('img/%s' % args.glasses_type)

    # start video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        faces = ocular.get_facial_keypoints_from_frame(frame)
        for (i, face) in enumerate(faces):
            pieces = glasses.place_glasses(face, width_factor=args.width_factor)
            for piece in pieces.itervalues():
                x, y, w, h = piece['loc']
                alpha_s = piece['data'][:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in xrange(0, 3):
                    # render images as (y, x, h, w) as openCV does 
                    # this means i need to swapaxes
                    try:
                        frame_slice = np.round((alpha_s * piece['data'][:, :, c] + 
                                                alpha_l * frame[y:y+h, x:x+w, c]))
                        frame[y:y+h, x:x+w, c] = frame_slice.astype(np.uint8)
                    except:
                        pass

            for (x, y) in face['keypoints']:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

            (x, y, w, h) = face['bbox']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
