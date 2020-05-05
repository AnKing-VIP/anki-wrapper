import sys

from aqt import mw
from aqt.utils import showWarning


userOption = None
addon = mw.addonManager.addonFromModule(__name__)
default = mw.addonManager.addonConfigDefaults(__name__)

def _getUserOption():
    global userOption
    if userOption is None:
        userOption = mw.addonManager.getConfig(__name__)


def getUserOption(keys=None, **kwargs):
    """Get the user option if it is set. Otherwise return the default
    value and add it to the config.
    When an add-on was updated, new config keys were not added. This
    was a problem because user never discover those configs. By adding
    it to the config file, users will see the option and can configure it.
    If keys is a list of string [key1, key2, ... keyn], it means that
    config[key1], ..., config[key1]..[key n-1] are dicts and we want
    to get config[key1]..[keyn]
    """
    _getUserOption()
    if keys is None:
        return userOption
    if isinstance(keys, str):
        keys = [keys]

    try:
        default_value = kwargs['default']
    except KeyError:
        default_on_block = False
    else:
        default_on_block = True

    # Path in the list of dict
    current = userOption
    current_default = default
    change = False
    for key in keys:
        if default_on_block and not isinstance(current, dict):
            return default_value
        else:
            assert isinstance(current, dict)

        if key not in current:
            try:
                current[key] = current_default[key]
                change = True
            except (TypeError, KeyError):
                return default_value
        if isinstance(current_default, dict) and key in current_default:
            current_default = current_default[key]
        else:
            current_default = None
        try:
            current = current[key]
        except (TypeError, KeyError):
            return default_value

    if change:
        writeConfig()
    return current

def writeConfig():
    mw.addonManager.writeConfig(__name__, userOption)




def update(_):
    global userOption, fromName
    userOption = None
    fromName = None


mw.addonManager.setConfigUpdatedAction(__name__, update)

fromName = None


def getFromName(name):
    global fromName
    if fromName is None:
        fromName = dict()
        for dic in getUserOption("columns"):
            fromName[dic["name"]] = dic
    return fromName.get(name)


def setUserOption(key, value):
    _getUserOption()
    userOption[key] = value
    writeConfig()

