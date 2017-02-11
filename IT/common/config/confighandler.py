# ================================================================================
# !/usr/bin/python
# TITLE           : confighandler.py
# DESCRIPTION     : Handler for config file
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           :
# VERSION         : 0.5
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import configparser
import os
import numpy as np

__project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
__inipath = __project_root_dir + '/common/config/config.ini'


# load ini file
def __loadconfig():
    config = configparser.ConfigParser()
    config.read(__inipath)
    return config


# convert string to boolean
def __str2bool(val):
    return val.lower() in ("True", "TRUE", "False", "FALSE")


# get Projectrootdir
def get_proj_rootdir():
    return __project_root_dir


# save changes to configfile
def __persistchanges(section, item, val):
    config = __loadconfig()
    config.set(section, item, val)
    with open(__inipath, "w") as configfile:
        config.write(configfile)


# fixed values
def get_opencv_font():
    import cv2
    return cv2.FONT_HERSHEY_COMPLEX_SMALL


# getter / setter for configfile values #

# Start Section "Settings" #

def get_settings_title():
    return __loadconfig().get('settings', 'title')


def set_settings_title(val):
    __persistchanges('settings', 'title', val)


def get_settings_project():
    return __loadconfig().get('settings', 'project')


def set_settings_project(val):
    __persistchanges('settings', 'project', val)


def get_settings_description():
    return __loadconfig().get('settings', 'description')


def set_settings_description(val):
    __persistchanges('settings', 'description', val)


def get_settings_copyright():
    return __loadconfig().get('settings', 'copyright')


def set_settings_copyright(val):
    __persistchanges('settings', 'copyright', val)


def get_settings_loglevel():
    return __loadconfig().getint('settings', 'loglevel')


def set_settings_loglevel(val):
    __persistchanges('settings', 'loglevel', val)


def get_settings_debug():
    return __loadconfig().getboolean('settings', 'debug')


def get_settings_debug_checkbox():
    if __loadconfig().getboolean('settings', 'debug'):
        return 'checked'
    else:
        return 'unchecked'


def set_settings_debug(val):
    if len(val) > 0:
        __persistchanges('settings', 'debug', 'True')
    else:
        __persistchanges('settings', 'debug', 'False')


# End Section "Settings" #

# Start Section "Color" #
def get_color_black_low():
    return __loadconfig().get('color', 'black_low')


def get_color_black_low_splited():
    return np.array([int(c) for c in get_color_black_low().split(',')])


def set_color_black_low(val):
    __persistchanges('color', 'black_low', val)


def get_color_black_high():
    return __loadconfig().get('color', 'black_high')


def get_color_black_high_splited():
    return np.array([int(c) for c in get_color_black_high().split(',')])


def set_color_black_high(val):
    __persistchanges('color', 'black_high', val)


def get_color_black():
    return __loadconfig().get('color', 'black')


def get_color_black_splited():
    return np.array([int(c) for c in get_color_black().split(',')])


def set_color_black(val):
    __persistchanges('color', 'black', val)


def get_color_white():
    return __loadconfig().get('color', 'white')


def get_color_white_splited():
    return np.array([int(c) for c in get_color_white().split(',')])


def set_color_white(val):
    __persistchanges('color', 'white', val)


def get_color_red():
    return __loadconfig().get('color', 'red')


def get_color_red_splited():
    return np.array([int(c) for c in get_color_red().split(',')])


def set_color_red(val):
    __persistchanges('color', 'red', val)


def get_color_green():
    return __loadconfig().get('color', 'green')


def get_color_green_splited():
    return np.array([int(c) for c in get_color_green().split(',')])


def set_color_green(val):
    __persistchanges('color', 'green', val)


def get_color_blue():
    return __loadconfig().get('color', 'blue')


def get_color_blue_splited():
    return np.array([int(c) for c in get_color_blue().split(',')])


def set_color_blue(val):
    __persistchanges('color', 'blue', val)


def get_color_cyan():
    return __loadconfig().get('color', 'cyan')


