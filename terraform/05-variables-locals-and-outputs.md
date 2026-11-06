# Variables, Locals, and Outputs

![[terraform/_assets/Pasted image 20261011201359.png]]

Terraform manages configuration data through three distinct tiers:
1. **Input Variables (`var.<name>`)**: Parameters passed *into* the module by the user or environment.
2. **Local Variables (`local.<name>`)**: Intermediate calculations and values computed *inside* the module.
3. **Output Values (`output`)**: Return values exported *out of* the module for consumers or CLI display.

---

## 1. Input Variables

Input variables parameterize your configuration so that templates can be deployed across different environments without modifying source code.

```hcl
variable "cluster_deployment_config" {
  type = object({
    cluster_name = string
    node_count   = number
    environment  = string
    alerts_email = optional(string, "devops-alerts@company.com")
  })
  
  description = "The global configuration block required to deploy a production-ready application cluster"
  default     = {
    cluster_name = "core-prod-cluster"
    node_count   = 3
    environment  = "production"
    alerts_email = "prod-alerts@company.com"
  }
  
  sensitive = true
  nullable  = false

  validation {
    condition     = var.cluster_deployment_config.node_count >= 3 && var.cluster_deployment_config.node_count <= 10
    error_message = "The node_count parameter must be between 3 and 10 nodes for high availability and budget limits."
  }

  validation {
    condition     = contains(["development", "staging", "production"], var.cluster_deployment_config.environment)
    error_message = "The environment parameter must be exactly 'development', 'staging', or 'production'."
  }
}
```

### Argument Breakdown

- **`type`**: Restricts the incoming data format. In this declaration, it enforces a structural `object` schema. This forces the input data to match a specific shape, ensuring required fields (`cluster_name`, `node_count`, and `environment`) are present with their designated data types before any cloud creation begins.
- **`optional()`**: Nested inside the object type schema, this modifier allows fields to be completely omitted by the user when passing values. If the user leaves out `alerts_email`, Terraform automatically injects the fallback value specified as the second parameter (`"devops-alerts@company.com"`).
- **`description`**: A human-readable text string that serves as the in-code documentation for the variable. It helps other developers understand what this configuration controls and is displayed automatically inside terminal prompts if the user is asked to enter inputs manually.
- **`default`**: Establishes a preset fallback value block. If a team executes a deployment without explicitly defining or overriding this variable via a `.tfvars` file, CLI flags, or environment variables, Terraform will automatically proceed with these exact parameters.
- **`sensitive`**: The security flag. Setting this to `true` tells Terraform to treat the contents of this variable with total privacy in terminal logs. During a `plan` or `apply` operation, any value printed or derived from this block will be masked out and displayed strictly as `(sensitive value)`.
- **`nullable`**: A strict toggle that determines how Terraform handles empty data. Setting `nullable = false` ensures that if a user explicitly passes a value of `null` to this variable, Terraform will reject it and dynamically snap back to utilizing the default block parameters instead of passing an empty value down to your cloud resources.
- **`validation {}`**: Custom assertion blocks used to build advanced business logic right into your template. Each block contains a `condition` (a boolean expression that must evaluate to `true`) and an `error_message` (the precise text displayed to halt the deployment execution immediately if the user passes bad data). You can stack multiple validation blocks sequentially to check different fields in the exact same variable.

### Data Types in HCL Quick Reference

```hcl
# Primitive Types
variable "region"         { type = string }     # "us-east-1"
variable "instance_count" { type = number }     # 3
variable "enable_logging" { type = bool }       # true

# Complex Collection Types
variable "availability_zones" { 
  type = list(string)                           # Ordered list: ["us-east-1a", "us-east-1b"]
}
variable "allowed_ip_set" { 
  type = set(string)                            # Unique, unordered set: ["10.0.0.1", "10.0.0.2"]
}
variable "resource_tags" { 
  type = map(string)                            # Key-value map: { Environment = "prod", Team = "core" }
}
```

![[terraform/_assets/Pasted image 20261011201751.png]]

![[terraform/_assets/Pasted image 20261011201931.png]]

---

