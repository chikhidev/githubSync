GitSync is an open source tool to keep your local git directories up to date by synchronizing them at regular intervals. It supports daily, weekly, and monthly synchronization schedules.

## Features

- Add directories to the synchronization list
- Remove directories from the synchronization list
- List all directories in the synchronization list
- Enable or disable the synchronization tool
- Configure synchronization interval and commit message
- Run synchronization manually or on a schedule
- Logs synchronization activities to a log file
- Queues synchronization tasks to ensure they run even if the computer is shut down before the scheduled time

## Installation

To install the required dependencies, run the `setup.sh` script:

```sh
./setup.sh
```

This script will install the necessary Python libraries and set up an alias for the gitsync command.

## Usage

### Commands

- `add .`: Add a directory to the synchronization list
- `remove .`: Remove a directory from the synchronization list
- `list`: List all directories in the synchronization list
- `enable`: Enable the synchronization tool
- `disable`: Disable the synchronization tool
- `config [-m, --message, -i, --interval]`: Configure the synchronization tool
    - `-m, --message <message>`: Set the commit message
    - `-i, --interval <interval>`: Set the synchronization interval (number of minutes, daily, weekly, monthly)
- `run`: Synchronize all directories immediately, use this command in case you want to push manually, or use a shortcut for it, or implement it in a crontab job!
- `run:scheduler` || `run:scheduler&` : Start the scheduler to synchronize directories according to the configured interval, use this command if you dont have cron, start it in a terminal that is gonna be opened for period you want to keep syncing your projects
- `logs`: Open the log file
- `logs:clear`: Clear the log file
- `help`: Display the help menu
- `version` || `--version` || `-v`: Display the version of the tool
- `status`: Display whether the tool is enabled or disabled

### Example Usage

- Add a directory to the synchronization list:
    ```sh
    cd /path/to/directory
    gitsync add .
    ```

- Remove a directory from the synchronization list:
    ```sh
    cd /path/to/directory
    gitsync remove .
    ```

- List all directories in the synchronization list:
    ```sh
    gitsync list
    ```

- Enable the synchronization tool:
    ```sh
    gitsync enable
    ```

- Disable the synchronization tool:
    ```sh
    gitsync disable
    ```

- Configure the synchronization interval:
    ```sh
    gitsync config --interval daily
    ```

- Configure the commit message:
    ```sh
    gitsync config --message "Updated via GitSync"
    ```

- Run synchronization manually (use this command in case you want to push manually, or use a shortcut for it, or implement it in a crontab job!)
    ```sh
    gitsync run
    ```

- Start the scheduler (use this command if you dont have cron, start it in a terminal that is gonna be opened for period you want to keep syncing your projects):
    ```sh
    gitsync run:scheduler&
    ```

- Open the log file:
    ```sh
    gitsync logs
    ```

- Clear the log file:
    ```sh
    gitsync logs:clear
    ```

- Display the help menu:
    ```sh
    gitsync help
    ```

- Display the version of the tool:
    ```sh
    gitsync version
    ```

- Display whether the tool is enabled or disabled:
    ```sh
    gitsync status
    ```

## Notes

- The tool is only available for Linux.
- Ensure that the directories you add are valid git repositories and you have the necessary permissions to access them.
- Synchronization activities are logged to a log file located at `~/.gitsync/gitsync.log`.
- Synchronization tasks are queued to ensure they run even if the computer is shut down before the scheduled time.

## License

This project is licensed under the MIT License.