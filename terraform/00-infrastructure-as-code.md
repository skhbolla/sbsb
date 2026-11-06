# Infrastructure as Code (IaC) Fundamentals

## What is Infrastructure as Code (IaC) ?

Broadly speaking, the below could be described as categories of IaC tools:

1. **Ad hoc scripts** (*Not really IaC, but worth noting*)
	> Think of a simple boto3 or shell script that creates a ec2 instance. While scripts like these do use code to provision infrastructure, they lack the foundational guardrails like state tracking and idempotency. So these are generally not considered true Infrastructure as Code (IaC), but instead are classified as **infrastructure automation or scripting**.
2. **Configuration management tools**
	> These tools set up and maintain the software, user accounts, and runtime environment _inside_ a server after it is running. They ensure that the operating system stays in a desired, compliant state. Popular options include [Ansible](https://www.ansible.com/), Puppet and SaltStack. Perhaps the most important feature of a Config management tool is that they are 'idempotent'.
3. **Server Templating tools**
	> These tools create custom, read-only system images (like Amazon AMIs or virtual machine snapshots) that already contain your software and dependencies pre-installed. These tools are fundamentally designed only for **immutable infrastructure** , eg: replacing old servers with fresh images instead of patching them live. Common tools are Packer, Docker and Vagrant.
4. **Orchestration tools** (*Mixed opinions on whether these should be classified as IaC, but still worth talking about*)
	> These tools automate the deployment, networking, and scaling of containerized applications using declarative configuration files. They manage how containers run across a cluster of servers. Leading examples include [Kubernetes](https://kubernetes.io/) and Helm.
5. **Provisioning tools** - *Declarative by nature*
	> These tools create and destroy the core cloud infrastructure like virtual machines, storage volumes, subnets, and databases. They use a declarative approach to map out your cloud architecture. Common examples include [Terraform](https://www.terraform.io/) and AWS CloudFormation.

### IaC Tool Categories at a Glance

| Category | Primary Focus | Infrastructure State | Typical Tools |
| :--- | :--- | :--- | :--- |
| **Ad hoc Scripts** | Procedural automation tasks | Unmanaged / Blind | Boto3, Bash, Python |
| **Server Templating** | Building base OS images (pre-boot) | Immutable Images | Packer, Docker |
| **Provisioning** | Creating cloud resources & topology | Declarative End-State | Terraform, CloudFormation, OpenTofu |
| **Configuration Mgmt** | Software & OS configuration (post-boot) | Mutable / Desired State | Ansible, Puppet, Chef |
| **Orchestration** | Container lifecycle & cluster networking | Declarative Workloads | Kubernetes, Helm |

---

## Why is true Infrastructure as Code (IaC) necessary if AWS already provides the Boto3 SDK (Ad hoc Scripting)?

While AWS Boto3 is a powerful Python SDK used to write scripts that interact with AWS services, it acts as an **imperative programming** tool. Infrastructure as Code (IaC) tools like Terraform or AWS CloudFormation are designed to manage the entire lifecycle of your cloud architecture. Relying solely on Boto3 scripts for large-scale environments introduces significant manual overhead, as Python code lacks built-in awareness of your existing infrastructure's state.

- **Declarative vs. Imperative Style**: Boto3 requires you to write scripts detailing exactly _how_ to build infrastructure step-by-step, whereas IaC tools allow you to simply define _what_ the final infrastructure should look like, and they automate the creation path for you. (i.e You write files describing what infrastructure you want (like virtual machines, subnets, or databases) rather than coding step-by-step procedural commands on how to build them)
- **State Management**: IaC tools maintain a persistent state file to track every resource and its dependencies, a critical feature that Boto3 lacks, making infrastructure updates and deletions risky to code manually.
- **Automatic Idempotency**: Running a Boto3 script twice often results in errors or duplicate resources, while IaC tools inherently check the current environment and only deploy changes if a difference exists.
- **Drift Detection**: IaC frameworks can instantly scan your live environment to identify and revert unauthorized manual changes made in the AWS Console, which Boto3 scripts cannot do natively.
- **Version Control and Auditing**: IaC configuration files live in Git, enabling clear peer reviews, pull requests, automated CI/CD pipelines, and seamless rollbacks for your entire architecture.

### Imperative Scripting vs. Declarative IaC

| Dimension | Imperative Scripts (e.g., Boto3, Python) | Declarative IaC (e.g., Terraform) |
| :--- | :--- | :--- |
| **Paradigm** | Focuses on the *process* (*how* to build step-by-step) | Focuses on the *destination* (*what* the end state should be) |
| **State Awareness** | None; runs commands blindly against live APIs | Maintains a persistent state ledger mapping code to reality |
| **Idempotency** | Manual: Developer must write extensive `try/except` and lookup guards | Built-in: Running 10 times produces the exact same outcome |
| **Drift Detection** | None; cannot identify manual GUI changes out of the box | Built-in: Compares desired vs. actual live state during `plan` |
| **Dependency Graph** | Must be manually coded in procedural order | Automatically calculates DAG (Directed Acyclic Graph) of dependencies |
| **Destruction / Rollback** | Complex: Must write dedicated teardown scripts | Trivial: `terraform destroy` or removing the resource block |

> [!TIP]
> **What is Idempotency?**
> In computer science, an operation is **idempotent** if applying it multiple times produces the same result as applying it once ($f(f(x)) = f(x)$). 
> In cloud engineering, if an imperative Boto3 script running `ec2.create_instances()` is executed twice, it creates duplicate instances and doubles your cloud bill. A declarative tool like Terraform checks if the instance already exists; if it matches desired state, it performs zero actions.
