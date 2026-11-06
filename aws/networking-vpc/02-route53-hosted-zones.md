In Amazon Route 53, a hosted zone is ==a container for DNS records that define how to route traffic for a domain and its subdomains==. Route 53 provides two types: public hosted zones for routing traffic across the public internet, and private hosted zones for routing traffic internally within Amazon VPCs. [1, 2, 3]

---

## Public Hosted Zones

- Definition: A container for DNS records that are visible and resolvable from anywhere on the public internet.
- Primary Use: Routing global user traffic to internet-facing resources like websites, public APIs, and mobile app backends.
- How it works: When an external user types your domain name into a browser, the query hits the global DNS system and matches the records (A, CNAME, TXT, etc.) inside your public hosted zone. [4]

## Private Hosted Zones

- Definition: A container for DNS records that are restricted and only resolvable from within specific, designated Amazon Virtual Private Clouds (VPCs). [4, 5]
- Primary Use: Managing internal naming for private infrastructure, such as backend microservices, internal databases, and intranet applications.
- How it works: These records resolve to private IP addresses. They remain entirely hidden from the public internet, keeping internal network layouts secure. [4, 5]

## Prerequisites for Activation

For a private hosted zone to function, you must enable two specific settings on your target VPC:

- `enableDnsHostnames` set to **true**
- `enableDnsSupport` set to **true**

> You might wonder **Why must `enableDnsHostnames` be true if we are manually mapping custom domains to private IPs, and doesn't forcing auto-generated AWS hostnames defeat the purpose of a private hosted zone?**
> 
> If you are manually creating clean, custom names like `db.internal`, the requirement to turn on a switch that generates messy default names like `ip-10-0-0-12.ec2.internal` feels redundant and counterintuitive.
> 
> The reason this setting is mandatory comes down to a limitation in how AWS built the VPC's internal DNS routing table, rather than the hostnames themselves
> 
> The auto-generated AWS hostnames are a byproduct of a combined architectural switch, not the actual feature you need. In the underlying AWS infrastructure, the private hosted zone database and the VPC network do not talk to each other directly; they communicate through a shared internal translation engine. Turning `enableDnsHostnames` to true is the only way to activate this processing engine. If it is off, the VPC's network interface operates in a pure IP-only mode, entirely ignoring the local DNS lookup table and preventing your custom domains from ever reaching Route 53.
> 
> While it feels like it defeats the purpose by cluttering your resources with unwanted default AWS names, you can safely ignore those auto-generated hostnames. They act merely as a background dependency required to open the gateway for your custom private hosted zone records to function.



## Common Architecture Example

Inside your secure corporate network, your frontend web servers need to talk to a backend database. You create a private hosted zone named `corp.internal` and associate it with your application VPC. Inside, you configure:

- An **A Record** mapping `db.corp.internal` to the private IP address (`10.0.2.45`) of your database instance.
- Since `enableDnsSupport` is true, frontend web servers can resolve the db.corp.internal to the specific IP address of the database.