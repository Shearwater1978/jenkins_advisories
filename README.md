# Automatic sentinel to track affected Jenkins plugins

## Prerequisites

- Linux based OS
- Python3 preinstalled
- pyenv preinstalled
- make preinstalled

## How to run in demo mode
1. Execute command (predefined variables is actually for 2024 year)
```
make
```

2. Make sure there is a message in ouput about affected plugin "HTMLResource"
```
2024-01-01 23:59:20,099 - INFO - [ALARM] One or more plugin(-s) is affeted
2024-01-01 23:59:20,099 - INFO - The list of affected plugin(-s): ['HTMLResource']
```

## How to run in prod mode
1. Set up all env variables
2. Execute command
```
make check
```
