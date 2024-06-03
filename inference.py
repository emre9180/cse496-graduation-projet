from ultralytics import YOLO
import cv2
import numpy as np
from ultralytics.utils.plotting import Annotator

# Load YOLO model
model = YOLO("best.pt")
# Customize validation settings
# validation_results = model.val(data=r"D:\Tomato-2.v1i.yolov5pytorch\data.yaml",
#                                imgsz=640,
#                                batch=16,
#                                conf=0.25,
#                                iou=0.6,
#                                device='cpu')
                               
# Load an image and resize it
img_path = r"C:\Users\emrey\source\repos\ConsoleApplication1\ConsoleApplication1\color_image_30nisan34.jpg"
image = cv2.imread(img_path)
image = cv2.resize(image, (640, 640))  # Resize image to 640x640

# Predict objects in the image
results = model.predict(image)

# Initialize an Annotator for the image
annotator = Annotator(image, line_width=2, font_size=2)

def refine_contours(contours):
    refined = []
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    for contour in contours:
        # Create a blank mask with the same dimensions as the original image
        mask = np.zeros(image.shape[:2], dtype=np.uint8)  # Ensure mask is single-channel

        # Draw the contour on the mask with white color
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)  # Fill contour with white
        
        # Apply morphological close operation
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find new contours in the modified mask
        new_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        refined.extend(new_contours)
    return refined


# Iterate through each detection in the results
for result in results:
    segments = result.masks.xy  # List of segments in pixel coordinates

    # Draw each segment as a polygon and calculate ellipse parameters
    for segment in segments:
        pts = np.array(segment, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Refine contours
        refined_contours = refine_contours([pts])
        for contour in refined_contours:
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                center, axes, angle = ellipse
                major_axis_length = max(axes) / 2  # Halved because cv2 returns full length
                minor_axis_length = min(axes) / 2  # Halved because cv2 returns full length

                # Draw ellipse for visualization
                cv2.ellipse(image, ellipse, (0, 0, 0), 2)

                # Display axis lengths on the image
                text = f'Maj: {major_axis_length:.2f}, Min: {minor_axis_length:.2f}'
                text_position = (int(center[0]), int(center[1]))
        cv2.putText(image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

       # Iterate over each box to draw it
    # for i, box in enumerate(xyxy):
    #     x1, y1, x2, y2 = map(int, box)
    #     cls = int(classes[i])
    #     conf = confidences[i]
    #     label = f'{model.names[cls]} {conf:.2f}'
    #     annotator.box_label([x1, y1, x2, y2], label, color=(255, 0, 0))

# Get the annotated image and display it
annotated_img = annotator.result()
cv2.imshow('YOLO V8 Detection', annotated_img)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()
#"D:\tugba_hoca_arsiv\train\images\IMG_1072.jpg"

"""
for result in results:
    # detection
    result.boxes.xyxy   # box with xyxy format, (N, 4)
    result.boxes.xywh   # box with xywh format, (N, 4)
    result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
    result.boxes.xywhn  # box with xywh format but normalized, (N, 4)
    result.boxes.conf   # confidence score, (N, 1)
    result.boxes.cls    # cls, (N, 1)

    # segmentation
    result.masks.masks     # masks, (N, H, W)
    result.masks.segments  # bounding coordinates of masks, List[segment] * N

    # classification
    result.probs     # cls prob, (num_class, )



# Customize validation settings
validation_results = model.val(data=r"D:\tugba_hoca_arsiv\example_dataset.yaml",
                               imgsz=640,
                               batch=16,
                               conf=0.25,
                               iou=0.6,
                               device='cpu')
    """