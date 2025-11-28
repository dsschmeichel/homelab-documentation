---
tags:
  - docker
  - infrastructure
  - hosts
aliases:
  - Docker Hosts
  - Container Hosts
created: 2024-11-24
updated: 2024-11-24
---

# Docker Host Fleet

Overview of the 7 Docker hosts running containerized services across the homelab infrastructure.

## Fleet Overview

| Host | Region | Architecture | Role | Stacks | Komodo Port |
|------|--------|--------------|------|--------|-------------|
| **hercules** | Amethyst | AMD64 | Primary + Komodo Core | 11 | host.docker.internal:8120 |
| **apollo** | Amethyst | ARM64 (Pi 4) | Monitoring hub | 10 | 100.102.0.11:8120 |
| **synology-nas** | Amethyst | x86_64 | Storage-backed services | 6 | 10.2.0.200:8120 |
| **codewizard** | Amethyst | AMD64 | Development services | 3+ | 10.2.0.65:8120 |
| **oci-dmz** | Oracle Cloud | AMD64 | DMZ/ingress gateway | 9 | 100.90.0.90:8120 |
| **oci-docker** | Oracle Cloud | ARM64 (Ampere) | Cloud worker | 12 | 100.70.1.70:8120 |
| **meade** | Remote Edge | ARM64 (Pi 4) | Edge services | 5 | 100.119.163.88:8120 |

**Total**: 53 stack instances across 7 hosts in 3 geographic regions.

## Geographic Distribution

### Amethyst Region (On-Premises)
Primary homelab location with 4 Docker hosts:
- **hercules**: Main workstation, runs Komodo Core
- **apollo**: Raspberry Pi 4, monitoring hub
- **synology-nas**: NAS appliance, storage services
- **codewizard**: KVM VM on Proxmox, development

**Connectivity**: Private LAN (10.2.0.0/24) + Tailscale mesh

### Oracle Cloud Region
2 cloud instances for DMZ and additional capacity:
- **oci-dmz**: AMD64 instance, public-facing reverse proxy
- **oci-docker**: ARM64 Ampere instance, application worker

**Connectivity**: Tailscale mesh (100.x.x.x/16)

### Remote Edge (Meade)
1 remote location host:
- **meade**: Raspberry Pi 4, WireGuard + monitoring agents

**Connectivity**: Tailscale + WireGuard site-to-site

## Host Details

### hercules
**Location**: Amethyst on-premises (10.2.0.70)
**Hardware**: Main workstation (AMD64)
**Role**: Primary Docker host + Komodo Core
**Connection**: host.docker.internal:8120 (local)

**Deployed Stacks** (11):
- **Applications**: homepage, karakeep, termix
- **Infrastructure**: komodo (Core), n8n, semaphore, newt-hercules
- **Monitoring**: dozzle (hub), dozzle-agent-hercules, diun-hercules

**Key Characteristics**:
- Runs Komodo Core with MongoDB
- Dozzle log aggregation hub
- Local Periphery agent via host.docker.internal
- High-performance AMD64 for resource-intensive workloads

**Storage**:
- Local SSD for containers and volumes
- NFS mounts to Synology NAS for shared data

**Access**:
```bash
ssh hercules
# Komodo Core
cd /home/docker/komodo && docker compose ps
# Stacks
cd /home/docker/stacks/ && ls -la
```

---

### apollo
**Location**: Amethyst on-premises (10.2.0.11)
**Hardware**: Raspberry Pi 4 (ARM64)
**Role**: Monitoring and observability hub
**Connection**: 100.102.0.11:8120 (Tailscale)

**Deployed Stacks** (10):
- **Applications**: phpipam
- **Infrastructure**: netbox, nebula-sync, newt-apollo
- **Monitoring**: beszel (hub), pulse, uptime-kuma, netalertx, dozzle-agent-apollo, diun-apollo

**Key Characteristics**:
- Beszel monitoring hub (collects metrics from all hosts)
- Network monitoring (NetAlertX, phpIPAM)
- Infrastructure documentation (NetBox)
- ARM64 efficiency for 24/7 monitoring workloads

**Storage**:
- MicroSD card (system)
- NFS mounts for persistent data

**Access**:
```bash
ssh apollo
cd /home/docker/stacks/ && ls -la
```

---

### synology-nas
**Location**: Amethyst on-premises (10.2.0.200)
**Hardware**: Synology NAS appliance (x86_64)
**Role**: Storage-intensive applications
**Connection**: 10.2.0.200:8120 (LAN)

