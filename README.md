# tortoise-client

This repository contains several scripts to communicate with [tortoise-service][1].

- Inside temperature / humidity Sensor
- Outside temperature / humidity Sensor
- 433Mhz sender to control wireless power plugs (turn light on/off)
- 433Mhz receiver (not used in production)
- Webcam which sends pictures regulary
- Service-Client communictation (via websockets) to control 433Mhz sender and webcam.

## Hardware Wiring

```

  PI PIN                               INTERMEDIATE INTERFACE      DEVICE CONNECTORS
                __________________________
             __|____                    __|________________________________________
            |  |    |                  |  |                           ___TEMP2     |
         3V3|  x x__|5V_____________   |  x 01 VCC3        ~         |   |         |
            |  . .  |     __________|__|__x 02 GND         ~       __|_x | DATA    |
            |  . x__|GND_|   _______|__|__x 03 D1 (GPIO18)_~______|  | x | GND     |
       GPIO4|  x_.__|_______|_______|__|__x 04 D2 (GPIO4)__~_____    | x | VCC3    |
   ______GND|__x .  |       |  _____|__|__x 05 S  (GPIO17)_~___  |   |___|         |
  |  _GPIO17|__x x__|GPIO18_| |  ___|__|__x 06 R  (GPIO27)_~_  | |    ___TEMP1     |
  | | GPIO27|__x .  |         | |  _|__|__x 07 GND         ~ | | |   |   |         |
  | | |     |  . .  |         | | | |__|__x 08 VCC5        ~ | | |___|_x | DATA    |
  | | |     |  . .  |         | | |    |                     | |     | x | GND     |
  | | |     |  . .  |         | | |    |                     | |     | x | VCC3    |
  | | |     |  . .  |         | | |    |                     | |     |___|         |
  | | |     |  . .  |         | | |    |                     | |      ___RECEIVER  |
  | | |     |  . .  |         | | |    |                     | |     |   |         |
  | | |     |  . .  |         | | |    |                     | |_____|_x | DATA    |
  | | |     |  . .  |         | | |    |                     |       | x | GND     |
  | | |     |  . .  |         | | |    |                     |       | x | VCC5    |
  | | |     |  . .  |         | | |    |                     |       |___|         |
  | | |     |  . .  |         | | |    |                     |        ___SENDER    |
  | | |     |  . .  |         | | |    |                     |       |   |         |
  | | |     |  . .  |         | | |    |                     |_______|_x | DATA    |
  | | |     |_______|         | | |    |                             | x | GND     |
  | | |_______________________| | |    |                             | x | VCC5    |
  | |___________________________| |    |                             |___|         |
  |_______________________________|    |___________________________________________|

```

Setup based on

- [Raspberry Pi: Luftfeuchtigkeit und Temperatur messen][2]
- [github milaq / rpi-rf][3]
- [github ninjablocks / 433Utils][4]
- [Raspberry Pi Funksteckdosen (433MHz) steuern – Tutorial][5]


[1]: https://github.com/keksnicoh/turtle-service/

[2]: https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/
[3]: https://github.com/milaq/rpi-rf
[4]: https://github.com/ninjablocks/433Utils
[5]: https://tutorials-raspberrypi.de/raspberry-pi-funksteckdosen-433-mhz-steuern/

