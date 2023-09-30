"""
 * Author:    Andreas Naoum
 * Created:   30.09.2023
 *
 * (c) Copyright iDeal
"""
from enum import Enum


class Deal(Enum):
    NONE = "Nan"
    STEAL = "Steal"
    ELITE = "Elite"
    SPEEDY = "Speedy"

    def get_discount_range(self):
        if self.STEAL:
            return 0.4, 0.7
        elif self.ELITE:
            return 0.2, 0.3
        elif self.SPEEDY:
            return 0.2, 0.5
        else:
            return 0.0, 0.01


class ProfitMargin(Enum):
    LOW = 1.2  # 120%
    MEDIUM = 1.5  # 150%
    HIGH = 2.0  # 200%