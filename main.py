from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Open the camera using the default camera index
cap = cv2.VideoCapture(1)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


def generate_frames():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame is read correctly, ret will be True
        if ret:
            # Convert the frame to JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Unable to encode frame.")
                break

            # Yield the frame in bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("Error: Unable to read frame from camera.")
            break


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
