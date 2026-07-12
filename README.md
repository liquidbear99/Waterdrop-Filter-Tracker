# Waterdrop Filter Tracker

![Waterdrop Filter Tracker icon](https://raw.githubusercontent.com/liquidbear99/Waterdrop-Filter-Tracker/main/custom_components/waterdrop_filter_tracker/brand/icon.png)

A HACS-ready Home Assistant custom integration for tracking Waterdrop filter
replacement timing from installation date, rated lifespan, rated capacity, and
estimated daily usage.

## Installation

### HACS

1. Open HACS in Home Assistant.
2. Go to **Integrations**.
3. Open the menu and choose **Custom repositories**.
4. Add this repository URL:

   `https://github.com/liquidbear99/Waterdrop-Filter-Tracker`

5. Select **Integration** as the category.
6. Install **Waterdrop Filter Tracker**.
7. Restart Home Assistant.

You can also open the custom repository form directly with this My Home
Assistant link:

[![Open your Home Assistant instance and add this repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=liquidbear99&repository=Waterdrop-Filter-Tracker&category=integration)

### Manual

Copy `custom_components/waterdrop_filter_tracker` into your Home Assistant
`custom_components` directory, then restart Home Assistant.

## Setup

1. In Home Assistant, go to **Settings > Devices & services**.
2. Select **Add integration**.
3. Search for **Waterdrop Filter Tracker**.
4. Choose a preset or **Custom**, then enter the installation date and estimated
   daily usage. Presets fill in rated life and capacity, and both values remain
   editable.

Available reverse osmosis presets:

- Waterdrop X12 F1A: 12 months, up to 1,100 gallons
- Waterdrop X12 F2: 6 months, up to 550 gallons
- Waterdrop X12-F3 RO membrane: 24 months, up to 2,900 gallons

## Sensors

The integration creates sensors for:

- Days remaining
- Life remaining percentage
- Estimated gallons used
- Gallons remaining
- Estimated replacement date

The replacement estimate is calculated from the more conservative of time-based
life and capacity-based life.

## Release

Current version: `v1.1.2`

## Reset Service

The integration provides `waterdrop_filter_tracker.reset_filter` for dashboard
buttons and automations. Pass either `filter_preset` or `entry_id`; the matching
tracker installation date is reset to today.

Example:

```yaml
action: waterdrop_filter_tracker.reset_filter
data:
  filter_preset: waterdrop_x12_f1a
```

## Dashboard Card

This dashboard card shows replacement dates, life remaining gauges, and
press-and-hold reset buttons for the three Waterdrop X12 filters. Update the
entity IDs if Home Assistant generated different names.

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Waterdrop X12 Filters
    show_header_toggle: false
    entities:
      - entity: sensor.waterdrop_x12_f1a_replacement_date
        name: F1A replacement date
      - entity: sensor.waterdrop_x12_f2_replacement_date
        name: F2 replacement date
      - entity: sensor.waterdrop_x12_f3_ro_membrane_replacement_date
        name: X12-F3 RO replacement date

  - type: grid
    columns: 3
    square: false
    cards:
      - type: gauge
        entity: sensor.waterdrop_x12_f1a_life_remaining
        name: F1A Life
        min: 0
        max: 100
        severity:
          green: 25
          yellow: 15
          red: 0
        needle: true
      - type: gauge
        entity: sensor.waterdrop_x12_f2_life_remaining
        name: F2 Life
        min: 0
        max: 100
        severity:
          green: 25
          yellow: 15
          red: 0
        needle: true
      - type: gauge
        entity: sensor.waterdrop_x12_f3_ro_membrane_life_remaining
        name: X12-F3 RO Life
        min: 0
        max: 100
        severity:
          green: 25
          yellow: 15
          red: 0
        needle: true

  - type: grid
    columns: 3
    square: false
    cards:
      - type: button
        name: Reset F1A
        icon: mdi:filter-sync
        show_state: false
        tap_action:
          action: none
        hold_action:
          action: call-service
          service: waterdrop_filter_tracker.reset_filter
          data:
            filter_preset: waterdrop_x12_f1a
      - type: button
        name: Reset F2
        icon: mdi:filter-sync
        show_state: false
        tap_action:
          action: none
        hold_action:
          action: call-service
          service: waterdrop_filter_tracker.reset_filter
          data:
            filter_preset: waterdrop_x12_f2
      - type: button
        name: Reset X12-F3
        icon: mdi:filter-sync
        show_state: false
        tap_action:
          action: none
        hold_action:
          action: call-service
          service: waterdrop_filter_tracker.reset_filter
          data:
            filter_preset: waterdrop_x12_f3
```

## HACS Compliance

This repository is structured as a HACS integration repository:

- `hacs.json` is in the repository root.
- The integration lives under `custom_components/waterdrop_filter_tracker`.
- The integration manifest includes `domain`, `documentation`, `issue_tracker`,
  `codeowners`, `name`, and `version`.
- Brand assets live under `custom_components/waterdrop_filter_tracker/brand/`.
- GitHub Actions validate the repository with HACS and Hassfest.
