# Socket Programming in UNIX Systems: A Comprehensive Deep Dive

## 1. Understanding Sockets and File Descriptors

### What Are Sockets?

A **socket** is an abstraction that represents an endpoint for network communication. Think of it as a virtual "plug" that allows processes to send and receive data across a network (or even on the same machine). Sockets provide a unified interface for different types of communication - whether you're talking to a process on the same machine, across a local network, or over the internet.

**Why do we need sockets?**

Before sockets, network programming was fragmented. Different protocols required different APIs, making it difficult to write portable network applications. The Berkeley Sockets API, introduced in BSD UNIX in the early 1980s, standardized network communication by providing a consistent interface regardless of the underlying protocol (TCP, UDP, etc.).

Sockets allow us to:
- Establish bidirectional communication channels
- Abstract away the complexities of network protocols
- Use familiar file I/O operations (read/write) for network communication
- Handle multiple concurrent connections efficiently

### File Descriptors: The Foundation

To understand sockets, we must first understand **file descriptors (FDs)**. In UNIX philosophy, "everything is a file" - and this includes network sockets.

A **file descriptor** is simply a non-negative integer that acts as a handle or reference to an open file, socket, pipe, or other I/O resource. When you open a file or create a socket, the kernel returns an integer (like 3, 4, 5) that you use in subsequent operations.

### The Two-Level File Descriptor Architecture

The kernel maintains file descriptor information at **two levels**:

#### 1. Process-Specific File Descriptor Table

