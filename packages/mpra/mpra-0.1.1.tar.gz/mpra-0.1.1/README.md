<h1>MPRA (Multipurpose Resource Automation) 🚀</h1>

<p><strong>MPRA</strong> is a powerful multipurpose utility package designed to automate common file and directory management tasks. From organizing files by extensions to checking disk space and monitoring directories for changes, <strong>MPRA</strong> provides an efficient and user-friendly solution to streamline your workflow.</p>

<hr />

<h2>Why MPRA? 🤔</h2>

<p>MPRA is designed to be an all-in-one toolkit to simplify everyday system tasks. Whether you’re managing files, running system commands, or filtering directories, <strong>MPRA</strong> provides a lightweight yet effective solution to cover your automation needs.</p>

<ul>
    <li>⚡ <strong>Efficiency</strong>: Speed up your tasks with automated processes.</li>
    <li>📁 <strong>Organization</strong>: Keep your directories clean and well-organized.</li>
    <li>🔧 <strong>Customizable</strong>: Perform operations tailored to your specific requirements.</li>
    <li>📊 <strong>System Monitoring</strong>: Easily monitor system resources and directories.</li>
</ul>

<hr />

<h2>Installation 💻</h2>

<p>Ready to give it a go? Just run the following command to install MPRA:</p>

<pre><code>pip install mpra</code></pre>

<hr />

<h2>Usage 🔧</h2>

<p>Here’s how you can integrate MPRA functions into your daily tasks.</p>

<pre><code>
from mpra import mpra

# Example usage
mpra.disk_stats("/path/to/directory")
mpra.file_organizer("/path/to/your/files")
</code></pre>

<hr />

<h2>Features 🛠️</h2>

<div class="function">
    <h2>Disk Usage Checker</h2>
    <p>
        <strong>Function:</strong> <code>disk_stats(directory_path)</code><br>
        <strong>Description:</strong> This function takes a directory path as input and returns the total, used, and free disk space in gigabytes.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The path of the directory to check.</li>
    </ul>
    <p><strong>Returns:</strong></p>
    <ul>
        <li>Total disk space, used space, and free space in gigabytes.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.disk_stats('/path/to/directory')</code></pre>
</div>

<div class="function">
    <h2>File Organizer</h2>
    <p>
        <strong>Function:</strong> <code>organize_files(directory_path)</code><br>
        <strong>Description:</strong> This function organizes files in the specified directory into subdirectories based on file extensions.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The path of the directory to organize.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.organize_files('/path/to/directory')</code></pre>
</div>

<div class="function">
    <h2>Directory Monitor</h2>
    <p>
        <strong>Function:</strong> <code>monitor_directory(directory_path)</code><br>
        <strong>Description:</strong> This function monitors a directory for new files and prints a message each time a new file is added.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The directory to monitor.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.monitor_directory('/path/to/directory')</code></pre>
</div>

<div class="function">
    <h2>File Backup</h2>
    <p>
        <strong>Function:</strong> <code>backup_files(source_directory, destination_directory)</code><br>
        <strong>Description:</strong> This function copies all files from the source directory to the destination directory.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>source_directory</code> (str): The path of the directory to copy files from.</li>
        <li><code>destination_directory</code> (str): The path of the directory to copy files to.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.backup_files('/source/directory', '/destination/directory')</code></pre>
</div>

<div class="function">
    <h2>Batch Rename Files</h2>
    <p>
        <strong>Function:</strong> <code>batch_rename(directory_path, prefix=None, suffix=None)</code><br>
        <strong>Description:</strong> This function renames all files in a directory by adding a prefix or suffix.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The path of the directory containing the files.</li>
        <li><code>prefix</code> (str, optional): The prefix to add to each file name.</li>
        <li><code>suffix</code> (str, optional): The suffix to add to each file name.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.batch_rename('/path/to/directory', prefix='backup_')</code></pre>
</div>

<div class="function">
    <h2>System Command Runner</h2>
    <p>
        <strong>Function:</strong> <code>run_command(command)</code><br>
        <strong>Description:</strong> This function takes a system command as input and executes it. It returns the command's output.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>command</code> (str): The system command to execute.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.run_command('ls -la')</code></pre>
</div>

<div class="function">
    <h2>Delete Empty Directories</h2>
    <p>
        <strong>Function:</strong> <code>delete_empty_dirs(directory_path)</code><br>
        <strong>Description:</strong> This function recursively searches through a directory and deletes all empty subdirectories.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The directory to clean up.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.delete_empty_dirs('/path/to/directory')</code></pre>
</div>

<div class="function">
    <h2>File Size Filter</h2>
    <p>
        <strong>Function:</strong> <code>filter_files_by_size(directory_path, min_size_bytes)</code><br>
        <strong>Description:</strong> This function lists all files in a directory that are larger than a specified size.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The path of the directory to search.</li>
        <li><code>min_size_bytes</code> (int): The minimum file size (in bytes) to filter.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.filter_files_by_size('/path/to/directory', min_size_bytes=1000000)</code></pre>
</div>

<div class="function">
    <h2>Log File Creator</h2>
    <p>
        <strong>Function:</strong> <code>create_log(directory_path)</code><br>
        <strong>Description:</strong> This function generates a log file in the specified directory, logging the current date and time each time the script runs.
    </p>
    <p><strong>Parameters:</strong></p>
    <ul>
        <li><code>directory_path</code> (str): The directory where the log file will be created.</li>
    </ul>
    <p><strong>Example:</strong></p>
    <pre><code>mpra.create_log('/path/to/directory')</code></pre>
</div>

<hr />

<h2>Feedback, Bugs, & Contributions 🐛</h2>

<p>Got feedback or found a bug? Feel free to open an issue or contribute on GitHub:</p>

<ul>
    <li>GitHub: <a href="https://github.com/ManojPennada/mpra">https://github.com/ManojPennada/mpra</a></li>
    <li>Email: manojpennada@gmail.com</li>
</ul>

<hr />

<h2>License</h2>

<p>Refer to the LICENSE file for details.</p>

<footer>
    <p>&copy; 2024 MPRA Documentation. All rights reserved.</p>
</footer>
