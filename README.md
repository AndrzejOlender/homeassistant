#  Home Assistant Configuration Files

## Server
* [ Intel NUC NUC7i3BNH, i3-7100U CPU 2.40GHz, 16GB RAM](https://ark.intel.com/content/www/us/en/ark/products/95066/intel-nuc-kit-nuc7i3bnh.html) (Ubuntu Server)
* Home Assistant in Kubernetes instalation ([Helm Charts](https://gitlab.olender.io/andrzej/infrastructure/-/tree/master/nuc/helm))

## ZigBee Devices
### ZigBee Adapter 
* [Texas Instruments LAUNCHXL-CC1352P-2](https://www.zigbee2mqtt.io/information/supported_adapters.html#texas-instruments-launchxl-cc1352p-2)

### Lights
* [Aqara bulb ZNLDP12LM](https://www.zigbee2mqtt.io/devices/ZNLDP12LM.html) x1
* [Ikea bulb GU10 LED1650R5](https://www.zigbee2mqtt.io/devices/LED1650R5.html) x11
* [Ikea bulb LED1649C5](https://www.zigbee2mqtt.io/devices/LED1649C5.html) x4
* [Ikea bulb RGB LED1624G9](https://www.zigbee2mqtt.io/devices/LED1624G9.html) x1
* [Osram bulb RGB AC08559](https://www.zigbee2mqtt.io/devices/AC08559.html) x3

### Switches
* [Aqara WXKG11LM](https://www.zigbee2mqtt.io/devices/WXKG11LM.html) x2
* [Aqara WXKG03LM](https://www.zigbee2mqtt.io/devices/WXKG03LM.html) x4
* [Aqara WXKG02LM](https://www.zigbee2mqtt.io/devices/WXKG02LM.html) x4

### Lock
* [Danalock V3-BTZB](https://www.zigbee2mqtt.io/devices/V3-BTZB.html) x1

### Thermostats
* [Eurotronic SPZB0001](https://www.zigbee2mqtt.io/devices/SPZB0001.html) x3

### Leak Sensors
* [Aqara SJCGQ11LM](https://www.zigbee2mqtt.io/devices/SJCGQ11LM.html) x2

### Motion Sensors
* [Aqara RTCGQ11LM](https://www.zigbee2mqtt.io/devices/RTCGQ11LM.html) x5

### Contact Sensor
* [Aqara MCCGQ11LM](https://www.zigbee2mqtt.io/devices/MCCGQ11LM.html) x7

### Vibration Sensor
* [Aqara DJT11LM](https://www.zigbee2mqtt.io/devices/DJT11LM.html) x1

## Wifi Devices
### Power Plugs
* [BlitWolf BW-SHP6](https://www.blitzwolf.com/BlitzWolf-BW-SHP6-2300W-WIFI-Smart-Socket-EU-Plug-Works-with-Alexa-Remote-Control-Time-Switch-Electricity-Monitoring-p-300.html) x7 ([eshome](https://gitlab.olender.io/andrzej/homeassistant/-/tree/master/esphome))
* [Shelly 2.5](https://shelly.cloud/products/shelly-25-smart-home-automation-relay/) x2 ([esphome](https://gitlab.olender.io/andrzej/homeassistant/-/tree/master/esphome))

### Air Purifier
* [Xiaomi Air Purifier 2S](https://www.mi.com/in/air2s/) x1

### IR Controller
* [Xiaomi Universal IR](https://www.gearbest.com/smart-home/pp_229556.html) x1

### Voice Assistants
* [Amazon Echo Dot 3](https://www.amazon.com/Echo-Dot/dp/B07FZ8S74R) x1
* [Amazon Echo Dot 4](https://www.amazon.com/All-New-Echo-Dot-4th-Gen/dp/B07XJ8C8F5) x1
* [Siri](https://www.apple.com/siri/) (iPhone, Apple Watch)

### Media Players
* [LG WebOS](https://www.lg.com/global/business/webos) x1
* [AppleTV 4K](https://www.apple.com/apple-tv-4k/) x1
* [Amazon Echo Dot 3](https://www.amazon.com/Echo-Dot/dp/B07FZ8S74R) x1

## Integrations
* [Mobile App](https://apps.apple.com/us/app/home-assistant-companion/id1099568401) (iPhone, Android, MacOS)
* [MQTT](https://www.home-assistant.io/integrations/mqtt/)
* [HomeKit](https://www.home-assistant.io/integrations/homekit/)
* [Airly](https://github.com/bieniu/ha-airly)
* [Speedtest](https://www.home-assistant.io/integrations/speedtestdotnet/)
* [Alexa Media Player](https://github.com/custom-components/alexa_media_player)
* [HACS](https://github.com/custom-components/hacs)
* [Burze dzi??](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net)
* [LG WebOS](https://www.home-assistant.io/integrations/webostv/)
* [Mini Graph Card](https://github.com/kalkih/mini-graph-card)

## Screenshots
### Main 
![HA.png](image/HA-20201231.png)
### Zigbee Mesh
![HA-zigbbe-mesh.png](image/HA-zigbbe-mesh.png)
