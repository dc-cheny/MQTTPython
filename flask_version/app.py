from flask import Flask, render_template, Response, jsonify, stream_with_context
import cv2
from base64 import encodebytes

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera


# for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_
# stream=0.sdp' instead of camera.
# for local webcam use cv2.VideoCapture(0).

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # yield {'frame_bytes': frame}
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_frames_dict():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield jsonify(
                status_code='200',
                raw_data=encodebytes(frame).decode('ascii')
            ).data


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_dict')
def video_feed_dict():
    # Video streaming route. Put this in the src attribute of an img tag
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(stream_with_context(gen_frames_dict()), mimetype='application/json')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
