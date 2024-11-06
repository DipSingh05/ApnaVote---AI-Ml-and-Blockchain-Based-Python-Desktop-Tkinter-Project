import cv2
import numpy as np
from mtcnn import MTCNN
import time

class HeadMovementVerification:
    def __init__(self, frame_width=320, frame_height=280):
        # Initialize video capture and detector
        self.cap = cv2.VideoCapture(0)
        self.detector = MTCNN(device="GPU:0")
        
        # Frame and box dimensions
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.box_w, self.box_h = self.frame_width // 2, self.frame_height // 2
        
        # Reference landmarks, flag, and fraud detection status
        self.reference_landmarks = None
        self.reference_set = False
        self.start_reference = False
        self.fraud_detection_active = False
        self.fraud_count = 0
        self.reference_timestamp = None  # To store time when reference is set

        # Checkpoints for head movement directions
        self.checkpoints = {
            "Head Up": False,
            "Head Down": False,
            "Head Left": False,
            "Head Right": False
        }

    def calculate_movement_direction(self, landmarks):
        movements = {"up": False, "down": False, "left": False, "right": False}
        ref_nose_tip = self.reference_landmarks[0]
        nose_tip = landmarks[0]

        # Define thresholds
        vertical_threshold = 10
        horizontal_threshold = 10

        # Movement detection
        if nose_tip[1] < ref_nose_tip[1] - vertical_threshold:
            movements["up"] = True
        elif nose_tip[1] > ref_nose_tip[1] + vertical_threshold:
            movements["down"] = True
        if nose_tip[0] < ref_nose_tip[0] - horizontal_threshold:
            movements["left"] = True
        elif nose_tip[0] > ref_nose_tip[0] + horizontal_threshold:
            movements["right"] = True

        return movements

    def update_frame(self, frame, is_start: bool):
        # Flip and resize frame
        frame = cv2.resize(frame, (self.frame_width, self.frame_height))
        frame = cv2.flip(frame, 1)
        self.start_reference = is_start

        try:
            results = self.detector.detect_faces(frame)
            movement_text = ""
            color = (0, 255, 0)

            for idx, result in enumerate(results):
                keypoints = result['keypoints']
                landmarks = np.array([
                    keypoints['nose'],
                    keypoints['left_eye'],
                    keypoints['right_eye'],
                    keypoints['mouth_left'],
                    keypoints['mouth_right']
                ])

                # Start reference if instructed
                if self.start_reference and not self.reference_set and idx == 0:
                    self.reference_landmarks = landmarks
                    self.reference_set = True
                    self.start_reference = False
                    self.reference_timestamp = time.time()  # Store the timestamp
                    movement_text = "Reference Set - Keep Head Aligned"
                    color = (255, 255, 0)
                    continue

                # Check if 2 seconds have passed before activating fraud detection
                if idx == 0 and self.reference_set and not self.fraud_detection_active:
                    if time.time() - self.reference_timestamp >= 5:  # 2-second delay
                        self.fraud_detection_active = True

                if idx == 0 and self.reference_set and self.fraud_detection_active:
                    movements = self.calculate_movement_direction(landmarks)

                    if all(self.checkpoints.values()):
                        color = (255, 0, 0)
                        if any(movements.values()):
                            color = (0, 0, 255)
                            movement_text = "Fraud Detected"
                            self.fraud_count += 1
                        else:
                            movement_text = "Head Aligned"
                    else:
                        color = (0, 255, 0)

                    if movements["up"]:
                        self.checkpoints["Head Up"] = True
                        movement_text = "Head Up"
                    elif movements["down"]:
                        self.checkpoints["Head Down"] = True
                        movement_text = "Head Down"
                    elif movements["left"]:
                        self.checkpoints["Head Left"] = True
                        movement_text = "Head Left"
                    elif movements["right"]:
                        self.checkpoints["Head Right"] = True
                        movement_text = "Head Right"

                x, y, width, height = result['box']
                if idx == 0:
                    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
                else:
                    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
                    cv2.putText(frame, "Intruder", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        except Exception as e:
            if self.fraud_detection_active:
                movement_text = "Fraud Detected: Error"
                color = (0, 0, 255)
                self.fraud_count += 1

        # self.display_info(frame, movement_text, color)
        return frame, self.fraud_count, self.checkpoints  # Return fraud count and checkpoints status

    # def display_info(self, frame, movement_text, color):
    #     #Display movement direction and fraud count
    #     cv2.putText(frame, movement_text, (10, self.frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    #     cv2.putText(frame, f"Fraud Count: {self.fraud_count}", (10, self.frame_height - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #     for i, (checkpoint, status) in enumerate(self.checkpoints.items()):
    #         check_color = (0, 255, 0) if status else (0, 0, 255)
    #         cv2.putText(frame, f"{checkpoint}: {'Checked' if status else 'Unchecked'}", (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, check_color, 1)

    def get_frame(self, start_res: bool):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame, fraud_count, checkpoints = self.update_frame(frame, start_res)  # Process the frame and get fraud count, checkpoints
        return frame, fraud_count, checkpoints  # Return the processed frame along with fraud count and checkpoint status

# Usage
if __name__ == "__main__":
    pass
    # head_movement_verification = HeadMovementVerification()
    # head_movement_verification.start_reference = True  # Start reference manually
