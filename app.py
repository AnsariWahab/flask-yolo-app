from flask import Flask, request, jsonify, send_file
import os
import torch
from pathlib import Path
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_boxes
from utils.torch_utils import select_device
from utils.dataloaders import letterbox
import cv2

# Initialize Flask app
app = Flask(__name__)

# Set device (GPU if available, otherwise CPU)
device = select_device('')

# Load YOLOv3 model from local .pt file
model = attempt_load('yolov3.pt', device=device)
model.eval()

# Upload and Output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def preprocess_image(image_path, img_size=640):
    """
    Preprocess the image for YOLOv3 inference.
    - Resize and pad the image while maintaining aspect ratio.
    - Ensures no negative strides with a memory copy.
    """
    img0 = cv2.imread(image_path)  # BGR
    assert img0 is not None, f"Image Not Found: {image_path}"
    img = letterbox(img0, img_size, stride=32, auto=True)[0]  # Resize

    # Ensure array is contiguous in memory to avoid negative strides
    img = img[:, :, ::-1].copy()  # BGR to RGB and copy to fix strides
    img = img.transpose(2, 0, 1)  # HWC to CHW
    img = torch.from_numpy(img).to(device).float() / 255.0  # Normalize to 0-1
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img, img0

@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the uploaded file
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)
        print(f"File received and saved: {image_path}")  # Debugging: Confirm file is received

        # Preprocess image
        print("Preparing image for inference...")  # Debugging: Check before model inference
        img, img0 = preprocess_image(image_path)

        # Perform inference
        print("Running inference...")  # Debugging: Check before model inference
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)
        print("Inference complete.")  # Debugging: Check after inference

        # Process detections
        output_image_path = os.path.join(OUTPUT_FOLDER, 'result_' + file.filename)
        for det in pred:
            if len(det):
                # Rescale boxes to original image
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()

                # Draw bounding boxes and labels on image
                for *xyxy, conf, cls in det:
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    img0 = draw_box(img0, xyxy, label)

        # Save the output image
        cv2.imwrite(output_image_path, img0)
        print(f"Output image saved: {output_image_path}")  # Debugging: Output image saved

        # Return the processed image
        return send_file(output_image_path, mimetype='image/jpeg')

    except Exception as e:
        print(f"Error during processing: {e}")  # Debugging: Log the error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def draw_box(image, xyxy, label, color=(0, 255, 0), thickness=2):
    """
    Draw bounding box with label on the image.
    """
    x1, y1, x2, y2 = map(int, xyxy)
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(image, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
    cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return image

if __name__ == '__main__':
    app.run(debug=True)
