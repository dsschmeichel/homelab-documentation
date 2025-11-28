---
tags:
  - docker
  - infrastructure
  - gitops
  - komodo
aliases:
  - Docker Infrastructure
  - Container Platform
created: 2024-11-24
updated: 2024-11-24
---

# Docker Infrastructure

Central hub for Docker containerized service deployment across the Badger Development homelab infrastructure.

## Overview

The Docker infrastructure uses a **GitOps workflow** powered by Komodo to manage 35+ containerized stacks across 7 hosts. All configuration lives in the `/Users/danielschmeichel/github/docker` repository, which Komodo polls every 5 minutes to automatically deploy changes.

**Key Characteristics:**
- **GitOps-first**: Git is the source of truth, changes trigger automatic deployment
- **Declarative configuration**: Docker Compose files with Komodo sync mappings
- **Multi-host topology**: 7 Docker hosts across 3 geographic regions
- **Centralized orchestration**: Komodo Core on hercules manages all deployments
- **Hub-agent architecture**: Beszel and Dozzle use centralized hubs with distributed agents

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Repository (docker)                                  │
│ - stacks/ (36 Docker Compose stacks)                        │
│ - syncs/ (Komodo host mappings)                             │
│ - komodo/ (Komodo Core + Periphery configs)                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Poll every 5 minutes
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Komodo Core (hercules:9120)                                 │
│ - Monitors Git repository                                    │
│ - Deploys stack changes automatically                        │
│ - Manages Periphery agents on remote hosts                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTPS (port 8120)
                 ▼
      ┌──────────┴──────────┐
      │                     │
      ▼                     ▼
┌─────────────┐      ┌─────────────┐
│ Periphery   │      │ Periphery   │
│ Agents      │ ...  │ Agents      │
│ (7 hosts)   │      │ (7 hosts)   │
└─────────────┘      └─────────────┘
      │                     │
      ▼                     ▼
