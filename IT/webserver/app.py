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
import sys
import os
import configparser

from ..trafficlight.trafficlightdetection_pi import TrafficLightDetectionPi
from ..trafficlight.trafficlightdetection_video import TrafficLightDetectionVideo
from ..trafficlight.trafficlightdetection_img import TrafficLightDetectionImg
from ..trafficlight.trafficlightdetection_stream import TrafficLightDetectionStream

from flask import Flask, render_template, request, Response
from ..common.logging.loghelper import LogHelper
from ..common.logging.fpshelper import FPSHelper

# Initialize Logger and FPS Helpers
LOG = LogHelper()
FPS = FPSHelper()

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


# Function for converting string to boolean (for example if in Config.ini)
def str2bool(v):
    return v.lower() in ("yes", "Yes", "YES", "true", "True", "TRUE", "1", "t")


# Set root dir for project (needed for example the Config.ini)
ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

# Initialize ConfigParser
config = configparser.ConfigParser()


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
    images_running = False
    video_running = False
    stream_running = False
    pi_running = False
    images_preview_running = False
    video_preview_running = False
    stream_preview_running = False
    pi_preview_running = False

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


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

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


# Stop TrafficLightDetection on images - http://localhost:5000/stop_images
@app.route('/stop_images', methods=['POST'])
def stop_images():
    global images_running
    global images_preview_running
    images_running = False
    images_preview_running = False

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


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

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


# Stop TrafficLightDetection on video - http://localhost:5000/stop_video
@app.route('/stop_video', methods=['POST'])
def stop_video():
    global video_running
    global video_preview_running
    video_running = False
    video_preview_running = False

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


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

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


# Stop TrafficLightDetection on stream - http://localhost:5000/stop_stream
@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global stream_running
    global stream_preview_running
    stream_running = False
    stream_preview_running = False

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


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

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


