# Rules and Advice

<aside class="warning">
Safety is of your top concern when developing for Solo. 
</aside>

We recommend the following advice when developing:

**Remove your propellers.** If you have terminal access into Solo, *don't* have your propellers attached. Solo is a closed system with few internal safeguards. It is very easy to trigger the motors from the command line. Create an environment where this is not a problem.

**Turn off Solo when not in use.** There are several ways in which you can directly power Solo instead of using batteries. Because you are dealing with a live system, prevent excess wear by turning off the device when not in use.

**Prevent gimbal wear by turning your Solo upside down ("turtling").** The gimbal is disabled if Solo has an inverted Y axis. This prevents the gimbal from burning its motors while powered on for extended periods, in particular when there is no GoPro mounted in the gimbal.

**Remove and power cycle your GoPro frequently.** Normal operation will not cause the GoPro to freeze, but fiddling with video settings has the capacity to lock up your GoPro, which under exotic circumstances can also prevent Solo from booting properly. Check that the GoPro interface does not display strange errors (reading "9999" shots left, locking up, etc.) When in doubt, remove GoPro and reset your Solo.

[**Factory reset your Solo and The Controller to a known good state.**](starting-troubleshooting.html#factory-reset) Development on Solo involves making live modifications, which do not always play well with updates and can unintentionally break components on the system. Factory resetting is a reliable way to undo changes. On that note...

**Track all changes made to a live Solo system.** Because it is easy to restore the file system, it is just as easy to wipe away your changes by accident. Keep track!

