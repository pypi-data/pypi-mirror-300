from xsigmamodules.Analytics import (
    calibrationIrTargetsConfiguration,
    calibrationHjmSettings,
    correlationManager,
)
from xsigmamodules.util.numpy_support import xsigmaToNumpy, numpyToXsigma
from xsigmamodules.Market import discountCurvePiecewiseConstant, irVolatilitySurface
from xsigmamodules.Util import dayCountConvention

from itertools import chain


class market_data:
    def __init__(self, path):
        self.__target_config_ = calibrationIrTargetsConfiguration.read_from_json(
            path + "/Data/staticData/calibration_ir_targets_configuration.json"
        )
        self.__calibration_settings_ = calibrationHjmSettings.read_from_json(
            path + "/Data/staticData/calibration_ir_hjm_settings_3f.json"
        )
        self.__discount_curve_ = discountCurvePiecewiseConstant.read_from_json(
            path + "/Data/marketData/discount_curve_piecewise_constant.json"
        )
        self.__correlation_mgr_ = correlationManager.read_from_json(
            path + "/Data/marketData/correlation_manager.json"
        )
        self.__ir_volatility_surface_ = irVolatilitySurface.read_from_json(
            path + "/Data/marketData/ir_volatility_surface.json"
        )
        self.__convention_ = dayCountConvention.read_from_json(
            path + "/Data/staticData/day_count_convention_360.json"
        )
        self.__valuation_date_ = self.__discount_curve_.valuation_date()

    def valuation_date(self):
        return self.__valuation_date_

    def discountCurve(self):
        return self.__discount_curve_

    def irVolatilitySurface(self):
        return self.__ir_volatility_surface_

    def dayCountConvention(self):
        return self.__convention_

    def calibrationIrTargetsConfiguration(self):
        return self.__target_config_

    def calibrationIrHjmSettings(self):
        return self.__calibration_settings_

    def correlationManager(self):
        return self.__correlation_mgr_

    def correlation(self, diffusion_ids):
        correlation = self.__correlation_mgr_.pair_correlation_matrix(
            diffusion_ids, diffusion_ids
        )
        return correlation