# Stop TrafficLightDetection on raspberry pi - http://localhost:5000/stop_pi
@app.route('/stop_pi', methods=['POST'])
def stop_pi():
    global pi_running
    global pi_preview_running
    pi_running = False
    pi_preview_running = False

    config.read(ROOT_DIR + '/common/config/config.ini')

    if config.get('settings', 'debug') == 'True':
        settings_debug = 'checked'
    else:
        settings_debug = 'unchecked'
    if config.get('debug', 'output_red') == 'True':
        debug_output_red = 'checked'
    else:
        debug_output_red = 'unchecked'
    if config.get('debug', 'output_green') == 'True':
        debug_output_green = 'checked'
    else:
        debug_output_green = 'unchecked'
    if config.get('debug', 'output_bgwhite') == 'True':
        debug_output_bgwhite = 'checked'
    else:
        debug_output_bgwhite = 'unchecked'

    return render_template('index.html',
                           settings_title=config.get('settings', 'title'),
                           settings_project=config.get('settings', 'project'),
                           settings_description=config.get('settings', 'description'),
                           settings_copyright=config.get('settings', 'copyright'),
                           settings_loglevel=config.get('settings', 'loglevel'),
                           settings_debug=settings_debug,
                           mask_trafficlight_red_low_l=config.get('mask_trafficlight', 'red_low_l'),
                           mask_trafficlight_red_low_h=config.get('mask_trafficlight', 'red_low_h'),
                           mask_trafficlight_red_high_l=config.get('mask_trafficlight', 'red_high_l'),
                           mask_trafficlight_red_high_h=config.get('mask_trafficlight', 'red_high_h'),
                           mask_trafficlight_green_l=config.get('mask_trafficlight', 'green_l'),
                           mask_trafficlight_green_h=config.get('mask_trafficlight', 'green_h'),
                           mask_letter_red_low_l=config.get('mask_letter', 'red_low_l'),
                           mask_letter_red_low_h=config.get('mask_letter', 'red_low_h'),
                           mask_letter_red_high_l=config.get('mask_letter', 'red_high_l'),
                           mask_letter_red_high_h=config.get('mask_letter', 'red_high_h'),
                           mask_letter_red_shift_l=config.get('mask_letter', 'red_shift_l'),
                           mask_letter_red_shift_h=config.get('mask_letter', 'red_shift_h'),
                           mask_letter_red_low_full=config.get('mask_letter', 'red_low_full'),
                           mask_letter_red_high_full=config.get('mask_letter', 'red_high_full'),
                           color_black=config.get('color', 'black'),
                           color_black_low=config.get('color', 'black_low'),
                           color_black_high=config.get('color', 'black_high'),
                           color_white=config.get('color', 'white'),
                           color_red=config.get('color', 'red'),
                           color_green=config.get('color', 'green'),
                           color_blue=config.get('color', 'blue'),
                           color_cyan=config.get('color', 'cyan'),
                           color_magenta=config.get('color', 'magenta'),
                           color_yellow=config.get('color', 'yellow'),
                           color_gray=config.get('color', 'gray'),
                           color_orange=config.get('color', 'orange'),
                           debug_output_red=debug_output_red,
                           debug_output_green=debug_output_green,
                           debug_output_bgwhite=debug_output_bgwhite,
                           camera_width=config.get('camera', 'width'),
                           camera_height=config.get('camera', 'height'),
                           camera_framerate=config.get('camera', 'framerate'),
                           camera_iso=config.get('camera', 'iso'),
                           camera_awb=config.get('camera', 'awb'),
                           files_multiimg1=config.get('files', 'multiimg1'),
                           files_multiimg2=config.get('files', 'multiimg2'),
                           files_multiimgcount=config.get('files', 'multiimgcount'),
                           files_video=config.get('files', 'video'),
                           files_stream=config.get('files', 'stream'),
                           cropimage_height=config.get('cropimage', 'height'),
                           cropimage_width=config.get('cropimage', 'width'),
                           imagetext_bordersize_left=config.get('imagetext', 'bordersize_left'),
                           imagetext_bordersize_top=config.get('imagetext', 'bordersize_top'),
                           imagetext_bordersize_bottom=config.get('imagetext', 'bordersize_bottom'),
                           imagetext_bordersize_right=config.get('imagetext', 'bordersize_right'),
                           imagetext_textspace=config.get('imagetext', 'textspace'),
                           filter_kernel_size=config.get('filter', 'kernel_size'),
                           filter_hsv_shift=config.get('filter', 'hsv_shift'),
                           letter_tolerance_i_gap=config.get('letter', 'tolerance_i_gap'))


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
    if pi_running:
        return Response(gen_pi(TrafficLightDetectionPi()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response()


# Save the values from the website into the Config.ini - http://localhost:5000/save
@app.route('/save', methods=['POST'])
def save():
    settings_title = request.form['settings_title']
    settings_project = request.form['settings_project']
    settings_description = request.form['settings_description']
    settings_copyright = request.form['settings_copyright']
    settings_loglevel = request.form['settings_loglevel']
    settings_debug = request.form.getlist('settings_debug')
    mask_trafficlight_red_low_l = request.form['mask_trafficlight_red_low_l']
    mask_trafficlight_red_low_h = request.form['mask_trafficlight_red_low_h']
    mask_trafficlight_red_high_l = request.form['mask_trafficlight_red_high_l']
    mask_trafficlight_red_high_h = request.form['mask_trafficlight_red_high_h']
    mask_trafficlight_green_l = request.form['mask_trafficlight_green_l']
    mask_trafficlight_green_h = request.form['mask_trafficlight_green_h']
    mask_letter_red_low_l = request.form['mask_letter_red_low_l']
    mask_letter_red_low_h = request.form['mask_letter_red_low_h']
    mask_letter_red_high_l = request.form['mask_letter_red_high_l']
    mask_letter_red_high_h = request.form['mask_letter_red_high_h']
    mask_letter_red_shift_l = request.form['mask_letter_red_shift_l']
    mask_letter_red_shift_h = request.form['mask_letter_red_shift_h']
    mask_letter_red_low_full = request.form['mask_letter_red_low_full']
    mask_letter_red_high_full = request.form['mask_letter_red_high_full']
    color_black = request.form['color_black']
    color_black_low = request.form['color_black_low']
    color_black_high = request.form['color_black_high']
    color_white = request.form['color_white']
    color_red = request.form['color_red']
    color_green = request.form['color_green']
    color_blue = request.form['color_blue']
    color_cyan = request.form['color_cyan']
    color_magenta = request.form['color_magenta']
    color_yellow = request.form['color_yellow']
    color_gray = request.form['color_gray']
    color_orange = request.form['color_orange']
    debug_output_red = request.form.getlist('debug_output_red')
    debug_output_green = request.form.getlist('debug_output_green')
    debug_output_bgwhite = request.form.getlist('debug_output_bgwhite')
    camera_width = request.form['camera_width']
    camera_height = request.form['camera_height']
    camera_framerate = request.form['camera_framerate']
    camera_iso = request.form['camera_iso']
    camera_awb = request.form['camera_awb']
    files_multiimg1 = request.form['files_multiimg1']
    files_multiimg2 = request.form['files_multiimg2']
    files_multiimgcount = request.form['files_multiimgcount']
    files_video = request.form['files_video']
    files_stream = request.form['files_stream']
    cropimage_height = request.form['cropimage_height']
    cropimage_width = request.form['cropimage_width']
    imagetext_bordersize_left = request.form['imagetext_bordersize_left']
    imagetext_bordersize_top = request.form['imagetext_bordersize_top']
    imagetext_bordersize_bottom = request.form['imagetext_bordersize_bottom']
    imagetext_bordersize_right = request.form['imagetext_bordersize_right']
    imagetext_textspace = request.form['imagetext_textspace']
    filter_kernel_size = request.form['filter_kernel_size']
    filter_hsv_shift = request.form['filter_hsv_shift']
    letter_tolerance_i_gap = request.form['letter_tolerance_i_gap']

    config2 = configparser.RawConfigParser()
    config2.read(ROOT_DIR + '/common/config/config.ini')

    config2.set('settings', 'title', settings_title)
    config2.set('settings', 'project', settings_project)
    config2.set('settings', 'description', settings_description)
    config2.set('settings', 'copyright', settings_copyright)
    config2.set('settings', 'loglevel', settings_loglevel)
    if len(settings_debug) > 0:
        config2.set('settings', 'debug', 'True')
    else:
        config2.set('settings', 'debug', 'False')
    config2.set('mask_trafficlight', 'red_low_l', mask_trafficlight_red_low_l)
    config2.set('mask_trafficlight', 'red_low_h', mask_trafficlight_red_low_h)
    config2.set('mask_trafficlight', 'red_high_l', mask_trafficlight_red_high_l)
    config2.set('mask_trafficlight', 'red_high_h', mask_trafficlight_red_high_h)
    config2.set('mask_trafficlight', 'green_l', mask_trafficlight_green_l)
    config2.set('mask_trafficlight', 'green_h', mask_trafficlight_green_h)
    config2.set('mask_letter', 'red_low_l', mask_letter_red_low_l)
    config2.set('mask_letter', 'red_low_h', mask_letter_red_low_h)
    config2.set('mask_letter', 'red_high_l', mask_letter_red_high_l)
    config2.set('mask_letter', 'red_high_h', mask_letter_red_high_h)
    config2.set('mask_letter', 'red_shift_l', mask_letter_red_shift_l)
    config2.set('mask_letter', 'red_shift_h', mask_letter_red_shift_h)
    config2.set('mask_letter', 'red_low_full', mask_letter_red_low_full)
    config2.set('mask_letter', 'red_high_full', mask_letter_red_high_full)
    config2.set('color', 'black', color_black)
    config2.set('color', 'black_low', color_black_low)
    config2.set('color', 'black_high', color_black_high)
    config2.set('color', 'white', color_white)
    config2.set('color', 'red', color_red)
    config2.set('color', 'green', color_green)
    config2.set('color', 'blue', color_blue)
    config2.set('color', 'cyan', color_cyan)
    config2.set('color', 'magenta', color_magenta)
    config2.set('color', 'yellow', color_yellow)
    config2.set('color', 'gray', color_gray)
    config2.set('color', 'orange', color_orange)
    if len(debug_output_red) > 0:
        config2.set('debug', 'output_red', 'True')
    else:
        config2.set('debug', 'output_red', 'False')
    if len(debug_output_green) > 0:
        config2.set('debug', 'output_green', 'True')
    else:
        config2.set('debug', 'output_green', 'False')
    if len(debug_output_bgwhite) > 0:
        config2.set('debug', 'output_bgwhite', 'True')
    else:
        config2.set('debug', 'output_bgwhite', 'False')
    config2.set('camera', 'width', camera_width)
    config2.set('camera', 'height', camera_height)
    config2.set('camera', 'framerate', camera_framerate)
    config2.set('camera', 'iso', camera_iso)
    config2.set('camera', 'awb', camera_awb)
    config2.set('files', 'multiimg1', files_multiimg1)
    config2.set('files', 'multiimg2', files_multiimg2)
    config2.set('files', 'multiimgcount', files_multiimgcount)
    config2.set('files', 'video', files_video)
    config2.set('files', 'stream', files_stream)
    config2.set('cropimage', 'height', cropimage_height)
    config2.set('cropimage', 'width', cropimage_width)
    config2.set('imagetext', 'bordersize_left', imagetext_bordersize_left)
    config2.set('imagetext', 'bordersize_top', imagetext_bordersize_top)
    config2.set('imagetext', 'bordersize_bottom', imagetext_bordersize_bottom)
    config2.set('imagetext', 'bordersize_right', imagetext_bordersize_right)
    config2.set('imagetext', 'textspace', imagetext_textspace)
    config2.set('filter', 'kernel_size', filter_kernel_size)
    config2.set('filter', 'hsv_shift', filter_hsv_shift)
    config2.set('letter', 'tolerance_i_gap', letter_tolerance_i_gap)

    with open(ROOT_DIR + '\\common\\config\\config.ini', 'w') as configfile:
        config2.write(configfile)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
