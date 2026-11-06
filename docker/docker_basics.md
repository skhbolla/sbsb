# Chapter 1 : Setting up docker

After installing docker using any method described on the official site, make sure to add the current user to the 'docker' group.	

> sudo usermod -aG docker $USER

## But why does docker need root privileges?

Docker isn’t a single program — it’s split into two main components:		
| Component                     | Role                                                                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Docker Daemon** (`dockerd`) | A background process that manages containers, images, networks, volumes. It listens on a **Unix socket** (`/var/run/docker.sock`). |
| **Docker CLI** (`docker`)     | The command-line client you use (`docker run`, `docker ps`, etc.). It talks to the daemon through that socket.                     |


That socket file (/var/run/docker.sock) is owned by root and has permissions like:		
srw-rw---- 1 root docker 0 Oct 10 22:00 /var/run/docker.sock	

The srw-rw---- part means:		

It’s a socket (s). Owner (root) has read/write. Group (docker) has read/write. Others have no access.		

So unless you’re root or part of the docker group, you can’t communicate with the daemon.	

Once you have docker installed , run 
> docker version

If you want to login to docker hub , run
> docker login

--------------

# Chapter 2 : Containers

Virtual machines virtualize hardware, they emulate what a physical computer does at a low level. Containers virtualize at the operating system level. Isolation between containers that are running on the same machine is still really good. For the most part, each container feels like it has its own operating and filesystem. In reality, a lot of resources are being shared, but they're being shared securely through namespaces.		

## What are Images?

An Image is a read-only definition of a container. Containers are an instance of a virtualized read-write environment. So basically, an image is a blueprint of what a container should be.

> docker run <image-name>
Creates a container from an image.

> docker pull docker/getting-started
The pull commands simply creates a copy of the image on our machine (downloads a image).	

> docker images
Lists all the images saved on the machine.

## Running a container