### Supplying Values: `.tfvars` Files & CLI Flags

Let's dive into `.tfvars` files and break down how they actually work when you're managing a real project.

Think of your `variables.tf` file as a blueprint or a blank form—it defines what fields are required, what data types they take, and what they do. A `.tfvars` file is where you actually fill in the blanks with real-world data. It separates your infrastructure architecture from your environment configuration. This means you can write one master template of cloud code and use different `.tfvars` files to spin up isolated environments for dev, staging, or production.

Inside a `.tfvars` file, you don't wrap things in `variable` blocks or declare types. You've already done that hard work in your main code. Here, you just write raw, clean key-value assignments. The keys must match the exact names of the variables you declared in your project.

```hcl
# staging.tfvars
instance_count = 3
environment    = "staging"
allowed_ips    = ["10.0.0.0/16", "192.168.1.0/24"]
cluster_tags   = {
  Department = "Engineering"
  CostCenter = "8082"
}
```

#### Autoloaded Files

Terraform has some built-in rules for files it will automatically pick up and read behind the scenes without you having to point to them in your terminal commands:

- **`terraform.tfvars`**: This is the default values file. If Terraform spots a file with this exact name in your working directory, it automatically injects those values into every single `plan` or `apply` you run.
- **`*.auto.tfvars`**: Any file that ends with this extension (like `networks.auto.tfvars` or `security.auto.tfvars`) gets automatically parsed too. This is incredibly helpful when your project grows large because it lets you split your configuration inputs into logical files instead of dumping hundreds of values into one massive, unreadable document.

#### Custom Environments: Using the `-var-file` Flag

If you're managing multiple environments, you don't want to rely on the default autoloading files because they apply globally. Instead, you create custom-named files like `dev.tfvars` and `prod.tfvars`.

Because Terraform doesn't load these by default, you tell it exactly which file to look at by passing a flag when you execute your commands:

```bash
# Spinning up your development sandbox
terraform plan -var-file="dev.tfvars"
terraform apply -var-file="dev.tfvars"

# Stepping up to the live production environment
terraform plan -var-file="prod.tfvars"
terraform apply -var-file="prod.tfvars"
```

---

#### The Fight for Priority: Variable Precedence

What happens if you accidentally set the same variable in three different places at once? Terraform doesn't crash; it has a built-in hierarchy to decide which value wins the conflict. It evaluates inputs from lowest to highest priority, where the highest priority always overrides everything below it:

| Priority | Source | How it is Set / Evaluated |
| :---: | :--- | :--- |
| **1 (Lowest)** | Default values | Fallback typed inside the `variable` block itself |
| **2** | Environment variables | Any terminal variable with prefix `TF_VAR_<name>` |
| **3** | `terraform.tfvars` | The standard default autoloaded file |
| **4** | `*.auto.tfvars` files | Autoloaded alphabetically by filename |
| **5** | `-var-file` flag | Custom environment files passed on CLI (e.g. `-var-file="prod.tfvars"`) |
| **6 (Highest)** | `-var` inline flag | Explicit override passed directly in command (e.g. `-var="node_count=10"`) |

![[terraform/_assets/Pasted image 20261011201420.png]]

#### The Git Safety Line: What to Commit vs. What to Ignore

When managing `.tfvars` files, you have to be careful with source control.

Files like `dev.tfvars` or `prod.tfvars` should be committed to Git. They track standard operational parameters like region names, node counts, or cluster configurations. It’s safe and highly recommended for your team to share these files so your deployments stay consistent.

> [!CAUTION]
> If you ever use a `.tfvars` file to hold temporary local secrets—like database root passwords or API tokens—you must name it something distinct like `secrets.auto.tfvars` and immediately add that exact name to your `.gitignore` file. If a secret-heavy `.tfvars` file accidentally gets pushed to a public repository, your cloud security posture is compromised instantly.

---

## 2. Locals: The Internal Transformers

If Input Variables are like function parameters that a user passes into a script, Locals (`locals`) are the internal variables defined inside the code itself.

Users cannot pass values into locals from a `.tfvars` file, a terminal flag, or an environment variable. Instead, a local value is evaluated behind the scenes to calculate, transform, or group data dynamically.

