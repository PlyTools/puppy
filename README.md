# puppy
This is a control system of the little car, kitte.
You need to follow the steps below to perform it.

# Step 1: set static IP of raspiberry wifi connection
As an example, it was set default to 192.168.3.111
+ open dhcpcd.conf
```
sudo vim /etc/dhcpcd.conf
```
+ add config at the end of dhcpcd.conf
```
interface wlan0       
static ip_address=192.168.3.111            #static IP
static routers=192.168.3.1                 #address of router
static domain_name_servers=192.168.3.1 114.114.114.114     #address of DNS
```

# Step 2: modify the ip config in config/config.py
In this example, the IP of my PC is 192.168.3.4, so you need to modify raspi_ip and compu_ip as the below
```
raspi_ip = '192.168.3.111'
compu_ip = '192.168.3.4'
```

# Step 3: run
+ make both raspiberry and pc connect to a same wifi
+ run compu_main.py on pc
```
python compu_main.py
```
+ run raspi_main.py on raspiberry
```
python raspi_main.py
```

enjoy yourself
