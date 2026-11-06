# Advanced Terraform Syntax

The six blocks covered in the basic syntax make up over 90% of everything you will write in a standard Terraform project. However, there are a handful of other keywords used for advanced configuration, looping, and logic.

---

## 1. Other Top-Level Configuration Blocks

- **`locals {}`**: Used to create internal, reusable expressions or variables within your module. Think of them as local variables in programming. Unlike a `variable` block (which takes user input), a local is calculated behind the scenes (e.g., combining two strings) to keep your code clean and prevent repetition.
- **`module`**: Used to instantiate a package of reusable Terraform configurations from another directory or Git repository. This is how you share architectural blueprints (like a "standard secure VPC setup") across different teams or environments.

```hcl
# Example: Instantiating a reusable external VPC module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["us-east-1a", "us-east-1b"]
}
```

---

## 2. Meta-Arguments (Keywords inside resources)

These are specific control keywords that can be placed inside _any_ `resource` or `module` block to change how Terraform behaves:

### `count`
A basic loop mechanism. If you set `count = 3` inside an `aws_instance` block, Terraform will automatically spin up 3 identical servers using that single block of code.

```hcl
resource "aws_instance" "server" {
  count         = 3
  ami           = "ami-0abc123"
  instance_type = "t3.micro"

  tags = {
    # Access the current iteration index (0, 1, 2)
    Name = "Web-Server-${count.index + 1}"
  }
}
```

### `for_each`
A more advanced loop that accepts a map or a set of strings. It allows you to loop through a dynamic list (like a list of user names) and create a resource for each item, giving you better control than `count`.

```hcl
variable "iam_users" {
  type    = set(string)
  default = ["alice", "bob", "charlie"]
}

resource "aws_iam_user" "team" {
  for_each = var.iam_users
  name     = each.key # References each individual item in the set
}
```

> [!CAUTION]
> **The `count` vs. `for_each` Index Trap**
> Avoid using `count` over lists when items might be deleted or inserted in the middle. 
> * **Why?** Terraform identifies `count` resources by numeric index: `aws_instance.server[0]`, `aws_instance.server[1]`, `aws_instance.server[2]`. If you remove item `[0]`, item `[1]` shifts to index `[0]`. Terraform interprets this as "destroy and rebuild everything after index 0"!
> * **The Fix:** Use `for_each` with maps or string sets. Resources are addressed by distinct string keys (`aws_iam_user.team["alice"]`). Deleting `"alice"` deletes *only* Alice, leaving Bob and Charlie completely untouched.

### `depends_on`
Forces an explicit deployment order. Terraform is usually smart enough to figure out dependencies on its own, but you use `depends_on` to tell it, _"Do not build Resource B until Resource A is 100% finished running."_

```hcl
resource "aws_s3_bucket" "logs" {
  bucket = "company-audit-logs"
}

resource "aws_instance" "app" {
  ami           = "ami-0abc123"
  instance_type = "t3.micro"

  # Force EC2 instance creation to wait until S3 bucket is 100% active
  depends_on = [aws_s3_bucket.logs]
}
```

### `lifecycle {}`
A special configuration block used to change how Terraform handles resource updates. For example, it contains flags like `create_before_destroy = true` (to prevent downtime during replacements) or `prevent_destroy = true` (to accidentally stop someone from deleting a critical production database).

```hcl
resource "aws_instance" "zero_downtime_app" {
  ami           = "ami-0abc123"
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true  # Launch new replacement before tearing down old
    prevent_destroy       = false # Set to true on production databases to block accidental deletes
    ignore_changes        = [tags] # Do not overwrite manual GUI tag modifications
  }
}
```

---

## 3. Structural Expression Keywords

When writing logic inside your resource parameters, you will use these inline programming keywords:

### `for` & `if` Expressions
Used inside loops to transform data structures (e.g., taking a list of server objects and filtering out only their IP addresses into a new list), paired with `if` expressions to introduce conditional filtering into your data loops.

```hcl
# List transformation with filtering
# Extracts only active server names into a list: ["web-1", "web-2"]
locals {
  active_server_names = [
    for server in var.server_list : server.name if server.is_active
  ]
  
  # Map transformation: converts list of objects into a name-to-ip lookup map
  name_to_ip = {
    for server in var.server_list : server.name => server.ip_address
  }
}
```

### Dynamic Blocks (`dynamic "setting" {}`)
Used to dynamically generate nested configuration blocks inside a resource based on a loop. For instance, if you want a security group to have 5 different firewall rules based on a list input, you use a `dynamic` block instead of copy-pasting the rule block 5 times.

```hcl
variable "firewall_ports" {
  type        = list(number)
  description = "List of ingress TCP ports to allow"
  default     = [80, 443, 8080]
}

resource "aws_security_group" "web_access" {
  name        = "web-ingress-rules"
  description = "Dynamically open multiple firewall ports"

  # Automatically repeats the nested "ingress" block for each port in the list
  dynamic "ingress" {
    for_each = var.firewall_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```