**Deployed Stacks** (6):
- **Applications**: immich, paperless-ngx
- **Infrastructure**: newt-synology
- **Monitoring**: beszel-agent-synology, dozzle-agent-synology, diun-synology

**Key Characteristics**:
- Direct access to large NAS storage arrays
- Optimized for media and document management
- Hardware transcoding for Immich
- RAID-backed persistent storage

**Storage**:
- Direct volume mounts to NAS shares
- No NFS overhead for storage-heavy apps

**Access**:
```bash
ssh synology-nas
cd /home/docker/stacks/ && ls -la
```

---

### codewizard
**Location**: Amethyst on-premises (10.2.0.65)
**Hardware**: KVM VM on Proxmox (AMD64)
**Role**: Development and experimental services
**Connection**: 10.2.0.65:8120 (LAN)

**Deployed Stacks** (3+):
- **Infrastructure**: newt-codewizard
- **Monitoring**: beszel-agent-codewizard, diun-codewizard
- *Additional stacks TBD*

**Key Characteristics**:
- Isolated environment for testing
- Snapshot capability via Proxmox
- Can be easily reset/rebuilt
- Development workspace isolation

**Storage**:
- Virtual disk on Proxmox storage
- Ephemeral by design (easy rollback)

**Access**:
```bash
ssh codewizard
cd /home/docker/stacks/ && ls -la
```

---

### oci-dmz
**Location**: Oracle Cloud (Phoenix datacenter)
**Hardware**: AMD64 VM (Always Free tier)
**Role**: DMZ and public ingress gateway
**Connection**: 100.90.0.90:8120 (Tailscale)

**Deployed Stacks** (9):
- **Infrastructure**: pangolin (Traefik reverse proxy), crowdsec, pocketid, dockflare, wireguard-dmz, newt-oci-dmz
- **Monitoring**: dozzle-agent-oci-dmz, diun-oci-dmz

**Key Characteristics**:
- Only host directly exposed to internet
- All external traffic enters via this gateway
- Pangolin/Traefik reverse proxy with CrowdSec
- WireGuard VPN endpoint
- PocketID OIDC provider for authentication

**Critical Services**:
- **Pangolin + Gerbil**: Traefik-based reverse proxy with tunnel termination
- **CrowdSec**: Security engine analyzing traffic
- **PocketID**: OIDC/OAuth2 authentication provider
- **Newt tunnels**: 7 tunnel endpoints from internal hosts

**Storage**:
- Minimal local storage (mostly stateless)
- Config files for Pangolin/Traefik

**Access**:
```bash
ssh oci-dmz
cd /home/docker/stacks/ && ls -la
```

**Security Considerations**:
- Hardened firewall rules (only 80/443/51820/21820 exposed)
- CrowdSec automatic IP banning
- Regular security updates critical
- Minimal attack surface (no user data)

---

### oci-docker
**Location**: Oracle Cloud (Phoenix datacenter)
**Hardware**: ARM64 Ampere VM (Always Free tier)
**Role**: Cloud application worker
**Connection**: 100.70.1.70:8120 (Tailscale)

**Deployed Stacks** (12):
- **Applications**: karakeep, mealie, it-tools, omni-tools, stirling-pdf, open-webui, openhands, qdrant, dock-dploy
- **Infrastructure**: newt-oci-docker
- **Monitoring**: dozzle-agent-oci-docker, diun-oci-docker

**Key Characteristics**:
- ARM64 Ampere architecture (efficient, always-free)
- Application worker for user-facing services
- No direct internet exposure (via Pangolin tunnel)
- Geographic redundancy for critical apps

**Storage**:
- Block volumes for persistent data
- Oracle Cloud backup integration

**Access**:
```bash
ssh oci-docker
cd /home/docker/stacks/ && ls -la
```

---

### meade
**Location**: Remote edge location
**Hardware**: Raspberry Pi 4 (ARM64)
**Role**: Remote monitoring and VPN gateway
**Connection**: 100.119.163.88:8120 (Tailscale)

**Deployed Stacks** (5):
- **Infrastructure**: wireguard, newt-meade
- **Monitoring**: beszel-agent-meade, dozzle-agent-meade, diun-meade

**Key Characteristics**:
- Remote site connectivity via WireGuard
- Monitoring presence at edge location
- Low-power ARM64 for 24/7 operation
- Site-to-site VPN endpoint

**Storage**:
- MicroSD card (minimal storage needs)

