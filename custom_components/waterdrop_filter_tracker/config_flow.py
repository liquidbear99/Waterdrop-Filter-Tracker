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
    CONF_INSTALL_DATE,
    CONF_RATED_CAPACITY_GALLONS,
    CONF_RATED_LIFE_DAYS,
    DEFAULT_DAILY_USAGE_GALLONS,
    DEFAULT_FILTER_NAME,
    DEFAULT_RATED_CAPACITY_GALLONS,
    DEFAULT_RATED_LIFE_DAYS,
    DOMAIN,
)


def _data_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
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

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_FILTER_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_data_schema(),
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

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Manage the integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        defaults = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_data_schema(defaults),
        )
