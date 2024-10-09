#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import math
import numpy as np

from sciveo.ml.images.object_detection import *


"""

Object Detection Evaluation

"""


class EvaluateObjectDetection:
  def __init__(self, X, Y_true, Y_predicted):
    self.X = X
    self.Y_true = Y_true
    self.Y_predicted = Y_predicted

  def evaluate(self):
    pass