**Access**:
```bash
ssh meade
cd /home/docker/stacks/ && ls -la
```

## Network Architecture

### Connectivity Matrix

| Host | Primary Network | Backup Network | Docker Networks |
|------|-----------------|----------------|-----------------|
| hercules | LAN (10.2.0.70) | Tailscale | pangolin-tunnel, komodo, default |
| apollo | Tailscale (100.102.0.11) | LAN (10.2.0.11) | pangolin-tunnel, default |
| synology-nas | LAN (10.2.0.200) | Tailscale | pangolin-tunnel, default |
| codewizard | LAN (10.2.0.65) | - | pangolin-tunnel, default |
| oci-dmz | Public IP | Tailscale (100.90.0.90) | cloudflare-net, pangolin-tunnel, default |
| oci-docker | Tailscale (100.70.1.70) | - | pangolin-tunnel, default |
| meade | Tailscale (100.119.163.88) | WireGuard | pangolin-tunnel, default |

### Komodo Connectivity

All hosts connect to Komodo Core via Periphery agents on port 8120 (HTTPS):

```
hercules → localhost:8120 (via host.docker.internal)
apollo → 100.102.0.11:8120 (Tailscale)
oci-dmz → 100.90.0.90:8120 (Tailscale)
oci-docker → 100.70.1.70:8120 (Tailscale)
synology-nas → 10.2.0.200:8120 (LAN)
meade → 100.119.163.88:8120 (Tailscale)
codewizard → 10.2.0.65:8120 (LAN)
```

### External Access Flow

```
Internet
   │
   ▼
oci-dmz (Public IP)
   │
   ├─► Pangolin/Traefik (ports 80/443)
   │   └─► CrowdSec filtering
   │
   ├─► WireGuard VPN (port 51820)
   │
   └─► Gerbil tunnel (receives Newt connections)
       │
       ├─► newt-hercules → internal services on hercules
       ├─► newt-apollo → internal services on apollo
       ├─► newt-synology → internal services on synology-nas
       └─► newt-oci-docker → internal services on oci-docker
```

## Stack Distribution Strategy

### By Purpose

**DMZ/External** (oci-dmz):
- Reverse proxy and ingress (Pangolin)
- Authentication provider (PocketID)
- Security filtering (CrowdSec)
- VPN gateway (WireGuard)

**Storage-Intensive** (synology-nas):
- Photo management (Immich)
- Document management (Paperless-ngx)

**Monitoring** (apollo):
- Metrics hub (Beszel)
- Service monitoring (Uptime Kuma)
- Network monitoring (NetAlertX, phpIPAM)
- Infrastructure docs (NetBox)

**Application Worker** (oci-docker):
- User-facing applications
- AI/ML services (open-webui, qdrant)
- Utility tools

**Central Services** (hercules):
- Orchestration (Komodo Core)
- Automation (n8n, Semaphore)
- Dashboard (Homepage)
- Log aggregation (Dozzle hub)

### By Architecture

**AMD64 hosts** (hercules, codewizard, oci-dmz):
- Resource-intensive workloads
- Legacy software compatibility
- Development environments

**ARM64 hosts** (apollo, oci-docker, meade):
- Energy-efficient 24/7 services
- Monitoring agents
- Cloud-native applications
- Cost optimization (Oracle Free Tier)

**x86_64 appliances** (synology-nas):
- Vendor-optimized workloads
- Storage appliance software

## Management Operations

### Fleet-Wide Operations

**Health check across all hosts**:
```bash
cd /Users/danielschmeichel/github/docker
bash scripts/multi-host-check.sh
```

**Git sync across all hosts**:
```bash
bash scripts/git-pull-all-hosts.sh
```

**Update all Periphery agents**:
```bash
bash scripts/update-komodo.sh --periphery-only
```

### Per-Host Operations

**SSH into any host**:
```bash
# Via SSH config aliases
ssh hercules
ssh apollo
ssh oci-dmz
ssh oci-docker
ssh synology-nas
ssh meade
ssh codewizard
```

**Check Docker status**:
```bash
ssh <host>
docker ps
docker stats --no-stream
df -h /var/lib/docker
```

**Check Periphery agent**:
```bash
ssh <host>
sudo systemctl status komodo-periphery
sudo journalctl -u komodo-periphery -f
```

**View stack logs**:
```bash
ssh <host>
cd /home/docker/stacks/<category>/<stack>
docker compose logs -f
```

## Resource Allocation

### CPU/Memory by Host

