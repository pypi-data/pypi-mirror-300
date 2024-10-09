"""

设置应用中使用到的配置信息
"""
from AnyQt.QtCore import QSettings

# 默认服务器地址
DEFAULT_URL = 'https://bo.dashenglab.com'


def get_url():
    if QSettings().contains('account/service'):
        return QSettings().value('account/service')
    else:
        return DEFAULT_URL
