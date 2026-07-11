# Waterdrop Filter Tracker

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

Current version: `v1.0.0`
