# Waterdrop Filter Tracker

![Waterdrop Filter Tracker icon](https://raw.githubusercontent.com/liquidbear99/Waterdrop-Filter-Tracker/main/brand/icon.png)

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
4. Enter the filter name, installation date, rated life, rated capacity, and
   estimated daily usage.

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

Current version: `v1.0.1`

## HACS Compliance

This repository is structured as a HACS integration repository:

- `hacs.json` is in the repository root.
- The integration lives under `custom_components/waterdrop_filter_tracker`.
- The integration manifest includes `domain`, `documentation`, `issue_tracker`,
  `codeowners`, `name`, and `version`.
- Brand assets live under `brand/`.
- GitHub Actions validate the repository with HACS and Hassfest.
