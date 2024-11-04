# GitSync

GitSync is a tool to keep your local git directories up to date by synchronizing them at regular intervals. It supports daily, weekly, and monthly synchronization schedules.

## Features

- Add directories to the synchronization list
- Remove directories from the synchronization list
- List all directories in the synchronization list
- Enable or disable the synchronization tool
- Configure synchronization interval and commit message
- Run synchronization manually or on a schedule

## Installation

To install the required dependencies, run the `setup.sh` script:

```sh
./setup.sh
```

This script will install the necessary Python libraries and set up an alias for the gitsync command.

## Usage

### Commands

- `add <directory>`: Add a directory to the synchronization list
- `remove <directory>`: Remove a directory from the synchronization list
- `list`: List all directories in the synchronization list
- `enable`: Enable the synchronization tool
- `disable`: Disable the synchronization tool
- `config [-m, --message, -i, --interval]`: Configure the synchronization tool
    - `-m, --message <message>`: Set the commit message
    - `-i, --interval <interval>`: Set the synchronization interval (number of minutes, daily, weekly, monthly)
- `run`: Synchronize all directories immediately
- `run:scheduler`: Start the scheduler to synchronize directories according to the configured interval
- `help`: Display the help menu

### Example Usage

- Add a directory to the synchronization list:
    ```sh
    gitsync add /path/to/directory
    ```
    or
    ```sh
    cd /path/to/directory
    gitsync add .
    ```

- Remove a directory from the synchronization list:
    ```sh
    gitsync remove /path/to/directory
    ```
    or
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

- Run synchronization manually:
    ```sh
    gitsync run
    ```

- Start the scheduler:
    ```sh
    gitsync run:scheduler
    ```

- Display the help menu:
    ```sh
    gitsync help
    ```

## Notes

- The tool is only available for Linux.
- Ensure that the directories you add are valid git repositories and you have the necessary permissions to access them.

## License

This project is licensed under the MIT License.