> docker run -d -p hostport:containerport namespace/name:tag
* -d -> Run in detached mode (doesn't block terminal)
* -p: Publish a container's port to the host (forwarding)
* hostport: The port on your local machine
* containerport: The port inside the container
* namespace/name: The name of the image (usually in the format username/repo)
* tag: The version of the image (often latest)
* -e : You can use the -e flag to set environment variables


## Stopping a container

> docker stop <container-id> #Issues a SIGTERM

or

> docker kill <container-id> #Issues a SIGKILL

--------------

# Chapter 3 : Storage

## Volumes

By default, Docker containers don't retain any state from past containers.	
For example , after i start a container , I update some packages inside the container; *remove* the container; start a *new* container with *same image* :		

**The new container  will not have the updates we made**

**However, if I restart a *stopped* container, it will have the changes I made. This is only worth mentioning because sometimes developers think that removing an old container and starting a new one is the same as restarting a process - but that's not true... killing/removing and starting a new one is more like resetting the state of the entire machine to the original image**

**All this said, Docker does have ways to support *Persistent State* through *Storage Volumes* . They are basically a *a file system that lives outside the container but can be accessed by the container*.** 

> docker volume create <volume-name>
Creates a empty volume with given name

> docker volume ls
Lists all created volumes

> docker volume inspect <volume-name>
Inspect the volume (shows details about volume including the mount point)

**Use the -v flag while running a container to mount volumes**		
> docker run -d -p 3001:2368 -v ghost-vol:/var/lib/ghost ghost
Here -v mounts a volume named "ghost-vol" (named volume) onto the container's /var/lib/ghost directory. **Note that if no volume with that name exists, docker creates it by default**

**Note: Stopping and removing containers are very different actions**

*Stopping a container sends SIGTERM to the container , and effectively sends it into EXITED state. The container data still exists and can be restarted* 
> docker stop <container-id>  OR
> docker container stop <container-id>

*Removing a container on the otherhand means that all the data related to container is gone -- No restart*
> docker rm <container-id>   OR
> docker container rm <container-id>		

 
You can use the -a flag with ps to show all containers , including stopped containersand -q for quiet mode (show only container IDs)		

> docker ps -a

**Pro Tip** : To remove/stop all containers, use
> docker stop $(docker ps -q)
> docker rm $(docker ps -aq)

**Deleting a docker volume**
> docker volume rm <volume-name>
> docker volume rm $(docker volume ls -q)  #Delete all volumes


-------

# Chapter 4 : Execute

To run a command inside a running container , use:
> docker exec <container-id> <command>

To run a full on shell session within the container , we can use the *-i* and *-t* flags
> docker exec -it <container-id> /bin/sh

* -i : makes the *exec* command interactive
* -t : gives us a tty keyboard interface
* Running /bin/sh : gives us a shell session inside the container


-------

# Chapter 5 : Networks

## Going offline !!

docker run has a useful flag called *--network none* flag that makes it so that the container cannot network with the outside world, this is useful for isolating containers.

> docker run -d -p 4068:80 --network none <image-name>

**Note that even though we are explicitly setting up port forwarding to 4068 , docker still does not setup the port because *--network none* is set**

Now if you run *docker ps* , you will notice that the ports section will be empty		

**Also , note that docker containers running with --network none , cannot access the internet (duh , because no network at all)**


## Load Balancers 

A load balancer behaves as advertised: it balances a load of network traffic across some number of servers. Think of a huge website like Google.com. There's no way that a single server (literally a single computer) could handle all of the Google searches for the entire world. Google uses load balancers to route requests to different servers.			

A central server, called the "load balancer", receives traffic from users (aka clients), then routes those requests to different back-end application servers. In the case of Google, this splits the world's traffic across potentially many different thousands of computers.		

A good load balancer sends new traffic to servers that have lower current resource utilization (CPU and memory). The goal is to "balance the load" so that no single backend server becomes overwhelmed. There are many strategies that load balancers use, but a simple strategy is the "round robin" where requests are simply routed one after the other to different back-end servers:

* Request 1 -> Server 1
* Request 2 -> Server 2
* Request 3 -> Server 3
* Request 4 -> Server 1
* Request 5 -> Server 2
* ...

## Custom network

We can create custom [bridge](https://docs.docker.com/network/bridge/) networks so that containers can communicate with each other if we want them to, but still otherwise remain isolated.		


Example usecase:
`A very common setup in backend architecture is that the load balancer is exposed to the public internet, but the application servers are only accessible via the load balancer.`


### Why Custom Networks ?

When containers run without a custom network, they’re attached to Docker’s default bridge network, where each container is isolated and can’t resolve others by name. Communication between them requires knowing dynamic IP addresses, which change whenever containers restart. This makes it nearly impossible for one container — such as a load balancer or API service — to reliably discover and route traffic to others.

By contrast, a custom Docker network provides an internal DNS and shared namespace, allowing containers to communicate seamlessly using service names instead of IPs. This creates a private virtual LAN where containers can discover each other automatically, scale easily, and maintain stable connections. Such networking is essential for microservices, load balancing, and orchestrating multi-container applications in a predictable way.


### Creating a custom network

> docker network create <network-name>

> docker network ls

You can then use --network <network-name> while creating containers to attch them to that network

> docker run -d --network <network-name> --name <container-nickname> <image>

**Docker will auto setup name resolution for us! The container nicknames resolve to the individual containers from all other containers on the same network**

---------------

# Chapter 6 : Dockerfiles

Docker images are built from Dockerfiles. A Dockerfile is just a text file that contains all the commands needed to assemble an image. It's essentially the "Infrastructure as Code" (IaC) for an image. It runs commands from top to bottom, kind of like a shell script.

**TO build a docker image from a docker file , use**:

> docker build -t <new-image-name>:<version-tag> -f Dockerfile <build-context-path>

* -t helps create tags for versioning
* -f indicates the path of Dockerfile to be used
* <build-context-path> represents the path that is used by docker while builiding the image. The build context is not where the Dockerfile necessarily lives — it’s the directory whose contents are available during the image build.

### Common Dockerfile instructions

* FROM debian:slim-stable  -> Define the base image
* CMD ["echo", "Hello World"] -> commands that will be executed when the container runs. Note , a dockerfile can have multiple CMD instructions but only the final CMD is actually executed.
* COPY hostpath guestpath -> Copies files from host into image
* ADD hostpath guestpath -> ADD and COPY are functionally similar. COPY supports basic copying of files into the container, from the build context or from a stage in a multi-stage build. ADD supports features for fetching files from remote HTTPS and Git URLs, and extracting tar files automatically when adding files from the build context.
* ENV MY_NAME="John Doe" ENV MY_DOG=Rex\ The\ Dog ENV MY_CAT=fluffy -> Sets the environment variable <key> to <value>
* RUN instruction will execute any commands to create a new layer on top of current image. The added layer is used in the next step of Dockerfile. RUN has two forms :
	* RUN [OPTIONS] <command> ..  -> Shell form 
	* RUN [OPTIONS] ["<command>: , ...] -> Exec form



-------------


# Chapter 7 : Debug

## Docker logs

> docker logs [OPTIONS] <CONTAINER>

**Common options include : **
* -f -> follow logs (live tail)
* --tail 5 -> displays 5 latest log lines

## Docker Stats

> docker stats [OPTIONS] <CONTAINER ... >

## Docker Top

**The docker *top* command shows the running processes inside a container.**
**Use `stats` for entire containers and `top` for *processes in a container*.**


> docker top <CONTAINER> [ps OPTIONS]

## Resource Limits

The docker run command provides flags to limit the resources a container has available.
* --memory : Limits memory available to container
* --cpus : Limits the CPU shares available to container

----------------

# Chapter 8 : Publish

> docker push USERNAME/imagename

> docker pull USERNAME/imagename

## Tags

With Docker, a tag is a label that you can assign to a specific version of an image, similar to a tag in Git.

The latest tag is the default tag that Docker uses when you don't specify one. It's a convention to use latest for the most recent version of an image, but it's also common to include other tags, often semantic versioning tags like 0.1.0, 0.2.0, etc.

When pushing a new version of an image to a registry , make sure to add a version tag	

> docker push USERNAME/imagename:<version-tag>


## Latest

**After pushing a new version with a tag to registry , you'll notice that your old version is tagged "latest"... that's a bit confusing. As it turns out, the latest tag doesn't always indicate that a specific tag is the latest version of an image. In reality, latest is just the default tag that's used if you don't explicitly supply one. We didn't use a tag on our first version, that's why it was tagged with "latest".**

### Should i use "latest" ??

The convention I'm familiar with is to use semantic versioning on all your images, but to also push to the "latest" tag on your most recent image. That way you can keep all of your old versions around, but the latest tag still always points to the latest version.			

So, for example, if I were updating an application to version 5.4.6, I would probably do it like this:		

> docker build -t bootdotdev/awesomeimage:5.4.6 -t bootdotdev/awesomeimage:latest .
> docker push bootdotdev/awesomeimage --all-tags


-----------
