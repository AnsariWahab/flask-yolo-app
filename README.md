# Documentation

## **Objective**
The objective of this assessment is to create a Flask-based object detection API using the YOLOv3 model. The application enables users to upload an image and receive the processed image with bounding boxes around detected objects. The entire application is dockerized to ensure portability and scalability.

---

## **Steps Performed**

### **1. Cloning the GitHub Repository**
- **Action:**
  - Cloned the YOLOv3 repository from GitHub.
  - Repository used: [https://github.com/ultralytics/yolov3](https://github.com/ultralytics/yolov3)
  
- **Commands:**
  ```bash
  git clone https://github.com/ultralytics/yolov3.git
  ```

- **Challenges:**
  - Ensuring all required files (like `yolov3.pt`, `utils`, and `models`) were present in the repository.
  - The repository used some features that required careful attention to updates in dependencies.

- **Resolution:**
  - Validated the cloned repository by running sample YOLO inference scripts.

---

### **2. Setting Up a Virtual Environment**
- **Action:**
  - Created a Python virtual environment to manage dependencies and avoid conflicts.

- **Commands:**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Linux/Mac
  venv\Scripts\activate    # On Windows
  ```

- **Challenges:**
  - Encountered system-level package installation issues (e.g., OpenCV requiring `libgl` on Linux).

- **Resolution:**
  - Installed missing system libraries using `apt-get` (Linux) or adjusted dependency requirements on Windows.

---

### **3. Installing Dependencies**
- **Action:**
  - Installed all required dependencies listed in `requirements.txt`.

- **Commands:**
  ```bash
  pip install -r requirements.txt
  ```

- **Challenges:**
  - Some dependencies (e.g., `torch`) required specific versions for compatibility.

- **Resolution:**
  - Researched compatible versions of PyTorch and OpenCV and updated the `requirements.txt` accordingly.

---

### **4. Setting Up the Flask Application**
- **Action:**
  - Built a Flask API to accept image uploads, perform object detection using YOLOv3, and return the processed image.

- **Key Features Implemented:**
  - **Image Upload:** Accepted images via a `/detect` endpoint.
  - **Object Detection:** Integrated YOLOv3 for inference and post-processing.
  - **Processed Image Return:** Returned images with bounding boxes and labels.

- **Challenges:**
  - Preprocessing the input image to ensure compatibility with the YOLOv3 model.
  - Handling bounding box scaling and formatting issues.

- **Resolution:**
  - Used OpenCV and YOLO utilities (like `letterbox`) to preprocess images and scale bounding boxes back to the original dimensions.
  - Added debugging statements to identify processing errors.

---

### **5. Testing the Flask Application**
- **Action:**
  - Tested the Flask app locally using Postman and `curl`.

- **Challenges:**
  - Encountered errors like "socket hang up" and file upload mismatches.

- **Resolution:**
  - Ensured Flask was configured to listen on `0.0.0.0`.
  - Validated that uploaded files were correctly saved and processed.

---

### **6. Debugging Issues During Development**
- **Key Issues and Fixes:**
  - **Negative Strides in Images:**
    - **Issue:** TensorFlow errors due to negative strides in numpy arrays.
    - **Fix:** Used `.copy()` on arrays to ensure they were contiguous in memory.
  
  - **Bounding Box Scaling Issues:**
    - **Issue:** Boxes did not align with the original image dimensions.
    - **Fix:** Used `scale_boxes` from YOLO utilities.

  - **"No File Uploaded" Errors:**
    - **Issue:** Flask did not detect uploaded files properly.
    - **Fix:** Added form validation and logging to identify and resolve file upload issues.

  - **YOLO Model Compatibility:**
    - **Issue:** Some functions (e.g., `scale_coords`) were deprecated.
    - **Fix:** Replaced them with updated functions (e.g., `scale_boxes`).

---

### **7. Dockerization of the Flask Application**
- **Action:**
  - Containerized the Flask app using Docker for portability and scalability.

- **Dockerfile:**
  ```dockerfile
  # Use the official Python slim image as the base
  FROM python:3.12-slim

  # Install system dependencies for OpenCV
  RUN apt-get update && apt-get install -y \
      libgl1 \
      libglib2.0-0

  # Set the working directory in the container
  WORKDIR /app

  # Copy the current directory contents into the container
  COPY . /app

  # Install the Python dependencies
  RUN pip install --no-cache-dir -r requirements.txt

  # Expose port 5000 for the Flask app
  EXPOSE 5000

  # Define the command to run the Flask app
  CMD ["python", "app.py"]
  ```

- **Challenges:**
  - **Dependency Installation Issues:** Missing system-level dependencies for OpenCV.
    - **Fix:** Installed `libgl1` and `libglib2.0-0` inside the container.

  - **Port Mapping:** Flask was initially configured to listen only on `localhost`.
    - **Fix:** Updated Flask configuration to listen on `0.0.0.0`.

  - **Large Image Size:** YOLO weights (`yolov3.pt`) added significantly to the image size.
    - **Fix:** Ensured efficient layer management during the build process.

---

### **8. Running and Testing the Dockerized Application**
- **Action:**
  - Built and ran the Docker container.

- **Commands:**
  ```bash
  docker build -t flask-yolo-app .
  docker run -p 5000:5000 flask-yolo-app
  ```

- **Testing:**
  - Tested the `/detect` endpoint using Postman.
  - Verified the processed image output.

---

## **Summary**
- **Key Achievements:**
  - Successfully built a Flask-based object detection API.
  - Dockerized the application for portability.
  - Resolved several technical challenges related to dependency management, image preprocessing, and Docker configuration.

- **Remaining Improvements:**
  - Enhance error handling for edge cases.
  - Optimize the Docker image size further.
  - Add GPU support for faster inference if a compatible device is available.

---

This documentation serves as a comprehensive guide for replicating the project and understanding the development lifecycle. Let me know if you need additional details or refinements!

