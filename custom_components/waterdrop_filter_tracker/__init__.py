"""Waterdrop Filter Tracker integration."""

from __future__ import annotations

from datetime import date
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_FILTER_PRESET,
    CONF_INSTALL_DATE,
    DOMAIN,
    SERVICE_FIELD_ENTRY_ID,
    SERVICE_RESET_FILTER,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

RESET_FILTER_SCHEMA = vol.Schema(
    {
        vol.Optional(SERVICE_FIELD_ENTRY_ID): str,
        vol.Optional(CONF_FILTER_PRESET): str,
    }
)


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up Waterdrop Filter Tracker services."""

    async def async_reset_filter(call: ServiceCall) -> None:
        """Reset matching filter install dates to today."""
        entry_id = call.data.get(SERVICE_FIELD_ENTRY_ID)
        filter_preset = call.data.get(CONF_FILTER_PRESET)

        if entry_id is None and filter_preset is None:
            raise HomeAssistantError(
                "Provide either entry_id or filter_preset to reset a filter"
            )

        matching_entries = [
            entry
            for entry in hass.config_entries.async_entries(DOMAIN)
            if _entry_matches_reset_target(entry, entry_id, filter_preset)
        ]

        if not matching_entries:
            raise HomeAssistantError("No matching Waterdrop filter tracker found")

        install_date = date.today().isoformat()
        for entry in matching_entries:
            hass.config_entries.async_update_entry(
                entry,
                options={**entry.options, CONF_INSTALL_DATE: install_date},
            )

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESET_FILTER,
        async_reset_filter,
        schema=RESET_FILTER_SCHEMA,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Waterdrop Filter Tracker from a config entry."""
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


def _entry_matches_reset_target(
    entry: ConfigEntry,
    entry_id: str | None,
    filter_preset: str | None,
) -> bool:
    """Return whether a config entry matches the reset service target."""
    if entry_id is not None and entry.entry_id != entry_id:
        return False

    if filter_preset is not None:
        data = {**entry.data, **entry.options}
        if data.get(CONF_FILTER_PRESET) != filter_preset:
            return False

    return True
