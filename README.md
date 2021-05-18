# Custom-Car-Dashboard
 A project of mine I have been working on for a long time to replace the center screen in my Subaru Legacy. Fully working for my build, Need to implement CAN Reading, Work out multitasking, and finish some things up; id say 80% done now??
 I have included the old CPP code for archival reasons; Its been so long I dont have the slightest clue how functional it is... Used PlatformIO and an ESP32, I didnt know if 2 cores on a little microcontroller would be enough. "go big or go home" It's prolly more safe because ik clusters usully run RTOS for saftey, but eh, It's just a display screen. Im not touching the cluster.... Maybe for """"FUN"""" I'll port it one day **shrug**

 [![](https://i.imgur.com/qkrK4sl.png[/img])](#) 

 The goal is to eventully release this as a completed, easily understood project for many and all to use, but I have to complete it first :) then spend 2,000 hours on documentation because I'm a psycopath and "like" doing that.

 Far from finished, thought I'd upload to git to have a "cloud" backup of over a thousnd? *thinking emoji* of hours of work into this project... including previous attempts and versions **thonk** 

 Current version intended to be ran on a linux machine, I had played with (and 75% wrote) the code for it to work on an ESP32 but decided to run it off the AtomicPi QuadCore SBC runining ubuntu 20 that I'll be installing in my car anyway... I am using my own library to communicate with the Nextion display. This project utilizes a 4.3 inch Nextion display (HMI); The display is programed seperatly (With the [Nextion Editor](https://nextion.tech/nextion-editor/)), and all the main code has to do is tell it what to do (over serial)

 
 See a demo of an older version on
 [YouTube](https://youtu.be/aLqDkDekaEg)

---
[SEE THE FULL ALBUM](https://imgur.com/a/RwYgJIP)

You can also check out the many more assets in ./Assets/ui

[![](https://i.imgur.com/OMguvC9.png[/img])](#) 

[![](https://i.imgur.com/g1dx1Ed.png[/img])](#) 
