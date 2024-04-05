import os
from .utils import *

class Camera:
    def __init__(self, index=0) -> None:
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.cap = cv2.VideoCapture(index)
        self.frame = None
        self.cropped_mask = None
        self.is_on_finger_recog = False

    def is_opened(self): 
        return self.cap.isOpened()

    def switch_finger_recog(self, new_state: bool):
        self.is_on_finger_recog = new_state
        self.cropped_mask = None

    def read_frame(self): 
        ret, self.frame = self.cap.read()  # BGR
        if self.is_on_finger_recog: self.process_hands()
        return ret, self.frame

    def process_hands(self, frame_rgb=None):
        if frame_rgb is None: 
            frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(frame_rgb)
    
        if results.multi_hand_landmarks:
            index_finger_pos = []
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x = int(index_finger.x * self.frame.shape[1])
                y = int(index_finger.y * self.frame.shape[0])
                index_finger_pos.append((x, y))
            # print(f'hand_num: {len(index_finger_pos)}')
            if len(index_finger_pos) == 2 and \
                    index_finger_pos[0][0] != index_finger_pos[1][0] and index_finger_pos[0][1] != index_finger_pos[1][1]:
                self.cropped_mask = index_finger_pos
                return self.cropped_mask

        self.cropped_mask = None
        return self.cropped_mask
    
    def read_drawn_frame(self):  # just readable
        if self.cropped_mask:
            drawn_frame = draw_on_image(self.frame, self.cropped_mask[0], self.cropped_mask[1])
        else:
            drawn_frame = self.frame
        return drawn_frame
    
    def read_cropped_frame(self):  # just readable
        if self.cropped_mask:
            cropped_image = crop_image_from(self.frame, self.cropped_mask)
        else:
            cropped_image = self.frame
        return cropped_image

    def save_frame_to_local(self) -> str:
        output_path = parameters['save_path']
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, self.read_cropped_frame())
        return parameters['save_path']
    
    def release_cap(self):
        self.cap.release()


if __name__ == '__main__':

    camera = Camera()

    while camera.is_opened():
        ret, _ = camera.read_frame()
        if not ret:
            break
        camera.process_hands()
        cv2.imshow('frame', camera.frame)
        cv2.imshow('drawn frame', camera.read_drawn_frame())
        cv2.imshow('cropped frame', camera.read_cropped_frame())
        if cv2.waitKey(10) & 0xFF == 27:
            break

    camera.release_cap()
    cv2.destroyAllWindows()