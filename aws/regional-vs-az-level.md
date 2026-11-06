No, you do not need to memorize every service because AWS services are scoped based on physical infrastructure logic and the blast radius of data. [1]

The level at which a service operates (Global, Regional, or Availability Zone) depends entirely on its purpose: whether it manages traffic across the world, mirrors data across a geographic area, or requires low-latency hardware isolation. [2, 3, 4]

---

## The Core Architectural Logic

Understanding how AWS builds its infrastructure reveals why services sit at different levels.

```unset
[ GLOBAL LEVEL: IAM, Route 53, CloudFront ]
                    │
                    ▼
[ REGIONAL LEVEL: S3, DynamoDB, VPC, ALB ]
                    │
                    ▼
[ AZ LEVEL: EC2, EBS, Subnets, RDS (Primary) ]
```

## 1. Availability Zone (AZ) Level: Hardware & Low Latency [5]

Services operate at the AZ level when they require physical hardware assignment or ultra-low network latency. [6]

- The Logic: Physical servers, hard drives, and cables exist in a specific building. If a service relies on a single piece of hardware running in real-time, it is bound to that AZ. [7, 8, 9]
- Examples:
    
    - EC2 Instances: A virtual machine must run on a physical host inside a specific data centre.
    - EBS Volumes: A network hard drive must be physically close to the EC2 instance it attaches to for single-digit millisecond latency.
    - Subnets: A subnet is a physical chunk of an AZ's network. [10, 11]
    

## 2. Regional Level: High Availability & Multi-Data Centre Replication [12, 13]

Services operate at the Regional level when they abstract away individual data centres to provide automatic backup and high availability. [14]

- The Logic: If an entire data centre (AZ) goes offline, a Regional service will keep running because AWS automatically mirrors its data and infrastructure across multiple AZs within that geographic boundary. [15, 16, 17]
- Examples:
    
    - S3 (Simple Storage Service): When you upload a file, AWS silently duplicates it across at least three distinct AZs. You don't manage the drives; you just see a Regional endpoint.
    - DynamoDB: A fully managed database that replicates data across multiple AZs in a region automatically.
    - VPC (Virtual Private Cloud): A logical network that spans the entire region, allowing you to carve out AZ-specific subnets inside it. [18, 19, 20, 21, 22]
    

## 3. Global Level: Centralized Control & Edge Distribution

Services operate at the Global level when they need to govern your entire AWS account or route traffic worldwide. [23, 24]

- The Logic: You cannot have different login rules or different domain routing rules per city; these systems must look at your infrastructure as a single global footprint.
- Examples:
    
    - IAM (Identity and Access Management): Users and permissions apply everywhere globally.
    - Route 53: The DNS service that directs users worldwide to the closest healthy region. [25, 26, 27, 28, 29]
    

---

## Cheat Sheet: How to Deduce the Service Level

Instead of memorizing, ask yourself these three architectural questions:

- Does it involve a physical boundary or data drive? → It is AZ-specific (EC2, EBS, Subnet).
- Does it contain the word "Virtual", "Registry", or boast "built-in high availability"? → It is Regional (VPC, ECR, S3, Lambda).
- Does it face the public internet or handle identity? → It is Global (Route 53, CloudFront, IAM). [30, 31, 32, 33, 34]

## The "Gotchas" (Where People Get Confused)

- RDS (Relational Database Service): The _database instance_ lives in one AZ for low latency. However, you configure it at the _Regional level_ because you can check a box to instantly spin up a standby replica in a second AZ. [35, 36, 37, 38, 39]
- Load Balancers (ALB/NLB): The load balancer _management_ is Regional, but it places individual entry points (nodes) inside specific AZ subnets to catch incoming traffic. [40, 41, 42]

---

Would you like to walk through a specific architectural scenario (like setting up a web application) to see how these layers connect in practice?
