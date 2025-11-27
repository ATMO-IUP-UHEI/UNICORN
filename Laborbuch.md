# Laborbuch für Unicorn-Nodes

node-wise timeline to easily find what you are looking for

## Node 1
| Date | Remark |
|----------|----------|
| 2024-12-03    | - back from workshop, installed Vaisala sensor (orginally assigned to node 5, plug deformed, but fixed) <br> - made disk image <br> - connected to Ethernet switch -> ip: 129.206.29.114 <br> - changed **password -> LAXnetwork241**   | 
| 2024-12-04    | - opened node 1 (next to node 5), burned candle for ca 1 min @ 8:55 UTC <br> -continued measurement ~5 mins  until 9:25 UTC   | 
| 2024-12-06    | - node 1 installed at the roof @12:00 UTC   | 
| 2025-05-16| - interior check: disconnected 12:30 UTC <br> - Vaisala serial no. N3720018; single power sources, mount of chemical sensors broken <br> - reconnect 12:36 UTC |
| 2025-07-29 | - installed wireguard <br> - tried changing password, but resets to LAXnetwork241 after each reboot <br> - noticed broken CO2-data since 2025-05-02 21:55:10 UTC <br> - unplugged from roof, taken to Lab 13:15 UTC |
| 2025-07-30 | - re-fastened damaged Vaisala connector, works for now <br> - re-installed node 1 on roof 09:37 UTC |
| 2025-08-06 | - changed **password -> CO2unicorn241** via temporary fix: <br> added *'beacon:CO2unicorn2401'|chpasswd* in /etc/rc.local <br> frshly sets the password during each boot |
| 2025-10-15    | -  ethernet unplugged at 11:41 UTC (noise reduction experiments)  |
| 2025-10-01 | - reconnected ethernet 11:30 UTC | 
| 2025-10-22 | - unplugged 12:26 UTC for interior check <br> - re-mounted electrochemical sensor (glued mounting fell of) <br> - re-plugin 12:50 UTC |  
| 2025-11-25 | - noticed noisy CO2 data since 2025-11-17 -> refastened Vaisala Connection <br> noticed also that e-chem. mounting losened again (improvised double sided tape, fixed temporary, should be re-done permanently with good tape <br> - power off between 12:00 and 12:07 UTC |

## Node 2
| Date | Remark |
|----------|----------|
| 2024-10-09    | - installed Vaisalla sensor   | 
| 2024-11-11    | - refurbishment from workshop finished (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding) <br> - installed Vaisala sensor <br> - made disk image -> /home/kvbuenau <br> -test: RaspPi recieves no power, power supply 12V and gorund ok, suspect problem with 5V DCDC converter <br> - ground of 5V DCDC converter floats -> need new terminals (12V), "Zugentlastung" and functional ground|
| 2024-12-12    | - returned node 2 to workshop to redo cables between power supply, DCDC conv and RaspPi, add functional ground   | 
|2024-11-14 | - recieved node 2 back from workshop with new cabling <br> - tested connection of ground, RaspPi now works <br> - changed **password -> LAXnetwork242** <br> - started lab test measurement (closed casing) @14:00 UTC |
| 2024-11-18 | - interrupted measurement shortly to check IP-address (129.206.29.48). closed again @ 13:40 UTC |
| 2024-11-21 | - opened node 2 for documentation @ 09:45 |
| 2024-12-04 | - brought node 2 to the roof, installation ~14/15:00 |
| 2025-02-12 | - removed node 2 from roof 9:00 UTC <br> - node 2 left at Czernyring, waiting for for Niklas Hevendehl open port acces|
| 2025-02-18 | - fixed conf file for wireguard connection <br> - mounted at Czernyring ~11UTC <br> - fixed IP (.32) <br> - weatherproof extension cable used|
|2025-03-12| - check data usage: installed vnstet on Node 2 -> 1MB/5min ? <br> -> data usage is around: daemon -> network communication (wouldn't be the case for LTE)|
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2402** |

## Node 3
| Date | Remark |
|----------|----------|
| 2024-10-04    | - disassembled case, installed Vaisalla sensor attached via zip-ties <br> - removed US-type plug, installed cable with open contacts & protective conductor <br> - grounded casing, "Zugentlastung for cables", cable connection scheme (US-DE): <br> L black -brown <br> N red - blue <br> blue - yellow <br> - raspberry pi login: user:beacon, passwrd:CO2Network2012 <br> - set WIFI details under /etc/wpa-supplicant/wpa_supplicant.conf , need admin rights (sudo nano [filename]) <br> - get IP-address for ssh acces (same user, passwd) via 'ip addr show' <br> - verified date/time: RTC and RPI (system time) correspond to UTC <br> - data check: realistic values for T, RH, p, T_dwq, O3, CO, NO, NO2, 0  for PM-values, (-999) for hight cts, low cts and particulate % <br> - high CO2 values (1130ppm) -> indoors w/o airflow <br> -measurements every 5s <br> - Raspberry Pi storage: 65MB/962MB occupied   | 
| 2024-10-07    | - made disk image of RaspPi SD-Card stored as .zip-> home/kvbuenau   | 
| 2024-10-09      | - test measurement in the lab, windows opened @ 12:45 and 13:00 UTC   | 
| 2024-10-10 | - tried to install eduroam on RaspPi -> unsuccesfull <br> - changed login password -> LAXnetzwerk243|
| 2024-10-21 | - test measurement series in lab 11:05 to 12:37 UTC, parallel roomtemp measurement with datlogger|
| 2024-10-23 | - longer test measurement with open case started at 11:30 |
| 2024-10-24 | - continued measurement, closed node at 14:05, short measurement interruption|
| 2024-10-25 | - interrupted measurement bet. 11-13:00 UTC, attempted change of settings <br> - installed Vaisalle USB device finder (unsuccesfull) <br> - tried direct connection of Vaisalla sensor to laptop, further installed drivers (checked via lsusb connected devices) -> still unsucessfull |
| 2024-12-04 | opened node 4 @ 9:20 UTC <br> - connected DC-DC to Oscill: <br> 12VDC-5VDC conv: AC signal on osci, frequency 1/(2mus), peak to peak 100mv, cope visible. with screwscp: right 12V, middle ground, left 5V <br> - disconnected AC-DC converter from DC-DC -> no AC signal on oscilloscope <br> -> AC signal comes from 12V-5V converter, probable reason for noise <br> -> need new step up/step down 12V-5V converter |
|2025-01-10 | - node 3 back from workshop <br> - started lab test measurement @11:00 UTC |
|2025-01-13 | - installed node 3 at rooftop|
|2025-02-06 | - brought node 3 down from roof, checked compensations (Oxygen ON, p,T,RH OFF) <br> - turned ON T,p,RH compensations and returned node 3 to roof |
|2025-02-18| - removed node 3 from roof to return settings to original (no T,p,RH correction) ~14:00 UTC <br> - brought node 3 up to the roof|
|2025-04-09 | - taken down from roof ~14:30 UTC |
|2025-04-17 | - installed wireguard on nodes 3 and 4 <br> - 14:45 UTC installed node 3 at Moritz' place in Eppelheim, connection via WiFi |
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2403** |
| 2025-05-07 | - node 3 disconnected 07:03-07:11 CEST and 18:23-18:26 CEST to reestablish wireguard connection |
| 2025-05-12 | - connected node 3 to LAN at 08:30 CEST <br> - fixed cronjob typo <br> - changed password to new scheme (again?) -> **CO2unicorn2403** <br> - rebooted several times <br> - wpa_supplicant is mowked(?)|
|2025-05-13 | - open node 18:20 CEST <br> -two reboots 19:00 & 19:10 CEST <br> - closed 19:20 CEST |
|2025-06-29 | - exhanged power cable 09:10 UTC |

## Node 4
| Date | Remark |
|----------|----------|
| 2024-10-24    | - connected Vaisalla sensor to Laptop, access via Arduino 101 programme   | 
| 2024-11-11    | - refurbishment from workshop finished (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding) <br> - installed Vaisala sensor <br> - made disk image -> /home/kvbuenau <br> - connected to monitor, checked IP-address <br> - closed node 4 for test lab measurement around 15:15 UTC   | 
| 2024-11-12    | - opened node 4 around 10:00 UTC to connect via ethernet <br> - returned node 4 to workshop to redo cables between power supply, DCDC conv and RaspPi, add functional ground    | 
|2024-11-14 | - recieved node 4 back from workshop with new cabling <br> - one cable was cut (potentially connection to vaisala?) <br> - changed **password -> LAXnetwork244** <br> - now measures CO2 <br> -started lab test measurement @14:06 UTC |
|2024-11-20 | - notice strong noise <br> - unplug electricity and all cables, restart to see noise behaviour |
| 2024-11-25 | - unplug, checked gorund connections <br> - powered with lab power source via contacts directly from 15:45 UTC for ~1h |
| 2024-11-26 | - another connection to lab power source ~ 8:00 UTC <br> - brought to workshop for power source check |
| 2024-11-27 | - workshop suggestion : try opposite way of how to plug in <br> - start test measurement at 11:00 to check if noise decreases <br> - using ethernet switch from now on -> ip: 129.206.29.122 |
|2024-12-10 | - measured max. current of RPI, for 12V: 450mA -> P=5.4W , for 5V -> 1A -> output current 5V DC-DC converter > 2A |
|2025-01-10 | - node 4+5 in workshop to install new 5V ACDC-converters to fix noise problems |
|2025-01-20 | - node 4+5 back from workshop <br> - started test measurement to see if noise improved |
|2025-02-05 | - node 4 installed on roof @13:45 UTC |
|2025-04-09 | - taken down from roof ~14:30 UTC |
|2025-04-17 | - installed wireguard on nodes 3 and 4 <br> - 13:00 UTC installed node 4 at ITP/Philosophenweg with pipe clamp mounting from workshop <br> - no data connection yet |
| 2025-05-26 | - exchanged power cord, unplug 15:17-15:24 UTC|
| 2025-07-03 | - installed LTE, fixed Wireguard <br> - changed Password -> **CO2unicorn2404** <br> - power off 11:28-12:55 UTC |
| 2025-11-03 | - added functional ground (negative terminal from both power supplies seperately to casing ground) <br> - unplugged between 14:17 and 14:37 UTC |



## Node 5
| Date | Remark |
|----------|----------|
| 2024-11-25    | - recieved back from workshop, started measurement @11:00 UTC   | 
| 2024-11-27    | - made RaspPi disk image <br> - changed **password -> LAXnetwork245** <br> - using ethernet switch from now on -> ip: 129.206.29.58 <br> - Vaisala sensor: connection plug is deformed -> use Vaisala sensor from node 1 for the moment and report problem | 
|2025-01-10 | - node 4+5 in workshop to install new 5V ACDC-converters to fix noise problems |
|2025-01-20 | - node 4+5 back from workshop <br> - started test measurement to see if noise improved |
|2025-02-05 | - node 5 disconnected for half an hour at 15:00 UTC to check Vaisala settings <br> - HyperTRM.exe(htpe7) -> settings in document from Berkeley|
|2025-02-12 | node 5: attempt WIFI connection 14:30 UTC, WIFI adapter: Edimax EW-76II ULB |
|2025-02-13 | - installed wireguard on node 5 after backup -> follow wireguard.md manual by Ralph <br> - sucessfull connection and re-connection after network reset |
|2025-02-18| - brought node 5 up to the roof
|2025-03-12 | - measured data use > 100MB/day (10MB/day expected) <br> - install vinstat on Node 5 +contact Berkley <br> - sudo vinstat -i eth0 enable -> high traffic on eth0 <br> -> data usage is around: daemon -> network communication (wouldn't be the case for LTE)|
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2405** | 
|2025-04-23 | - 12:30-13:00 UTC disconnected node 5 for checking settings <br> - 14:05 UTC reconnected node 5 - settings were ok |
| 2025-05-16| - interior check: disconnected 12:22 UTC <br> - Vaisala serial no. N470003; two power sources, no bridged minus terminals <br> - reconnect 12:25 UTC |
| 2025-06-12 | - disconnected node 5 09:49 UTC for return to vaisala (warranty checks for high temp-corssensitivity) |
| 2025-09-02 | - reassembled returned vaisala sensor (N4740003) and installed at roof 11:36 UTC |
| 2025-10-02 | - noticed missing data for nodes 5 and 17 between Sept 22 and Oct 2nd <br> reason: blown fuse of rooftop electricity supply box (already occured twice with this outlet a few months earlier, noted in fuse cabinet logbook)|
| 2025-10-29 | - disabled Wi-Fi (via dtoverlay=disable_wifi entry in /boot/config.txt - comment out to re-activate) to see if there is an effect on noise, reboot 15:00 UTC | 

## Node 6
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-06-04    | - installed vaisalla sensor (serial no. W3530002) <br> - powered for setup and wireguard @ 11:39 UTC <br> - changed passwd -> **CO2unicorn2406** <br> - plugged LTE stick with new Vodafone Sim (card nr. 30 2452 0094 383 3D) in -> wireguard works initially <br> - dis- and reconnected USB dongle -> connection persists   | 
| 2025-06-16    | - disconnected node 6 @ 12:37 UTC for PoE testing   | 
| 2025-06-18 | - powered node 6 @11:12 UTC for PoE testing <br> - remark: Vaisala sensor was shortly powered with wrong polarity, but seems unharmed | 

## Node 7
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-07-08    | - installed Vaisalle sensor Ser.No. W3510002 <br> - power on 12:53 UTC, passwd -> **CO2unicorn2407** <br> - re-set time and date <br> - installed wireguard <br> - shutdown 14:01 UTC   | 
| 2025-07-09    | - installed at roof 12:05 UTC   | 
| 2025-10-15    | -  ethernet unplugged at 11:36, re-plug 11:40 (noise reduction experiments)  | 
| 2025-10-22 | - taken from roof to workshop (unplug 11:57 UTC) <br> - changed functional ground of power supplies (try to reduce noise) <br> - re-plugin on roof: 12:50 UTC |

## Node 8
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-05-22    | - installed Vaisala sensor serial-no. W3530003 <br> - plug in 13:00 UTC, check Vaisala function and install wireguard <br> - change passwd -> **CO2unicorn2408** <br> - wireguard installation succesfull, had to re-set RPI and RTC time according to berkley manual <br> - unplug 14:17 UTC   | 
| 2025-05-23    | - installation on roof @13:56 UTC   | 
| 2025-09-09 | - unplug 09:25 UTC for visit at Pumpwerk Sandhofen, not set-up yet |
| 2025-10-02 | - installed at Pumpwerk Sandhofen 06:58 UTC |

## Node 9
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-04-08    | - borught up nodes 9,12,13,16,18 <br> - configuration with connected minus terminals <br> - installed Vaisala sensors in nodes 9,12 and 13   | 
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2409** | 
| 2025-05-08 | - connected node 9 to monitor power with Jackery 13:45 UTC -> ~12 W <br> - Ralph to measure USB dongle|
| 2025-05-19 | - setup wireguard in lab 09:15-09:55 UTC <br> - 11:15 installation on roof <br> - 11:25 start measurement|
| 2025-07-21 | - unplugged node 9 12:03 UTC, installed mounting for Stadtbücherei |
| 2025-08-13 | - installed node 9 at Stadtbücherei <br> - used SIM: card nr. 312452 1594 661 4 D* <br> - powered on 07:33 UTC |

## Node 10
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   |
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-03-11    | - nodes 11 and 10 brought to Lab from workshop after refurbishment   |   
| 2025-04-09    | - connected negative terminals in nodes 10,11,14  <br> - MAC-addr: b8:27:eb:9f:6f:f3 <br> - roof measurement started 14:30 UTC|  
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2410** | 
|2025-05-20 | - stopped measurement 11:15 UTC <br> - tried to add wifi <br> - reconnect 11:48 UTC |
|2025-05-21 | - 10:45 UTC stopped roof measurement <br> - 10:55 UTC plug-in in lab for wireguard installtion <br> - 12:40 UTC wireguard installation succesful <br> - 12:52 UTC restart roof measurement|
|2025-06-20 | - disconnect node 10 from roof @10:18 UTC for Collegium Academicum installation <br> - connected node 10 @12:49 UTC at Collegium Academicum |

## Node 11
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-03-11    | - node 11 and 14 brought to Lab from workshop after refurbishment   | 
| 2025-04-09    | - connected negative terminals in nodes 10,11,14 <br> - MAC-addr: b8:27:eb:1c:79:65   |  
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2411** | 
| 2025-04-23 | - ~12:30 UTC connected node 11, started measurement |
|2025-05-19 | - noticed problems (node not running) <br> - 11:30 disconnected <br> - 11:33 tried different outlets <br> - 11:35 restart measurement|
| 2025-07-08 | - unplugged 07:35 UTC, installed at UB, yet without power connection (to be done by electrician) |

## Node 12
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-04-08    | - borught up nodes 9,12,13,16,18 <br> - configuration with connected minus terminals <br> - installed Vaisala sensors in nodes 9,12 and 13   | 
| 2025-05-22 | - 09:40 UTC wireguard installation in lab <br> - changed passwd -> **CO2unicorn2412** <br> wireguard installation succesfull, unplugged 11:29 UTC| 
| 2025-05-23    | - installation on roof @ 14:24 UTC   | 
| 2025-09-18 | - unplug 11:08 UTC <br> - brought to Werkstatt for change to 24V supply |
| 2025-10-29 | - connected in lab for heating experiment v2 (control node) 13:15 UTC, LTE Stick |
| 2025-11-04 | - removed power supplies from casing, set up as temporary lab test with power supplies external, 1m away from node <br> - unplugged between 13:40 and 15:19 UTC |
| 2025-11-05 | - noticed less noise in trace gas sensors, however increased noise in CO2 <br> - tried removing the connection between the - terminals (possible inductive loop with vaisala USB connector) <br> - power off around 11:30 UTC |
|2025-11-06 | - no change noticed, tried to reduce 12V cable length by re-connecting - terminals of power supply, - connector of vaisala on WAGO-Klemme with 5V - cables. <br> - unplugged from 13:10 to 13:20 UTC |
| 2025-11-10 | - next try in reducing noise: power supplies as close to the node casing as possible (short cables), wrapped supplies and node casing losely in aluminium foil <br> - unplugged between 14:30 and 14:50 UTC |
| 2025-11-12 | - tried switching the supplies position to side of the sensor, away from openings <br> -down between 10:00 and 10:20 UTC |
| 2025-11-18 | - noted strong increase in e-chem. sensor noise since Nov.13, 03:30 UTC <br> - no external explanation. Interior check: Fan by the em-sensors was not working. Worked again after re-connecting to e-chem. board. <br> running since 12:10 UTC | 
| 2025-11-19 | - installed Capacitors directly next to Vaisalla sensor <br> - test first with close power supplies at side of node. Later planned with longer cables to see if "antenna" effect is diminished <br> - shut off for installation 13:00-14:00 UTC |
| 2025-11-20 | - changed to long-cable-setup to see if there is a positive effect of capacitors |  
| 2025-11-25 | - re-wired the problematic 5V fan directly to the power supply (not via echem-sensors) <br> - noticed loose connection directly at fan, needs replacement <br> - unplugged 14:45 to 15:25 UTC |
| 2025-11-26 | - closer fan examination with oscilloscope to see noise-producing RF impulses, <br> - node off/open between 11:30 UTC and 14:00 UTC | 
## Node 13
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-04-08    | - borught up nodes 9,12,13,16,18 <br> - configuration with connected minus terminals <br> - installed Vaisala sensors in nodes 9,12 and 13   |  
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2413** | 
| 2025-05-21    | - connected for wireguard installation 09:05-09:40 UTC <br> - started roof measurement 10:43 UTC   | 
| 2025-09-02 | - unplug 08:52 UTC -> NRW campaign |
| 2025-10-14 | - brought to R226 for CO-zero-measurement. power ~11:10 UTC |
| 2025-10-22 | - started heating experiment via headlight 12:26 UTC |
| 2025-10-23 | - stopped heating experiment 13:54 UTC <br> - node still running in R226 |
| 2025-10-29 | - connected in lab for heating experiment v2 13:00 UTC , LAN|

## Node 14
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-03-14    | - brought and prepared node 14 for LTE tests <br> - lab meas should start ~14 UTC, first with disconnected CO2 <br> - user called DEnode14 -> **covers may be switched!** <br> - set **passwd -> LAXnetwork254** <br> - connected lte dongle to usb0 <br> - sudo dhclient usb0 <br> - opened MAC for ethernet as pia_raspi6 <br> - bought 4 weeks 2GB data <br> - set DHCP consistent for usb0 (nano /etc/dhcpd.conf)  <br> ->  interface usb0 , fallback static, at the end of the file install vnstat, wireguard (copied script from another node via scp), iftop <br> - removing Dongle causes tunnels to appear temporarily in ifconfig <br> - 15:00 UTC connected CO2-sensor, node running successful via LTE   |
| 2025-03-17    | - 10-12 UTC unplugged CO2 to connect keyboard   | 
| 2025-04-09    | - connected negative terminals in nodes 10,11,14 <br> - roof measurement started 14:30 UTC  |  
|2025-04-22 | - changed pwd to new scheme -> **CO2unicorn2414** |
|2025-04-23 | - connected to node 14 via Wifi router (Ralph) <br> - fixed crontab typo <br> -> couldn't connect via wireguard and stopped bc of rain |
|2025-05-14 | - 15:00 UTC several reboots, setup wifi with phone hotspot <br> solution: <br> sudo systemctl enable wpa_supplicant@wlan0.service <br> sudo systemctl start wpa_supplicant@wlan0.service <br> systemctl status wpa_supplicant@wlan0.service <br> reboot |
|2025-05-25 | - checked data: weather data & PM missing/strange since Jan 2025 <br> - 14:30 UTC reboot <br> - 15:15 UTC power off, start repairs, change USB port <br> - 15:19 UTC power on, weather data looks normal -> for calibration use neighboring node (1 or 10) data |
| 2025-05-16| - disconnected 12:38 UTC for Seckenheim installation |


## Node 15
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-07-08 | - installed Vaisala sensor (Ser.No. W3520004), power on @14:11 UTC <br> - changed passwd -> **CO2unicorn2415** <br> - installed wireguard <br> - shutdown @14:57 UTC |
| 2025-07-09    | - powered at roof 11:49 UTC   | 
| 2025-10-29 | - removed from roof 10:22 UTC |
| 2025-11-03 | - setup for co-location at OPI (radiation effects, noise reduction tests) <br> - plug in 14:37 UTC |


## Node 16
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-04-08    | - borught up nodes 9,12,13,16,18 <br> - configuration with connected minus terminals  |  
| 2025-08-14 | - installed vaisala sensor No. W3530001 <br> - powered for setup 11:29 UTC <br> - changed **password -> CO2unicorn2416** (needed same fix as for node1 (set passwd during boot via rc.local)) <br> - time was freshly set <br> - installed wireguard <br> - power off 12:18 UTC |
| 2025-09-02 | - brought to roof, plug-in 09:12 UTC |
| 2025-10-29 | - removed from roof 10:22 UTC |
| 2025-10-29 | - connected in lab for heating experiment v2 (control node) 13:08 UTC , LAN|

## Node 17
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-08-14 | - installed vaisala sensor no. W3510001 <br> - power on 12:28 UTC <br> - changed passwd -> **CO2unicorn2417**, needed temporary rc.local-fix to do that <br> - installed wireguard <br> - power off 13:16 UTC |
| 2025-09-18 | - installed at roof 11:17 UTC |
| 2025-10-02 | - noticed missing data for nodes 5 and 17 between Sept 22 and Oct 2nd <br> reason: blown fuse of rooftop electricity supply box (already occured twice with this outlet a few months earlier, noted in fuse cabinet logbook)|

## Node 18
| Date | Remark |
|----------|----------|
| 2025-01-09    | - brought node 6-18 to workshop for refurbishment (power plug, ethernet feed-through, RPI isolation and mounting, power supply mounting, case grounding)   | 
| 2025-04-08    | - borught up nodes 9,12,13,16,18 <br> - configuration with connected minus terminals  |   
