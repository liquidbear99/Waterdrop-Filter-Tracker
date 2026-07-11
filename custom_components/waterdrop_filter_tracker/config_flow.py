"""Config flow for Waterdrop Filter Tracker."""

from __future__ import annotations

from datetime import date
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_DAILY_USAGE_GALLONS,
    CONF_FILTER_NAME,
    CONF_FILTER_PRESET,
    CONF_INSTALL_DATE,
    CONF_RATED_CAPACITY_GALLONS,
    CONF_RATED_LIFE_DAYS,
    DEFAULT_DAILY_USAGE_GALLONS,
    DEFAULT_FILTER_NAME,
    DEFAULT_RATED_CAPACITY_GALLONS,
    DEFAULT_RATED_LIFE_DAYS,
    DOMAIN,
    FILTER_PRESETS,
    PRESET_CUSTOM,
)


def _preset_schema(default_preset: str = PRESET_CUSTOM) -> vol.Schema:
    """Build the preset selection schema."""
    options = [
        selector.SelectOptionDict(value=PRESET_CUSTOM, label="Custom"),
        *(
            selector.SelectOptionDict(value=preset_key, label=preset["label"])
            for preset_key, preset in FILTER_PRESETS.items()
        ),
    ]

    return vol.Schema(
        {
            vol.Required(
                CONF_FILTER_PRESET,
                default=default_preset,
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


def _defaults_for_preset(
    preset_key: str,
    defaults: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Merge saved/default data with preset defaults."""
    merged_defaults = defaults.copy() if defaults else {}
    preset = FILTER_PRESETS.get(preset_key)
    if preset is None:
        return merged_defaults

    merged_defaults[CONF_FILTER_NAME] = preset["filter_name"]
    merged_defaults[CONF_RATED_LIFE_DAYS] = preset["rated_life_days"]
    return merged_defaults


def _data_schema(
    defaults: dict[str, Any] | None = None,
) -> vol.Schema:
    """Build the config/options schema."""
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_FILTER_NAME,
                default=defaults.get(CONF_FILTER_NAME, DEFAULT_FILTER_NAME),
            ): selector.TextSelector(),
            vol.Required(
                CONF_INSTALL_DATE,
                default=defaults.get(CONF_INSTALL_DATE, date.today().isoformat()),
            ): selector.DateSelector(),
            vol.Required(
                CONF_RATED_LIFE_DAYS,
                default=defaults.get(CONF_RATED_LIFE_DAYS, DEFAULT_RATED_LIFE_DAYS),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=3650,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="days",
                )
            ),
            vol.Required(
                CONF_RATED_CAPACITY_GALLONS,
                default=defaults.get(
                    CONF_RATED_CAPACITY_GALLONS,
                    DEFAULT_RATED_CAPACITY_GALLONS,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=100000,
                    mode=selector.NumberSelectorMode.BOX,
                    step=0.1,
                    unit_of_measurement="gal",
                )
            ),
            vol.Required(
                CONF_DAILY_USAGE_GALLONS,
                default=defaults.get(
                    CONF_DAILY_USAGE_GALLONS,
                    DEFAULT_DAILY_USAGE_GALLONS,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0.1,
                    max=1000,
                    mode=selector.NumberSelectorMode.BOX,
                    step=0.1,
                    unit_of_measurement="gal/day",
                )
            ),
        }
    )


class WaterdropFilterTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waterdrop Filter Tracker."""

    VERSION = 1
    _selected_preset: str

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Select a Waterdrop filter preset."""
        if user_input is not None:
            self._selected_preset = user_input[CONF_FILTER_PRESET]
            return await self.async_step_filter_details()

        return self.async_show_form(
            step_id="user",
            data_schema=_preset_schema(),
        )

    async def async_step_filter_details(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle filter details after preset selection."""
        if user_input is not None:
            user_input[CONF_FILTER_PRESET] = self._selected_preset
            return self.async_create_entry(
                title=user_input[CONF_FILTER_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="filter_details",
            data_schema=_data_schema(_defaults_for_preset(self._selected_preset)),
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> WaterdropFilterTrackerOptionsFlow:
        """Create the options flow."""
        return WaterdropFilterTrackerOptionsFlow(config_entry)


class WaterdropFilterTrackerOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Waterdrop Filter Tracker."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry
        self._selected_preset: str = PRESET_CUSTOM

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Select a Waterdrop filter preset for options."""
        if user_input is not None:
            self._selected_preset = user_input[CONF_FILTER_PRESET]
            return await self.async_step_filter_details()

        defaults = {**self._config_entry.data, **self._config_entry.options}
        default_preset = str(defaults.get(CONF_FILTER_PRESET, PRESET_CUSTOM))
        return self.async_show_form(
            step_id="init",
            data_schema=_preset_schema(default_preset),
        )

    async def async_step_filter_details(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Manage the integration options."""
        if user_input is not None:
            user_input[CONF_FILTER_PRESET] = self._selected_preset
            return self.async_create_entry(title="", data=user_input)

        defaults = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(
            step_id="filter_details",
            data_schema=_data_schema(
                _defaults_for_preset(self._selected_preset, defaults),
            ),
        )
