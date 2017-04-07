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
from flask import Flask, render_template, request, Response, jsonify
from common.communication.communicationvalues import CommunicationValues
from webserver.imagewebhandler import ImageWebHandler

# Initialize Logger
fileConfig(cfg.get_logging_config_fullpath())
__log = logging.getLogger()

# Initialize Flask Server
app = Flask(__name__)

# Set initialize values
pi_running = False
image_handler = None
communicationvalues = None


# http://localhost:5000/
@app.route('/')
def index():
    """Streaming home page."""
    global pi_running
    global image_handler
    global communicationvalues
    pi_running = False
    image_handler = None
    communicationvalues = None
    return __call_render_template()


# Start TrafficLightDetection on raspberry pi - http://localhost:5000/start_pi
@app.route('/start_pi', methods=['POST'])
def start_pi():
    global pi_running
    pi_running = True
    return __call_render_template()


# Stop TrafficLightDetection on raspberry pi - http://localhost:5000/stop_pi
@app.route('/stop_pi', methods=['POST'])
def stop_pi():
    global pi_running
    pi_running = False
    return __call_render_template()


# Response frame from raspberry pi feed - http://localhost:5000/pi_feed
@app.route('/pi_feed')
def pi_feed():
    """Pi streaming route. Put this in the src attribute of an img tag."""
    global pi_running
    global image_handler
    if pi_running:
        image_handler = ImageWebHandler()
        return Response(gen_pi(image_handler), mimetype='multipart/x-mixed-replace; boundary=frame')
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
    cfg.set_maskletter_min_maskarea_size(request.form['mask_letter_min_maskarea_size'])
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
    cfg.set_letter_tolerance_v_gap(request.form['letter_tolerance_v_gap'])
    cfg.set_letter_min_amount_processed_letters(request.form['letter_min_amount_processed_letters'])
    cfg.set_controls_tof_side(request.form['controls_tof_side'])
    cfg.set_controls_tof_front(request.form['controls_tof_front'])
    cfg.set_controls_gyro_p(request.form['controls_gyro_p'])
    cfg.set_controls_gyro_i(request.form['controls_gyro_i'])
    cfg.set_controls_gyro_d(request.form['controls_gyro_d'])
    cfg.set_controls_tof_p(request.form['controls_tof_p'])
    cfg.set_controls_tof_i(request.form['controls_tof_i'])
    cfg.set_controls_tof_d(request.form['controls_tof_d'])

    return Response("Data successfully saved")


# Set all changed serial values
@app.route('/get_serialvalues', methods=['GET'])
def get_serialvalues():
    # Function for serial communication values - getter / IST Werte holen
    global communicationvalues
    if communicationvalues is None:
        communicationvalues = CommunicationValues()
    serial_hello = communicationvalues.get_hello()
    serial_start = communicationvalues.get_start()
    serial_course = communicationvalues.get_course()
    serial_tof_l_i = communicationvalues.get_tof_left()
    serial_tof_r_i = communicationvalues.get_tof_right()
    serial_tof_f_i = communicationvalues.get_tof_front()
    serial_raupe_l_i = communicationvalues.get_raupe_left()
    serial_raupe_r_i = communicationvalues.get_raupe_right()
    serial_gyro_n = communicationvalues.get_gyro_n()
    serial_gyro_g = communicationvalues.get_gyro_g()
    serial_gyroskop_i = communicationvalues.get_gyroskop()
    serial_servo_i = communicationvalues.get_servo()
    serial_gyrop = communicationvalues.get_kpG()
    serial_gyroi = communicationvalues.get_kiG()
    serial_gyrod = communicationvalues.get_kdG()
    serial_tofp = communicationvalues.get_kpT()
    serial_tofi = communicationvalues.get_kiT()
    serial_tofd = communicationvalues.get_kdT()
    serial_letter = communicationvalues.get_letter()
    serial_parcstate = communicationvalues.get_parcstate()
    serial_errstate = communicationvalues.get_error()

    return jsonify(result=dict(serial_hello=serial_hello, serial_start=serial_start, serial_course=serial_course,
                               serial_tof_l_i=serial_tof_l_i, serial_tof_r_i=serial_tof_r_i,
                               serial_tof_f_i=serial_tof_f_i, serial_raupe_l_i=serial_raupe_l_i,
                               serial_raupe_r_i=serial_raupe_r_i, serial_gyro_n=serial_gyro_n,
                               serial_gyro_g=serial_gyro_g, serial_gyroskop_i=serial_gyroskop_i,
                               serial_servo_i=serial_servo_i, serial_gyrop=serial_gyrop, serial_gyroi=serial_gyroi,
                               serial_gyrod=serial_gyrod, serial_tofp=serial_tofp, serial_tofi=serial_tofi,
                               serial_tofd=serial_tofd, serial_letter=serial_letter,
                               serial_parcstate=serial_parcstate, serial_errstate=serial_errstate))


