# Troubleshooting

## Factory resetting
Factory resetting is the most reliable way to undo changes that break your system. To factory reset your Solo back to the "Gold Master" state, follow the [Factory Reset Procedure](http://3drobotics.com/kb/factory-reset/).

<aside class="note">
We are working on a programmatic way to [reflash Solo and the Controller](https://github.com/3drobotics/solodevguide/issues/5).
</aside>

## Fetching System Logs

On both Solo and the Controller, system logs live in the `/log` directory. (This folder is actually a dedicated partition and separate from the system partition.) These are files ending in the suffix `.log`. These roll over every boot, such that the current log is always `.log`, next is `.log.1`, `.log.2`, etc. Only 20 logs are saved in total, so filling up the log partition will not be an issue.

_**ShotManager**_ logs are named `shotlog.log.n`. and contain various high level events triggered by the shots, such as received input and which mode Pixhawk is transitioning into. If *ShotManager* happens to crash, in most cases the Python exception and callstack will be written to this log as the last event.

<aside class="todo">
Explain what the other files found in this directory are.
</aside>
