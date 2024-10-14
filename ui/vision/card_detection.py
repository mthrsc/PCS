
import cv2
import numpy as np

class Card_detection():
    def __init__(self):
        self._card_detected = False


    def detect_card_shape(self, frame, vid):
        """Detect rectangular shapes (Pokémon card-like) in the given frame."""
        cam_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        cam_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the size of the rectangle (relative to the video resolution)
        rect_width = int(cam_width * 0.4)  # 40% of camera width
        rect_height = int(cam_height * 0.8)  # 40% of camera height

        # Calculate starting and ending coordinates to center the rectangle
        rect_start = (
            (cam_width - rect_width) // 2,  # Centered on X-axis
            (cam_height - rect_height) // 2  # Centered on Y-axis
        )
        rect_end = (
            rect_start[0] + rect_width,  # Bottom-right corner X
            rect_start[1] + rect_height  # Bottom-right corner Y
        )

        # Create a darkened overlay for the whole frame
        overlay = frame.copy()
        darkened_overlay = np.zeros_like(frame, dtype=np.uint8)  # Black overlay
        darkened_overlay[:] = (50, 50, 50)  # Set dimming intensity (darker color)

        # Blend the original frame with the darkened overlay
        frame_with_overlay = cv2.addWeighted(frame, 0.5, darkened_overlay, 0.5, 0)

        # Cut out the detection area (clear rectangle) from the darkened overlay
        frame_with_overlay[rect_start[1]:rect_end[1], rect_start[0]:rect_end[0]] = \
            frame[rect_start[1]:rect_end[1], rect_start[0]:rect_end[0]]

        # Now proceed with card detection within the clear rectangle (ROI)
        roi = frame[rect_start[1]:rect_end[1], rect_start[0]:rect_end[0]]

        # Convert the frame to grayscale and apply edge detection in ROI only
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Detect contours in the edges within the ROI
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Approximate the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the approximated contour has 4 vertices (i.e., it's a quadrilateral)
            if len(approx) == 4:
                # Compute the bounding box of the contour
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                # Ensure the contour is large enough to be a card and has the right aspect ratio
                if 0.7 < aspect_ratio < 0.72 and w > 50 and h > 50:
                    # Draw the contour (rectangle) on the ROI
                    cv2.drawContours(roi, [approx], -1, (255, 0, 0), 2)

                    if not self.card_detected:
                        # Extract the region inside the detected contour (the card)
                        card_img = roi[y:y+h, x:x+w]

                        # Save the image file only when the full quadrilateral is detected
                        cv2.imwrite("detected_card.png", card_img)
                        print("Card saved as detected_card.png")
                        self.card_detected = True  # Flag to avoid multiple saves

        return frame_with_overlay
    
    @property
    def card_detected(self):
        return self._card_detected
    @card_detected.setter
    def card_detected(self, value):
        self._card_detected = value