Locals are declared inside a single `locals` block. Inside this block, you can define as many key-value pairs as you want.

```hcl
locals {
  # 1. Basic configuration cleanup
  environment_type = var.is_production ? "prod" : "dev"

  # 2. String interpolation / manipulation
  resource_prefix = "${var.company_name}-${local.environment_type}"

  # 3. Complex data grouping (Maps)
  standard_tags = {
    Project     = var.project_name
    Environment = local.environment_type
    ManagedBy   = "Terraform"
  }
}
```

Once defined, you access a local value anywhere in your project files using the prefix `local.` followed by the specific key name (note that it is singular `local.`, not plural `locals.`).

```hcl
resource "aws_vpc" "network" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "${local.resource_prefix}-vpc" # Using the combined string
  }
}
```

### Why and When to Use Locals

- **Preventing Code Duplication (DRY)**: If you find yourself writing the exact same complex naming convention or tag dictionary across 50 different resources, abstract it into a local. If the naming schema changes tomorrow, you update it once inside the `locals` block instead of editing 50 resources.
- **Complex Logic Processing**: Input variables are rigid; they only hold data. Locals allow you to run programming expressions—like ternary operators (`condition ? true : false`), string concatenations, or built-in functions—to reshape your inputs into usable formats.
- **Simplifying Resource Parameters**: Keep your resource blocks readable. Instead of cramming complex lookups and logic directly into a resource parameter, compute the value quietly inside a local and pass the clean `local.value` straight to the resource.

---

## 3. Outputs: The Return Statements

Think of an `output` block as the explicit **export mechanism** for your infrastructure.

When you run `terraform apply`, Terraform talks to the cloud APIs, spins up your resources, and generates a massive web of metadata. By default, all of that information stays inside the project's state file. 

An output block is you telling Terraform: _"Hey, this specific piece of data generated by the cloud is incredibly important. I need you to grab it, format it, and expose it so other systems, modules, or teams can actually use it."_

Each output variable requires its own individual named block. Inside, you define what value to expose, along with optional visibility controls.

```hcl
output "web_server_connection_string" {
  value       = "ssh -i my-key.pem ubuntu@${aws_instance.web.public_ip}"
  description = "The exact terminal command to connect to the new server"
  sensitive   = false
}
```

### Argument Breakdown

- **`value` (Mandatory)**: The data expression you want to export. This can pull from variable values, local calculations, or raw resource attributes generated dynamically by the cloud (like public IPs, resource IDs, or creation timestamps).
- **`description`**: A human-readable note explaining what this output represents.
- **`sensitive`**: A security toggle. If set to `true`, Terraform will completely mask the value from your terminal output using `(sensitive value)` to prevent exposing database strings, private tokens, or passwords to your deployment logs.
- **`depends_on`**: An explicit ordering flag. It tells Terraform to delay calculating this output value until a specific dependency resource is 100% created. (Use this sparingly, as Terraform usually infers order automatically).

### Why and When to Use Outputs

- **Post-Deployment Visibility**: Instead of forcing engineers to open the AWS Web Console and search through pages of servers to find a public IP or a Load Balancer URL, outputs print these critical values straight to the terminal screen the moment `terraform apply` finishes.
- **Cross-Project Integration**: In large architectures, teams split their infrastructure into separate codebases (e.g., one project for the core Networking, and a separate project for the Applications). The network team _outputs_ the Subnet IDs. The application team then reads those specific outputs from the network's state file to deploy their servers into the right spot.
- **CI/CD Pipeline Consumption**: Automated build systems (like Jenkins or GitHub Actions) read Terraform outputs in plain text or JSON format using the command `terraform output -json`. The pipeline can then feed those live cloud configurations down to later steps, like automated software deployment scripts.

### Querying Outputs via CLI

```bash
# Display all outputs in standard terminal format
terraform output

# Extract a single output as raw text (useful for bash scripts and SSH commands)
terraform output -raw web_server_connection_string

# Export all outputs as a JSON payload for automation pipelines
terraform output -json
```
