---
title: Homelab Documentation Hub
tags: [index, moc]
created: 2025-11-23
updated: 2025-11-23
---

# 🏠 Homelab Documentation Hub

Welcome to the comprehensive documentation for the Badger Development homelab infrastructure. This vault serves as the central knowledge base linking together all infrastructure components, configurations, and operational procedures.

## 🗺️ Navigation

### Core Infrastructure Maps
- [[📊 Infrastructure Overview|Infrastructure Overview]] - Physical and virtual infrastructure inventory
- [[🔧 Architecture|Architecture]] - System architecture and design decisions  
- [[📁 Repository Map|Repository Map]] - Guide to the three main Git repositories

### Quick Access
- [[🚀 Quick Start Guide|Quick Start Guide]] - Get up and running quickly
- [[🆘 Emergency Procedures|Emergency Procedures]] - Critical troubleshooting steps
- [[📞 Contact Information|Contact Information]] - Key contacts and escalation paths

## 📚 Main Documentation Areas

### Infrastructure & Compute
- [[Infrastructure/Infrastructure MOC|Infrastructure Overview]]
- [[Infrastructure/Hosts Inventory|Hosts Inventory]] - All physical and virtual hosts
- [[Infrastructure/Proxmox|Proxmox]] - Virtualization platform
- [[Infrastructure/Hardware|Hardware]] - Physical hardware specifications

### Configuration Management
- [[Ansible/Ansible MOC|Ansible Documentation]]
- [[Ansible/Playbooks|Playbooks]] - Playbook reference
- [[Ansible/Roles|Roles]] - Role documentation
- [[Ansible/Inventory Management|Inventory Management]]

### Container Platform
- [[Docker/Docker MOC|Docker Documentation]]
- [[Docker/Stacks Inventory|Stacks Inventory]] - All deployed stacks
- [[Docker/Komodo|Komodo]] - Orchestration platform
- [[Docker/Host Fleet|Host Fleet]] - Docker host topology

### Services & Applications
- [[Services/Services MOC|Services Overview]]
- [[Services/Application Catalog|Application Catalog]] - All deployed applications
- [[Services/Service Dependencies|Service Dependencies]] - Dependency mapping

### Networking
- [[Network/Network MOC|Network Documentation]]
- [[Network/Topology|Network Topology]] - Network design and layout
- [[Network/VPN|VPN]] - WireGuard and Tailscale configuration
- [[Network/DNS|DNS]] - DNS infrastructure

### Security & Access
- [[Security/Security MOC|Security Documentation]]
- [[Security/FreeIPA|FreeIPA]] - Identity management
- [[Security/LDAP|LDAP]] - LDAP configuration
- [[Security/Certificates|Certificates]] - Certificate management
- [[Security/Firewall Rules|Firewall Rules]] - UFW and firewall configs

### Monitoring & Observability
- [[Monitoring/Monitoring MOC|Monitoring Documentation]]
- [[Monitoring/Beszel|Beszel]] - Infrastructure monitoring
- [[Monitoring/Dozzle|Dozzle]] - Container log aggregation
- [[Monitoring/Alerts|Alerts]] - Alerting configuration

### Backup & Recovery
- [[Backups/Backups MOC|Backup Documentation]]
- [[Backups/Kopia|Kopia]] - Backup system
- [[Backups/Recovery Procedures|Recovery Procedures]] - Disaster recovery
- [[Backups/Backup Schedule|Backup Schedule]] - Backup jobs and retention

### Operational Procedures
- [[Procedures/Procedures MOC|Procedures Overview]]
- [[Procedures/Deployment|Deployment]] - Deployment workflows
- [[Procedures/Troubleshooting|Troubleshooting]] - Common issues and solutions
- [[Procedures/Maintenance|Maintenance]] - Routine maintenance tasks

### Development Environment
- [[Development/Development MOC|Development Overview]]
- [[Development/Dotfiles|Dotfiles]] - Shell and tool configuration
- [[Development/CLI Tools|CLI Tools]] - Development tools inventory
- [[Development/AI Assistants|AI Assistants]] - Claude/Gemini integration

## 🔗 External Resources

### GitHub Repositories
- **Ansible**: `/Users/danielschmeichel/github/ansible`
- **Docker**: `/Users/danielschmeichel/github/docker`  
- **Dotfiles**: `/Users/danielschmeichel/github/dotfiles`

### Key Documentation Files
- [Ansible README](file:///Users/danielschmeichel/github/ansible/README.md)
- [Docker README](file:///Users/danielschmeichel/github/docker/README.md)
- [Ansible Workflows](file:///Users/danielschmeichel/github/ansible/docs/WORKFLOWS.md)
- [Docker Operations](file:///Users/danielschmeichel/github/docker/docs/operations.md)

## 🏷️ Documentation by Tag

Use these tags to find related documentation across the vault:

`#infrastructure` `#ansible` `#docker` `#network` `#security` `#monitoring` `#backup` `#procedure` `#emergency` `#service` `#host` `#troubleshooting`

## 📝 Recent Updates

- 2025-11-23: Initial comprehensive vault structure created
- View [[📅 Changelog|Changelog]] for complete update history

## 🎯 Quick Tasks

- [ ] Complete initial infrastructure inventory
- [ ] Document all Docker stacks
- [ ] Create role documentation for all Ansible roles
- [ ] Map service dependencies
- [ ] Document disaster recovery procedures

---

*This is an Obsidian vault stored at: `/Users/danielschmeichel/Library/Mobile Documents/com~apple~CloudDocs/Homelab Documentation`*
