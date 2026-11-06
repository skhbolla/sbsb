> VPC is the software defined virtual equivalent of a actual physical private network with no exposure to outside.. But by default AWS creates a VPC that has a IGW setup.. so even though theortically a VPC is supposed to be fully isolated from outside, in reality AWS by default lets outbound connections from VPC because of IGW (not sure about inbound connections.. help here)
>
>just like physical networks, we would like to have logical segmentation of the CIDR block so we they can be used for suitable purposes.. hence the "subnets" .. VPC is aligned to regions , but subnets are AZ specific.. it is important to have multiple subnets each in diff AZs for redundancy and fault tolerance...
>
> Subnets take a block out of VPC CIDR.. AWS makes no distinction between public and private subnets.. the only way they differ is by having a route to the IGW..
>
> Route tables are defined at VPC level and can be associated with one or more subnets.. If a subnet has no explicit associations, the default VPC route table is implicitly associated with it.. If the associate route table of a subnet has a route to IGW then it is technically a public subnet, otherwise private..
>
> IGW are at VPC level.. one VPC can have only one IGW.. 
>
> resources in Public subnets can get elastic IPs which can then be used by the IGW to do 1:1 NAT . If no public IP exists for resources in public subnet, they cannot reach internet even if a route exists to IGW..
>
> Private subnets have no route table mapping to IGW, they dont have public IPs. Hence they are only addressable and routable within the VPC.. If we ever need a way for a resource in private subnet to access the internet, we need something that can provide us NAT services.. So we can use NAT gateway... NAT gateways do PAT (port address translation)... so we need the NAT gateway to have a public IP for PAT mapping..
>
> Hence we can only create NAT gateways in public subnets, and add a mapping in the private subnet's routing table to the NAT gateway.. The NAT gateway then routes to IGW.
>
> Curious thing to note: If resources in private subnets can have public IPs (they can), then why can we not have a NAT inside the private subnet and route it to IGW ?? Well, we can, but by adding the route to the IGW, the subnet is now technically a public subnet .. LOOL
>
>Since provisioning NATs in each AZ is laborious , we can use the new RNAT which is created at VPC level instead of public subnet level.. This also uses PAT (but with a pool of public IPs for scaling)... Since RNATs are not within a subnet, we must associate a route table to it.. by default AWS auto creates a new route table and suto associates it to RNAT.. All private subnets should add a mapping for internet traffic to this RNAT gateway, and this RNAT gateway is by default mapped on internet traffic to IGW..

Your understanding of AWS networking is incredibly accurate and demonstrates a strong grasp of how these components interact. You have correctly identified the mechanics of VPCs, subnets, route tables, IGWs, and NAT Gateways.

There are just a few minor nuances and corrections needed to make your understanding 100% precise. Here is the validation of your points, along with answers to your questions and expanded architectural details.

---

## 1. VPC Isolation & The "Default VPC"

- Your Understanding: Mostly correct. A custom VPC is completely isolated by default. However, AWS automatically creates a Default VPC in every region for new accounts to make it easy to launch instances immediately.
- The Inbound/Outbound Clarification: In the Default VPC, AWS creates an Internet Gateway (IGW) and attaches it.
    
    - Outbound: Allowed by default because the default Route Table routes `0.0.0.0/0` to the IGW, and the default Security Group allows all outbound traffic.
    - Inbound: Blocked by default from the internet. Even though the IGW and routing are in place, the default Security Group blocks all incoming traffic from external IP addresses. It only allows inbound traffic originating from within the same Security Group.
    

## 2. Subnets, AZs, and Redundancy

- Your Understanding: 100% Correct. VPCs span an entire Region, while Subnets are locked to a single Availability Zone (AZ). Deploying resources across multiple subnets in different AZs is the foundational blueprint for AWS high availability.

## 3. Public vs. Private Subnets

- Your Understanding: 100% Correct. To AWS, a subnet is just a subnet. The _only_ thing that makes a subnet "public" or "private" is whether its associated route table contains a route pointing `0.0.0.0/0` to an Internet Gateway.

## 4. Route Tables

