# mpra Package

## Overview

The `mpra` package offers a variety of utility functions to manage files and directories, such as checking disk usage, organizing files by extension, monitoring directories, and more.

## Features

- **Disk Usage Checker**: Get the total, used, and free disk space of a directory.
- **File Organizer**: Organize files by extension into subdirectories.
- **Directory Monitor**: Watch a directory for new files.
- **File Backup**: Backup files from one directory to another.
- **Batch Rename**: Add prefixes or suffixes to filenames.
- **System Command Runner**: Run system commands and handle errors.
- **Delete Empty Directories**: Remove all empty subdirectories.
- **File Size Filter**: List files larger than a specified size.
- **Log File Creator**: Generate a log file with current date and time.

## Usage

```python
import mpra

mpra.disk_stats("/path/to/directory")
mpra.organize_files("/path/to/directory")
```