def get_color_cyan_splited():
    return np.array([int(c) for c in get_color_cyan().split(',')])


def set_color_cyan(val):
    __persistchanges('color', 'cyan', val)


def get_color_magenta():
    return __loadconfig().get('color', 'magenta')


def get_color_magenta_splited():
    return np.array([int(c) for c in get_color_magenta().split(',')])


def set_color_magenta(val):
    __persistchanges('color', 'magenta', val)


def get_color_yellow():
    return __loadconfig().get('color', 'yellow')


def get_color_yellow_splited():
    return np.array([int(c) for c in get_color_yellow().split(',')])


def set_color_yellow(val):
    __persistchanges('color', 'yellow', val)


def get_color_gray():
    return __loadconfig().get('color', 'gray')


def get_color_gray_splited():
    return np.array([int(c) for c in get_color_gray().split(',')])


def set_color_gray(val):
    __persistchanges('color', 'gray', val)


def get_color_orange():
    return __loadconfig().get('color', 'orange')


def get_color_orange_splited():
    return np.array([int(c) for c in get_color_orange().split(',')])


def set_color_orange(val):
    __persistchanges('color', 'orange', val)


# End Section "Color" #

# Start Section "Masktrafficlight" #

def get_masktrafficlight_red_low_l():
    return __loadconfig().get('mask_trafficlight', 'red_low_l')


def get_masktrafficlight_red_low_l_splited():
    return np.array([int(c) for c in get_masktrafficlight_red_low_l().split(',')])


def set_masktrafficlight_red_low_l(val):
    __persistchanges('mask_trafficlight', 'red_low_l', val)


def get_masktrafficlight_red_low_h():
    return __loadconfig().get('mask_trafficlight', 'red_low_h')


def get_masktrafficlight_red_low_h_splited():
    return np.array([int(c) for c in get_masktrafficlight_red_low_h().split(',')])


def set_masktrafficlight_red_low_h(val):
    __persistchanges('mask_trafficlight', 'red_low_h', val)


def get_masktrafficlight_red_high_l():
    return __loadconfig().get('mask_trafficlight', 'red_high_l')


def get_masktrafficlight_red_high_l_splited():
    return np.array([int(c) for c in get_masktrafficlight_red_high_l().split(',')])


def set_masktrafficlight_red_high_l(val):
    __persistchanges('mask_trafficlight', 'red_high_l', val)


def get_masktrafficlight_red_high_h():
    return __loadconfig().get('mask_trafficlight', 'red_high_h')


def get_masktrafficlight_red_high_h_splited():
    return np.array([int(c) for c in get_masktrafficlight_red_high_h().split(',')])


def set_masktrafficlight_red_high_h(val):
    __persistchanges('mask_trafficlight', 'red_high_h', val)


def get_masktrafficlight_green_l():
    return __loadconfig().get('mask_trafficlight', 'green_l')


def get_masktrafficlight_green_l_splited():
    return np.array([int(c) for c in get_masktrafficlight_green_l().split(',')])


def set_masktrafficlight_green_l(val):
    __persistchanges('mask_trafficlight', 'green_l', val)


def get_masktrafficlight_green_h():
    return __loadconfig().get('mask_trafficlight', 'green_h')


def get_masktrafficlight_green_h_splited():
    return np.array([int(c) for c in get_masktrafficlight_green_h().split(',')])


def set_masktrafficlight_green_h(val):
    __persistchanges('mask_trafficlight', 'green_h', val)


# End Section "Masktrafficlight" #

# Start Section "Maskletter" #


def get_maskletter_red_low_l():
    return __loadconfig().get('mask_letter', 'red_low_l')


def set_maskletter_red_low_l(val):
    __persistchanges('mask_letter', 'red_low_l', val)


def get_maskletter_red_low_h():
    return __loadconfig().get('mask_letter', 'red_low_h')


def set_maskletter_red_low_h(val):
    __persistchanges('mask_letter', 'red_low_h', val)


def get_maskletter_red_high_l():
    return __loadconfig().get('mask_letter', 'red_high_l')