Docker Stacks          Docker Stacks
```

## Stack Categories

### Applications (15+ stacks)
User-facing services and productivity tools.

- **[[Docker/Stacks Inventory#homepage|homepage]]** - Dashboard and service directory
- **[[Docker/Stacks Inventory#immich|immich]]** - Photo management platform
- **[[Docker/Stacks Inventory#paperless-ngx|paperless-ngx]]** - Document management system
- **[[Docker/Stacks Inventory#ntfy|ntfy]]** - Push notification service
- **[[Docker/Stacks Inventory#mealie|mealie]]** - Recipe manager
- **[[Docker/Stacks Inventory#karakeep|karakeep]]** - Karaoke library manager
- **[[Docker/Stacks Inventory#it-tools|it-tools]]** - Developer utilities collection
- **[[Docker/Stacks Inventory#omni-tools|omni-tools]]** - Multi-purpose toolbox
- **[[Docker/Stacks Inventory#stirling-pdf|stirling-pdf]]** - PDF manipulation tool
- **[[Docker/Stacks Inventory#termix|termix]]** - Web-based terminal
- **[[Docker/Stacks Inventory#phpipam|phpipam]]** - IP address management
- **[[Docker/Stacks Inventory#open-webui|open-webui]]** - LLM interface
- **[[Docker/Stacks Inventory#openhands|openhands]]** - AI coding assistant
- **[[Docker/Stacks Inventory#qdrant|qdrant]]** - Vector database
- **[[Docker/Stacks Inventory#dock-dploy|dock-dploy]]** - Deployment dashboard

### Infrastructure (11 stacks)
Platform services supporting the homelab ecosystem.

- **[[Docker/Komodo|komodo]]** - GitOps orchestration platform (Core)
- **[[Docker/Stacks Inventory#n8n|n8n]]** - Workflow automation
- **[[Docker/Stacks Inventory#postgres|postgres]]** - PostgreSQL database cluster
- **[[Docker/Stacks Inventory#pocketid|pocketid]]** - OIDC authentication provider
- **[[Docker/Stacks Inventory#crowdsec|crowdsec]]** - Security and threat detection
- **[[Docker/Stacks Inventory#pangolin|pangolin]]** - Traefik reverse proxy
- **[[Docker/Stacks Inventory#dockflare|dockflare]]** - Cloudflare DNS automation
- **[[Docker/Stacks Inventory#wireguard|wireguard]]** - VPN tunnels
- **[[Docker/Stacks Inventory#netbox|netbox]]** - Infrastructure documentation
- **[[Docker/Stacks Inventory#nebula-sync|nebula-sync]]** - Configuration sync service
- **[[Docker/Stacks Inventory#newt|newt]]** - Pangolin tunnel agents (7 instances)
- **[[Docker/Stacks Inventory#semaphore|semaphore]]** - Ansible automation UI

### Monitoring (8 stacks)
Observability, alerting, and system health tracking.

- **[[Docker/Stacks Inventory#beszel|beszel]]** - Infrastructure monitoring hub
- **[[Docker/Stacks Inventory#beszel-agent|beszel-agent]]** - Beszel monitoring agents (6 instances)
- **[[Docker/Stacks Inventory#dozzle|dozzle]]** - Docker log aggregation hub
- **[[Docker/Stacks Inventory#dozzle-agent|dozzle-agent]]** - Dozzle log collection agents (6 instances)
- **[[Docker/Stacks Inventory#uptime-kuma|uptime-kuma]]** - Service uptime monitoring
- **[[Docker/Stacks Inventory#netalertx|netalertx]]** - Network device tracking
- **[[Docker/Stacks Inventory#diun|diun]]** - Docker image update notifications (7 instances)
- **[[Docker/Stacks Inventory#alertmanager|alertmanager]]** - Alert routing and management

## Docker Hosts

The infrastructure spans **7 Docker hosts** across 3 regions:

| Host | Region | Role | Stacks | Connection |
|------|--------|------|--------|------------|
| **[[Infrastructure/Hosts Inventory#hercules\|hercules]]** | Amethyst | Primary AMD64 node + Komodo Core | 11 | 10.2.0.70:8120 |
| **[[Infrastructure/Hosts Inventory#apollo\|apollo]]** | Amethyst | Monitoring hub | 10 | 100.102.0.11:8120 |
| **[[Infrastructure/Hosts Inventory#synology-nas\|synology-nas]]** | Amethyst | Storage-backed services | 4 | 10.2.0.200:8120 |
| **[[Infrastructure/Hosts Inventory#codewizard\|codewizard]]** | Amethyst | Development services | 3 | 10.2.0.65:8120 |
| **[[Infrastructure/Hosts Inventory#oci-dmz\|oci-dmz]]** | Oracle Cloud | DMZ/ingress services | 9 | 100.90.0.90:8120 |
| **[[Infrastructure/Hosts Inventory#oci-docker\|oci-docker]]** | Oracle Cloud | ARM64 worker | 5 | 100.70.1.70:8120 |
| **[[Infrastructure/Hosts Inventory#meade\|meade]]** | Remote Edge | Edge services | 3 | 100.119.163.88:8120 |

See **[[Docker/Host Fleet]]** for detailed host configurations and deployment topology.

## GitOps Workflow

### Repository Structure

```
docker/
├── stacks/              # Docker Compose definitions
│   ├── applications/    # User-facing services
│   ├── infrastructure/  # Platform services
│   ├── monitoring/      # Observability stacks
│   └── _stack_archive/  # Retired services
├── syncs/               # Komodo configuration
│   ├── servers.toml     # Host definitions
│   ├── stacks-*.toml    # Per-host stack mappings
│   └── resourcesync.toml # Git polling config
├── komodo/              # Komodo deployment
│   ├── compose.yaml     # Komodo Core
│   └── periphery/       # Periphery agents
├── scripts/             # Operational scripts
├── docs/                # Repository documentation
└── config/              # Shared templates
```

### Deployment Process

1. **Local development**: Edit stack compose files in `stacks/<category>/<name>/`
2. **Validation**: Run `docker compose config` from stack directory
3. **Commit changes**: Push to `main` branch in GitHub
4. **Automatic deployment**: Komodo polls repository every 5 minutes
5. **Stack update**: Komodo pulls changes and redeploys affected stacks
6. **Verification**: Check deployment status in Komodo UI at https://komodo.badger-dev.com

**Important**: Changes to `main` branch deploy automatically to production. Use feature branches for testing.

### Host-Specific Configuration

Per-host environment overrides are defined in `syncs/stacks-<host>.toml`:

```toml
[[stack]]
name = "dozzle-agent-hercules"
[stack.config]
server = "hercules"
project_name = "dozzle-agent"
poll_for_updates = true
auto_update = true
run_directory = "stacks/monitoring/dozzle-agent"
environment = """
DOZZLE_HOSTNAME=hercules
"""
```

This allows single compose files to be deployed to multiple hosts with different configurations.

## Integration with Ansible

Docker deployment is **Phase 4** of the Ansible automation:

1. **Phase 0-1**: System prerequisites, users, SSH
2. **Phase 2-3**: Networking, storage, base services
3. **[[../Infrastructure/Ansible#Phase 4 Docker|Phase 4]]**: Docker installation and Komodo Periphery agent setup
4. **Phase 5-9**: Monitoring, backups, validation

The `docker` Ansible role:
- Installs Docker Engine and Docker Compose
- Configures daemon.json with logging and storage drivers
- Deploys Komodo Periphery agent systemd service
- Creates `/home/docker/stacks/` directory structure
- Clones docker repository to each host

See **[[../Infrastructure/Ansible]]** for full automation details.

## Monitoring Integration

### Beszel Hub-Agent Architecture

**Beszel Hub** runs on **apollo** and collects metrics from 6 Beszel agents:
- hercules, oci-dmz, oci-docker, synology-nas, meade, codewizard

Provides:
- CPU, memory, disk, network utilization
- Container stats and health
- Historical metrics and alerting

### Dozzle Hub-Agent Architecture

**Dozzle Hub** runs on **hercules** and aggregates logs from 6 Dozzle agents:
- hercules, apollo, oci-dmz, oci-docker, synology-nas, meade

Provides:
- Real-time container log streaming
- Multi-host log search
- Log filtering and export

### Other Monitoring

- **Uptime Kuma**: HTTP/TCP service availability checks
- **NetAlertX**: Network device discovery and tracking
- **DIUN**: Docker image update notifications across all hosts
- **Pulse**: Proxmox hypervisor monitoring

See **[[../Monitoring/Monitoring MOC]]** for comprehensive monitoring documentation.

## Security Architecture

### Authentication

- **PocketID**: OIDC provider for SSO across services
  - Deployed on oci-dmz for external access
  - Integrates with FreeIPA LDAP backend
  - Provides OAuth2/OIDC for modern applications

- **FreeIPA LDAP**: Centralized authentication backend
  - Server: ipa1.int.badger-dev.com (10.2.0.20)
  - Base DN: `dc=int,dc=badger-dev,dc=com`
  - Used by phpIPAM, Semaphore, and other legacy LDAP clients

### Network Security

- **Pangolin (Traefik)**: Reverse proxy on oci-dmz
  - TLS termination with Let's Encrypt
  - CrowdSec integration for threat detection
  - Route traffic to internal services via Newt tunnels

- **CrowdSec**: Security engine analyzing logs and blocking threats
  - Deployed on oci-dmz
  - LAPI key shared with Pangolin
  - Community threat intelligence integration

- **WireGuard**: Site-to-site and remote access VPN
  - DMZ instance on oci-dmz for external access
  - Meade instance for remote edge connectivity
  - Tailscale provides primary mesh VPN (100.x.x.x/16)

See **[[../Security/Security MOC]]** for detailed security documentation.

## Operational Procedures

### Common Tasks

**View Komodo status:**
```bash
ssh hercules
cd /home/docker/komodo
docker compose ps
docker compose logs -f core
```

**Manual stack deployment:**
```bash
# Via Komodo UI
https://komodo.badger-dev.com
# Click stack → Deploy

