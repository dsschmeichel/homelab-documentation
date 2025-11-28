# Project Purpose and Scope

## Project Type
This is an **Obsidian documentation vault** for a comprehensive homelab infrastructure, not a traditional code project. The vault serves as centralized knowledge management for a multi-repository homelab setup.

## Primary Purpose
- Document homelab infrastructure architecture and configuration
- Provide operational procedures and troubleshooting guides
- Maintain cross-repository knowledge and dependency mapping
- Serve as single source of truth for infrastructure inventory

## Scope and Coverage

### Three Main Code Repositories
1. **Ansible Repository** (`~/github/ansible`)
   - 19 roles for configuration management
   - Phase-based deployment system (phases 0-9)
   - Host management and orchestration

2. **Docker Repository** (`~/github/docker`) 
   - Declarative Docker infrastructure
   - Komodo orchestration platform
   - 15+ application and infrastructure stacks

3. **Dotfiles Repository** (`~/github/dotfiles`)
   - Personal development environment
   - Shell configurations and CLI tools
   - AI assistant integrations

### Infrastructure Components
- **6 Active Hosts**: hercules, oci-dmz, oci-docker, synology-nas, apollo, meade
- **Identity Management**: FreeIPA/LDAP integration
- **Container Platform**: Docker + Komodo orchestration
- **Monitoring**: Beszel, Dozzle for infrastructure and container monitoring
- **Networking**: Tailscale VPN, UFW firewall, network sharing (NFS/SMB)

### Documentation Structure
- **MOC (Map of Content) system** for navigation
- **Wiki links** `[[ ]]` for internal connections
- **External file:// links** to repository files
- **Tag-based categorization** for cross-referencing

## Key Features
- Three-tier automation workflow (Packer → OpenTofu → Ansible → Docker)
- Risk-based phase deployment system
- Comprehensive host and service inventory
- Emergency and troubleshooting procedures
- Development environment documentation

## Maintenance Approach
- Git-tracked with iCloud sync
- Updated after infrastructure changes
- Cross-referenced with actual code repositories
- Living documentation that evolves with the homelab