* Display a line of text
> echo "Hello World"

* id - print real and effective user and group IDs
> id

* Print effective user id
> whoami

* Evaluate an expression
> expr 123+456

* Display the shell's command history
> history

* Print the current working directory
> pwd

* list directory contents
> ls /path/to/dir

* Change the working directory
> cd /path/to/dir

* Concatenate files and print on std out 
> cat [OPTION]... [FILE]...

* Ouput the first part of file
> head [OPTION]... [FILE]...
> head -n 15 file1.txt

* Output the last part of file
> tail [OPTIONS]... [FILE]...
> tail -n 5 file1.txt file2.txt

* more - file perusal filter for crt viewing
> more [OPTIONS] [FILE] ...

* less - opposite of more (The less command does everything more can do , and also has more features. As a general rule , always prefer less instead of more)			
> less [OPTIONS] [FILE]
> less -N file1.txt #Displays line numbers

* touch - change file timestamps
	**By default if a specified file does not exist, touch will create an empty file with the given filename. Because of this side-effect, you’ll often see this command used to quickly create new empty files.**

> touch new_file.txt
> touch new_file1.txt new_file2.txt


* mkdir - make directories
> mkdir [OPTION]... DIRECTORY...

* mv - move(rename) files
> mv [OPTION]... [-T] SOURCE DEST
> mv [OPTION]... SOURCE... DIRECTORY
> mv [OPTION]... -t DIRECTORY SOURCE...

* rm - Remove command deletes a file or empty directory

> rm somefile.txt
> rm some_directory #this dir must be empty
> rm -r some_directory #Recursively remove files in the dir, and then delete the dir.

* cp - copy files/directories from one location to another

> cp source_file.txt destination/
> cp -R source_dir dest_dir

* grep - print lines that match pattern

> grep "hello" words.txt #By default grep is case sensitive
> grep "hello" words1.txt words2.txt
> grep -r "hello" . #Recursive search entire dir


* find - search for files in a directory hierarchy

> find some_dir -name hello.txt

	* Find also support pattern searching
	> find some_dir -name "*.txt"

* chmod - change permissions(mode) of a file or directory

> chmod -R u=rwx,g=,o= /path/to/dir     #Here -R recursively applies permissions to all files within the directory

> chmod -x filename 

> chmod u+wx filename

* chown - change the owner of a file or directory
> sudo chown -R root path/to/dir/

* chgrp - change group ownership of a file or directory
> chgrp <groupname> <filename or dirname>


* which - shows the location of the binary
> which bash 

* env - list all environment variables set in current shell
> env

* export - used to set a new env variables in shell session
> export NAME="VALUE"
> export PATH="$PATH:/some/new/path"     #This will append some new path to the PATH variable

* unset - unset an env variable
> unset NAME

* realpath - prints resolved path (Used to get absolute path of a given relative path)
> realpath /some/relative/path


* man - open reference manuals
> man ls

* ps - report current snapshot of running processes
> ps aux
