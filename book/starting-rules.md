# Rules and Advice

<aside class="caution">
Safety must be your top concern when developing for Solo. 
</aside>

We recommend the following advice when developing:

**Remove your propellers.** Solo is a closed system with few internal safeguards&mdash;it is very easy to trigger the motors from the command line. Create an environment where this is not a problem by removing your propellers whenever you are about to have terminal access into Solo. 

**Turn off Solo when not in use.** There are several ways in which you can directly power Solo instead of using batteries. Because you are dealing with a live system, prevent excess wear by turning off the device when not in use.

**Disable gimbal activity by turning your Solo upside down ("turtling").**  The gimbal is disabled if Solo has an inverted Y axis. You can use this feature to prevent the gimbal from moving during development, or if you have no camera installed.

**Remove and power cycle your GoPro frequently.** The GoPro will not freeze in normal operation, but may do so if you modify the video pipeline (under exotic circumstances this may additionally prevent Solo from booting properly). Check that the GoPro interface does not display strange errors, i.e. reading "9999" shots left, becoming unresponsive to user input, etc. When in doubt, remove the GoPro and restart your Solo.

[**Factory reset your Solo and the Controller to a known good state.**](starting-troubleshooting.html#factory-resetting) Development on Solo involves making live modifications, which do not always play well with updates and can unintentionally break components on the system. Factory resetting is a reliable way to undo changes. On that note...

**Track all changes made to a live Solo system.** Because it is easy to restore the file system, it is just as easy to wipe away your changes by accident. Keep track!