Each process has its own **file descriptor table** (part of the process's task structure). This is an array where:
- The **index** is the file descriptor number (0, 1, 2, 3...)
- The **value** is a pointer to an entry in the global file table

Standard file descriptors are pre-assigned:
- FD 0: stdin (standard input)
- FD 1: stdout (standard output)  
- FD 2: stderr (standard error)

When you call `socket()` or `open()`, the kernel finds the lowest available index in this table and returns it as your file descriptor.

#### 2. Global File Table (System-Wide)

The **global file table** (also called the open file table) is shared across all processes. Each entry contains:

- **File status flags**: Whether the file was opened O_RDONLY, O_WRONLY, O_RDWR, O_NONBLOCK, etc.
- **Current file offset**: The current position for read/write operations (the "cursor")
- **Reference count**: How many file descriptors point to this entry (important for fork() and dup())
- **Pointer to the v-node/i-node table entry**: This points to the actual file metadata

#### 3. The V-node/I-node Table

Each entry in the global file table points to a **v-node** (virtual node) or **i-node** (index node) which contains:

- **File type**: Regular file, directory, socket, pipe, device, etc.
- **File permissions**: Read, write, execute permissions
- **File size**
- **Timestamps**: Access time, modification time, creation time
- **Pointer to actual data**: For regular files, this includes information about disk blocks

**For a regular file on disk**, the i-node contains:
- **Device ID**: Which disk/partition the file is on
- **I-node number**: Unique identifier on that filesystem
- **Block pointers**: Direct pointers to data blocks, indirect pointers for large files
- **Disk sectors/blocks**: The actual locations on disk where data is stored (organized as direct blocks, single indirect, double indirect, triple indirect for large files)

**For a socket**, the i-node contains:
- **Socket type**: SOCK_STREAM (TCP), SOCK_DGRAM (UDP), etc.
- **Protocol**: TCP, UDP, etc.
- **Socket state**: LISTENING, ESTABLISHED, CLOSED, etc.
- **Send/receive buffers**: Kernel buffers for data in transit
- **Connection information**: For connected sockets, the remote address/port

This three-level indirection allows multiple processes to share the same file (via fork) while maintaining independent file positions, allows a single process to have multiple FDs pointing to the same file (via dup2), and enables the kernel to manage resources efficiently.

---

## 2. The Four Stages of Socket Creation

Creating a useful server socket involves four distinct system calls, each with a specific purpose. Let's examine each in detail.

### Stage 1: `socket()` - Creating the Endpoint

```c
int socket(int domain, int type, int protocol);
```

**Parameters:**
- `domain`: Address family (AF_INET for IPv4, AF_INET6 for IPv6, AF_UNIX for local)
- `type`: Communication semantics (SOCK_STREAM for TCP, SOCK_DGRAM for UDP)
- `protocol`: Usually 0 (kernel chooses appropriate protocol)

**Returns:** A file descriptor (non-negative integer) on success, -1 on error

**What happens internally:**
1. Kernel allocates a socket structure in kernel memory
2. Kernel finds the lowest available FD in the process's FD table
3. Creates an entry in the global file table pointing to the socket structure
4. Returns the FD to user space

At this point, the socket is **unbound** - it has no address or port associated with it. It's like creating a phone that isn't connected to any phone line yet.

### Stage 2: `bind()` - Assigning an Address

```c
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

**Parameters:**
- `sockfd`: The socket file descriptor from `socket()`
- `addr`: Pointer to a sockaddr structure containing the address to bind to
- `addrlen`: Size of the address structure

**Returns:** 0 on success, -1 on error

**What happens internally:**
1. Kernel validates the address (checks if it's already in use, if we have permission, etc.)
2. Associates the socket with the specified IP address and port
3. Updates the socket structure with binding information
4. For port 0, kernel auto-assigns an available ephemeral port

**Example:**
```c
struct sockaddr_in server_addr;
server_addr.sin_family = AF_INET;
server_addr.sin_addr.s_addr = INADDR_ANY; // Accept connections on any interface
server_addr.sin_port = htons(8080); // Port 8080 in network byte order

bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
```

**Key insight:** `INADDR_ANY` (0.0.0.0) means "accept connections on any network interface" - whether localhost, ethernet, WiFi, etc.

### Stage 3: `listen()` - Marking as Passive Socket

```c
int listen(int sockfd, int backlog);
```

**Parameters:**
- `sockfd`: The bound socket file descriptor
- `backlog`: Maximum length of the pending connection queue

**Returns:** 0 on success, -1 on error

**What happens internally:**
1. Kernel marks the socket as a **passive socket** (ready to accept incoming connections)
2. Allocates two queues (more on this in section 3):
   - **SYN queue** (incomplete connection queue)
   - **Accept queue** (complete connection queue)
3. The socket transitions to LISTEN state

**The backlog parameter** is subtle and often misunderstood:
- Historically, it specified the size of the accept queue
- Modern Linux uses it to determine the size of BOTH queues
- The actual limit is `min(backlog, /proc/sys/net/core/somaxconn)`
- Setting backlog too low causes connection rejections during traffic bursts
- Setting it too high wastes kernel memory

**Critical distinction:** After `listen()`, the socket is in **listening mode** - it can't send or receive data itself. It exists solely to spawn new connected sockets via `accept()`.

### Stage 4: `accept()` - Extracting Established Connections

```c
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

**Parameters:**
- `sockfd`: The **listening socket** file descriptor
- `addr`: Pointer to a structure to receive the client's address (can be NULL)
- `addrlen`: Pointer to the size of addr structure (value-result parameter)

**Returns:** A **new file descriptor** for the connected client on success, -1 on error

**This is the most conceptually important call** - let's break it down carefully:

**Why does `accept()` take the server FD and return a client FD?**

This is fundamental to understanding socket architecture:

1. **The listening socket (server FD)** is a factory - it exists solely to create new connections. It never transmits data itself. Think of it as a receptionist who answers the phone but transfers calls to specialists.

2. **The connected socket (client FD)** is the actual communication channel. This is where data flows. Each accepted connection gets its own unique FD, representing a dedicated channel to that specific client.

**Why separate them?**
- **Scalability**: A single listening socket can spawn thousands of connected sockets
- **Isolation**: Each client connection is independent - closing one doesn't affect others
- **Clarity**: The listening socket has different semantics (can't send/receive data) than connected sockets
- **Multiplexing**: You can use select/poll/epoll to monitor both the listening socket (for new connections) and all connected sockets (for data) simultaneously

**What happens internally:**
1. Kernel checks the **accept queue** (completed connections)
2. If the queue is empty and the socket is blocking, the process sleeps
3. When a connection is available, kernel:
   - Removes the connection from the accept queue
   - Creates a NEW socket structure for this specific connection
   - Allocates a new FD in the process's FD table
   - Returns the new FD
4. The returned FD is a fully connected socket - you can immediately read/write on it

**Important:** The listening socket (server FD) remains unchanged and continues accepting new connections. The client FD is specific to one client connection.

### Additional Essential Knowledge

**Socket Options with `setsockopt()`:**

Before binding, you'll often want to set socket options:

```c
int optval = 1;
setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));
```

**SO_REUSEADDR** is critical - it allows immediately rebinding to a port after your server crashes/restarts, avoiding the "Address already in use" error caused by TIME_WAIT state.

**SO_REUSEPORT** (Linux 3.9+) allows multiple sockets to bind to the same port, with kernel load-balancing incoming connections across them.

**Handling Errors:**

Every socket call can fail. Common errors:
- `EADDRINUSE`: Port already in use (forgot SO_REUSEADDR)
- `EACCES`: Permission denied (ports < 1024 require root)
- `EMFILE`: Process FD limit reached
- `ENFILE`: System-wide FD limit reached

Always check return values and use `perror()` or `strerror(errno)` to understand failures.

---

## 3. The Accept Call: Kernel Magic and the Two-Queue System

The `accept()` call appears simple, but beneath the surface lies sophisticated kernel machinery implementing the TCP three-way handshake and connection queuing.

### The TCP Three-Way Handshake (Brief Review)

Before understanding accept's queues, recall how TCP establishes connections:

1. **Client → Server: SYN** - "I want to connect"
2. **Server → Client: SYN-ACK** - "OK, I acknowledge"
3. **Client → Server: ACK** - "Acknowledged your acknowledgment"

Only after step 3 is the connection **fully established**.

### The Two-Queue Architecture

When you call `listen()`, the kernel creates **two separate queues** for the socket:

#### Queue 1: SYN Queue (Incomplete Connection Queue)

**Purpose:** Holds connections in the SYN_RECEIVED state (after receiving SYN, before receiving final ACK)

**What it contains:**
- Connections that have received a SYN
- Connections for which the server has sent SYN-ACK
- Connections waiting for the final ACK from the client

**Structure:** Each entry contains:
- Source IP and port
- Destination IP and port
- Sequence numbers
- TCP options (window size, MSS, etc.)
- Timestamp for retransmission logic
- SYN cookie information (if SYN cookies are enabled)

**Why this queue exists:**
- TCP requires state tracking between SYN and ACK
- Protects against SYN flood attacks (attackers send SYNs but never complete handshake)
- Allows kernel to retransmit SYN-ACK if client's ACK is lost

**Size:** Determined by `tcp_max_syn_backlog` sysctl parameter

#### Queue 2: Accept Queue (Completed Connection Queue)

**Purpose:** Holds fully established connections waiting to be accepted by the application

**What it contains:**
- Connections that have completed the three-way handshake
- Fully established sockets ready for data transfer
- Waiting for the application to call `accept()` to claim them

**Structure:** Each entry is essentially a completed socket structure with:
- Established TCP state (ESTABLISHED)
- Allocated send and receive buffers
- Client address and port information
- All TCP state (sequence numbers, window sizes, etc.)

**Size:** Determined by the `backlog` parameter in `listen()`, capped by `/proc/sys/net/core/somaxconn`

### The Accept Flow: Step by Step

Let's trace what happens when a client connects:

**Step 1: SYN Arrives**
```
1. Packet arrives at network interface
2. Kernel IP layer routes it to TCP
3. TCP looks up the listening socket by (IP, port)
4. Kernel checks: Is SYN queue full?
   - If YES: Drop SYN (or use SYN cookies if enabled)
   - If NO: Create entry in SYN queue
5. Kernel sends SYN-ACK to client
6. Starts retransmission timer
```

**Step 2: Final ACK Arrives**
```
1. Client's ACK arrives
2. Kernel finds matching entry in SYN queue
3. Kernel validates ACK (sequence number, etc.)
4. Kernel checks: Is accept queue full?
   - If YES: 
     * Drop the ACK
     * Leave entry in SYN queue (for retransmission)
     * Client will retransmit ACK
   - If NO:
     * Remove entry from SYN queue
     * Create fully connected socket
     * Add to accept queue
5. Connection is now ESTABLISHED
```

**Step 3: Application Calls `accept()`**
```
1. Kernel checks accept queue
2. If queue is EMPTY:
   - If socket is BLOCKING: Process sleeps (added to wait queue)
   - If socket is NON-BLOCKING: Return EAGAIN/EWOULDBLOCK
3. If queue has connections:
   - Dequeue the oldest connection (FIFO order)
   - Allocate new FD in process's FD table
   - Copy client address to user-provided buffer
   - Return new FD
```

### Why Accept Blocks

When you call `accept()` on a blocking socket and the accept queue is empty:

**Kernel-side operations:**
1. Current process is marked as SLEEPING/WAITING
2. Process is added to the socket's **wait queue**
3. Process context is saved
4. Scheduler picks another process to run
5. CPU is yielded

**What wakes the process:**
1. When the final ACK completes a connection
2. Kernel moves connection to accept queue
3. Kernel checks: Is anyone waiting on this socket?
4. Kernel wakes all processes in the wait queue
5. Process transitions from SLEEPING to RUNNABLE
6. Scheduler eventually runs the process
7. `accept()` returns with the new FD

**Signal interruption:** If the process receives a signal while blocked in `accept()`, it wakes up with errno set to EINTR. Your code should handle this:

```c
while ((client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &addrlen)) < 0) {
    if (errno == EINTR) continue; // Interrupted by signal, retry
    perror("accept failed");
    break;
}
```

### SYN Cookies: A Special Case

Modern systems use **SYN cookies** to defend against SYN flood attacks:

**Problem:** SYN queue has limited size. Attackers can fill it with fake SYNs, preventing legitimate connections.

**Solution:** When SYN queue is full, kernel doesn't store state:
1. Encodes connection info into the sequence number of SYN-ACK
2. Doesn't allocate SYN queue entry
3. When ACK arrives, decodes info from sequence number
4. Validates and creates connection directly in accept queue

**Trade-off:** Some TCP options are lost (window scaling, SACK) when using SYN cookies.

### Practical Implications

**Queue overflow scenarios:**

1. **SYN queue full:** New SYNs are dropped. Client sees connection timeout. Enable SYN cookies to mitigate.

2. **Accept queue full:** Final ACKs are dropped. Connection stays in SYN queue. Client thinks it's connected, but server hasn't accepted. Client's first send() triggers RST. This is why slow accept() loops hurt performance.

**Best practices:**
- Set appropriate backlog (typically 128-1024 for busy servers)
- Call `accept()` in a tight loop to drain the queue quickly
- Monitor `/proc/net/netstat` for `ListenOverflows` counter
- Use non-blocking sockets with epoll for scalability

---

## 4. Multi-Threaded Server: The Boss-Worker Pattern

The simplest concurrent server model is the **boss-worker pattern** (also called thread-per-connection or thread pool model).

### Architecture Overview

**Boss Thread:**
- Runs the main accept loop
- Listens on the server socket
- Accepts new connections
- Spawns/assigns worker thread for each client
- Never handles client data directly

**Worker Threads:**
- Each handles exactly one client connection
- Owns the client FD for that connection's lifetime
- Reads requests, processes them, sends responses
- Cleans up and exits when client disconnects

### Basic Implementation

```c
void* handle_client(void* arg) {
    int client_fd = *(int*)arg;
    free(arg); // Free the heap-allocated FD
    
    char buffer[4096];
    while (1) {
        ssize_t bytes = recv(client_fd, buffer, sizeof(buffer), 0);
        if (bytes <= 0) break; // Client disconnected or error
        
        // Process request...
        send(client_fd, response, response_len, 0);
    }
    
    close(client_fd);
    return NULL;
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    // ... bind, listen ...
    
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t addrlen = sizeof(client_addr);
        
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &addrlen);
        if (client_fd < 0) continue;
        
        // CRITICAL: Heap allocate the FD
        int* client_fd_ptr = malloc(sizeof(int));
        *client_fd_ptr = client_fd;
        
        pthread_t thread;
        pthread_create(&thread, NULL, handle_client, client_fd_ptr);
        pthread_detach(thread); // Don't need to join
    }
}
```

### Why Heap Allocation is CRITICAL

This is a common bug that causes mysterious, intermittent failures. Let's understand why:

**Broken approach (stack allocation):**
```c
while (1) {
    int client_fd = accept(server_fd, ...);
    
    pthread_create(&thread, NULL, handle_client, &client_fd); // BUG!
}
```

**The problem:**
1. `client_fd` is a **local variable** on the main thread's stack
2. Its address (`&client_fd`) is passed to the worker thread
3. Main thread loops immediately, accepting the next connection
4. `client_fd` gets **overwritten** with the new client's FD
5. Worker thread reads `client_fd` at some point → **sees the wrong FD!**

**Race condition scenario:**
```
Time 0: Client A connects, client_fd = 5, thread A created
Time 1: Thread A hasn't read client_fd yet
Time 2: Client B connects, client_fd = 6 (OVERWRITES)
Time 3: Thread A finally reads *arg → gets 6 instead of 5!
Time 4: Thread A handles Client B's connection
Time 5: Thread B (created for client 6) also handles client 6
Result: Client A's connection is orphaned, Client B is handled by two threads!
```

**Solution - heap allocation:**
```c
int* client_fd_ptr = malloc(sizeof(int));
*client_fd_ptr = client_fd;
pthread_create(&thread, NULL, handle_client, client_fd_ptr);
```

Now each thread gets its **own heap-allocated copy** that persists beyond the loop iteration. The worker thread must `free()` it after copying the value.

**Alternative (better for performance) - thread pool:**
```c
typedef struct {
    int client_fd;
    struct sockaddr_in client_addr;
} client_info_t;

// Pre-allocate from a pool, reuse after thread finishes
```

### Thread Detachment vs. Joining

**Detached threads:**
```c
pthread_detach(thread);
```
- Thread resources are automatically cleaned up when it exits
- Can't join (wait for) the thread later
- Good for fire-and-forget worker threads

**Joinable threads:**
```c
pthread_join(thread, NULL); // Blocks until thread exits
```
- Must explicitly join to free resources
- Allows retrieving thread's return value
- Useful when you need to wait for completion

For a long-running server with potentially thousands of connections, detached threads are preferable - you don't want to track and join thousands of threads.

### Resource Management

**File descriptor limits:**
- Each thread keeps a client FD open
- System has limits: `ulimit -n` (typically 1024 default)
- Need to raise limits for high-concurrency servers
- Each FD consumes kernel memory

**Thread limits:**
- Creating threads has overhead (stack allocation, typically 2-10 MB per thread)
- System limits on thread count (varies by kernel configuration)
- Thread creation/destruction has CPU cost

**Better approach for high concurrency:**
- **Thread pool**: Pre-create a fixed number of threads
- Threads pull work from a queue instead of creating new threads per connection
- Bounds resource usage
- Eliminates thread creation overhead

---

## 5. Complexities of Multi-Threading: Synchronization and Race Conditions

While the boss-worker pattern seems straightforward, shared state introduces serious complexity.

### When Shared State is Necessary

Consider these common scenarios:

1. **Connection counter**: Tracking how many clients are currently connected
2. **Shared cache**: Multiple clients querying the same data
3. **Rate limiting**: Tracking requests per client IP across all connections
4. **Statistics**: Aggregating metrics from all worker threads
5. **Graceful shutdown**: Signaling all workers to stop

All of these require **shared memory** that multiple threads access concurrently.

### Race Conditions: The Fundamental Problem

A **race condition** occurs when the correctness of the program depends on the relative timing of events, specifically when multiple threads access shared data without proper synchronization.

**Classic example: Increment counter**

```c
int connection_count = 0; // Shared global

void* handle_client(void* arg) {
    connection_count++; // RACE CONDITION!
    
    // ... handle client ...
    
    connection_count--;
}
```

**Why this is broken:**

The seemingly atomic `connection_count++` actually compiles to multiple assembly instructions:

```assembly
mov eax, [connection_count]  ; Read current value into register
inc eax                       ; Increment register
mov [connection_count], eax  ; Write back to memory
```

**Interleaving scenario:**
```
Initial: connection_count = 10

Thread A: mov eax, [connection_count]  → eax = 10
Thread B: mov eax, [connection_count]  → eax = 10
Thread A: inc eax                       → eax = 11
Thread B: inc eax                       → eax = 11
Thread A: mov [connection_count], eax   → connection_count = 11
Thread B: mov [connection_count], eax   → connection_count = 11

Expected: 12, Actual: 11 (lost update!)
```

This is called a **lost update** - one thread's write is overwritten by another.

### Types of Race Conditions

**1. Read-Modify-Write**
```c
x = x + 1;  // Read x, modify it, write back
```

**2. Check-Then-Act**
```c
if (cache[key] == NULL) {     // Check
    cache[key] = fetch_data(); // Act
}
// Two threads might both see NULL and both fetch!
```

**3. Multiple variable inconsistency**
```c
// Transfer money between accounts
account_a -= 100;
// THREAD SWITCH HERE - accounts temporarily inconsistent!
account_b += 100;
```

### Synchronization Primitives

**Mutexes (Mutual Exclusion Locks)**

```c
pthread_mutex_t count_mutex = PTHREAD_MUTEX_INITIALIZER;
int connection_count = 0;

void* handle_client(void* arg) {
    pthread_mutex_lock(&count_mutex);
    connection_count++; // Now atomic
    pthread_mutex_unlock(&count_mutex);
    
    // ... handle client ...
    
    pthread_mutex_lock(&count_mutex);
    connection_count--;
    pthread_mutex_unlock(&count_mutex);
}
```

**How mutexes work:**
- Only one thread can hold the lock at a time
- If lock is held, other threads block (sleep) waiting for it
- Kernel manages the waiting queue
- When lock is released, kernel wakes one waiting thread

**Critical section:** Code between lock/unlock is the **critical section** - only one thread executes it at a time.

**Deadlock danger:**
```c
pthread_mutex_t mutex_a, mutex_b;

// Thread 1
pthread_mutex_lock(&mutex_a);
pthread_mutex_lock(&mutex_b); // Waits for Thread 2
pthread_mutex_unlock(&mutex_b);
pthread_mutex_unlock(&mutex_a);

// Thread 2
pthread_mutex_lock(&mutex_b);
pthread_mutex_lock(&mutex_a); // Waits for Thread 1 - DEADLOCK!
pthread_mutex_unlock(&mutex_a);
pthread_mutex_unlock(&mutex_b);
```

**Deadlock prevention:** Always acquire locks in the same order globally.

**Reader-Writer Locks**

When you have many readers, few writers, and reads don't modify data:

```c
pthread_rwlock_t cache_lock;

// Multiple readers can hold this simultaneously
pthread_rwlock_rdlock(&cache_lock);
data = cache[key];
pthread_rwlock_unlock(&cache_lock);

// Writers get exclusive access
pthread_rwlock_wrlock(&cache_lock);
cache[key] = new_data;
pthread_rwlock_unlock(&cache_lock);
```

**Condition Variables**

For signaling between threads:

```c
pthread_mutex_t queue_mutex;
pthread_cond_t queue_cond;
Queue work_queue;

// Producer (main thread)
pthread_mutex_lock(&queue_mutex);
enqueue(&work_queue, client_fd);
pthread_cond_signal(&queue_cond); // Wake one waiting worker
pthread_mutex_unlock(&queue_mutex);

// Consumer (worker thread)
pthread_mutex_lock(&queue_mutex);
while (is_empty(&work_queue)) {
    pthread_cond_wait(&queue_cond, &queue_mutex); // Atomically unlocks and waits
}
client_fd = dequeue(&work_queue);
pthread_mutex_unlock(&queue_mutex);
```

### Performance Implications

**Lock contention:**
- If many threads compete for the same lock, they serialize
- Performance degrades to single-threaded (or worse due to context switching)
- Solution: Fine-grained locking (separate locks for different data) or lock-free data structures

**Context switching:**
- Threads blocking on locks trigger context switches
- Saving/restoring CPU state is expensive (flush pipeline, TLB, cache pollution)
- Excessive context switching can make multi-threaded code slower than single-threaded

**Cache coherence:**
- Modern CPUs have per-core caches
- When thread on CPU A writes shared data, CPU B's cache must invalidate
- Causes cache misses and memory bus traffic
- False sharing: Two variables on same cache line accessed by different threads

### Why This Led to Event Loops

The multi-threaded model has inherent problems:

1. **Complexity**: Synchronization primitives are error-prone
2. **Scalability**: Thread-per-connection doesn't scale to 10,000+ connections
3. **Resource overhead**: Each thread consumes stack space (megabytes)
4. **Context switching**: OS scheduling overhead grows with thread count
5. **Debugging**: Race conditions are non-deterministic and hard to reproduce

This motivated a different approach: **event-driven architecture**.

---

## 6. The Event Loop Philosophy

An **event loop** is a fundamentally different approach to concurrency that avoids threads entirely (or uses very few).

### Core Concept

Instead of blocking and waiting for events, you:
1. Register interest in multiple events (new connection, data ready, etc.)
2. Wait for ANY of them to occur
3. When an event fires, handle it
4. Immediately return to waiting

**Pseudo-code:**
```c
while (true) {
    events = wait_for_events(); // Blocks until something happens
    for each event in events:
        handle_event(event);
}
```

### Why Event Loops Must Be Non-Blocking

This is **CRITICAL**: Every operation in the event loop must be non-blocking.

**Why?** The entire application runs in a single thread (or very few threads). If ANY operation blocks:
- The entire event loop freezes
- All clients stop being served
- New connections pile up in the accept queue
- The application appears hung

**Example of blocking disaster:**
```c
while (true) {
    events = wait_for_events();
    for each event in events:
        if (event is new connection):
            client_fd = accept(server_fd, ...); // OK, we know connection is ready
        if (event is client data ready):
            // BLOCKING READ - DISASTER!
            recv(client_fd, buffer, 1024, 0); // If client sends slowly, entire loop blocks!
```

**Solution:** All I/O must be **non-blocking**:
```c
fcntl(fd, F_SETFL, O_NONBLOCK);
```

With non-blocking mode:
- `recv()` returns immediately even if no data available (returns -1, errno = EAGAIN)
- `send()` returns immediately even if send buffer is full
- `accept()` returns immediately even if no connections pending

### Event Loop Benefits

1. **No context switching:** Single thread serving all clients
2. **No synchronization:** No locks, mutexes, or race conditions
3. **Predictable performance:** No surprising lock contention
4. **Scalability:** Can handle 10,000+ connections with minimal memory
5. **Simplicity:** Linear control flow, easier to reason about

### Event Loop Challenges

1. **Everything must be non-blocking:** Can't call `sleep()`, blocking file I/O, etc.
2. **Callback hell:** Complex logic becomes nested callbacks (mitigated by async/await in modern languages)
3. **CPU-intensive tasks block:** Long computations still freeze the loop (solution: offload to thread pool)
4. **Debugging**: Stack traces are less informative with callbacks

---

## 7. State Machines in Event-Driven Servers

In a threaded model, each connection has its own thread, so you can write linear code:

```c
void handle_client(int fd) {
    recv_request(fd);
    process_request();
    send_response(fd);
}
```

In an event loop, you can't block waiting for the full request. You must track **state** for each connection.

### The State Machine Approach

Each connection is in one of several states:

```c
typedef enum {
    STATE_READING_REQUEST,
    STATE_PROCESSING,
    STATE_WRITING_RESPONSE,
    STATE_CLOSED
} connection_state_t;

typedef struct {
    int fd;
    connection_state_t state;
    char* request_buffer;
    size_t bytes_received;
    char* response_buffer;
    size_t bytes_sent;
} connection_t;
```

**Event handling becomes state transitions:**

```c
void handle_event(connection_t* conn, int event_type) {
    switch (conn->state) {
        case STATE_READING_REQUEST:
            if (event_type == DATA_AVAILABLE) {
                ssize_t n = recv(conn->fd, conn->request_buffer + conn->bytes_received, ...);
                if (n > 0) {
                    conn->bytes_received += n;
                    if (request_complete(conn)) {
                        conn->state = STATE_PROCESSING;
                        process_request(conn);
                        conn->state = STATE_WRITING_RESPONSE;
                    }
                }
            }
            break;
            
        case STATE_WRITING_RESPONSE:
            if (event_type == SOCKET_WRITABLE) {
                ssize_t n = send(conn->fd, conn->response_buffer + conn->bytes_sent, ...);
                if (n > 0) {
                    conn->bytes_sent += n;
                    if (conn->bytes_sent >= conn->response_length) {
                        conn->state = STATE_READING_REQUEST;
                        reset_connection(conn);
                    }
                }
            }
            break;
    }
}
```

### Why State Machines?

**Problem:** In an event loop, you're called when data arrives, but you might not have the complete request yet. You return control to the event loop, and when more data arrives, you're called again.

**Solution:** Store the connection's state (what stage of the request/response cycle it's in) so you can resume where you left off.

**Real-world example - HTTP request:**
```
Event 1: "GET /index.html" arrives → STATE_ADING_HEADERS
Event 2: " HTTP/1.1\r\n" arrives → Still reading headers
Event 3: "Host: example.com\r\n" arrives → Still reading headers
Event 4: "\r\n" arrives → Headers complete! STATE_PROCESSING
```

Without state tracking, you'd lose context between events.

### State Explosion Challenge

Complex protocols lead to many states:

```c
enum {
    STATE_INIT,
    STATE_READING_HEADERS,
    STATE_READING_BODY,
    STATE_PARSING_REQUEST,
    STATE_AUTHENTICATING,
    STATE_FETCHING_DATA,
    STATE_RENDERSPONSE,
    STATE_WRITING_HEADERS,
    STATE_WRITING_BODY,
    STATE_KEEPALIVE,
    STATE_CLOSING
};
```

**Managing complexity:**
- Hierarchical state machines (substates)
- Protocol parsers that maintain their own state
- Framework abstractions (like Node.js promises/async-await)

---

## 8. epoll: The Ultimate Event Notification Mechanism

`epoll` is Linux's high-performance I/O event notification system, designed to scale to tens of thousands of file descriptors.

### Why Not select() or poll()?

**select():**
```c
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(fd1, &readfds);
FD_SET(fd2, &readfds);
// ... set all FDs ...
select(max_fd + 1, &readfds, NULL, NULL, NULL);
// Check which FDs are ready
if (FD_ISSET(fd1, &readfds)) { /* handle fd1 */ }
```

**Problems:**
- Limited to 1024 FDs (FD_SETSIZE limit)
- O(n) kernel overhead: Kernel must iterate all FDs to check readiness
- O(n) userspace overhead: Must check each FD with FD_ISSET
- Must rebuild fd_set on every call

**poll():**
```c
struct pollfd fds[1000];
fds[0].fd = fd1;
fds[0].events = POLLIN;
// ... setup all FDs ...
poll(fds, nfds, -1);
// Check which FDs are ready
for (int i = 0; i < nfds; i++) {
    if (fds[i].revents & POLLIN) { /* handle */ }
}
```

**Better than select:**
- No 1024 FD limit
- Uses array instead of bitmask

**Still problematic:**
- O(n) kernel overhead: Kernel still iterates all FDs
- O(n) userspace overhead: Must iterate to find ready FDs
- Must pass entire array on each call

**Why this matters:**
- With 10,000 connections, kernel scans 10,000 FDs on each poll
- Even if only 10 have events, you scan all 10,000
- Doesn't scale

### epoll Design Philosophy

epoll solves this with a fundamentally different approach:

1. **Persistent registration**: Tell kernel once which FDs to monitor
2. **Interest list**: Kernel maintains which FDs you care about
3. **Ready list**: Kernel maintains which FDs have events
4. **Return only ready FDs**: Get back only what's ready

**Performance:**
- O(1) to add/modify/delete FD
- O(number of ready FDs) to wait - not O(total FDs)
- No copying entire set on each call

### The Three epoll System Calls

**1. epoll_create1() - Create an epoll instance**

```c
int epoll_fd = epoll_create1(0);
```

**Returns:** A file descriptor representing the epoll instance itself

**What it creates:**
- Interest list (red-black tree in kernel)
- Ready list (doubly-linked list in kernel)
- Wait queue for processes calling epoll_wait

**The epoll FD** is itself a file descriptor. You can even add it to another epoll instance for advanced use cases!

**2. epoll_ctl() - Control the interest list**

```c
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
```

**Parameters:**
- `epfd`: The epoll instance FD
- `op`: Operation (EPOLL_CTL_ADD, EPOLL_CTL_MOD, EPOLL_CTL_DEL)
- `fd`: The file descriptor to add/modify/delete
- `event`: Describes what events to monitor and any user data

**epoll_event structure:**
```c
struct epoll_event {
    uint32_t events;  // Event mask (EPOLLIN, EPOLLOUT, etc.)
    epoll_data_t data; // User data
};

typedef union epoll_data {
    void *ptr;
    int fd;
    uint32_t u32;
    uint64_t u64;
} epoll_data_t;
```

**Common events:**
- `EPOLLIN`: Data available to read (recv won't block)
- `EPOLLOUT`: Socket ready for writing (send won't block)
- `EPOLLRDHUP`: Peer closed connection (half-close)
- `EPOLLERR`: Error on FD
- `EPOLLHUP`: Hangup (full close)
- `EPOLLET`: Edge-triggered mode (more on this later)
- `EPOLLONESHOT`: Disable FD after one event (for thread safety)

**Usage examples:**

```c
// Add listening socket
struct epoll_event ev;
ev.events = EPOLLIN; // Interested in incoming connections
ev.data.fd = server_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);

// Add client socket
ev.events = EPOLLIN | EPOLLET; // Read + edge-triggered
ev.data.fd = client_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);

// Modify to also watch for writability
ev.events = EPOLLIN | EPOLLOUT | EPOLLET;
epoll_ctl(epoll_fd, EPOLL_CTL_MOD, client_fd, &ev);

// Remove FD
epoll_ctl(epoll_fd, EPOLL_CTL_DEL, client_fd, NULL);
```

**3. epoll_wait() - Wait for events**

```c
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
```

**Parameters:**
- `epfd`: The epoll instance
- `events`: Array to receive ready events (OUTPUT parameter)
- `maxevents`: Size of events array
- `timeout`: Milliseconds to wait (-1 = infinite, 0 = non-blocking)

**Returns:** Number of ready FDs, or -1 on error

**What happens:**
1. Kernel checks ready list
2. If empty and timeout != 0, process sleeps
3. When events occur, kernel wakes process
4. Kernel copies ready events to user's array
5. Returns count of ready events

**Usage:**
```c
struct epoll_event events[MAX_EVENTS];

while (1) {
    int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
    
    for (int i = 0; i < nfds; i++) {
        if (events[i].data.fd == server_fd) {
            // New connection
            handle_accept();
        } else {
            // Existing client
            handle_client(events[i].data.fd);
        }
    }
}
```

### The Two Lists: Interest and Ready

**Interest List (epoll instance internals):**

Data structure: **Red-black tree** (self-balancing binary search tree)
- Key: file descriptor number
- Value: struct with events mask and user data
- O(log n) lookup, insertion, deletion

**Why red-black tree?**
- Need fast lookup when FD has an event
- Need fast add/remove when connections come/go
- Hash table would work too, but RB-tree has better worst-case

**Ready List:**

Data structure: **Doubly-linked list**
- Contains FDs that have events right now
- Populated by kernel callbacks when events occur

**How FDs move to ready list:**
1. When you register an FD with epoll_ctl, kernel attaches a callback to the FD's wait queue
2. When the FD becomes ready (data arrives, socket writable, etc.), kernel invokes the callback
3. Callback adds the FD to epoll's ready list (if not already there)
4. If a process is blocked in epoll_wait, kernel wakes it

**Example flow:**
```
1. FD 5 registered with epoll (in interest list)
2. Packet arrives for FD 5
3. Kernel's network stack processes packet
4. Data added to FD 5's receive buffer
5. FD 5's wait queue callbacks invoked
6. epoll's callback adds FD 5 to ready list
7. Process in epoll_wait woken up
8. epoll_wait returns FD 5 in events array
```

### Edge-Triggered (ET) vs Level-Triggered (LT) Modes

This is one of the most misunderstood aspects of epoll.

**Level-Triggered (LT) - DEFAULT**

**Behavior:** epoll_wait returns a FD as ready whenever the condition is true.

**Example:**
```
1. 100 bytes arrive on socket
2. epoll_wait returns FD 5 as ready
3. You read 50 bytes
4. Next epoll_wait STILL returns FD 5 (50 bytes remain!)
5. You read 50 bytes
6. Next epoll_wait doesn't return FD 5 (buffer empty)
```

**Characteristics:**
- You can read less than all available data
- If you don't drain the buffer, you'll be notified again
- Works with blocking or non-blocking FDs
- More forgiving, less efficient

**Edge-Triggered (ET) - EPOLLET flag**

**Behavior:** epoll_wait returns a FD as ready only when state **changes** (transitions).

**Example:**
```
1. 100 bytes arrive on socket (state change: empty → has data)
2. epoll_wait returns FD 5 as ready
3. You read 50 bytes
4. Next epoll_wait DOES NOT return FD 5 (no state change, still has data)
5. You read 50 bytes
6. Next epoll_wait DOES NOT return FD 5 (no new data arrived)
7. 200 bytes arrive (state change: idle → new data)
8. epoll_wait returns FD 5 as ready
```

**Characteristics:**
- MUST use non-blocking FDs
- MUST read untiGAIN (drain completely)
- More efficient (fewer spurious wake-ups)
- Less forgiving (easy to miss data if not careful)

**Critical ET requirement - read loop:**
```c
if (events[i].events & EPOLLIN) {
    while (1) {
        ssize_t n = recv(fd, buffer, sizeof(buffer), 0);
        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                break; // No more data, we're done
            } else {
                perror("recv error");
                break;
            }
        } else if (n == 0) {
            // Connection closed
            break;
        }
        // Process n bytes...
    }
}
```

**Why ET is faster:**
- LT: If 1000 sockets have pending data, epoll_wait returns all 1000 every call until you drain them
- ET: epoll_wait returns them once when data arrives, then only again when NEW data arrives
- Reduces number of system calls
- Reduces CPU time spent in kernel

**When to use which:**
- LT: Simpler, good for lower-concurrency servers, compatible with existing code
- ET: More control, better performance at scale, requires careful programming

### Putting It Together: epoll Lifecycle

```c
// 1. Create epoll instance
int epoll_fd = epoll_create1(0);

// 2. Add listening socket
struct epoll_event ev;
ev.events = EPOLLIN;
ev.data.fd = server_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);

// 3. Event loop
struct epoll_event events[MAX_EVENTS];
while (1) {
    int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
    
    for (int i = 0; i < nfds; i++) {
        if (events[i].data.fd == server_fd) {
            // Accept new connection
            int client_fd = accept(server_fd, NULL, NULL);
            fcntl(client_fd, F_SETFL, O_NONBLOCK); // CRITICAL!
            
            ev.events = EPOLLIN | EPOLLET;
            ev.data.fd = client_fd;
            epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);
        } else {
            // Handle client event
            handle_client_event(events[i].data.fd, events[i].events);
        }
    }
}
```

---

## 9. Integrating epoll into the Event Loop

Now we bring everything together: event loop + state machines + epoll.

### Server Architecture

```c
typedef struct {
    int fd;
    connection_state_t state;
    char recv_buffer[4096];
    size_t recv_offset;
    char send_buffer[4096];
    size_t send_offset;
    size_t send_len;
} connection_t;

// Hash map: fd → connection_t
connection_t* connections[MAX_CONNECTIONS];
```

### The Complete Event Loop

```c
int main() {
    // Setup
    int server_fd = socket(AFNET, SOCK_STREAM, 0);
    // ... bind, listen ...
    fcntl(server_fd, F_SETFL, O_NONBLOCK);
    
    int epoll_fd = epoll_create1(0);
    
    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = server_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);
    
    struct epoll_event events[MAX_EVENTS];
    
    // Event loop
    while (1) {
        int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
        
        for (int i = 0; i < nfds; i++) {
            int fd = events[i].data.fd;
            uint32_t ev_mask = events[i].events;
            
            // Case 1: New connection on listening socket
            if (fd == server_fd) {
                handle_new_connection(epoll_fd, server_fd);
            }
            // Case 2: Event on existing client connection
            else {
                handle_client_event(epoll_fd, fd, ev_mask);
            }
        }
    }
}
```

### Handling New Connections

```c
void handle_new_connection(int epoll_fd, int server_fd) {
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t addrlen = sizeof(client_addr);
        
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &addrlen);
        
        if (client_fd < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // No more pending connections
                break;
            } else {
                perror("accept");
                break;
            }
        }
        
        // Make non-blocking (CRITICAL!)
        fcntl(client_fd, F_SETFL, O_NONBLOCK);
        
        // Create connection state
        connection_t* conn = malloc(sizeof(connection_t));
        conn->fd = client_fd;
        conn->state = STATE_READING_REQUEST;
        conn->recv_offset = 0;
        conn->send_offset = 0;
        conn->send_len = 0;
        connections[client_fd] = conn;
        
        // Register with epoll
        struct epoll_event ev;
        ev.events = EPOLLIN | EPOLLET; // Read + edge-triggered
        ev.data.fd = client_fd;
        epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);
        
        printf("New connection: fd=%d\n", client_fd);
    }
}
```

**Why the while loop?** 

In edge-triggered mode, if multiple connections are pending, we only get ONE notification. We must drain the accept queue completely.

### Classifying Events

```c
void handle_client_event(int epoll_fd, int fd, uint32_t events) {
    connection_t* conn = connections[fd];
    if (!conn) return; // Stale event
    
    // Connection error or closed
    if (events & (EPOLLERR | EPOLLHUP)) {
        close_connection(epoll_fd, fd);
        return;
    }
    
    // Peer closed write side (half-close)
    if (events & EPOLLRDHUP) {
        // Can still send remaining data, then close
        conn->state = STATE_CLOSING;
    }
    
    // Data available to read
    if (events & EPOLLIN) {
        handle_read(epoll_fd, conn);
    }
    
    // Socket ready for writing
    if (events & EPOLLOUT) {
        handle_write(epoll_fd, conn);
    }
}
```

### Handling Reads (ET Mode)

```c
void handle_read(int epoll_fd, connection_t* conn) {
    while (1) {
        ssize_t n = recv(conn->fd, 
                        conn->recv_buffer + conn->recv_offset,
                        sizeof(conn->recv_buffer) - conn->recv_offset,
                        0);
        
        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // No more data available
                break;
            } else {
                perror("recv");
                close_connection(epoll_fd, conn->fd);
                return;
            }
        } else if (n == 0) {
            // Connection closed by peer
            close_connection(epoll_fd, conn->fd);
            return;
        }
        
        conn->recv_offset += n;
        
        // Try to process complete requests
        while (has_complete_request(conn)) {
            process_request(conn);
            
            // If we have a response ready, enable EPOLLOUT
            if (conn->send_len > 0) {
                struct epoll_event ev;
                ev.events = EPOLLIN | EPOLLOUT | EPOLLET;
                ev.data.fd = conn->fd;
                epoll_ctl(epoll_fd, EPOLL_CTL_MOD, conn->fd, &ev);
            }
        }
    }
}
```

### Registering New Connections to epoll

When we accept a new connection, we immediately register it with epoll:

```c
struct epoll_event ev;
ev.events = EPOLLIN | EPOLLET;
ev.data.fd = client_fd;
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);
```

**Why EPOLLIN initially?**
- We want to know when the client sends data
- We don't set EPOLLOUT initially because we have nothing to send yet

**When to add EPOLLOUT?**
- Only when we have data to send but the send buffer is full
- Modify the registration to include EPOLLOUT
- After sending all data, modify back to just EPOLLIN

**Optimizing epoll_ctl calls:**
- Each epoll_ctl is a system call (expensive)
- Only modify when necessary
- Some servers batch modifications

---

## 10. Non-Blocking I/O: The recv() Challenge

### Why recv() is Blocking by Default

When you call `recv()` on a blocking socket:

```c
ssize_t n = recv(fd, buffer, 1024, 0);
```

**Kernel behavior:**
1. Check if data is in the receive buffer
2. If YES: Copy data to user buffer, return immediately
3. If NO: Put process to sleep until data arrives

**The kernel knows when "full data" arrives** because:
- For TCP: Kernel maintains the TCP stream. Data is "ready" as soon as ANY bytes arrive.
- Kernel doesn't understand application protocols (HTTP, Redis, etc.)
- Kernel just provides bytes - YOU define what's "complete"

### The Problem with Blocking recv() in Event Loops

```c
// BROKEN - Don't do this!
if (events & EPOLLIN) {
    recv(fd, buffer, 1024, 0); // Might block if only 512 bytes available!
}
```

**Scenario:**
1. epoll_wait returns fd as ready (1024 bytes available)
2. You call recv(fd, buffer, 2048, 0)
3. recv only copies 1024 bytes and... **BLOCKS waiting for more!**
4. Entire event loop freezes
5. All clients stop being served

### Making Sockets Non-Blocking

```c
fcntl(fd, F_SETFL, O_NONBLOCK);
```

Now `recv()` never blocks:
```c
ssize_t n = recv(fd, buffer, 1024, 0);
if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
    // No data available right now - normal in non-blocking mode
}
```

### The Partial Data Problem

**Challenge:** You need to know if you received a complete message or partial data.

**Example - HTTP:**
```
Data received in 3 chunks:
Chunk 1: "GET /index.html HTTP/"
Chunk 2: "1.1\r\nHost: example.c"
Chunk 3: "om\r\n\r\n"
```

You only have a complete request after chunk 3!

### Protocol-Specific Parsing

**Solution 1: Delimiter-based (e.g., HTTP, Redis RESP)**

```c
bool has_complete_request(connection_t* conn) {
    // Look for "\r\n\r\n" in buffer
    char* end = memmem(conn->recv_buffer, conn->recv_offset, "\r\n\r\n", 4);
    return (end != NULL);
}
```

**Solution 2: Length-prefixed (common in binary protocols)**

```c
bool has_complete_request(connection_t* conn) {
    if (conn->recv_offset < 4) return false; // Need length header
    
    uint32_t msg_len = *(uint32_t*)conn->recv_buffer;
    return (conn->recv_offset >= 4 + msg_len);
}
```

**Solution 3: Fixed-length messages**

```c
bool has_complete_request(connection_t* conn) {
    return (conn->recv_offset >= FIXED_MESSAGE_SIZE);
}
```

### Answering the Critical Question

**"Why can't we leverage the kernel's knowledge of when full data is received for non-blocking recv()?"**

**The answer: The kernel DOESN'T know when your "full message" is received.**

**What the kernel knows:**
- TCP: Data in the receive buffer (any amount)
- TCP push flag: Sender says "deliver what you have"
- FIN: Sender closed connection

**What the kernel DOESN'T know:**
- Your application protocol (HTTP, custom binary, etc.)
- Message boundaries
- When a "complete request" has arrived

**Example:**

Your protocol: "Send a 4-byte length, then that many bytes of data"

```
Server expects: [0x00, 0x00, 0x04, 0x00, 'T', 'E', 'S', 'T'] (8 bytes total)

Packet 1 arrives: [0x00, 0x00]
Packet 2 arrives: [0x04, 0x00, 'T', 'E']
Packet 3 arrives: ['S', 'T']
```

Kernel knows:
- After packet 1: 2 bytes available
- After packet 2: 6 bytes available
- After packet 3: 8 bytes available

Kernel doesn't know:
- That you need 8 bytes for a complete message
- That the first 4 bytes define the length
- When to "flush" data to userspace

**Why blocking recv() seems to "know":**

Blocking recv(fd, buf, 1024, 0) returns when:
- At least 1 byte is available, OR
- Connection is closed

It doesn't wait for "complete" anything - just ANY data.

If you call recv(fd, buf, 1024, 0) requesting 1024 bytes but only 100 are available:
- Blocking socket: Returns 100 immediately
- Non-blocking socket: Returns 100 immediately

**The key difference:**

Blocking recv when NO data is available: **Waits** for data to arrive

Non-blocking recv when NO data is available: **Returns EAGAIN** immediately

Neither "knows" about message boundaries - you must implement that logic.

### Best Practice: Parsing State Machine

```c
typedef enum {
    PARSE_NEED_MORE,
    PARSE_COMPLETE,
    PARSE_ERROR
} parse_result_t;

parse_result_t parse_request(connection_t* conn, request_t* out_req) {
    // Protocol-specific parsing
    // Returns PARSE_NEED_MORE if incomplete
    // Returns PARSE_COMPLETE when full request ready
    // Advances conn->recv_offset past parsed data
}
```

---

## 11. The send() Blocking Problem and EPOLLOUT

Just as `recv()` can block, `send()` can too - and it's equally problematic in event loops.

### Why send() Blocks

When you call `send()`:

```c
ssize_t n = send(fd, buffer, 1024, 0);
```

**Kernel process:**
1. Copy data from user buffer to **socket send buffer** (in kernel memory)
2. TCP stack sends data over network
3. Data remains in send buffer until **acknowledged by peer**
4. If send buffer is full, send() blocks (on blocking sockets)

**Send buffer can fill up because:**
- Client reads slowly (slow consumer)
- Network congestion
- Client's receive buffer is full (TCP flow control)
- Large response doesn't fit in one buffer

### TCP Flow Control Mechanism

TCP prevents sender from overwhelming receiver using **window size**:

1. Receiver advertises "receive window" size (how much buffer space it has)
2. Sender can't send more data than receiver's window allows
3. When receiver's buffer fills, it advertises window size 0
4. Sender must wait until receiver drains buffer and advertises window > 0
5. This is automatic - TCP handles it

**Problem:** If client stops reading (crashed app, slow processing), your server's send() blocks waiting for window to open.

### Non-Blocking send() Behavior

```c
fcntl(fd, F_SETFL, O_NONBLOCK);
ssize_t n = send(fd, response, response_len, 0);
```

**Possible outcomes:**

1. **All data sent:** `n == response_len` (send buffer had space)
2. **Partial send:** `0 < n < response_len` (send buffer partially full)
3. **No data sent:** `n == -1, errno == EAGAIN/EWOULDBLOCK` (send buffer completely full)

**Example:**
```c
char response[10000];
// ... populate response ...

ssize_t n = send(fd, response, 10000, 0);
// n might be 10000, 5000, 0, or -1!
```

### Handling Partial Sends

**Broken approach:**
```c
// DON'T DO THIS!
send(fd, response, response_len, 0);
// What if only half sent? Data lost!
```

**Correct approach:**
```c
void handle_write(int epoll_fd, connection_t* conn) {
    while (conn->send_offset < conn->send_len) {
        ssize_t n = send(conn->fd,
                        conn->send_buffer + conn->send_offset,
                        conn->send_len - conn->send_offset,
                        0);
        
        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // Send buffer full - wait for EPOLLOUT
                return;
            } else {
                perror("send");
                close_connection(epoll_fd, conn->fd);
                return;
            }
        }
        
        conn->send_offset += n;
    }
    
    // All data sent!
    conn->send_offset = 0;
    conn->send_len = 0;
    
    // Disable EPOLLOUT (no more data to send)
    struct epoll_event ev;
    ev.events = EPOLLIN | EPOLLET;
    ev.data.fd = conn->fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_MOD, conn->fd, &ev);
}
```

### Using EPOLLOUT

**EPOLLOUT means:** "The send buffer has space available"

**When to register for EPOLLOUT:**

```c
// Initial send attempt
ssize_t n = send(fd, response, response_len, 0);
if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
    // Send buffer full - register for EPOLLOUT
    struct epoll_event ev;
    ev.events = EPOLLIN | EPOLLOUT | EPOLLET;
    ev.data.fd = fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_MOD, fd, &ev);
    
    // Save response for later
    memcpy(conn->send_buffer, response, response_len);
    conn->send_len = response_len;
    conn->send_offset = 0;
} else if (n < response_len) {
    // Partial send - register for EPOLLOUT
    struct epoll_event ev;
    ev.events = EPOLLIN | EPOLLOUT | EPOLLET;
    ev.data.fd = fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_MOD, fd, &ev);
    
    // Save remaining data
    memcpy(conn->send_buffer, response + n, response_len - n);
    conn->send_len = response_len - n;
    conn->send_offset = 0;
}
```

**When EPOLLOUT fires:**

The kernel is telling you: "I have space in the send buffer now. You can call send() and it won't block (or will send more data)."

**Critical: Disable EPOLLOUT when done:**

If you keep EPOLLOUT registered when you have nothing to send:
- epoll_wait returns immediately every time (send buffer is usually ready)
- Your event loop spins (busy-wait)
- Wastes 100% CPU

**Always:** After sending all data, remove EPOLLOUT from the event mask.

### The TCP Buffering Architecture

Understanding the full picture helps:

```
Application (your code)
    ↓ send()
[Socket Send Buffer] ← Kernel memory, limited size
    ↓ TCP Layer
[Network Interface Card]
    ↓ Network
[Remote NIC]
    ↓ TCP Layer
[Socket Receive Buffer] ← Receiver's kernel memory
    ↓ recv()
Remote Application
```

**Flow control:**
- Receiver advertises receive buffer space via TCP window
- Sender e than receiver's window
- If receiver's buffer full, window = 0, sender must wait
- This propagates: Network full → Send buffer fills → send() blocks/returns EAGAIN

**Congestion control:**
- TCP also throttles sending rate based on network conditions
- Packet loss → slower sending
- This also causes send buffer to fill

### Complete Example: Read and Write

```c
void handle_client_event(int epoll_fd, int fd, uint32_t events) {
    connection_t* conn = connections[fd];
    
    if (events & EPOLLIN)     // Read loop
        while (1) {
            ssize_t n = recv(fd, conn->recv_buffer + conn->recv_offset,
                            sizeof(conn->recv_buffer) - conn->recv_offset, 0);
            if (n < 0) {
                if (errno == EAGAIN) break;
                close_connection(epoll_fd, fd);
                return;
            } else if (n == 0) {
                close_connection(epoll_fd, fd);
                return;
            }
            
            conn->recv_offset += n;
            
            // Process complete requests
            while (has_complete_request(conn)) {
                char response[4096];
                size_t response_len = process_request(conn, response);
                
                // Try to send immediately
                ssize_t sent = send(fd, response, response_len, 0);
                if (sent < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
                    sent = 0; // Treat as "sent nothing"
                }
                
                if (sent < response_len) {
                    // Couldn't send all - save remainder and enable EPOLLOUT
                    memcpy(conn->send_buffer, response + sent, response_len - sent);
                    conn->send_len = response_len - sent;
                    conn->send_offset = 0;
                    
                    struct epoll_event ev;
                    ev.events = EPOLLIN | EPOLLOUT | EPOLLET;
                    ev.data.fd = fd;
                    epoll_ctl(epoll_fd, EPOLL_CTL_MOD, fd, &ev);
                }
            }
        }
    }
    
    if (events & EPOLLOUT) {
        // Write loop
        while (conn->send_offset < conn->send_len) {
            ssize_t n = send(fd, conn->send_buffer + conn->send_offset,
                            conn->send_len - conn->send_offset, 0);
            if (n < 0) {
                if (errno == EAGAIN) return; // Wait for next EPOLLOUT
                close_connection(epoll_fd, fd);
                return;
            }
            conn->send_offset += n;
        }
        
        // All sent - disable EPOLLOUT
        conn->send_len = 0;
        conn->send_offset = 0;
        
        struct epoll_event ev;
        ev.events = EPOLLIN | EPOLLET;
        ev.data.fd = fd;
        epoll_ctl(epoll_fd, EPOLL_CTL_MOD, fd, &ev);
    }
}
```

### Why This Architecture Works

**Concurrency without threads:**
- Single thread serves thousands of connections
- No context switching overhead
- No synchronization complexity

**Fair scheduling:**
- Event loop naturally round-robins between ready connections
- No single slow client can block others

**Resource efficiency:**
- Minimal memory per connection (just state structure)
- No thread stack overhead (typically 2-10 MB per thread)

**Scalability:**
- O(number of ready connections) scaling with epoll
- Handles 10,000+ connections on modest hardware

---

## Conclusion

We've covered the full journey from basic sockets to high-performance event-driven servers:

1. **Sockets as abstractions** for network communication and file descriptors as the unified handle
2. **The socket lifecycle** (socket, bind, listen, accept) and how the kernel manages connection queues
3. **TCP's two-queue system** and how accept() extracts established connections
4. **Multi-threaded approaches** and their complexity (synchronization, resource overhead)
5. **Event loops** as an alternative that avoids threading issues
6. **State machines** for tracking connection progress across multiple events
7. **epoll** as the scalable event notification mechanism with interest/ready lists
8. **Integration** of epoll into event loops, classifying events between new connections and existing clients
9. **Non-blocking I/O challenges** and protocol-specific parsing for determining complete messages
10. **EPOLLOUT** for handling send buffer fullness and avoiding busy-waiting

This architecture - event loop + epoll + non-blocking I/O + state machines - is the foundation of high-performance servers like nginx, Redis, Node.js, and many others. It's more complex than threaded servers but scales to orders of magnitude higher concurrency with better resource efficiency.

The key insight: Instead of threads waiting (blocking) for events, have a single thread **react** to events as they occur, processing each efficiently and moving on to the next. This inversion of control - from "wait for my event" to "I'll tell you when events happen" - is what makes modern servers fast.
