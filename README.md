# Automatic sentinel to track affected Jenkins plugins

## Prerequisites

- Linux based OS
- Python3 preinstalled
- pyenv preinstalled
- make preinstalled

## How to run in demo mode
* Open URL: https://www.jenkins.io/security/advisories/ and pick up any random plugin from the latest report.
* Adjust the number of days for value ```LOOKING_DAYS```. Execute command
```
SENSITIVE_PLUGINS='Git server' HOW_DEEP_ITEMS_LOOK_BACK=1 LOOKING_DAYS=31 make check
```

* Make sure there is a message in the output about the affected plugin "Git server"
```
2024-02-06 23:59:34,179 - INFO - [ALARM] One or more plugin(-s) is affeted
2024-02-06 23:59:34,179 - INFO - The list of affected plugin(-s): ['Git server']
```

## How to run in prod mode
* Set up all env variables
* Execute command:
```
make check
```
