# Infralint

Infralint is a powerful command-line tool for linting, security scanning, and reporting on infrastructure code. It supports a variety of linters and security checkers, making it an essential tool for maintaining high-quality infrastructure-as-code (IaC) projects, particularly Terraform configurations.

## Table of Contents

- [Motivation](#motivation)
- [Python Versions](#python-versions)
- [Features](#features)
- [Installation](#installation)
  - [Option 1: Using a Virtual Environment and Symbolic Links](#option-1-using-a-virtual-environment-and-symbolic-links)
  - [Option 2: Installing Directly to System Python](#option-2-installing-directly-to-system-python)
- [Setting Up](#setting-up)
- [Commands](#commands)
- [Sample Configuration](#sample-configuration)
- [Contact](#contact)

## Motivation

Managing infrastructure code in a secure and scalable way is essential, especially with the rise of cloud-native technologies. Infralint was developed to automate the process of ensuring that your infrastructure code adheres to best practices by utilizing various linters and security scanners, generating detailed reports to highlight issues.

This tool ensures that your infrastructure is both secure and follows the necessary guidelines by default using Checkov, while also supporting other popular linters such as TFLint and TFSec.

## Python Versions

This project supports Python versions specified in the `pyproject.toml` file:

````toml
[tool.poetry.dependencies]
python = "3.10.14"

## Features

- **Lint Terraform Code**: Support for Checkov by default, with optional support for TFLint and TFSec.
- **Security Scanning**: Detect vulnerabilities in your infrastructure code using popular security tools.
- **Customizable Reports**: Generate detailed reports in JSON or HTML format.
- **Configurable Color Scheme**: Customize the color scheme for different severity levels (CRITICAL, HIGH, MEDIUM, LOW, INFO).
- **Modular Linter Support**: Easily enable or disable linters through the configuration file.

## Installation

Ensure you are using Python 3.10 or above.

### Option 1: Using a Virtual Environment and Symbolic Links

1. **Ensure Python Version**
   - Verify you have Python 3.10 or later:
     ```bash
     python --version
     ```

2. **Create and Activate Virtual Environment**
   - **Create**:
     ```bash
     python -m venv myenv
     ```

   - **Activate**:
     - **Windows**:
       ```bash
       myenv\\Scripts\\activate
       ```
     - **macOS/Linux**:
       ```bash
       source myenv/bin/activate
       ```

3. **Install Infralint**
   ```bash
   pip install infralint
````

### Option 2: Installing Directly to System Python

1. **Ensure Python Version**

   - Verify you have Python 3.10 or later:
     ```bash
     python --version
     ```

2. **Install Infralint**
   ```bash
   python -m pip install infralint
   ```

### Setting Up

To configure Infralint, follow these steps:

1. You can view the default structure by running `infralint show-config`.

2. The default configuration file will be located in `~/.infralint/config.yaml`.

3. By default, Checkov is the main linter used, but you can enable TFLint and TFSec as needed.

4. Edit the `config.yaml` file to enable/disable linters and set the report output format.

## Sample Configuration

Here’s a sample `config.yaml` to get started:

```yaml
linters:
  tflint:
    enabled: false
  tfsec:
    enabled: false
  checkov:
    enabled: true
    framework: terraform # Default framework to be used by Checkov
output:
  format: json # Options: json, html
  save_to: ./reports/report.json
color_scheme:
  CRITICAL: "#FF6F61"
  HIGH: "#FFA07A"
  MEDIUM: "#FFD700"
  LOW: "#90EE90"
  INFO: "#B0C4DE"
```

## Commands

Here are some useful commands to interact with Infralint:

- `infralint <path>`: Run the linters on the specified path and generate a report.
- `infralint show-config`: Display the current configuration.
- `infralint set-config`: Update the configuration settings in `config.yaml`.

## Contact

If you encounter any issues or have any suggestions, please feel free to send them to dev@darrenrabbitt.com. Thank you for your support!