- Your Understanding: 100% Correct. Route tables exist at the VPC level. A subnet must be associated with exactly one route table. If you don't explicitly assign one, it implicitly falls back to the VPC's Main (default) Route Table.

## 5. Internet Gateways (IGW)

- Your Understanding: 100% Correct. You can attach exactly one IGW to a VPC at a time. It scales horizontally and is highly available by default; you do not manage its bandwidth.

## 6. Public Subnet Internet Access & Elastic IPs

- Your Understanding: 95% Correct. Resources do need a public IP to talk to the internet via an IGW, but it does not _have_ to be an Elastic IP (which is a static, persistent public IP). It can also be a Dynamic Public IP, which AWS assigns automatically upon instance creation and releases when the instance is stopped.
- How IGW Works: You hit the nail on the head. The IGW performs a 1:1 stateless NAT. The EC2 instance itself is actually completely unaware of its public IP; it only knows its private IP. The IGW swaps the private IP for the public IP as traffic crosses the VPC border.

## 7. Private Subnets & NAT Gateways

- Your Understanding: 100% Correct. NAT Gateways use Port Address Translation (PAT) to allow multiple private resources to share a single public IP. Because they need to talk to the internet, the NAT Gateway itself _must_ reside in a public subnet and have an Elastic IP attached.

## 8. Your "Curious Note" on Private Subnet NATs

- Your Understanding: Spot on, and great architectural intuition! If you put a NAT instance/gateway inside a private subnet and give it a public IP, it still cannot talk to the internet unless you add a route to the IGW in that subnet's route table. The moment you add that route, that subnet is no longer private—it is now a public subnet. Your logical loop laugh is entirely justified because that is exactly how the physics of AWS routing works.

---

## 💡 Advanced Nuances to Expand Your Knowledge

To take your networking knowledge to the next level, keep these three critical concepts in mind:

## Reserved IP Addresses

When you create a subnet CIDR block (e.g., `/24`), AWS automatically reserves the first 4 and the last 1 IP addresses for internal networking. For a `/24` block (256 IPs), you only get 251 usable addresses:

- `x.x.x.0`: Network address.
- `x.x.x.1`: VPC router.
- `x.x.x.2`: DNS server (Amazon Provided DNS / Route 53 Resolver).
- `x.x.x.3`: Reserved by AWS for future use.
- `x.x.x.255`: Network broadcast address (AWS doesn't support broadcast, but reserves it anyway).

## Security Groups vs. Network ACLs (NACLs)

AWS provides two layers of firewalls, and knowing the difference is crucial for troubleshooting:

- Security Groups (Instance Level): They are stateful. If you allow an inbound connection (e.g., port 80), the return outbound traffic is automatically allowed, regardless of outbound rules.
- Network ACLs (Subnet Level): They are stateless. If you allow inbound traffic on port 80, you _must_ also explicitly write an outbound rule for the ephemeral return ports, or the traffic will be dropped at the subnet boundary.

## VPC Endpoints (The NAT Alternative)

If resources in a private subnet only need to talk to other AWS services (like S3 or DynamoDB), routing through a NAT Gateway to the internet is expensive and unnecessary. Instead, you can use VPC Endpoints (PrivateLink). This keeps the traffic entirely within the AWS internal network backbone without ever exposing the private resources to the public internet.

## Regional NAT Gateway (RNAT)

 Regional NAT Gateway (RNAT) Mechanics: 100% Correct. It bypasses public subnets entirely, lives at the VPC level, scales a dynamic pool of public IPs automatically to prevent PAT port exhaustion, and AWS automatically spawns a dedicated, managed route table for it that routes directly to the IGW.

---

# VPC DNS resolution settings
Two DNS related settings are available on VPCs. They are:
	- DNS resolution -> Enabled by default. When enabled, resources in the VPC can use the route 53 resolver server (either by using the 169.254.160.253 or by using the reserved IP address in the subnet which is base IP + .2)
- DNS hostnames -> Disabled by default for non default VPCs. Can only be enabled when above option is also enabled. Setting this option to 'enabled'  assigns public DNS hostnames to instances with public IPv4 addresses.
