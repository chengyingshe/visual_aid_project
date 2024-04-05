import cv2
import mediapipe as mp

parameters = {
    'save_path': 'temp/frame.jpg',
}

def draw_on_image(img, point1, point2, point_color=(0, 0, 255), rec_color=(0, 255, 0)):
    drawn_img = img.copy()
    cv2.circle(drawn_img, (point1[0], point1[1]), 5, point_color, -1)
    cv2.circle(drawn_img, (point2[0], point2[1]), 5, point_color, -1)
    cv2.rectangle(drawn_img, point1, point2, rec_color, 2)
    return drawn_img

def crop_image_from(img, crop_mask):
    x1 = min(crop_mask[0][0], crop_mask[1][0])
    x2 = max(crop_mask[0][0], crop_mask[1][0])
    y1 = min(crop_mask[0][1], crop_mask[1][1])
    y2 = max(crop_mask[0][1], crop_mask[1][1])
    return img[y1: y2, x1: x2]
