---
title: Ansible Documentation
tags: [ansible, moc, automation]
created: 2025-11-27
updated: 2025-11-27
---

# 🤖 Ansible Configuration Management

Comprehensive Ansible infrastructure automation for homelab deployment and configuration management.

**Repository**: `/Users/danielschmeichel/github/ansible`

## Quick Links

- [[Repository Map#Ansible Repository|Repository Overview]]
- [README](file:///Users/danielschmeichel/github/ansible/README.md)
- [Workflows Guide](file:///Users/danielschmeichel/github/ansible/docs/WORKFLOWS.md)
- [Role Standards](file:///Users/danielschmeichel/github/ansible/docs/ROLE_STANDARDS.md)

## 📚 Documentation

### Core Documentation
- [[Ansible/Getting Started|Getting Started]] - Installation and setup
- [[Ansible/Architecture|Architecture]] - Three-tier workflow and phase system
- [[Ansible/Inventory Management|Inventory Management]] - Host and group organization
- [[Ansible/Variable Management|Variable Management]] - Variable precedence and vaults
- [[Ansible/Workflows|Workflows]] - Deployment and validation workflows

### Playbooks
- [[Ansible/Playbooks/Site|site.yml]] - Main infrastructure deployment playbook
- [[Ansible/Playbooks Overview|Playbooks Overview]] - All available playbooks

### Roles Documentation

#### Phase 1: System Baseline
- [[Ansible/Roles/system_baseline|system_baseline]] - Core system configuration
- [[Ansible/Roles/system_tools|system_tools]] - Essential system packages
- [[Ansible/Roles/system_update|system_update]] - Update management
- [[Ansible/Roles/time_sync|time_sync]] - NTP/chrony configuration
- [[Ansible/Roles/security_hardening|security_hardening]] - Security baseline

#### Phase 2: Networking
- [[Ansible/Roles/ufw_firewall|ufw_firewall]] - UFW firewall rules
- [[Ansible/Roles/tailscale|tailscale]] - Tailscale VPN client
- [[Ansible/Roles/network_toolbox|network_toolbox]] - Network diagnostic tools
- [[Ansible/Roles/hosts_distribution|hosts_distribution]] - /etc/hosts management
- [[Ansible/Roles/linux_firewall|linux_firewall]] - Legacy firewall management

#### Phase 3: Network Sharing
- [[Ansible/Roles/network_sharing|network_sharing]] - NFS/SMB configuration

#### Phase 4: Containers
- [[Ansible/Roles/docker|docker]] - Docker engine installation and configuration
- [[Ansible/Roles/komodo|komodo]] - Komodo orchestration setup
- [[Ansible/Roles/komodo_periphery|komodo_periphery]] - Komodo periphery agents

#### Phase 6: Developer Environment
- [[Ansible/Roles/developer_environment|developer_environment]] - Development tools
- [[Ansible/Roles/ai_cli_tools|ai_cli_tools]] - AI assistant CLI tools
- [[Ansible/Roles/dotfiles|dotfiles]] - User environment setup

#### Identity Management
- [[Ansible/Roles/freeipa_client|freeipa_client]] - FreeIPA client integration
- [[Ansible/Roles/freeipa_local_user_migration|freeipa_local_user_migration]] - User migration

#### Development & Synchronization
- [[Ansible/Roles/docker_git_sync|docker_git_sync]] - Docker stack git synchronization

#### Hardware & Performance
- [[Ansible/Roles/hardware_tuning|hardware_tuning]] - Hardware-specific optimizations

### Host Management
- [[Ansible/Host Management/Overview|Host Management Overview]]
- [[Ansible/Host Management/Onboarding|Onboarding New Hosts]] - Add new hosts
- [[Ansible/Host Management/Modification|Modifying Hosts]] - Update host configuration
- [[Ansible/Host Management/Removal|Removing Hosts]] - Decommission hosts
- [[Ansible/Host Management/Status|Onboarding Status]] - Check host status

### Operational Procedures
- [[Ansible/Procedures/Deployment|Deployment Procedures]] - Standard deployment workflow
- [[Ansible/Procedures/Validation|Validation]] - Pre-flight checks and testing
- [[Ansible/Procedures/Troubleshooting|Troubleshooting]] - Common issues and solutions
- [[Ansible/Procedures/Emergency|Emergency Procedures]] - Recovery workflows
- [[Ansible/Procedures/Performance|Performance Optimization]] - Scaling and tuning

## 📊 Phase Architecture

Ansible deploys infrastructure in numbered phases for controlled rollout:

| Phase | Purpose | Risk | Components |
|-------|---------|------|-----------|
| phase0 | Validation & facts | Low | Facts gathering, prerequisites |
| phase1 | Core system | Medium | Baseline, updates, security |
| phase2 | Networking | **High** | Firewall, VPN, routing |
| phase3 | Network sharing | Medium | NFS, SMB, mounts |
| phase4 | Containers | **High** | Docker, Komodo |
| phase5 | Reserved | N/A | Future use |
| phase6 | Developer tools | Low | AI CLI, dotfiles |
| phase7 | Monitoring | Medium | Health checks, metrics |
| phase8 | Validation | Low | Post-deploy verification |
| phase9 | Summary | Low | Failure reporting |

### Deployment Best Practices

1. **Always validate first**: Run `make check` before `make deploy`
2. **Use canary hosts**: Test on non-critical host first
3. **Deploy phases incrementally**: Don't deploy all phases at once
4. **Watch high-risk phases**: phase2 and phase4 require extra caution
5. **Monitor during deployment**: Watch logs and system resources

## 📝 Quick Commands

### Discovery
```bash
cd ~/github/ansible

# List all hosts
make list-hosts

# List all groups  
make list-groups

# List available tags
make list-tags site.yml

# List playbooks
make list-playbooks
```

### Validation
```bash
# Install dependencies
make galaxy-install

# Lint and syntax check
make lint
make syntax-check

# Dry-run with diff preview
make check site.yml DIFF=1
make check site.yml TAGS=phase1 LIMIT=hostname DIFF=1
```

### Deployment
```bash
# Deploy all phases to all hosts
make deploy site.yml

# Deploy specific phase
make deploy site.yml TAGS=phase1

# Deploy to specific host
make deploy site.yml LIMIT=hostname

# Scoped deployment
make deploy site.yml TAGS=phase4 LIMIT=docker_hosts

# Verbose output
make deploy site.yml VERBOSE=-vv
```

### Host Management
```bash
cd ~/github/ansible

# Add new host (interactive)
python3 scripts/host_management/onboard_host.py

# Check onboarding status
python3 scripts/host_management/check_onboarding_status.py

# Modify existing host
python3 scripts/host_management/modify_machine.py

# Remove host
python3 scripts/host_management/remove_machine.py
```

### Testing
```bash
# Test specific role with Molecule
make molecule-test ROLE=docker

# Debug Molecule test
cd roles/docker
molecule --debug converge
```

## 🔗 Integration Points

### With Docker Repository
- Ansible deploys Docker engine (phase4)
- Ansible installs Komodo periphery agents
- Docker stacks reference Ansible-configured hosts
- See [[Docker/Docker MOC|Docker Documentation]]

### With FreeIPA
- Ansible joins hosts to FreeIPA domain
- Manages FreeIPA client configuration
- See [[Security/FreeIPA|FreeIPA Documentation]]

### With Monitoring
- Ansible deploys monitoring agents
- Configures health check endpoints
- See [[Monitoring/Monitoring MOC|Monitoring Documentation]]

## 🐞 Common Issues

### SSH Connection Failures
**Symptom**: `Failed to connect to the host via ssh`
**Solutions**:
1. Verify host is reachable: `ping hostname`
2. Check SSH config: `ssh user@hostname`
3. Verify SSH keys are configured
4. Check firewall rules allow SSH

### Permission Denied
**Symptom**: `Permission denied (publickey)` or `sudo: a password is required`
**Solutions**:
1. Verify SSH keys in `~/.ssh/authorized_keys`
2. Check `ansible_user` in inventory
3. Add `ansible_become_pass` to vault.yml
4. Configure passwordless sudo

### High-Risk Phase Failures
**phase2 (Networking)**: Can disconnect hosts
- Always test on canary first
- Keep console access available
- Have rollback plan ready

**phase4 (Docker)**: Resource intensive
- Monitor disk space during deployment
- Watch memory usage
- Docker daemon failures need manual intervention

### Variable Not Found
**Symptom**: `'variable_name' is undefined`
**Solutions**:
1. Check variable precedence: host_vars > group_vars > role defaults
2. Verify variable is defined in correct location
3. Check for typos in variable name
4. Ensure required variables are in vault.yml

## 📚 Additional Resources

### In Repository
- [docs/WORKFLOWS.md](file:///Users/danielschmeichel/github/ansible/docs/WORKFLOWS.md) - Detailed workflows
- [docs/ROLE_STANDARDS.md](file:///Users/danielschmeichel/github/ansible/docs/ROLE_STANDARDS.md) - Development standards
- [docs/TROUBLESHOOTING.md](file:///Users/danielschmeichel/github/ansible/docs/TROUBLESHOOTING.md) - Troubleshooting guide
- [CLAUDE.md](file:///Users/danielschmeichel/github/ansible/CLAUDE.md) - AI assistant integration
- [AGENTS.md](file:///Users/danielschmeichel/github/ansible/AGENTS.md) - Quick start guide

### Related Vault Pages
- [[Repository Map]]
- [[Infrastructure/Infrastructure MOC|Infrastructure Overview]]
- [[Security/Security MOC|Security Documentation]]
- [[Procedures/Procedures MOC|Operational Procedures]]

---

**Last updated**: 2025-11-27
**Repository**: `/Users/danielschmeichel/github/ansible`
**Maintainer**: Daniel Schmeichel
