# NetBox - Sop-Voice plugin

> [NetBox](https://github.com/netbox-community/netbox) plugin to manage voice informations for each site.

## Installation

### Prerequisites

This plugin requires phonenumbers to work.

```bash
echo -e "phonenumbers" >> local_requirements.txt
```

### Auto-upgrade installation

Add the plugin to NetBox local_requirements
```bash
echo -e "sop_voice" >> local_requirements.txt
```

Add the plugin to netbox/configuration.py
```python
PLUGINS = [
    ...
    'sop_voice',
]
```

Run NetBox upgrade.sh script
```bash
sudo ./upgrade.sh
```

## Features

This plugin provides the following features:
-   Add a new "**Voice**" tab in */dcim/sites/your_site_id*
-   Add a new item "**Voice**" in the navigation menu bar
-   A fast voice-number quicksearch for every in-range numbers.

## Models

-   [**Voice Maintainer**](https://github.com/sop-it/sop-voice/tree/main/docs/voice-maintainer.md)
-   [**Voice Delivery**](https://github.com/sop-it/sop-voice/tree/main/docs/voice-delivery.md)
-   [**Voice DIDs**](https://github.com/sop-it/sop-voice/tree/main/docs/voice-dids.md)

## API

-   [**Voice API**](https://github.com/sop-it/sop-voice/tree/main/docs/api.md)
