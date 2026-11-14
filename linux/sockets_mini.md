This primer covers the evolution of network programming, from basic file abstractions to high-performance event-driven architectures.

---

## 1. The Foundation: Sockets and File Descriptors

In Unix-like systems, **"Everything is a file."** A **Socket** is simply a special type of file that allows for Inter-Process Communication (IPC) over a network. It acts as an endpoint for sending or receiving data.

### File Descriptors (FDs)
When you open a file or create a socket, the kernel provides your process with a **File Descriptor**—a small, non-negative integer. This integer is an index into a private table managed by the kernel.

* **Process-Specific FD Table:** Each process has its own table. If you have FD `3`, it points to an entry in the Global File Table.
* **Global File Table:** This is the kernel's master list. It tracks every open file/socket in the entire system. It stores the "file offset" (where you are currently reading) and the status flags (read/write/non-blocking).
* **Inode Table (The Hardware Link):** If the FD refers to a file on a disk, the Global File Table points to an **Inode**. The Inode contains the actual disk sector addresses where the data lives. If the FD refers to a socket, it points to a **Socket Structure** in memory containing network buffers and TCP state info.



---

## 2. The 4 Stages of a Server Socket

To make a server functional, it must pass through four distinct system calls.

1.  **`socket()`**: Creates the endpoint. It returns a brand new FD. At this stage, the socket is just an empty resource; it doesn't have an address or a port.
2.  **`bind()`**: Assigns a local address and port to the socket (e.g., "Listen on port 80"). It maps the FD to a specific identity on the network interface.
3.  **`listen()`**: Moves the socket into a **Passive State**. The kernel begins internalizing the "Handshake" process. It returns `0` on success.
4.  **`accept()`**: This is the "extraction" phase. 
    * **The Switch:** You pass the `server_fd` (the "Boss" socket) to `accept()`. 
    * **The Result:** It returns a **new FD** representing the specific connection to that client (the "Worker" socket).
    * **Why two FDs?** The `server_fd` must stay open to continue listening for *other* new people, while the `client_fd` is dedicated to talking to the person who just arrived.

---

## 3. The Kernel’s Waiting Room: How `accept()` Works

The kernel handles the TCP 3-way handshake (`SYN` -> `SYN-ACK` -> `ACK`) entirely in the background. It maintains two internal structures for every listening socket:

* **The SYN Queue:** Holds clients who have sent a `SYN` but haven't finished the handshake yet.
* **The Accept Queue:** Holds clients who have completed the handshake and are ready to be "picked up."

**The Blocking Nature:** When you call `accept()`, your process looks at the **Accept Queue**. If it is empty, the kernel puts your process to sleep. The moment a client moves from the "SYN Queue" to the "Accept Queue," the kernel wakes your process and hands over the FD.



---

## 4. Multi-Threading: The Boss-Worker Approach

To handle multiple clients simultaneously with blocking I/O, we use threads.

* **The Boss:** The main thread stays in a loop calling `accept()`.
* **The Worker:** Every time `accept()` returns a `client_fd`, the Boss spawns a new thread and hands that FD to it.

**Heap Allocation is Critical:** When passing the `client_fd` to a new thread, you must `malloc` a copy of the integer on the heap. If you pass a pointer to a local variable in the Boss loop, the Boss might overwrite that variable with a *new* client's FD before the previous thread has even started, leading to a "race" where two threads try to talk to the same client.

---

## 5. Complexities and Race Conditions

As you add more threads, complexity explodes:

* **Synchronization:** If two threads need to update a shared counter (like "Total Clients Served"), they might both read `5`, increment it to `6`, and write it back. One increment is lost. This is a **Race Condition**. 
* **Primitives:** You must use **Mutexes** (Locks) to ensure only one thread can touch shared data at a time.
* **Context Switching:** Spawning 10,000 threads consumes massive RAM (for stacks) and wastes CPU cycles as the kernel constantly swaps between them.

---

## 6. The Event Loop Philosophy

An **Event Loop** is a single-threaded architecture that handles concurrency without spawning new threads.

* **Non-Blocking Requirement:** For an event loop to work, every operation must be **Non-Blocking**. 
* **The Logic:** If you call `recv()` and there is no data, the function must return immediately with an error code (`EAGAIN`) rather than putting the thread to sleep. This allows the single thread to quickly move on to the next task.

---

## 7. State Machines in Servers

In an event loop, the server becomes a **State Machine**. Because you can't "block" until a command is finished, you have to "remember" where you are for each client.

* **Example:** If a client sends 5 bytes of a 10-byte message, you save those 5 bytes in a buffer and set the client's state to `PARTIAL_READ`. When more data arrives, you check the state and append the new bytes.



---

## 8. Deep Dive into `epoll`

`epoll` is the Linux kernel's highly efficient notification system. It replaces the old, slow `select()` and `poll()` calls. It maintains two key lists:

1.  **The Interest List:** A Red-Black Tree of all File Descriptors you want the kernel to watch.
2.  **The Ready List:** A Doubly Linked List of FDs that have actually had an event (data arrived, connection finished).

### `epoll_wait`
Your program calls `epoll_wait()`. The kernel puts your thread to sleep. When hardware interrupts (NIC) signal that data has arrived, the kernel moves that FD to the **Ready List** and wakes you up. You only receive the list of FDs that have work to do—no more looping through 10,000 idle sockets.

### ET vs. LT Modes
* **Level-Triggered (LT):** The kernel "nags" you. If data is in the buffer, `epoll_wait` will keep telling you the FD is ready until the buffer is empty.
* **Edge-Triggered (ET):** The kernel notifies you **only once** when data arrives. You **must** read until you hit `EAGAIN`, or you will never get another notification for that client.

---

## 9. Applying `epoll` to the Loop

1.  **Register `server_fd`**: Tell `epoll` to watch for `EPOLLIN` on the listener.
2.  **The Loop**: Call `epoll_wait`.
3.  **Classification**:
    * If `event.fd == server_fd`: It's a **New Connection**. Call `accept()`, set the new `client_fd` to non-blocking, and register it with `epoll`.
    * If `event.fd == client_fd`: It's **Data**. Call your read/write logic.

---

## 10. The Challenge of Partial Data

> **Your Question:** Why can we not leverage the kernel's knowledge to know if a "full body" is received for non-blocking `recv()`?

**The Answer:** The TCP stack operates at the **Transport Layer**. It only understands "Bytes." It has no idea what your application data looks like (e.g., a Redis PING or an HTTP GET). 
The kernel "flushes" data to user space as soon as it passes the checksum and ordering checks. It cannot wait for a "full body" because it doesn't know what a "body" is. **You** (the Application Layer) are the only one who knows the protocol rules, so you must be the one to decide if the received bytes constitute a complete request.

---

## 11. `send()` and `EPOLLOUT`

Just like `recv()`, `send()` can block. This happens when the **Kernel's Outgoing Buffer** is full because the client is slow at reading.

* **The Flow:** You try to `send()`. It returns `EAGAIN`.
* **The Strategy:** You don't wait. You save the remaining data in a "Pending Send" buffer and tell `epoll` to watch for **`EPOLLOUT`**.
* **The Resolution:** When the client's TCP window opens up (they send an ACK), your kernel's buffer clears. The kernel triggers an `EPOLLOUT` event. Your event loop sees this, sends the remaining saved data, and then stops watching for `EPOLLOUT`.