def set_maskletter_red_high_l(val):
    __persistchanges('mask_letter', 'red_high_l', val)


def get_maskletter_red_high_h():
    return __loadconfig().get('mask_letter', 'red_high_h')


def set_maskletter_red_high_h(val):
    __persistchanges('mask_letter', 'red_high_h', val)


def get_maskletter_red_shift_l():
    return __loadconfig().get('mask_letter', 'red_shift_l')


def get_maskletter_red_shift_l_splited():
    return np.array([int(c) for c in get_maskletter_red_shift_l().split(',')])


def set_maskletter_red_shift_l(val):
    __persistchanges('mask_letter', 'red_shift_l', val)


def get_maskletter_red_shift_h():
    return __loadconfig().get('mask_letter', 'red_shift_h')


def get_maskletter_red_shift_h_splited():
    return np.array([int(c) for c in get_maskletter_red_shift_h().split(',')])


def set_maskletter_red_shift_h(val):
    __persistchanges('mask_letter', 'red_shift_h', val)


def get_maskletter_red_low_full():
    return __loadconfig().get('mask_letter', 'red_low_full')


def get_maskletter_red_low_full_splited():
    return np.array([int(c) for c in get_maskletter_red_low_full().split(',')])


def set_maskletter_red_low_full(val):
    __persistchanges('mask_letter', 'red_low_full', val)


def get_maskletter_red_high_full():
    return __loadconfig().get('mask_letter', 'red_high_full')


def get_maskletter_red_high_full_splited():
    return np.array([int(c) for c in get_maskletter_red_high_full().split(',')])


def set_maskletter_red_high_full(val):
    __persistchanges('mask_letter', 'red_high_full', val)


def get_maskletter_min_maskarea_size():
    return __loadconfig().getint('mask_letter', 'min_maskarea_size')


def set_maskletter_min_maskarea_size(val):
    __persistchanges('mask_letter', 'min_maskarea_size', val)


# End Section "Maskletter" #

# Start Section "Debug" #


def get_debug_output_red():
    return __loadconfig().getboolean('debug', 'output_red')


def get_debug_output_red_checkbox():
    if __loadconfig().getboolean('debug', 'output_red'):
        return 'checked'
    else:
        return 'unchecked'


def set_debug_output_red(val):
    if len(val) > 0:
        __persistchanges('debug', 'output_red', 'True')
    else:
        __persistchanges('debug', 'output_red', 'False')


def get_debug_output_green():
    return __loadconfig().getboolean('debug', 'output_green')


def get_debug_output_green_checkbox():
    if __loadconfig().getboolean('debug', 'output_green'):
        return 'checked'
    else:
        return 'unchecked'


def set_debug_output_green(val):
    if len(val) > 0:
        __persistchanges('debug', 'output_green', 'True')
    else:
        __persistchanges('debug', 'output_green', 'False')


def get_debug_output_bgwhite():
    return __loadconfig().getboolean('debug', 'output_bgwhite')


def get_debug_output_bgwhite_checkbox():
    if __loadconfig().getboolean('debug', 'output_bgwhite'):
        return 'checked'
    else:
        return 'unchecked'


def set_debug_output_bgwhite(val):
    if len(val) > 0:
        __persistchanges('debug', 'output_bgwhite', 'True')
    else:
        __persistchanges('debug', 'output_bgwhite', 'False')


def get_debug_logging_config():
    return __loadconfig().get('debug', 'logging_config')


def get_logging_config_fullpath():
    return __project_root_dir + __loadconfig().get('debug', 'logging_config')


def set_debug_logging_config(val):
    __persistchanges('debug', 'logging_config', val)


# End Section "Debug" #

# Start Section "Camera" #


def get_camera_width():
    return __loadconfig().getint('camera', 'width')


def set_camera_width(val):
    __persistchanges('camera', 'width', val)


def get_camera_height():
    return __loadconfig().getint('camera', 'height')


def set_camera_height(val):
    __persistchanges('camera', 'height', val)


def get_camera_framerate():
    return __loadconfig().getint('camera', 'framerate')


