


class Card_detection():
    def __init__(self):
        ...


    def detect_card_shape(self, frame, cv2):
        """Detect rectangular shapes (Pokémon card-like) in the given frame."""
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply edge detection (Canny)
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edged image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate through contours to find rectangular shapes
        for contour in contours:
            # Approximate the contour to a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the approximated polygon has 4 vertices (i.e., it's a rectangle or square)
            if len(approx) == 4:
                # Get the bounding box of the contour
                (x, y, w, h) = cv2.boundingRect(approx)

                # Optionally filter by aspect ratio (approximate size of a Pokémon card)
                aspect_ratio = w / float(h)
                if 0.6 < aspect_ratio < 0.8:  # Adjust range based on actual card dimensions
                    # Draw the contour on the original frame
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)  # Draw a green rectangle
        return frame
