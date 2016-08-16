# FoodLapse
Generate a daily timelapse of the [MIT Media Lab Foodcam](http://foodcam.media.mit.edu). This program was made to run on a Raspberry Pi 3. You can see example videos in the [video folder](html/videos/).

## Install dependencies
First, you'll need to install some dependencies : (opencv, avconv)

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python-opencv libopencv-dev
$ sudo apt-get -y install libav-tools
```

## Get the code
You can download the folder 'as it' and put it in a 'prog' folder in your home directory. (Or you can adjust the path in the scripts to make sure everything works)

## Set up the CRON
Edit the crontab file :

```
$ sudo crontab -e
```

Then add the following lines :

```
@reboot sh /home/pi/prog/utils/foodcamLauncher.sh >/home/pi/prog/utils/logs/foodcamlog 2>&1
01 00 * * * sh /home/pi/prog/utils/makeDailyVideo.sh >/home/pi/prog/utils/logs/makevidlog 2>&1
```

The first command starts the FoodLapse script when the Pi reboots and the second one start the 'make timelapse' script everyday at 00:01 AM

## Set up the Apache Web Server
Install Apache2 and PHP : 

```
$ sudo apt-get install apache2 -y
$ sudo apt-get install php5 libapache2-mod-php5 -y
```

Edit the apache2.conf file to change the root folder of the Apache server :

```
$ cd /etc/apache2
$ nano apache2.conf
```

You should edit the directory path like this :

```
<Directory /home/pi/prog/html>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```