def set_camera_framerate(val):
    __persistchanges('camera', 'framerate', val)


def get_camera_iso():
    return __loadconfig().getint('camera', 'iso')


def set_camera_iso(val):
    __persistchanges('camera', 'iso', val)


def get_camera_awb():
    return __loadconfig().get('camera', 'awb')


def set_camera_awb(val):
    __persistchanges('camera', 'awb', val)


# End Section "Camera" #

# Start Section "Files" #


def get_files_multiimg1():
    return __loadconfig().get('files', 'multiimg1')


def set_files_multiimg1(val):
    __persistchanges('files', 'multiimg1', val)


def get_files_multiimg2():
    return __loadconfig().get('files', 'multiimg2')


def set_files_multiimg2(val):
    __persistchanges('files', 'multiimg2', val)


def get_files_multiimgcount():
    return __loadconfig().getint('files', 'multiimgcount')


def set_files_multiimgcount(val):
    __persistchanges('files', 'multiimgcount', val)


def get_files_video():
    return __loadconfig().get('files', 'video')


def set_files_video(val):
    __persistchanges('files', 'video', val)


def get_files_stream():
    return __loadconfig().getint('files', 'stream')


def set_files_stream(val):
    __persistchanges('files', 'stream', val)


# End Section "Files" #

# Start Section "Cropimage" #


def get_cropimage_width():
    return __loadconfig().getint('cropimage', 'width')


def set_cropimage_width(val):
    __persistchanges('cropimage', 'width', val)


def get_cropimage_height():
    return __loadconfig().getint('cropimage', 'height')


def set_cropimage_height(val):
    __persistchanges('cropimage', 'height', val)


# End Section "Cropimage" #

# Start Section "Imagetext" #


def get_imagetext_bordersize_left():
    return __loadconfig().getint('imagetext', 'bordersize_left')


def set_imagetext_bordersize_left(val):
    __persistchanges('imagetext', 'bordersize_left', val)


def get_imagetext_bordersize_top():
    return __loadconfig().getint('imagetext', 'bordersize_top')


def set_imagetext_bordersize_top(val):
    __persistchanges('imagetext', 'bordersize_top', val)


def get_imagetext_bordersize_bottom():
    return __loadconfig().getint('imagetext', 'bordersize_bottom')


def set_imagetext_bordersize_bottom(val):
    __persistchanges('imagetext', 'bordersize_bottom', val)


def get_imagetext_bordersize_right():
    return __loadconfig().getint('imagetext', 'bordersize_right')


def set_imagetext_bordersize_right(val):
    __persistchanges('imagetext', 'bordersize_right', val)


def get_imagetext_textspace():
    return __loadconfig().getint('imagetext', 'textspace')


def set_imagetext_textspace(val):
    __persistchanges('imagetext', 'textspace', val)


# End Section "Imagetext" #

# Start Section "Filter" #


def get_filter_kernel_size():
    return __loadconfig().getint('filter', 'kernel_size')


def set_filter_kernel_size(val):
    __persistchanges('filter', 'kernel_size', val)


def get_filter_hsv_shift():
    return __loadconfig().getint('filter', 'hsv_shift')


def set_filter_hsv_shift(val):
    __persistchanges('filter', 'hsv_shift', val)


# End Section "Filter" #

# Start Section "Letter" #


def get_letter_tolerance_i_gap():
    return __loadconfig().getint('letter', 'tolerance_i_gap')


def set_letter_tolerance_i_gap(val):
    __persistchanges('letter', 'tolerance_i_gap', val)


def get_letter_tolerance_v_gap():
    return __loadconfig().getint('letter', 'tolerance_v_gap')


def set_letter_tolerance_v_gap(val):
    __persistchanges('letter', 'tolerance_v_gap', val)


def get_letter_min_amount_processed_letters():
    return __loadconfig().getint('letter', 'min_amount_processed_letters')


def set_letter_min_amount_processed_letters(val):
    __persistchanges('letter', 'min_amount_processed_letters', val)

# End Section "Letter" #
