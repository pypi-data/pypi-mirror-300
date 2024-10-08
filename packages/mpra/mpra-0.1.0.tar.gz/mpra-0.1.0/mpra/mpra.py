'''
*******************************************************************************
*IT'S OPENSOURCE ENJOY* 
SCRIPT NAME             : mpra.py
DESCRIPTION             : The `mpra` package offers a variety of utility
                          functions to manage files and directories, 
                          such as checking disk usage, organizing files 
                          by extension, monitoring directories, and more.
SCRIPT REV              : 1.0
SCRIPT DATE             : 2024-10-07
AUTHOR                  : Manoj Pennada, S K mpraalya
*******************************************************************************
'''


import os
import shutil
import time
import subprocess


class Mpra:
    @staticmethod
    def disk_stats(directory_path):
        """Print total, used, and free disk space in GB."""
        try:
            total, used, free = shutil.disk_usage(directory_path)
            print(f"Total: {total // (2**30)} GB")
            print(f"Used: {used // (2**30)} GB")
            print(f"Free: {free // (2**30)} GB")
        except FileNotFoundError:
            print(f"Error: Directory {directory_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def organize_files(directory_path):
        """Organize files in the directory by extension."""
        if not os.path.exists(directory_path):
            print("Directory not found!")
            return

        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath):
                file_ext = filename.split('.')[-1]
                ext_dir = os.path.join(directory_path, file_ext)

                if not os.path.exists(ext_dir):
                    os.mkdir(ext_dir)

                shutil.move(filepath, os.path.join(ext_dir, filename))
        print("Files organized by extension.")

    @staticmethod
    def monitor_directory(directory_path):
        """Monitor directory for new files."""
        if not os.path.exists(directory_path):
            print("Directory does not exist!")
            return

        print(f"Monitoring directory: {directory_path}")
        files_before = set(os.listdir(directory_path))
        try:
            while True:
                time.sleep(2)
                files_after = set(os.listdir(directory_path))
                new_files = files_after - files_before
                if new_files:
                    print(f"New files added: {', '.join(new_files)}")
                files_before = files_after
        except KeyboardInterrupt:
            print("Directory monitoring stopped.")

    @staticmethod
    def backup_files(src_directory, dest_directory):
        """Backup files from one directory to another."""
        if not os.path.exists(src_directory):
            print(f"Source directory {src_directory} does not exist.")
            return
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        try:
            for filename in os.listdir(src_directory):
                src_file = os.path.join(src_directory, filename)
                dest_file = os.path.join(dest_directory, filename)
                shutil.copy2(src_file, dest_file)
            print(f"All files backed up to {dest_directory}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def batch_rename(directory_path, prefix="", suffix=""):
        """Add a prefix or suffix to all file names in a directory."""
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            return

        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath):
                new_filename = f"{prefix}{filename}{suffix}"
                new_filepath = os.path.join(directory_path, new_filename)
                os.rename(filepath, new_filepath)
        print("All files renamed.")

    @staticmethod
    def run_command(command):
        """Run a system command."""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"Command failed: {e}")

    @staticmethod
    def delete_empty_dirs(directory_path):
        """Delete all empty subdirectories."""
        if not os.path.exists(directory_path):
            print("Directory not found!")
            return

        for dirpath, dirnames, filenames in os.walk(directory_path, topdown=False):
            if not dirnames and not filenames:
                os.rmdir(dirpath)
                print(f"Deleted empty directory: {dirpath}")
        print("Empty directories removed.")

    @staticmethod
    def filter_files_by_size(directory_path, min_size_bytes):
        """List all files larger than a given size in bytes."""
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            return

        large_files = []
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath) and os.path.getsize(filepath) > min_size_bytes:
                large_files.append(filename)

        if large_files:
            print("Files larger than specified size:")
            for file in large_files:
                print(file)
        else:
            print("No files larger than the specified size.")

    @staticmethod
    def create_log(directory_path):
        """Generate a log file with the current date and time."""
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            return

        log_filename = os.path.join(directory_path, "logfile.txt")
        with open(log_filename, "a") as log_file:
            log_file.write(f"Log Entry at {
                           time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"Log file created at {log_filename}")


# Main interface for easy access
mpra = Mpra()
