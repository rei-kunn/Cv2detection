import cv2
import numpy as np


class Buttons:
    def __init__(self):
        # Font
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.text_scale = 3
        self.text_thick = 3
        self.x_margin = 20
        self.y_margin = 10

        # Buttons
        self.buttons = {}
        self.button_index = 0
        self.buttons_area = []

        np.random.seed(0)
        self.colors = []
        self.generate_random_colors()

        # Initialize detection state
        self.detection = False

    def generate_random_colors(self):
        for i in range(91):
            random_c = np.random.randint(256, size=3)
            self.colors.append((int(random_c[0]), int(random_c[1]), int(random_c[2])))

    def add_button(self, x, y):
        # Create a Detect/Stop button
        self.buttons['detect'] = {"text": "Detect", "position": [x, y, x+220, y+50], "active": False}

    def display_buttons(self, frame):
        for button_name, button_value in self.buttons.items():
            button_text = button_value["text"]
            (x, y, right_x, bottom_y) = button_value["position"]
            active = button_value["active"]

            if active:
                button_color = (0, 255, 0)
                text_color = (0, 0, 0)
                thickness = -1
            else:
                button_color = (0, 0, 255)
                text_color = (255, 255, 255)
                thickness = -1

            cv2.rectangle(frame, (x, y), (right_x, bottom_y), button_color, thickness)
            cv2.putText(frame, button_text, (x + self.x_margin, y + self.y_margin + 30), self.font, self.text_scale, text_color, self.text_thick)

        return frame

    def button_click(self, mouse_x, mouse_y):
        for button_name, button_value in self.buttons.items():
            (x, y, right_x, bottom_y) = button_value["position"]
            active = button_value["active"]
            area = [(x, y), (right_x, y), (right_x, bottom_y), (x, bottom_y)]

            inside = cv2.pointPolygonTest(np.array(area, np.int32), (int(mouse_x), int(mouse_y)), False)
            if inside > 0:
                if button_name == 'detect':
                    if self.detection:
                        self.buttons[button_name]["text"] = "Detect"
                        self.detection = False
                    else:
                        self.buttons[button_name]["text"] = "Stop"
                        self.detection = True

    def get_detection_status(self):
        return self.detection
