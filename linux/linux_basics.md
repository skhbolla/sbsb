# Ohm namo vigneshawaraya namaha:: Ohm namo venkatesaya namaha:: Ohm namo narayanaya namaha::


--------

# Chapter 1 : Terminals and Shells

## What's a CLI ?

You'll often hear the terms "terminal", "shell", "command line", "CLI", and "command prompt" used interchangeably (despite some technical differences) to refer to the same thing: a program that allows you to interact with your computer in a text-based way.

## What is a Terminal ?
As we talked about, the terms "shell", "CLI", and "terminal" are often used to refer to the same thing: a program for issuing text-based commands.		

But to get pedantic, the "terminal" is just one specific part of that program. Historically, the word "terminal" meant a physical device that you could type commands into, essentially a keyboard and a screen.		

These days, when we say "terminal", we really mean "terminal emulator". A terminal emulator is a program that emulates a physical terminal. It's a program that lets you type commands into a window on your computer.		

Which commands you're able to use isn't determined by the terminal emulator, but by the shell, which we'll talk about later.		

Your terminal emulator is just responsible for drawing text on the screen and processing your keystrokes.		
**TLDR; A terminal(terminal emulator) is a program that is responsible for accepting text based commands and rendering text on the screen**

**Read tty.md for in depth knowledge on terminals**

## What is a shell ?

So if your terminal is just a program that lets you issue text-based commands and renders the output of those commands...

...What is the program that runs those commands???

That's a shell.

Shells do a lot of things, but their main job is to interpret the commands you type and execute them.

### REPL 

Shells are often referred to as "REPL"s. REPL stands for

Read
Eval (evaluate)
Print
Loop

## Variables

Both Bash and Zsh are *shells*, and they also happen to be *powerful programming languages*. They have variables, functions, loops, and more.

A common misnomer is that bash is simply a shell , but no, the defintion of bash is as follows:

> Bash (Bourne Again SHell) is a free, open-source command-line interpreter and scripting language for Unix-like operating systems like Linux and macOS

### Creating and using varaibles

> name="Srikanth"
> echo $name

------------

# Chapter 2 : File Systems

All the data stored on your computer is organized into files and directories. Files and directories are organized into a tree-like structure called a filesystem.

* Directories (or "folders" on Windows) are just containers that hold files and other directories.
* Files are just a dump of raw binary data: 1's and 0's. The bytes in a file can represent anything: text, images, videos, etc.

The filesystem tree starts with a single directory called the *root* directory. The root directory contains files and directories, which can contain more files and directories, and so on.

## Absolute vs Relative Paths

If a path has a `/` at the beginning , it is a *Absoulte Path* . A / prefix represents the *root* directory in linux


If no `/` is prepended to the file path , then it is a *relative path* , which takes into account your current directory.


--------------

# Chapter 3 : Permissions

Sudo ("Super user do") lets us run commands as a "superuser"

> sudo whoami

## Permissions
In linux , every file/directory has a single owner and single group associated with it (even if the owner/creator belongs to multiple groups , only the primary group of the owner gets to have group ownership)

The permissions of an individual file or directory are visually represented as a 10-character string:

`drwxrwxrwx`

Let's break down each character. The first one just tells you whether you're looking at a file or a directory:

* -: Regular file (e.g. -rwxrwxrwx)
* d: Directory (e.g. drwxrwxrwx)

The next 9 characters are broken up into 3 sets of rwx and represent the permissions themselves for the "owner", "group", and "others", in order. Each group of 3 represents the permissions for reading, writing, and executing, in order. So, for example:

* rwx: All permissions

* rw-: Read and write, but not execute

* r-x: Read and execute, but not write

* The first 3 characters are "owner" permissions. The "owner" is usually just the user who created the file or directory, but it can be manually changed.

* The next 3 characters are "group" permissions. Unix-like systems support groups of users, and each file or directory is assigned to exactly one owning group. Anyone who is not the owner and not a member of that group falls under "others". To be honest, unless you're a system administrator, you won't often worry about groups.

* The last 3 characters are "others" permissions. This is everyone else.

## chmod
Lets you change the permissions of any file or directory that *you own*.

## chown
Lets you change the owner of any file or directory (obviously need root privileges *even if you are the owner*)

## chgrp
Lets you change the group ownership of a file or directory


-------------

# Chapter 4 : Programs

## Shebang
When running a compiled program , we usually just do `./program` . This works because program here is bytecode executable that can run natively without needing a interpreter.      

But when running a interpreted program like `main.py` , we need to specify which program we want to use to intrepret the code. Eg : `python3 main.py`      

This is where **shebang** comes in:
> A "shebang" is a special line at the top of a script that tells your shell which program to use to execute the file.

The syntax for shebang is :

```
#! interpreter [optional-arg]

```

For example:
```
#!/usr/bin/python3

```

## Environment Variables

* We can list all env variables set in out current shell session using `env`

* We can set a new env variable in shell using `export NAME="VALUE"`

* Environment variables can be accessed in shell by prefixing the keyname with `$` . Eg: echo $PATH


### PATH
* The PATH environment variable is a list of directories that your shell will look into when you try to run a command.

```bash
export PATH="$PATH:/some/new/path"     #This will append some new path to the PATH variable

```

--------------


# Chapter 5 : Input/Output

## Exit Codes

Exit codes (sometimes called "return codes" or "status codes") are how programs communicate back whether they ran successfully or not.

* `0` is the exit code for `success`
* Any other exit code is an error. But most of the times a non-zero error code (error) will be a 1

> **PRO-TIP** : `echo $?` will return the exit code of the last run program

## Standard Output, Standard Error, Standard Input
**Read streams.md for in depth guide**

## Interrupts

* When we press ctrl+c during the executions of a program , it sends a `SIGINT` signal to the program. This tells it to stop.

* But sometimes, the program could be in such a bad state that it may not even respond to a `SIGINT`. In this case it's better to open a new shell session and use `kill <pid>`
* When we do `kill <pid>` it sends a `SIGKILL` to the process with given pid

---------------

# Chapter 6 : Packages

A package manager is a software tool that helps you install other software. Its primary functions include:

* Downloading software from official sources
* Installing software
* Updating software
* Removing software
* Managing dependencies
