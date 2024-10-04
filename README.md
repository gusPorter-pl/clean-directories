## Clean directories

A python script that checks the specified folders for expired contents.

### config.json

Specify a `directories` object that contains file paths and corresponding days until files and directories should be removed.

```json
{
  "directories": {
    "C:/ProgramData/JetBrains/TeamCity/system/artifacts/MainBuildChain/*": 90,
    "C:/ProgramData/JetBrains/TeamCity/system/artifacts/OtherBuildChain/*": 90,
    "C:/ProgramData/JetBrains/TeamCity/system/artifacts/Integration/": 30
  }
}
```

- A '\*' at the end indicates to check all those subfolders.

### \logs

All runs will be logged to a `\logs` folder.

### clean_directories.py

- `setup_log_file()`: Creates the log file and returns the absolute path of the file.
- `load_config()`: Loads the directories from the config file. a '\*' will loop through the subfolders of the directory specified, adding all to the directories dictionary.
- `clean_directories()`: Loops through each directory, and calls `remove_old_files()`.
- `remove_old_files()`: Checks all files in the directory recursively. If they were last modified past the specified time delta, then they are removed. This returns an `items_deleted` count.

### Task Scheduler

#### Open Task Scheduler:

Press Windows + S and search for Task Scheduler.

#### Create a New Task:

In the Actions pane, click Create Task.
Give the task a name (e.g. DiskCleanup).

#### Set the Trigger:

Go to the Triggers tab and click New.
Set the trigger to Weekly and choose Sunday at 11:00 PM.

#### Set the Action:

Go to the Actions tab and click New.
For Action, select Start a program.
In the Program/script field, enter the path to your Python executable (e.g., C:\path\to\python.exe).
In the Add arguments field, enter the path to your script (e.g., C:/path/to/your_script.py).

#### Finish:

Click OK to save the task. The script will now run every Sunday at 11 PM.

#### Testing

To test, refresh and select 'Task Scheduler Library' on the left tab.
The task should be displayed. Right-click and select 'Run'.
It will not tell you when it is done, you will have to refresh again.
Then check the logs to see the outcome.
