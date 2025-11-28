---
title: Repository Map
tags: [infrastructure, moc, repos]
created: 2025-11-23
updated: 2025-11-23
---

# 📁 Repository Map

This homelab infrastructure is managed through three main Git repositories, each serving a distinct purpose in the automation pipeline.

## 🔗 Three-Tier Architecture

The infrastructure follows a three-tier automation workflow:

```
Packer (Golden Images) → OpenTofu (Provisioning) → Ansible (Configuration)
                                                      ↓
                                                   Docker (Services)
```

### Tier 1: Packer
- **Purpose**: Build golden VM templates
- **Scope**: Base OS, foundational software, hardening
- **Not tracked in these repos** (separate Packer repository)

### Tier 2: OpenTofu
- **Purpose**: Infrastructure provisioning  
- **Scope**: VM cloning, networking, resource allocation
- **Not tracked in these repos** (separate OpenTofu repository)

### Tier 3: Ansible + Docker
- **Purpose**: Configuration management and service deployment
- **Scope**: Host configuration, security, applications
- **Repos**: `ansible`, `docker`, `dotfiles`

## 📚 Repository Details

### Ansible Repository

**Location**: `/Users/danielschmeichel/github/ansible`
**Purpose**: Configuration management and infrastructure automation

#### Key Components
- **Playbooks**: `playbooks/infrastructure/site.yml` - Main orchestration
- **Roles**: 19 roles organized by function
- **Inventory**: `inventory.yml` - Source of truth for hosts
- **Variables**: `group_vars/`, `host_vars/` - Configuration data
- **Scripts**: Host management tools and utilities

#### Key Documentation
- [[Ansible/README|README]]
- [[Ansible/Workflows|Workflows]] - Deployment procedures
- [[Ansible/Role Standards|Role Standards]] - Development guidelines
- [[Ansible/Troubleshooting|Troubleshooting]] - Common issues

#### Phase Architecture
Ansible executes in numbered phases:
- `phase0`: Validation and facts (Low risk)
- `phase1`: Core system baseline (Medium risk)
- `phase2`: Networking (High risk)
- `phase3`: Network sharing (Medium risk)
- `phase4`: Containers/Docker (High risk)
- `phase5`: Reserved for future use
- `phase6`: Developer/AI tooling (Low risk)
- `phase7`: Monitoring/health checks (Medium risk)
- `phase8`: Validation sweeps (Low risk)
- `phase9`: Failure summary (Low risk)

#### Role Inventory
1. `ai_cli_tools` - AI assistant CLI tools
2. `developer_environment` - Development tools setup
3. `docker` - Docker engine configuration
4. `dotfiles` - User environment configuration
5. `freeipa_client` - FreeIPA integration
6. `freeipa_local_user_migration` - User migration utilities
7. `hardware_tuning` - Hardware optimization
8. `hosts_distribution` - /etc/hosts management
9. `komodo` - Komodo orchestration setup
10. `linux_firewall` - Legacy firewall management
11. `network_sharing` - NFS/SMB configuration
12. `network_toolbox` - Network diagnostic tools
13. `security_hardening` - Security baseline
14. `system_baseline` - Core system configuration
15. `system_tools` - System utility packages
16. `system_update` - Update management
17. `tailscale` - Tailscale VPN client
18. `time_sync` - NTP/chrony configuration
19. `ufw_firewall` - UFW firewall rules

### Docker Repository

**Location**: `/Users/danielschmeichel/github/docker`
**Purpose**: Declarative Docker infrastructure management

#### Key Components
- **Stacks**: Docker Compose files organized by category
  - `applications/` - User-facing applications
  - `infrastructure/` - Core infrastructure services
  - `monitoring/` - Monitoring and observability
- **Syncs**: Komodo configuration files
  - `servers.toml` - Host registration
  - `stacks-*.toml` - Per-host stack assignments
- **Komodo**: Orchestration platform deployment
- **Scripts**: Provisioning, backup, and maintenance tools
- **Docs**: Operational runbooks

#### Key Documentation
- [[Docker/README|README]]
- [[Docker/Operations|Operations]] - Day-to-day operations
- [[Docker/Deployment|Deployment]] - Deployment workflows
- [[Docker/Host Inventory|Host Inventory]] - Fleet topology
- [[Docker/Troubleshooting|Troubleshooting]]

#### Active Hosts
| Host | Role | Purpose |
|------|------|----------|
| `hercules` | Primary AMD64 + Komodo Core | Main workload host |
| `oci-dmz` | DMZ/front-door | Oracle Cloud public services |
| `oci-docker` | ARM64 worker | Oracle Cloud compute |
| `synology-nas` | Storage node | NAS-backed services |
| `apollo` | Monitoring hub | Internal monitoring |
| `meade` | Remote edge | Edge deployment |

