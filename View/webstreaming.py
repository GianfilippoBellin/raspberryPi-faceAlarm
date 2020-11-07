# Import necessary libraries
from flask import Flask, render_template, Response

# Initialize the Flask app
from Models.Detectors import DetectorFace

app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(DetectorFace().find(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


