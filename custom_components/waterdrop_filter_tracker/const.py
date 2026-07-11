"""Constants for Waterdrop Filter Tracker."""

DOMAIN = "waterdrop_filter_tracker"

CONF_FILTER_PRESET = "filter_preset"
CONF_FILTER_NAME = "filter_name"
CONF_INSTALL_DATE = "install_date"
CONF_RATED_LIFE_DAYS = "rated_life_days"
CONF_RATED_CAPACITY_GALLONS = "rated_capacity_gallons"
CONF_DAILY_USAGE_GALLONS = "daily_usage_gallons"

PRESET_CUSTOM = "custom"
PRESET_X12_F1A = "waterdrop_x12_f1a"
PRESET_X12_F2 = "waterdrop_x12_f2"
PRESET_X12_F3 = "waterdrop_x12_f3"

DEFAULT_FILTER_NAME = "Waterdrop Filter"
DEFAULT_RATED_LIFE_DAYS = 180
DEFAULT_RATED_CAPACITY_GALLONS = 400.0
DEFAULT_DAILY_USAGE_GALLONS = 2.0

FILTER_PRESETS = {
    PRESET_X12_F1A: {
        "label": "Waterdrop X12 F1A",
        "filter_name": "Waterdrop X12 F1A",
        "rated_life_days": 365,
        "rated_capacity_gallons": 1100.0,
    },
    PRESET_X12_F2: {
        "label": "Waterdrop X12 F2",
        "filter_name": "Waterdrop X12 F2",
        "rated_life_days": 180,
        "rated_capacity_gallons": 550.0,
    },
    PRESET_X12_F3: {
        "label": "Waterdrop X12-F3 RO membrane",
        "filter_name": "Waterdrop X12-F3 RO membrane",
        "rated_life_days": 730,
        "rated_capacity_gallons": 2900.0,
    },
}
