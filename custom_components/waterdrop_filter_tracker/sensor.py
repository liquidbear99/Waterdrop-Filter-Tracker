"""Sensors for Waterdrop Filter Tracker."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTime, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

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


@dataclass(frozen=True)
class FilterMetrics:
    """Calculated filter metrics."""

    filter_name: str
    installed_on: date
    rated_life_days: int
    rated_capacity_gallons: float
    daily_usage_gallons: float
    elapsed_days: int
    estimated_used_gallons: float
    remaining_days: int
    remaining_life_percent: float
    remaining_gallons: float
    replacement_date: date

    @classmethod
    def from_entry(cls, entry: ConfigEntry) -> FilterMetrics:
        """Build metrics from a config entry."""
        data = {**entry.data, **entry.options}
        installed_on = date.fromisoformat(
            data.get(CONF_INSTALL_DATE, dt_util.now().date().isoformat())
        )
        rated_life_days = int(data.get(CONF_RATED_LIFE_DAYS, DEFAULT_RATED_LIFE_DAYS))
        rated_capacity_gallons = float(
            data.get(CONF_RATED_CAPACITY_GALLONS, DEFAULT_RATED_CAPACITY_GALLONS)
        )
        daily_usage_gallons = float(
            data.get(CONF_DAILY_USAGE_GALLONS, DEFAULT_DAILY_USAGE_GALLONS)
        )
        elapsed_days = max(0, (dt_util.now().date() - installed_on).days)
        estimated_used_gallons = min(
            rated_capacity_gallons,
            elapsed_days * daily_usage_gallons,
        )
        remaining_gallons = max(0.0, rated_capacity_gallons - estimated_used_gallons)
        remaining_days_by_capacity = (
            remaining_gallons / daily_usage_gallons if daily_usage_gallons > 0 else 0
        )
        remaining_days_by_time = rated_life_days - elapsed_days
        remaining_days = max(
            0,
            int(min(remaining_days_by_time, remaining_days_by_capacity)),
        )
        remaining_life_percent = round(
            max(0.0, min(100.0, (remaining_days / rated_life_days) * 100)),
            1,
        )
        replacement_days = min(
            rated_life_days,
            int(rated_capacity_gallons / daily_usage_gallons)
            if daily_usage_gallons > 0
            else rated_life_days,
        )

        return cls(
            filter_name=str(data.get(CONF_FILTER_NAME, DEFAULT_FILTER_NAME)),
            installed_on=installed_on,
            rated_life_days=rated_life_days,
            rated_capacity_gallons=round(rated_capacity_gallons, 1),
            daily_usage_gallons=round(daily_usage_gallons, 1),
            elapsed_days=elapsed_days,
            estimated_used_gallons=round(estimated_used_gallons, 1),
            remaining_days=remaining_days,
            remaining_life_percent=remaining_life_percent,
            remaining_gallons=round(remaining_gallons, 1),
            replacement_date=installed_on + timedelta(days=replacement_days),
        )


@dataclass(frozen=True, kw_only=True)
class WaterdropSensorEntityDescription(SensorEntityDescription):
    """Description for a Waterdrop sensor."""

    value_fn: Callable[[FilterMetrics], Any]


SENSOR_DESCRIPTIONS: tuple[WaterdropSensorEntityDescription, ...] = (
    WaterdropSensorEntityDescription(
        key="days_remaining",
        translation_key="days_remaining",
        native_unit_of_measurement=UnitOfTime.DAYS,
        device_class=SensorDeviceClass.DURATION,
        value_fn=lambda metrics: metrics.remaining_days,
    ),
    WaterdropSensorEntityDescription(
        key="life_remaining",
        translation_key="life_remaining",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda metrics: metrics.remaining_life_percent,
    ),
    WaterdropSensorEntityDescription(
        key="estimated_used",
        translation_key="estimated_used",
        native_unit_of_measurement=UnitOfVolume.GALLONS,
        value_fn=lambda metrics: metrics.estimated_used_gallons,
    ),
    WaterdropSensorEntityDescription(
        key="gallons_remaining",
        translation_key="gallons_remaining",
        native_unit_of_measurement=UnitOfVolume.GALLONS,
        value_fn=lambda metrics: metrics.remaining_gallons,
    ),
    WaterdropSensorEntityDescription(
        key="replacement_date",
        translation_key="replacement_date",
        device_class=SensorDeviceClass.DATE,
        value_fn=lambda metrics: metrics.replacement_date,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Waterdrop Filter Tracker sensors."""
    async_add_entities(
        WaterdropFilterSensor(entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class WaterdropFilterSensor(SensorEntity):
    """Waterdrop filter metric sensor."""

    entity_description: WaterdropSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        description: WaterdropSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer="Waterdrop",
            name=entry.title,
            model="Filter Tracker",
        )

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        metrics = FilterMetrics.from_entry(self._entry)
        return self.entity_description.value_fn(metrics)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return filter calculation details."""
        metrics = FilterMetrics.from_entry(self._entry)
        return {
            "filter_name": metrics.filter_name,
            "installed_on": metrics.installed_on.isoformat(),
            "rated_life_days": metrics.rated_life_days,
            "rated_capacity_gallons": metrics.rated_capacity_gallons,
            "daily_usage_gallons": metrics.daily_usage_gallons,
            "elapsed_days": metrics.elapsed_days,
        }
