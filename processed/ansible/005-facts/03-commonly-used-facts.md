---
title: "03. Commonly Used Facts Reference"
slug: "03-commonly-used-facts"
estimated_time: 6
has_hands_on: false
---

## 03. Core Facts Reference Guide

Ansible discovers hundreds of system attributes during fact gathering. Here are the most frequently used facts categorized by operational domain.

---

### 1. System Information & Operating System

| Fact Variable | Description | Example Value |
| :--- | :--- | :--- |
| `ansible_distribution` | Specific Linux distribution name | `Ubuntu`, `CentOS`, `Debian`, `Rocky` |
| `ansible_distribution_version` | Distribution release version | `22.04`, `9.2`, `11` |
| `ansible_distribution_release` | Release codename | `jammy`, `focal`, `bullseye` |
| `ansible_os_family` | Broad operating system umbrella | `Debian`, `RedHat`, `Darwin`, `Windows` |
| `ansible_architecture` | Hardware architecture | `x86_64`, `aarch64`, `armv7l` |
| `ansible_hostname` | Short hostname without domain | `web-prod-01` |
| `ansible_fqdn` | Fully Qualified Domain Name | `web-prod-01.us-east.corp` |
| `ansible_facts` | Complete container dictionary of all facts | `{ ... }` |

> [!NOTE]
> **`ansible_os_family` vs `ansible_distribution`**:
> - `ansible_os_family == "Debian"` matches Ubuntu, Debian, Linux Mint, and Kali.
> - `ansible_os_family == "RedHat"` matches RHEL, CentOS, Fedora, Rocky Linux, and AlmaLinux.
> Always prefer `ansible_os_family` when writing package installation tasks that apply broadly across a distro lineage.

---

### 2. Networking Facts

| Fact Variable | Description | Example Value |
| :--- | :--- | :--- |
| `ansible_default_ipv4.address` | Primary outbound IPv4 address | `192.168.1.50` |
| `ansible_default_ipv4.gateway` | Default gateway IPv4 address | `192.168.1.1` |
| `ansible_default_ipv4.netmask` | Primary interface subnet mask | `255.255.255.0` |
| `ansible_default_ipv4.interface` | Primary network interface name | `eth0`, `ens3` |
| `ansible_all_ipv4_addresses` | List of all IPv4 addresses bound to host | `["192.168.1.50", "10.0.0.12"]` |
| `ansible_dns.nameservers` | List of configured DNS resolvers | `["8.8.8.8", "1.1.1.1"]` |

---

### 3. Hardware & Capacity Facts

| Fact Variable | Description | Unit / Format |
| :--- | :--- | :--- |
| `ansible_memory_mb.real.total` | Total physical RAM | Integer (Megabytes) |
| `ansible_memory_mb.real.free` | Available / unused physical RAM | Integer (Megabytes) |
| `ansible_memory_mb.swap.total` | Total swap space | Integer (Megabytes) |
| `ansible_processor_count` | Number of physical CPU sockets | Integer (e.g. `2`) |
| `ansible_processor_cores` | Number of cores per processor | Integer (e.g. `8`) |
| `ansible_processor_vcpus` | Total logical virtual CPUs | Integer (e.g. `16`) |

---

### 4. User & Runtime Identity

| Fact Variable | Description | Example Value |
| :--- | :--- | :--- |
| `ansible_user` | Current remote login username | `ubuntu`, `ec2-user`, `ansible` |
| `ansible_user_id` | Effective user account name | `root` or `shadab` |
| `ansible_user_gid` | Primary group numeric ID | `1000` |
| `ansible_group` | Primary group name of user | `developers`, `wheel` |
