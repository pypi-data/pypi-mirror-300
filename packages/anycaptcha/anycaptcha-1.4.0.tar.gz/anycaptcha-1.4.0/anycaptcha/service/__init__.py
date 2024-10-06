import enum
from . import (
    anti_captcha,
    azcaptcha,
    captcha_guru,
    cptch_net,
    deathbycaptcha,
    rucaptcha,
    twocaptcha,
    multibot_captcha,
    sctg_captcha
)


class Service(enum.Enum):
    """CAPTCHA solving service enum"""

    ANTI_CAPTCHA        = "anti-captcha.com"
    AZCAPTCHA           = "azcaptcha.com"
    CAPTCHA_GURU        = "cap.guru"
    CPTCH_NET           = "cptch.net"
    DEATHBYCAPTCHA      = "deathbycaptcha.com"
    RUCAPTCHA           = "rucaptcha.com"
    TWOCAPTCHA          = "2captcha.com"
    MULTIBOT_CAPTCHA    = "multibot.in"
    SCTG_CAPTCHA        = "api.sctg.xyz"


# supported CAPTCHA solving services
SOLVING_SERVICE = {
    Service.ANTI_CAPTCHA: anti_captcha,
    Service.AZCAPTCHA: azcaptcha,
    Service.CAPTCHA_GURU: captcha_guru,
    Service.CPTCH_NET: cptch_net,
    Service.DEATHBYCAPTCHA: deathbycaptcha,
    Service.RUCAPTCHA: rucaptcha,
    Service.TWOCAPTCHA: twocaptcha,
    Service.MULTIBOT_CAPTCHA: multibot_captcha,
    Service.SCTG_CAPTCHA: sctg_captcha
}
