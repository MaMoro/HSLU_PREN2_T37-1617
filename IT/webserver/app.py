# =======================================================================
# !/usr/bin/python
# TITLE           : app.py
# DESCRIPTION     : This program holds the logic for the Flask Server (UI)
# AUTHOR          : Rohrbach Fabrizio
# DATE            : 10.11.2016
# VERSION         : 0.2
# USAGE           : python app.py
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# =======================================================================

# Import the modules needed to run the script.
import logging
import common.config.confighandler as cfg

from logging.config import fileConfig
from flask import Flask, render_template, request, Response
from trafficlight.trafficlightdetection_pi import TrafficLightDetectionPi
from trafficlight.trafficlightdetection_video import TrafficLightDetectionVideo
from trafficlight.trafficlightdetection_img import TrafficLightDetectionImg
from trafficlight.trafficlightdetection_stream import TrafficLightDetectionStream

# Initialize Logger
fileConfig(cfg.get_logging_config_fullpath())
__log = logging.getLogger()

# Initialize Flask Server
app = Flask(__name__)

# Set initialize values
images_running = False
video_running = False
stream_running = False
pi_running = False
images_preview_running = False
video_preview_running = False
stream_preview_running = False
pi_preview_running = False
pi_thread = None


# http://localhost:5000/
@app.route('/')
def index():
    """Streaming home page."""
    global images_running
    global video_running
    global stream_running
    global pi_running
    global images_preview_running
    global video_preview_running
    global stream_preview_running
    global pi_preview_running
    global pi_thread
    images_running = False
    video_running = False
    stream_running = False
    pi_running = False
    images_preview_running = False
    video_preview_running = False
    stream_preview_running = False
    pi_preview_running = False
    pi_thread = None

    return __call_render_template()


# Start TrafficLightDetection on images - http://localhost:5000/start_images
@app.route('/start_images', methods=['POST'])
def start_images():
    value = request.form.getlist('preview')
    global images_running
    global images_preview_running
    images_running = True
    if len(value) > 0:
        images_preview_running = True
    else:
        images_preview_running = False

    return __call_render_template()


# Stop TrafficLightDetection on images - http://localhost:5000/stop_images
@app.route('/stop_images', methods=['POST'])
def stop_images():
    global images_running
    global images_preview_running
    images_running = False
    images_preview_running = False

    return __call_render_template()


# Start TrafficLightDetection on video - http://localhost:5000/start_video
@app.route('/start_video', methods=['POST'])
def start_video():
    value = request.form.getlist('preview')
    global video_running
    global video_preview_running
    video_running = True
    if len(value) > 0:
        video_preview_running = True
    else:
        video_preview_running = False

    return __call_render_template()


# Stop TrafficLightDetection on video - http://localhost:5000/stop_video
@app.route('/stop_video', methods=['POST'])
def stop_video():
    global video_running
    global video_preview_running
    video_running = False
    video_preview_running = False

    return __call_render_template()


# Start TrafficLightDetection on stream  - http://localhost:5000/start_stream
@app.route('/start_stream', methods=['POST'])
def start_stream():
    value = request.form.getlist('preview')
    global stream_running
    global stream_preview_running
    stream_running = True
    if len(value) > 0:
        stream_preview_running = True
    else:
        stream_preview_running = False

    return __call_render_template()


# Stop TrafficLightDetection on stream - http://localhost:5000/stop_stream
@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global stream_running
    global stream_preview_running
    stream_running = False
    stream_preview_running = False

    return __call_render_template()


# Start TrafficLightDetection on raspberry pi - http://localhost:5000/start_pi
@app.route('/start_pi', methods=['POST'])
def start_pi():
    value = request.form.getlist('preview')
    global pi_running
    global pi_preview_running
    pi_running = True
    if len(value) > 0:
        pi_preview_running = True
    else:
        pi_preview_running = False

    return __call_render_template()


# Stop TrafficLightDetection on raspberry pi - http://localhost:5000/stop_pi
@app.route('/stop_pi', methods=['POST'])
def stop_pi():
    global pi_running
    global pi_preview_running
    global pi_thread
    pi_running = False
    pi_preview_running = False
    if pi_thread is not None:
        pi_thread.stop()

    return __call_render_template()