#### Stack Categories
- **Applications**: 15 user-facing services
- **Infrastructure**: Core platform services (LDAP, DNS, etc.)
- **Monitoring**: Observability stack (Beszel, Dozzle, etc.)

### Dotfiles Repository

**Location**: `/Users/danielschmeichel/github/dotfiles`
**Purpose**: Personal development environment configuration

#### Key Components
- **Shell Configuration**: Bash and Zsh configs
- **Tool Configs**: Git, tmux, CLI tool settings
- **CLI Tools**: Installation and update scripts
- **AI Integration**: Claude and Gemini configurations
- **Chezmoi**: Dotfile management with templating

#### Key Files
- `.bashrc`, `.zshrc` - Shell environments
- `.gitconfig.macos` - Git configuration
- `.tmux.conf` - Terminal multiplexer config
- `dot_cli_tools_config` - CLI tool settings
- `.claude/`, `.gemini/` - AI assistant configs

## 🔄 Workflow Integration

### Standard Deployment Flow

1. **Packer** builds base image → Upload to Proxmox
2. **OpenTofu** provisions VM → Clone from template
3. **Ansible** configures host → Run `site.yml`
4. **Docker** deploys services → Komodo sync from repo
5. **Dotfiles** personalize environment → Applied per-user

### Development Workflow

1. Make changes in appropriate repository
2. Test locally or on canary host
3. Validate with linting/syntax checks
4. Commit and push to GitHub
5. Deploy via Ansible or Komodo
6. Document changes in this vault

### Emergency Recovery Workflow

1. Consult [[🆘 Emergency Procedures]]
2. Identify failed component (Ansible, Docker, Service)
3. Check relevant repo's troubleshooting docs
4. Apply fixes from version control
5. Document incident and resolution

## 📝 Documentation Strategy

### In-Repo Documentation
**What goes in Git repos**:
- Technical implementation details
- Code-level comments and docstrings
- Role/stack-specific README files
- Workflow and procedure guides
- Troubleshooting specific to that repo

### In Obsidian Vault
**What goes in this vault**:
- Cross-repository architecture
- Infrastructure inventory and topology
- Operational procedures spanning multiple repos
- Service dependency mapping
- Historical context and decision records
- Personal notes and investigations

### Linking Strategy
- Use `[[Wiki Links]]` for cross-vault navigation
- Use `file://` URLs for direct links to repo files
- Use tags for cross-cutting concerns
- Maintain bidirectional links between related topics

## 🛠️ Repository Maintenance

### Git Workflow
```bash
# Update all repos
cd ~/github/ansible && git pull
cd ~/github/docker && git pull  
cd ~/github/dotfiles && git pull

# Check status across all repos
for repo in ansible docker dotfiles; do
  echo "=== $repo ==="
  cd ~/github/$repo && git status -sb
done
```

### Backup Strategy
- All repos backed up to GitHub
- Local clones in `~/github/`
- Obsidian vault synced via iCloud
- Critical configs encrypted with Ansible Vault

### Update Cadence
- **Ansible**: Weekly updates, deploy on-demand
- **Docker**: Continuous deployment via Komodo
- **Dotfiles**: As-needed personal updates
- **This Vault**: Updated after infrastructure changes

## 🔍 Quick Search Patterns

Use these patterns to find information across repos:

| Looking for... | Check here |
|----------------|-------------|
| Host configuration | `ansible/host_vars/` or `ansible/inventory.yml` |
| Service deployment | `docker/stacks/` and `docker/syncs/` |
| Network settings | `ansible/group_vars/` and [[Network/Network MOC]] |
| Backup procedures | `docker/scripts/` and [[Backups/Backups MOC]] |
| Monitoring setup | `docker/stacks/monitoring/` and [[Monitoring/Monitoring MOC]] |
| Shell aliases | `dotfiles/dot_bash/` or `dotfiles/dot_zsh/` |
| Security configs | `ansible/roles/security_hardening/` and [[Security/Security MOC]] |

## Related Pages

- [[🏠 Home|Home]]
- [[🔧 Architecture|Architecture]]
- [[Ansible/Ansible MOC|Ansible Documentation]]
- [[Docker/Docker MOC|Docker Documentation]]
- [[Development/Dotfiles|Dotfiles Documentation]]

---

**Repository Locations**:
- Ansible: `/Users/danielschmeichel/github/ansible`
- Docker: `/Users/danielschmeichel/github/docker`
- Dotfiles: `/Users/danielschmeichel/github/dotfiles`
