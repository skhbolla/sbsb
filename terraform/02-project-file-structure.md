# Terraform Project File Structure

A standard Terraform (TF) project uses a modular, flat file structure rather than deeply nested folders. Terraform automatically reads all files ending in `.tf` within your working directory and combines them at runtime.

A typical, production-ready directory looks like this:

```text
my-terraform-project/
├── .terraform/            # (Hidden & Ignored) Provider plugins & downloaded modules
├── .terraform.lock.hcl    # (Committed to Git) Exact cryptographic hashes of provider versions
├── main.tf                # Primary entry point: resource declarations & architecture
├── providers.tf           # Cloud connector blocks, required provider versions, & credentials
├── variables.tf           # Variable schemas (types, defaults, validation rules)
├── terraform.tfvars       # Concrete input values assigned to variables (e.g., dev/prod)
├── outputs.tf             # Data exposed to terminal logs or downstream configurations
└── terraform.tfstate      # (Ignored locally) Single source of truth mapping code to cloud IDs
```

> [!NOTE]
> **Why Flat Files?**
> Terraform does not care how you name your `.tf` files or how many files you have in your root directory. At execution time, Terraform concatenates all files ending in `.tf` into a single unified configuration. Dividing your code into `main.tf`, `variables.tf`, and `outputs.tf` is a standard community convention for readability and team organization.

---

## Core Files and Their Roles

- **`main.tf` (The Architecture)**: This is the primary entry point where you define your actual infrastructure resources (such as EC2 instances, VPCs, or databases). For small projects, all resource blocks live here; for larger projects, it orchestrates connections between reusable modules.
- **`providers.tf` (The Connectors)**: This file declares the cloud platforms or systems Terraform needs to talk to (e.g., AWS, Azure, Google Cloud). It specifies the provider version, region, and credentials required to authenticate with those APIs.
- **`variables.tf` (The Inputs)**: This file defines the dynamic inputs your configuration accepts. Instead of hardcoding values like region names or server sizes inside your `main.tf`, you declare them here along with optional data types, descriptions, and default values.
- **`outputs.tf` (The Results)**: This file defines what data Terraform should expose on your command line or pass to other configurations after a successful deployment. Typical examples include server IP addresses, database endpoints, or resource IDs.
- **`terraform.tfvars` (The Values)**: This file contains the actual data values assigned to the inputs declared in `variables.tf`. It separates your structural infrastructure logic from environment-specific configurations (e.g., deploying to `dev` vs. `prod`).

---

## Generated and State Files (Do Not Edit Manually)

- **`.terraform/` Folder**: This hidden directory is created when you run `terraform init`. It downloads and stores the provider plugins and modules required to run your project.
- **`terraform.tfstate` and `.backup`**: This is the single source of truth for your deployment. It is a JSON file that maps your HCL code to the real-world resource IDs in your cloud provider.
- **`.terraform.lock.hcl`**: A lock file generated automatically to track the exact versions of the provider plugins you used, ensuring everyone on your team deploys with the exact same dependencies.

### Git Source Control Rules: What to Commit vs. What to Ignore

| File / Folder | Git Status | Reason |
| :--- | :---: | :--- |
| `*.tf` (`main.tf`, `variables.tf`, etc.) | **Commit** | Your declarative infrastructure logic. |
| `.terraform.lock.hcl` | **Commit** | Guarantees deterministic provider builds across team members and CI/CD pipelines (like `package-lock.json`). |
| `terraform.tfvars` (non-sensitive) | **Commit** | Standard operational parameters for environments (e.g., region, node counts). |
| `.terraform/` | **Ignore** | Transient binary downloads; easily recreated via `terraform init`. |
| `*.tfstate` / `*.tfstate.backup` | **Ignore** | Contains real-world resource mappings and potentially sensitive data in plain text. |
| `*.auto.tfvars` (with secrets) | **Ignore** | Prevents credentials or API keys from leaking to public or team Git repositories. |
