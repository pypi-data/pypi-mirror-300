import unittest
from few_shot_priming.argument_sampling.stance_priming import *
class StancePrimingUnitTest(unittest.TestCase):
    def testPercentilesCalc(self):
        path_similarity = "/bigwork/nhwpajjy/few-shot-priming-data/contrastive_learning/models/perspectrum-stance-similarties.json"
        thresholds = get_thresholds_for_percentiles("/bigwork/nhwpajjy/few-shot-priming-data/contrastive_learning/models/perspectrum-stance-similarties.json", 10)
        print(thresholds)