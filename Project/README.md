# Project

## Install Dependencies

```shell
$ pip install -r requirements.txt
```

## Start

```shell
$ python main.py
```

## Configuration Tasks

- Configure tasks in setup_scheduler() in main.py
- if you want to add a task, add a tuple type element to the tasks[] array like: `(taskFunc, trigger)`
  - taskFunc, is a function type variable
  - trigger, can be a CronTrigger or an IntervalTrigger (more details see the doc of apscheduler)