| Host | CPU | Memory | Disk | Stack Load |
|------|-----|--------|------|------------|
| hercules | 16 cores | 64GB | 2TB NVMe | Heavy (Komodo + services) |
| apollo | 4 cores (ARM) | 8GB | 128GB SD | Light (monitoring agents) |
| synology-nas | 4 cores | 16GB | 48TB RAID | Medium (storage apps) |
| codewizard | 4 cores | 8GB | 100GB | Light (dev/experimental) |
| oci-dmz | 1 core | 1GB | 50GB | Medium (ingress + security) |
| oci-docker | 4 cores (ARM) | 24GB | 200GB | Medium (applications) |
| meade | 4 cores (ARM) | 4GB | 64GB SD | Light (edge services) |

### Capacity Planning

**High-capacity hosts** (new services):
- oci-docker (24GB RAM, ARM64)
- hercules (64GB RAM, AMD64)
- synology-nas (16GB RAM, unlimited storage)

**Constrained hosts** (agents only):
- oci-dmz (1GB RAM - Oracle Free Tier limit)
- meade (4GB RAM - Pi 4)
- apollo (8GB RAM - Pi 4, monitoring hub)

**Development/Testing**:
- codewizard (isolated, snapshot-able)

## Deployment Topology

### Hub-Agent Patterns

**Beszel** (Infrastructure Monitoring):
```
apollo (hub)
├─► hercules (agent)
├─► oci-dmz (agent)
├─► oci-docker (agent)
├─► synology-nas (agent)
├─► meade (agent)
└─► codewizard (agent)
```

**Dozzle** (Log Aggregation):
```
hercules (hub)
├─► hercules (agent)
├─► apollo (agent)
├─► oci-dmz (agent)
├─► oci-docker (agent)
├─► synology-nas (agent)
└─► meade (agent)
```

**Pangolin/Newt** (Reverse Proxy Tunneling):
```
oci-dmz (Pangolin + Gerbil hub)
├─► hercules (newt-hercules)
├─► apollo (newt-apollo)
├─► oci-dmz (newt-oci-dmz - self-tunnel)
├─► oci-docker (newt-oci-docker)
├─► synology-nas (newt-synology)
├─► meade (newt-meade)
└─► codewizard (newt-codewizard)
```

## Maintenance Schedule

### Daily
- Automated container updates (via Komodo polling)
- Log rotation (Docker daemon)
- Health checks (multi-host-check.sh)

### Weekly
- Periphery agent restarts (if needed)
- Disk space checks
- Security updates (unattended-upgrades)

### Monthly
- Full system updates (Ansible playbooks)
- Backup verification
- Certificate renewal checks

### Quarterly
- Host OS upgrades (Debian point releases)
- Capacity planning review
- Performance optimization

## Troubleshooting

### Host Unreachable

1. Check network connectivity:
```bash
ping <host-ip>
tailscale status | grep <host>
```

2. Verify SSH access:
```bash
ssh -v <host>
```

3. Check Periphery agent:
```bash
# From Komodo UI: Servers → <host> → Status
# Shows last heartbeat timestamp
```

### Docker Daemon Issues

1. Check daemon status:
```bash
ssh <host>
sudo systemctl status docker
```

2. View daemon logs:
```bash
sudo journalctl -u docker -f
```

3. Restart if needed:
```bash
sudo systemctl restart docker
```

### Resource Exhaustion

1. Check disk space:
```bash
ssh <host>
df -h
docker system df
```

2. Check memory:
```bash
free -h
docker stats --no-stream
```

3. Clean up if needed:
```bash
docker system prune -a --volumes
# WARNING: Removes unused containers, images, volumes
```

## Related Documentation

- **[[Docker/Docker MOC]]** - Docker infrastructure overview
- **[[Docker/Komodo]]** - Komodo orchestration details
- **[[Docker/Stacks Inventory]]** - All stack configurations
- **[[../Infrastructure/Hosts Inventory]]** - Complete host details (all 13 hosts)
- **[[../Infrastructure/Proxmox]]** - Virtualization for codewizard
- **[[../Network/Topology]]** - Network architecture
- **[[../Monitoring/Beszel]]** - Beszel monitoring setup
- **[[../Monitoring/Dozzle]]** - Dozzle log aggregation

## External References

- **Komodo Servers**: https://komodo.badger-dev.com → Settings → Servers
- **Beszel Dashboard**: https://beszel.badger-dev.com
- **Dozzle Dashboard**: https://logs.badger-dev.com
