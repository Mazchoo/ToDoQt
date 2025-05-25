![image](https://github.com/user-attachments/assets/c09581d4-b1ac-4c3c-ab61-f33b72d99f9b)

## Description

Project manager that can:
* Create projects that summarise progress
* Add tasks to project with three states: pending, doing and done
* Can add estimates and record time spend in tasks in doing state
* Add descriptions with markdown to tasks and projects
* Can use emoji's in titles (very important)

Made using PyQt5.

## Installation

Using only pip and the command line

```
pip install -r requirements.txt
python main.py
```

## Usage Example

* Add a project name to the line edit next to "Add New Project"
* Click "Add New Project"
* Edit the description of the project under "Project Description"
* Add a task name to the line edit next to "Add New Task" button
* Click "Add New Task"
* Edit the description of the task under "Task Description"
* Drag and drop the task into Doing
* Add an estimate to the task (by default points are added at 1 point per hour)
* Click "Log Time" to record time in the task
* Move the task into done when finished
* Click "Backup" to save changes locally
