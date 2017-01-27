import numpy as np
import autoFocus.focus as af
import cv2
from nose.tools import *
from utils.cvUtils import  get_images_from_dir
import pdb

class TestDetector(object):
    @classmethod
    def setup_class(self):
        self.image = cv2.imread("tests/test_yag_images_01/image01.jpg", 
                                cv2.IMREAD_GRAYSCALE)
    def test_scanfocus_correctness_01(self):
        const = 0
        mot = VirtualMotorTest(self.image)
        cam = VirtualCameraTest(mot, const=const)
        pos = (-11, 11, 2)
        focus = af.Focus(motor_pv=mot, camera_pv=cam, positions=pos)
        res = focus.focus()
        assert res == -1 + const or res == 1 + const

class VirtualMotorTest(af.VirtualMotor):
    """Virtual motor class until the real one works."""
    def __init__(self, image, const=0):
        self.image = image
        self.num_motors = 1
        self.cur_position = None
        self.name="Test Virtual Motor"
    def mv(self, pos):
	    self.cur_position = pos
    def wm(self):
        return self.cur_position
    def wait(self):
	    pass

class VirtualCameraTest(af.VirtualCamera):
    """Virtual camera class until one is found/implemented."""
    def __init__(self, motor, const=0):
        self.motor = motor
        self.const = int(const)
    def _get_kernel(self):
        return int(np.ceil(abs(self.motor.wm())) + self.const)
    def get(self):
        print self.motor.wm()
        kernel = self._get_kernel()
        return cv2.GaussianBlur(self.motor.image, (kernel, kernel), 0)
	