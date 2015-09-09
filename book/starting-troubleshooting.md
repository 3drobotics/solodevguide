# Troubleshooting

## Factory resetting
Factory resetting is the most reliable way to undo changes that break your system. To factory reset your Solo back to the "Gold Master" state, follow the [Factory Reset Procedure](http://3drobotics.com/kb/factory-reset/).

<aside class="note">
We are working on a programmatic way to [re-flash Solo and the Controller](https://github.com/3drobotics/solodevguide/issues/5).
</aside>

## Fetching System Logs

On both Solo and the Controller, system logs live in the `/log` directory and have the suffix `.log[.n]` (this folder is actually a dedicated partition and separate from the system partition). These logs roll over at every boot, such that the current log is always `.log`, the previous log is renamed to `.log.1`, `.log.1` is renamed to `.log.2`, and so on. Only 20 logs are saved in total, so filling up the log partition will not be an issue.

_**ShotManager**_ logs are named `shotlog.log.n`. and contain various high level events triggered by the shots, such as received input and which mode Pixhawk is transitioning into. If *ShotManager* happens to crash, in most cases the Python stack trace will be written to the log.

<aside class="todo">
Explain what the other files found in this directory are.
</aside>
