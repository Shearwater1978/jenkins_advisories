# Automatic sentinel to track affected Jenkins plugins

## Prerequisites

- Linux based OS
- Python3 preinstalled
- pyenv preinstalled
- make preinstalled

## How to run in demo mode
0. Open URL: https://www.jenkins.io/security/advisories/ and pick up any random plugin from the latest report. Look an example below
1. Execute command
```
SENSITIVE_PLUGINS='Git server' HOW_DEEP_ITEMS_LOOK_BACK=1 LOOKING_DAYS=31 make check
```

2. Make sure there is a message in ouput about selected affected plugin "Git server"
```
2024-02-06 23:59:34,179 - INFO - [ALARM] One or more plugin(-s) is affeted
2024-02-06 23:59:34,179 - INFO - The list of affected plugin(-s): ['Git server']
```

## How to run in prod mode
1. Set up all env variables
2. Execute command
```
make check
```