# Via SSH (emergency only)
ssh <host>
cd /home/docker/stacks/<category>/<stack-name>
docker compose pull
docker compose up -d
```

**Update Komodo Core:**
```bash
cd /Users/danielschmeichel/github/docker
bash scripts/update-komodo.sh --core-only
```

**Update Periphery agents:**
```bash
cd /Users/danielschmeichel/github/docker
bash scripts/update-komodo.sh --periphery-only
# Or target specific host:
bash scripts/update-komodo.sh --host apollo
```

**Validate stack configuration:**
```bash
cd /Users/danielschmeichel/github/docker/stacks/<category>/<stack>
docker compose config
```

**Health check across all hosts:**
```bash
cd /Users/danielschmeichel/github/docker
bash scripts/multi-host-check.sh
```

### Emergency Procedures

**Komodo Core failure:**
1. SSH to hercules: `ssh hercules`
2. Check Core logs: `cd /home/docker/komodo && docker compose logs -f core`
3. Check MongoDB: `docker compose logs -f mongo`
4. Restart if needed: `docker compose restart core`
5. If Core is unrecoverable, deploy stacks manually via SSH

**Stack deployment failure:**
1. Check Komodo UI for error messages
2. SSH to target host and check Periphery logs: `sudo journalctl -u komodo-periphery -f`
3. Validate compose file locally: `docker compose config`
4. Check for missing environment variables in `syncs/stacks-<host>.toml`
5. Manual deployment if needed: `docker compose up -d`

**Mass container failures:**
1. Check Beszel for resource exhaustion (disk, memory)
2. Check Dozzle for error patterns across containers
3. Investigate Docker daemon: `systemctl status docker`
4. Review recent Git commits for breaking changes

See **[[../Procedures/Emergency Procedures]]** for comprehensive emergency response procedures.

## Related Documentation

### Infrastructure
- **[[Docker/Komodo]]** - Komodo orchestration platform details
- **[[Docker/Host Fleet]]** - Docker host topology and configuration
- **[[Docker/Stacks Inventory]]** - Complete inventory of all 36 stacks
- **[[../Infrastructure/Ansible]]** - Ansible automation including Docker setup

### Services
- **[[../Services/Application Catalog]]** - User-facing application documentation
- **[[../Services/Service Dependencies]]** - Service dependency mapping

### Operations
- **[[../Procedures/Deployment]]** - Deployment procedures and best practices
- **[[../Procedures/Troubleshooting]]** - Docker troubleshooting guide
- **[[../Monitoring/Beszel]]** - Beszel monitoring configuration
- **[[../Monitoring/Dozzle]]** - Dozzle log aggregation configuration

### Security
- **[[../Security/LDAP]]** - FreeIPA/LDAP integration details
- **[[../Security/Certificates]]** - TLS certificate management

## External References

- **Komodo Documentation**: https://komo.do/docs
- **Docker Repository**: /Users/danielschmeichel/github/docker
- **Komodo UI**: https://komodo.badger-dev.com
- **GitHub Actions**: Automated validation and deployment

