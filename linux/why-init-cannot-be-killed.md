init (sysmlinked to systemd in most modern distributions) is the root process created by kernel.
It is the first user space process created.. So it's PID will be 1

The kernel spawns this init by running a hardcoded subroutine... Here's the code excerpt from the linux kernel source code

```C
/init/main.c


if (!try_to_run_init_process("/sbin/init") ||
	    !try_to_run_init_process("/etc/init") ||
	    !try_to_run_init_process("/bin/init") ||
	    !try_to_run_init_process("/bin/sh"))
		return 0;

	panic("No working init found.  Try passing init= option to kernel. "
	      "See Linux Documentation/admin-guide/init.rst for guidance.");
```

Basically the kernel expects a binary called 'init' exists in any of above 4 paths. If does not exist, it panics.

init process cannot be killed (try kill -n 9 1) ... because even though the kernel does not give a damn about what the init does..
it still cares about how orphned processes should be handled.. if ever the kernel finds a user process with no parent , it reassigns this
orphan process to init ... ie all orphan processes become init's children..

Also many crtitical user processes are implemented specifically such that in the event they crash , they are automatically
spawned by the init..

With all this in mind, i think we can understand why init cannot be killed.. Which is exactly why the 