# Get all serial values
@app.route('/set_serialvalues', methods=['POST'])
def set_serialvalues():

    global communicationvalues
    if communicationvalues is None:
        communicationvalues = CommunicationValues()

    changedProperty = request.json['ChangedProperty']
    newValue = request.json['NewValue']

    # TODO: buttons for send hello and start
    # communicationvalues.send_hello()
    # communicationvalues.send_start()
    if changedProperty == "serial_course_l":
        communicationvalues.send_course(1)
    elif changedProperty == "serial_course_r":
        communicationvalues.send_course(0)
    elif changedProperty == "serial_letter_s":
        communicationvalues.send_letter(newValue)
    elif changedProperty == "serial_tof_l_s":
        communicationvalues.send_tof_left(newValue)
    elif changedProperty == "serial_tof_f_s":
        communicationvalues.send_tof_front(newValue)
    elif changedProperty == "serial_raupe_l_s":
        communicationvalues.send_raupe_left(newValue)
    elif changedProperty == "serial_gyroskop_s":
        communicationvalues.send_gyroskop(newValue)
    elif changedProperty == "serial_servo_s":
        communicationvalues.send_servo(newValue)
    elif changedProperty == "serial_gyrop":
        communicationvalues.send_kpG(newValue)
    elif changedProperty == "serial_gyroi":
        communicationvalues.send_kiG(newValue)
    elif changedProperty == "serial_gyrod":
        communicationvalues.send_kdG(newValue)
    elif changedProperty == "serial_tofp":
        communicationvalues.send_kpT(newValue)
    elif changedProperty == "serial_tofi":
        communicationvalues.send_kiT(newValue)
    elif changedProperty == "serial_tofd":
        communicationvalues.send_kdT(newValue)
    elif changedProperty == "serial_errors":
        communicationvalues.send_error(newValue)

    return jsonify(request.json['ChangedProperty'])


# Get frame and return jpeg-frame string from raspberry pi
def gen_pi(imagehandler):
    global pi_running
    while True:
        frame = imagehandler.get_frame()
        if pi_running and frame is not None:
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
                           mask_letter_min_maskarea_size=cfg.get_maskletter_min_maskarea_size(),
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
                           letter_tolerance_i_gap=cfg.get_letter_tolerance_i_gap(),
                           letter_tolerance_v_gap=cfg.get_letter_tolerance_v_gap(),
                           letter_min_amount_processed_letters=cfg.get_letter_min_amount_processed_letters(),
                           controls_tof_side=cfg.get_controls_tof_side(),
                           controls_tof_front=cfg.get_controls_tof_front(),
                           controls_gyro_p=cfg.get_controls_gyro_p(),
                           controls_gyro_i=cfg.get_controls_gyro_i(),
                           controls_gyro_d=cfg.get_controls_gyro_d(),
                           controls_tof_p=cfg.get_controls_tof_p(),
                           controls_tof_i=cfg.get_controls_tof_i(),
                           controls_tof_d=cfg.get_controls_tof_d())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