# Response frame from image feed - http://localhost:5000/img_feed
@app.route('/img_feed')
def img_feed():
    """Image streaming route. Put this in the src attribute of an img tag."""
    global images_preview_running
    if images_running:
        return Response(gen_img(TrafficLightDetectionImg()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response()


# Response frame from video feed - http://localhost:5000/video_feed
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    global video_preview_running
    if video_running:
        return Response(gen_video(TrafficLightDetectionVideo()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response()


# Response frame from stream feed - http://localhost:5000/stream_feed
@app.route('/stream_feed')
def stream_feed():
    """Webcam streaming route. Put this in the src attribute of an img tag."""
    global stream_preview_running
    if stream_running:
        return Response(gen_stream(TrafficLightDetectionStream()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response()


# Response frame from raspberry pi feed - http://localhost:5000/pi_feed
@app.route('/pi_feed')
def pi_feed():
    """Webcam streaming route. Put this in the src attribute of an img tag."""
    global pi_preview_running
    global pi_thread
    if pi_running:
        pi_thread = TrafficLightDetectionPi()
        return Response(gen_pi(pi_thread), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response()


# Save the values from the website into the Config.ini - http://localhost:5000/save
@app.route('/save', methods=['POST'])
def save():
    cfg.set_settings_title(request.form['settings_title'])
    cfg.set_settings_project(request.form['settings_project'])
    cfg.set_settings_description(request.form['settings_description'])
    cfg.set_settings_copyright(request.form['settings_copyright'])
    cfg.set_settings_loglevel(request.form['settings_loglevel'])
    cfg.set_settings_debug(request.form.getlist('settings_debug'))
    cfg.set_masktrafficlight_red_low_l(request.form['mask_trafficlight_red_low_l'])
    cfg.set_masktrafficlight_red_low_h(request.form['mask_trafficlight_red_low_h'])
    cfg.set_masktrafficlight_red_high_l(request.form['mask_trafficlight_red_high_l'])
    cfg.set_masktrafficlight_red_high_h(request.form['mask_trafficlight_red_high_h'])
    cfg.set_masktrafficlight_green_l(request.form['mask_trafficlight_green_l'])
    cfg.set_masktrafficlight_green_h(request.form['mask_trafficlight_green_h'])
    cfg.set_maskletter_red_low_l(request.form['mask_letter_red_low_l'])
    cfg.set_maskletter_red_low_h(request.form['mask_letter_red_low_h'])
    cfg.set_maskletter_red_high_l(request.form['mask_letter_red_high_l'])
    cfg.set_maskletter_red_high_h(request.form['mask_letter_red_high_h'])
    cfg.set_maskletter_red_shift_l(request.form['mask_letter_red_shift_l'])
    cfg.set_maskletter_red_shift_h(request.form['mask_letter_red_shift_h'])
    cfg.set_maskletter_red_low_full(request.form['mask_letter_red_low_full'])
    cfg.set_maskletter_red_high_full(request.form['mask_letter_red_high_full'])
    cfg.set_color_black(request.form['color_black'])
    cfg.set_color_black_low(request.form['color_black_low'])
    cfg.set_color_black_high(request.form['color_black_high'])
    cfg.set_color_white(request.form['color_white'])
    cfg.set_color_red(request.form['color_red'])
    cfg.set_color_green(request.form['color_green'])
    cfg.set_color_blue(request.form['color_blue'])
    cfg.set_color_cyan(request.form['color_cyan'])
    cfg.set_color_magenta(request.form['color_magenta'])
    cfg.set_color_yellow(request.form['color_yellow'])
    cfg.set_color_gray(request.form['color_gray'])
    cfg.set_color_orange(request.form['color_orange'])
    cfg.set_debug_output_red(request.form.getlist('debug_output_red'))
    cfg.set_debug_output_green(request.form.getlist('debug_output_green'))
    cfg.set_debug_output_bgwhite(request.form.getlist('debug_output_bgwhite'))
    cfg.set_debug_logging_config(request.form['debug_logging_config'])
    cfg.set_camera_width(request.form['camera_width'])
    cfg.set_camera_height(request.form['camera_height'])
    cfg.set_camera_framerate(request.form['camera_framerate'])
    cfg.set_camera_iso(request.form['camera_iso'])
    cfg.set_camera_awb(request.form['camera_awb'])
    cfg.set_files_multiimg1(request.form['files_multiimg1'])
    cfg.set_files_multiimg2(request.form['files_multiimg2'])
    cfg.set_files_multiimgcount(request.form['files_multiimgcount'])
    cfg.set_files_video(request.form['files_video'])
    cfg.set_files_stream(request.form['files_stream'])
    cfg.set_cropimage_height(request.form['cropimage_height'])
    cfg.set_cropimage_width(request.form['cropimage_width'])
    cfg.set_imagetext_bordersize_left(request.form['imagetext_bordersize_left'])
    cfg.set_imagetext_bordersize_top(request.form['imagetext_bordersize_top'])
    cfg.set_imagetext_bordersize_bottom(request.form['imagetext_bordersize_bottom'])
    cfg.set_imagetext_bordersize_right(request.form['imagetext_bordersize_right'])
    cfg.set_imagetext_textspace(request.form['imagetext_textspace'])
    cfg.set_filter_kernel_size(request.form['filter_kernel_size'])
    cfg.set_filter_hsv_shift(request.form['filter_hsv_shift'])
    cfg.set_letter_tolerance_i_gap(request.form['letter_tolerance_i_gap'])

    return Response("Data successfully saved")


# Get frame and return jpeg-frame string from images
def gen_img(camera):
    global images_running
    global images_preview_running
    while True:
        frame = camera.get_frame()
        if images_running and images_preview_running and frame is not None:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')


# Get frame and return jpeg-frame string from video
def gen_video(camera):
    global video_running
    global video_preview_running
    while True:
        frame = camera.get_frame()
        if video_running and video_preview_running and frame is not None:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')


# Get frame and return jpeg-frame string from stream
def gen_stream(camera):
    global stream_running
    global stream_preview_running
    while True:
        frame = camera.get_frame()
        if stream_running and stream_preview_running and frame is not None:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')


# Get frame and return jpeg-frame string from raspberry pi
def gen_pi(camera):
    global pi_running
    global pi_preview_running
    while True:
        frame = camera.get_frame()
        if pi_running and pi_preview_running and frame is not None:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')


# Caller with settings to render template
def __call_render_template():
    return render_template('index.html', settings_title=cfg.get_settings_title(),
                           settings_project=cfg.get_settings_project(),
                           settings_description=cfg.get_settings_description(),
                           settings_copyright=cfg.get_settings_copyright(),
                           settings_loglevel=cfg.get_settings_loglevel(),
                           settings_debug=cfg.get_settings_debug_checkbox(),
                           mask_trafficlight_red_low_l=cfg.get_masktrafficlight_red_low_l(),
                           mask_trafficlight_red_low_h=cfg.get_masktrafficlight_red_low_h(),
                           mask_trafficlight_red_high_l=cfg.get_masktrafficlight_red_high_l(),
                           mask_trafficlight_red_high_h=cfg.get_masktrafficlight_red_high_h(),
                           mask_trafficlight_green_l=cfg.get_masktrafficlight_green_l(),
                           mask_trafficlight_green_h=cfg.get_masktrafficlight_green_h(),
                           mask_letter_red_low_l=cfg.get_maskletter_red_low_l(),
                           mask_letter_red_low_h=cfg.get_maskletter_red_low_h(),
                           mask_letter_red_high_l=cfg.get_maskletter_red_high_l(),
                           mask_letter_red_high_h=cfg.get_maskletter_red_high_h(),
                           mask_letter_red_shift_l=cfg.get_maskletter_red_shift_l(),
                           mask_letter_red_shift_h=cfg.get_maskletter_red_shift_h(),
                           mask_letter_red_low_full=cfg.get_maskletter_red_low_full(),
                           mask_letter_red_high_full=cfg.get_maskletter_red_high_full(),
                           color_black=cfg.get_color_black(),
                           color_black_low=cfg.get_color_black_low(),
                           color_black_high=cfg.get_color_black_high(),
                           color_white=cfg.get_color_white(),
                           color_red=cfg.get_color_red(),
                           color_green=cfg.get_color_green(),
                           color_blue=cfg.get_color_blue(),
                           color_cyan=cfg.get_color_cyan(),
                           color_magenta=cfg.get_color_magenta(),
                           color_yellow=cfg.get_color_yellow(),
                           color_gray=cfg.get_color_gray(),
                           color_orange=cfg.get_color_orange(),
                           debug_output_red=cfg.get_debug_output_red_checkbox(),
                           debug_output_green=cfg.get_debug_output_green_checkbox(),
                           debug_output_bgwhite=cfg.get_debug_output_bgwhite_checkbox(),
                           debug_logging_config=cfg.get_debug_logging_config(),
                           camera_width=cfg.get_camera_width(),
                           camera_height=cfg.get_camera_height(),
                           camera_framerate=cfg.get_camera_framerate(),
                           camera_iso=cfg.get_camera_iso(),
                           camera_awb=cfg.get_camera_awb(),
                           files_multiimg1=cfg.get_files_multiimg1(),
                           files_multiimg2=cfg.get_files_multiimg2(),
                           files_multiimgcount=cfg.get_files_multiimgcount(),
                           files_video=cfg.get_files_video(),
                           files_stream=cfg.get_files_stream(),
                           cropimage_height=cfg.get_cropimage_height(),
                           cropimage_width=cfg.get_cropimage_width(),
                           imagetext_bordersize_left=cfg.get_imagetext_bordersize_left(),
                           imagetext_bordersize_top=cfg.get_imagetext_bordersize_top(),
                           imagetext_bordersize_bottom=cfg.get_imagetext_bordersize_bottom(),
                           imagetext_bordersize_right=cfg.get_imagetext_bordersize_right(),
                           imagetext_textspace=cfg.get_imagetext_textspace(),
                           filter_kernel_size=cfg.get_filter_kernel_size(),
                           filter_hsv_shift=cfg.get_filter_hsv_shift(),
                           letter_tolerance_i_gap=cfg.get_letter_tolerance_i_gap())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)