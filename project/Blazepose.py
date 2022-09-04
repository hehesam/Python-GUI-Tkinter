# while 1 :
#     print("hi")
import time

import cv2
import tensorflow as tf
import numpy as np
import mediapipe_utils as mpu
from FPS import FPS
import redis

POSE_DETECTION_MODEL = 'models/pose_detection.tflite'
LANDMARK_MODEL_FULL = 'models/pose_landmark_full.tflite'
LANDMARK_MODEL_LITE = 'models/pose_landmark_lite.tflite'
LANDMARK_MODEL_HEAVY = 'models/pose_landmark_heavy.tflite'

# LINES_*_BODY are used when drawing the skeleton onto the source image.
# Each variable is a list of continuous lines.
# Each line is a list of keypoints as defined at https://google.github.io/mediapipe/solutions/pose.html#pose-landmark-model-blazepose-ghum-3d
LINES_FULL_BODY = [[28,30,32,28,26,24,12,11,23,25,27,29,31,27],
                    [23,24],
                    [22,16,18,20,16,14,12],
                    [21,15,17,19,15,13,11],
                    [8,6,5,4,0,1,2,3,7],
                    [10,9],
                    ]

class Blazepose:
    def __init__(self,
                 pd_tflite=POSE_DETECTION_MODEL,
                 pd_score_thresh=0.5,
                 lm_tflite=LANDMARK_MODEL_FULL,
                 lm_score_thresh=0.5,
                 show_landmarks=True,
                 show_fps=True):

        self.pd_score_thresh = pd_score_thresh
        self.lm_score_thresh = lm_score_thresh

        # Rendering flags
        self.show_landmarks = show_landmarks
        self.show_fps = show_fps

        # The full body landmark model predict 39 landmarks.
        # We are interested in the first 35 landmarks
        # from 1 to 33 correspond to the well documented body parts,
        # 34th (mid hips) and 35th (a point above the head) are used to predict ROI of next frame
        self.nb_lms = 35

        filter_window_size=5
        filter_velocity_scale=10
        self.filter = mpu.LandmarksSmoothingFilter(filter_window_size, filter_velocity_scale, (self.nb_lms-2, 3))

        # Load tflite models
        self.load_models(pd_model_path=pd_tflite, lm_model_path=lm_tflite)

        # Create SSD anchors
        # https://github.com/google/mediapipe/blob/master/mediapipe/modules/pose_detection/pose_detection_cpu.pbtxt

        anchor_options = mpu.SSDAnchorOptions(
                                num_layers=5,
                                min_scale=0.1484375,
                                max_scale=0.75,
                                input_size_height=224,
                                input_size_width=224,
                                anchor_offset_x=0.5,
                                anchor_offset_y=0.5,
                                strides=[8, 16, 32, 32, 32],
                                aspect_ratios= [1.0],
                                reduce_boxes_in_lowest_layer=False,
                                interpolated_scale_aspect_ratio=1.0,
                                fixed_anchor_size=True)

        self.anchors = mpu.generate_anchors(anchor_options)

        self.red = redis.Redis(host='localhost', port=6379)

    def load_models(self, pd_model_path, lm_model_path):

        # Pose detection model
        # Input blob: input_1 - shape: [1, 224, 224, 3] ---> [0]
        # Output blob: Identity - shape: [1, 2254, 12] ---> [0]
        # Output blob: Identity_1 - shape: [1, 2254, 1] --->[1]

        print("Loading pose detection model")
        self.pd_interpreter = tf.lite.Interpreter(model_path=pd_model_path)
        self.pd_interpreter.allocate_tensors()

        self.pd_input_details = self.pd_interpreter.get_input_details()
        self.pd_output_details = self.pd_interpreter.get_output_details()

        _,self.pd_h,self.pd_w,_ = self.pd_input_details[0]['shape']
        self.pd_scores = 1
        self.pd_bboxes = 0

        # Landmarks model
        # Input blob: input_1 - shape: [1, 256, 256, 3] ---> [0]
        # Output blob: ld_3d - shape: [1, 195] --->[0]
        # Output blob: output_poseflag - shape: [1, 1] --->[1]

        print("Loading landmark model")
        self.lm_interpreter = tf.lite.Interpreter(model_path=lm_model_path)
        self.lm_interpreter.allocate_tensors()

        self.lm_input_details = self.lm_interpreter.get_input_details()
        self.lm_output_details = self.lm_interpreter.get_output_details()

        _,self.lm_h,self.lm_w,_ = self.lm_input_details[0]['shape']
        self.lm_score = 1
        self.lm_landmarks = 0

    def pd_postprocess(self, interpreter):
        scores = np.squeeze(interpreter.get_tensor(self.pd_output_details[self.pd_scores]['index']))  # 2254
        bboxes = interpreter.get_tensor(self.pd_output_details[self.pd_bboxes]['index'])[0] # 2254x12
        # Decode bboxes
        self.regions = mpu.decode_bboxes(self.pd_score_thresh, scores, bboxes, self.anchors, best_only=True)

        mpu.detections_to_rect(self.regions, kp_pair=[0,1])
        mpu.rect_transformation(self.regions, self.frame_size, self.frame_size)

    def lm_postprocess(self, region, interpreter):
        region.lm_score = np.squeeze(interpreter.get_tensor(self.lm_output_details[self.lm_score]['index']))
        if region.lm_score > self.lm_score_thresh:

            lm_raw = interpreter.get_tensor(self.lm_output_details[self.lm_landmarks]['index']).reshape(-1,5)
            # Each keypoint have 5 information:
            # - X,Y coordinates are local to the region of
            # interest and range from [0.0, 255.0].
            # - Z coordinate is measured in "image pixels" like
            # the X and Y coordinates and represents the
            # distance relative to the plane of the subject's
            # hips, which is the origin of the Z axis. Negative
            # values are between the hips and the camera;
            # positive values are behind the hips. Z coordinate
            # scale is similar with X, Y scales but has different
            # nature as obtained not via human annotation, by
            # fitting synthetic data (GHUM model) to the 2D
            # annotation.
            # - Visibility, after user-applied sigmoid denotes the
            # probability that a keypoint is located within the
            # frame and not occluded by another bigger body
            # part or another object.
            # - Presence, after user-applied sigmoid denotes the
            # probability that a keypoint is located within the
            # frame.

            # Normalize x,y,z. Here self.lm_w = self.lm_h and scaling in z = scaling in x = 1/self.lm_w
            lm_raw[:,:3] /= self.lm_w
            # Apply sigmoid on visibility and presence (if used later)
            # lm_raw[:,3:5] = 1 / (1 + np.exp(-lm_raw[:,3:5]))

            # region.landmarks contains the landmarks normalized 3D coordinates in the relative oriented body bounding box
            region.landmarks = lm_raw[:,:3]
            # Calculate the landmark coordinate in square padded image (region.landmarks_padded)
            src = np.array([(0, 0), (1, 0), (1, 1)], dtype=np.float32)
            dst = np.array([ (x, y) for x,y in region.rect_points[1:]], dtype=np.float32) # region.rect_points[0] is left bottom point and points going clockwise!
            mat = cv2.getAffineTransform(src, dst)
            lm_xy = np.expand_dims(region.landmarks[:self.nb_lms,:2], axis=0)
            lm_xy = np.squeeze(cv2.transform(lm_xy, mat))
            # A segment of length 1 in the coordinates system of body bounding box takes region.rect_w_a pixels in the
            # original image. Then I arbitrarily divide by 4 for a more realistic appearance.
            lm_z = region.landmarks[:self.nb_lms,2:3] * region.rect_w_a / 4
            lm_xyz = np.hstack((lm_xy, lm_z))
            lm_xyz = self.filter.apply(lm_xyz)
            region.landmarks_padded = lm_xyz.astype(int)
            # If we added padding to make the image square, we need to remove this padding from landmark coordinates
            # region.landmarks_abs contains absolute landmark coordinates in the original image (padding removed))
            region.landmarks_abs = region.landmarks_padded.copy()
            if self.pad_h > 0:
                region.landmarks_abs[:,1] -= self.pad_h
            if self.pad_w > 0:
                region.landmarks_abs[:,0] -= self.pad_w

    def lm_render(self, frame, region):
        if region.lm_score > self.lm_score_thresh:

            if self.show_landmarks:
                list_connections = LINES_FULL_BODY
                lines = [np.array([region.landmarks_padded[point,:2] for point in line]) for line in list_connections]
                cv2.polylines(frame, lines, False, (255, 180, 90), 2, cv2.LINE_AA)

                for i,x_y in enumerate(region.landmarks_padded[:self.nb_lms-2,:2]):
                    cv2.circle(frame, (x_y[0], x_y[1]), 4, (0,0,255), -11)

            points = region.landmarks_abs

            point_str = ''
            for i in points:
                for j in i:
                    point_str = point_str + ' ' + str(j)

            self.red.set('key_points', point_str[1:])

    def run(self):

        dispW = 640
        dispH = 480
        flip = 2

        #camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink drop=1'
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

        h = dispH
        w = dispW
        # Padding on the small side to get a square shape
        self.frame_size = max(h, w)
        self.pad_h = int((self.frame_size - h)/2)
        self.pad_w = int((self.frame_size - w)/2)

        self.fps = FPS()

        get_new_frame = True
        use_previous_landmarks = False

        while True:

            if get_new_frame:

                ok, vid_frame = cap.read()
                if not ok:
                    break

                video_frame = cv2.copyMakeBorder(vid_frame, self.pad_h, self.pad_h, self.pad_w, self.pad_w, cv2.BORDER_CONSTANT)
                annotated_frame = video_frame.copy()

            if use_previous_landmarks:
                self.regions = regions_from_landmarks
                mpu.detections_to_rect(self.regions, kp_pair=[0,1]) # self.regions.pd_kps are initialized from landmarks on previous frame
                mpu.rect_transformation(self.regions, self.frame_size, self.frame_size)
            else:
                # Infer pose detection
                # Resize image to NN square input shape
                frame_nn = cv2.resize(video_frame, (self.pd_w, self.pd_h), interpolation=cv2.INTER_AREA)
                # Transpose hxwx3 -> 1xhxwx3
                frame_nn = frame_nn[None,]
                frame_nn = tf.cast(frame_nn, dtype=tf.float32) / 255.0

                self.pd_interpreter.set_tensor(self.pd_input_details[0]['index'], np.array(frame_nn))
                self.pd_interpreter.invoke()
                self.pd_postprocess(self.pd_interpreter)

            # Landmarks
            self.nb_active_regions = 0
            if len(self.regions) == 1:
                r = self.regions[0]
                frame_nn = mpu.warp_rect_img(r.rect_points, video_frame, self.lm_w, self.lm_h)
                 # Transpose hxwx3 -> 1xhxwx3
                frame_nn = frame_nn[None,]
                frame_nn = tf.cast(frame_nn, dtype=tf.float32) / 255.0

                # Get landmarks
                self.lm_interpreter.set_tensor(self.lm_input_details[0]['index'], np.array(frame_nn))
                self.lm_interpreter.invoke()
                self.lm_postprocess(r, self.lm_interpreter)

                if get_new_frame:
                    if not use_previous_landmarks:
                        # With a new frame, we have run the landmark NN on a ROI found by the detection NN...
                        if r.lm_score > self.lm_score_thresh:
                            # ...and succesfully found a body and its landmarks
                            # Predict the ROI for the next frame from the last 2 landmarks normalized coordinates (x,y)
                            regions_from_landmarks = [mpu.Region(pd_kps=r.landmarks_padded[self.nb_lms-2:self.nb_lms,:2]/self.frame_size)]
                            use_previous_landmarks = True
                    else :
                        # With a new frame, we have run the landmark NN on a ROI calculated from the landmarks of the previous frame...
                        if r.lm_score > self.lm_score_thresh:
                            # ...and succesfully found a body and its landmarks
                            # Predict the ROI for the next frame from the last 2 landmarks normalized coordinates (x,y)
                            regions_from_landmarks = [mpu.Region(pd_kps=r.landmarks_padded[self.nb_lms-2:self.nb_lms,:2]/self.frame_size)]
                            use_previous_landmarks = True
                        else:
                            # ...and could not find a body
                            # We don't know if it is because the ROI calculated from the previous frame is not reliable (the body moved)
                            # or because there is really no body in the frame. To decide, we have to run the detection NN on this frame
                            get_new_frame = False
                            use_previous_landmarks = False
                            continue
                else:
                    # On a frame on which we already ran the landmark NN without founding a body,
                    # we have run the detection NN...
                    if r.lm_score > self.lm_score_thresh:
                        # ...and succesfully found a body and its landmarks
                        use_previous_landmarks = True
                        # Predict the ROI for the next frame from the last 2 landmarks normalized coordinates (x,y)
                        regions_from_landmarks = [mpu.Region(pd_kps=r.landmarks_padded[self.nb_lms-2:self.nb_lms,:2]/self.frame_size)]
                        use_previous_landmarks = True
                    # else:
                        # ...and could not find a body
                        # We are sure there is no body in that frame

                    get_new_frame = True

                self.lm_render(annotated_frame, r)

            else:
                # Detection NN hasn't found any body
                get_new_frame = True

            self.fps.update()

            self.filter.reset()

            if self.show_fps:
                self.fps.draw(annotated_frame, orig=(50,50), size=1, color=(0,0,255))
            # cv2.imshow("Blazepose", annotated_frame)

#---------------------------------------------------------------------------------------------------------------------------------------------
            r = redis.Redis(host='localhost', port=6379)
            data = cv2.imencode('.jpg', annotated_frame)[1].tostring()
            r.set('pose_frame', data)
            # print("snap", r.get("stop pose process"))
            if int(r.get("stop pose process")) == 1:
                # r.set('pose_frame', 'stop')
                break

#---------------------------------------------------------------------------------------------------------------------------------------------


            key = cv2.waitKey(1)
            if key == ord('q') or key == 27:
                break
            elif key == 32:
                # Pause on space bar
                cv2.waitKey(0)

BP = Blazepose()

BP.run()
