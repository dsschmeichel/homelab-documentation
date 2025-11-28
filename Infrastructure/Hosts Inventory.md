---
title: Hosts Inventory
tags: [infrastructure, hosts, inventory, specifications]
created: 2025-11-27
updated: 2025-11-27
---

# Hosts Inventory

Complete inventory of all managed hosts in the Badger Development homelab infrastructure. Includes physical hardware, virtual machines, LXC containers, and cloud resources.

## Quick Overview

| Location | Host Count | Primary Purpose | Host Types |
|----------|------------|----------------|------------|
| **Amethyst (On-prem)** | 10 | Core infrastructure | 4 VMs + 3 LXC + 3 Raspberry Pi |
| **Oracle Cloud** | 3 | Cloud services | 2 VMs + 1 remote edge |
| **Total** | **13** | Complete homelab | Mixed infrastructure |

## Host Categories

### Virtual Machines (Proxmox)
Virtual machines running on Proxmox hypervisor for general-purpose workloads and containerization.

### LXC Containers (Proxmox)
Lightweight containers optimized for specific services (database, DNS, etc.).

### Physical Hardware
Standalone physical devices including Raspberry Pi devices and specialized hardware.

### Cloud Infrastructure
Oracle Cloud VMs for public-facing services and geographic distribution.

---

## Amethyst Location (On-premises)

### Virtual Machines

#### genesis
```yaml
Hostname: genesis.int.badger-dev.com
Type: Proxmox VM
Hardware: proxmox_vm
CPU: amd64
Location: amethyst
Tailscale IP: 100.102.0.100
SSH Port: 2024
Status: Production
```

**Purpose**: Management and orchestration host for system administration tasks.

**Key Features**:
- Primary Ansible control node
- System management and monitoring
- Backup coordination
- Emergency access host

**Services**:
- Ansible automation
- SSH key management
- System administration tools
- Backup orchestration

**Access**:
- Tailscale: 100.102.0.100:2024
- Ansible inventory: `genesis`

---

#### hercules
```yaml
Hostname: hercules.int.badger-dev.com
Type: Proxmox VM
Hardware: proxmox_vm
CPU: amd64
Location: amethyst
Tailscale IP: 100.102.0.70
SSH Port: 2024
Status: Production - Critical
```

**Purpose**: Primary Docker host and core infrastructure services.

**Key Features**:
- Main Docker runtime environment
- Komodo orchestration core
- Development and production workloads
- High resource allocation

**Services**:
- Docker runtime with Komodo Core
- Application containers (homepage, karaoke, termix)
- Infrastructure services (n8n, semaphore)
- Monitoring hub (Dozzle)
- Development tooling

**Resource Profile**:
- High CPU and memory allocation
- Large storage volumes
- Network-intensive workloads
- Mission-critical services

**Access**:
- Tailscale: 100.102.0.70:2024
- Ansible inventory: `hercules`

**Related**: [[Docker/Host Fleet]], [[Docker/Komodo]]

---

#### codewizard
```yaml
Hostname: codewizard.int.badger-dev.com
Type: Proxmox VM
Hardware: proxmox_vm
CPU: amd64
Location: amethyst
Tailscale IP: 100.102.0.140
SSH Port: 2024
Status: Development
```

**Purpose**: Development and testing environment with isolation from production.

**Key Features**:
- Isolated development environment
- Testing and staging area
- CI/CD integration
- Feature development

**Services**:
- Development Docker runtime
- Testing environments
- Staging applications
- Development tooling

**Resource Profile**:
- Medium resource allocation
- Development-optimized configurations
- Snapshot-based rollbacks
- Feature branch deployments

**Access**:
- Tailscale: 100.102.0.140:2024
- Ansible inventory: `codewizard`

---

### LXC Containers

#### postgres-svr
```yaml
Hostname: postgres-svr.int.badger-dev.com
Type: Proxmox LXC
Hardware: proxmox_lxc
Location: amethyst
Status: Production - Critical
```

**Purpose**: Centralized PostgreSQL database server for all infrastructure services.

**Key Features**:
- Dedicated database server
- High-performance storage
- Automated backups
- Point-in-time recovery

**Services**:
- PostgreSQL database cluster
- Database backups and replication
- Performance monitoring
- Connection pooling

**Database Services**:
- n8n workflow automation
- NetBox infrastructure documentation
- Immich photo management
- Paperless-ngx document management
- Other PostgreSQL-dependent services

**Resource Profile**:
- Optimized for database workloads
- High I/O performance storage
- Memory-optimized configuration
- Regular backup schedules

**Access**:
- Internal network access only
- Port: 5432 (PostgreSQL)
- Ansible inventory: `postgres-svr`

**Backup Strategy**:
- Continuous WAL archiving
- Daily full backups
- Point-in-time recovery capability
- Offsite backup replication

---

#### homeassistant
```yaml
Hostname: homeassistant.int.badger-dev.com
Type: Proxmox LXC
Hardware: proxmox_lxc
Location: amethyst
Status: Production
```

**Purpose**: Home Assistant smart home automation controller.

**Key Features**:
- Smart home device integration
- Automation workflows
- Voice assistant integration
- Mobile application access

**Services**:
- Home Assistant server
- Zigbee device coordination
- Voice processing
- Mobile app backend

**Integration**:
- Zigbee devices
- Voice assistants
- Mobile applications
- IoT device management

**Access**:
- Internal network access
- Mobile app via Tailscale
- Ansible inventory: `homeassistant`

---

#### pihole-backup
```yaml
Hostname: pihole-backup.int.badger-dev.com
Type: Proxmox LXC
Hardware: proxmox_lxc
Location: amethyst
Status: Production
```

**Purpose**: Backup DNS server and Pi-hole redundancy.

**Key Features**:
- DNS resolution backup
- Ad-blocking redundancy
- DHCP failover support
- Network protection

**Services**:
- Pi-hole DNS server
- DHCP server (backup)
- Network protection
- Ad blocking

**Role in Network**:
- Secondary DNS server
- Redundant ad-blocking
- Network security
- Performance optimization

**Access**:
- Internal network access
- DNS: Port 53
- Admin interface: Port 8080
- Ansible inventory: `pihole-backup`

---

### Physical Hardware

#### apollo
```yaml
Hostname: apollo.int.badger-dev.com
Type: Raspberry Pi 4 Model B
CPU: ARM64 (bcm2711)
Memory: 8GB
Storage: 128GB MicroSD + 256GB USB SSD
Location: amethyst
Status: Production - Critical
```

**Purpose**: Central monitoring hub and network observability platform.

**Key Features**:
- Infrastructure monitoring hub (Beszel)
- Network device discovery (NetAlertX)
- Proxmox monitoring (Pulse)
- Service uptime monitoring (Uptime Kuma)

**Services**:
- Beszel monitoring hub (port 8090)
- NetAlertX network monitoring
- Pulse Proxmox monitoring
- Uptime Kuma service monitoring
- Dozzle log agent
- Beszel agent (local)
- Diun image monitoring
- Newt tunnel agent

**Storage Configuration**:
```bash
MicroSD (128GB): OS and applications
USB SSD (256GB): 
  ├── /data/beszel     # Monitoring data and metrics
  ├── /data/netalertx  # Network device database
  └── /data/logs       # Local logs and cache
```

**Network Configuration**:
- Primary: Gigabit Ethernet
- Tailscale: 100.102.0.50
- VPN connectivity for remote access

**Power Management**:
- USB-C power supply (15W)
- UPS protection via network UPS
- Graceful shutdown capability

**Access**:
- Tailscale: 100.102.0.50:2024
- SSH: 192.168.1.50:2024 (local network)
- Ansible inventory: `apollo`

**Monitoring Role**:
- Collects metrics from all infrastructure components
- Provides centralized dashboards
- Sends alerts for critical issues
- Maintains historical performance data

**Related**: [[Monitoring/Beszel]], [[Network/Network Topology]]

---

#### ipa1
```yaml
Hostname: ipa1.int.badger-dev.com
Type: Raspberry Pi 4 Model B
CPU: ARM64 (bcm2711)
Memory: 8GB
Storage: 256GB USB SSD (USB boot)
Location: amethyst
Status: Production - CRITICAL ⚠️
```

**Purpose**: FreeIPA identity management server - single source of truth for authentication.

**Critical Infrastructure Warning**: 
**SPOF (Single Point of Failure)** - This host is critical for all infrastructure authentication. Loss of this server will break access to all services.

**Key Features**:
- FreeIPA identity and authentication
- LDAP directory service
- Kerberos KDC
- Dogtag Certificate Authority
- BIND DNS integration
- User and group management

**Services**:
- FreeIPA server (web UI, LDAP, Kerberos)
- 389 Directory Server
- Dogtag Certificate Authority
- BIND DNS server
- Apache HTTP Server

**Storage Configuration**:
```bash
USB SSD (256GB):
  ├── /var/lib/dirsrv     # 389 Directory Server data
  ├── /var/lib/ipa        # FreeIPA configuration and data
  ├── /var/kerberos       # Kerberos database and tickets
  ├── /var/lib/pki        # Certificate authority data
  └── OS                  # RHEL/Fedora-based FreeIPA OS
```

**Network Configuration**:
- Primary: Gigabit Ethernet
- Static IP: 10.2.0.53
- Services: LDAP (389), LDAPS (636), Kerberos (88), HTTP (443)
- Tailscale: 100.102.0.53

**Authentication Services**:
- LDAP authentication for all services
- Kerberos ticket-based authentication
- SSH key management
- User group and role management
- Certificate management

**Dependencies**:
All hosts depend on this server for:
- User authentication
- SSH access via LDAP
- Service authentication
- DNS resolution
- Certificate validation

**Access**:
- Tailscale: 100.102.0.53:2024
- Web UI: https://ipa1.int.badger-dev.com
- Ansible inventory: `ipa1`

**High Availability Status**:
- **Current**: Single instance (no replica)
- **Risk**: Complete authentication failure if this host fails
- **Recommendation**: Deploy ipa2 replica on Proxmox LXC
- **Backup**: Daily ipa-backup with offsite storage

**Backup Strategy**:
- Daily automated backups via ipa-backup utility
- Offsite backup to secure storage
- Regular backup verification
- Disaster recovery testing

**Maintenance Requirements**:
- Daily health checks
- Weekly backup verification
- Monthly security updates
- Quarterly disaster recovery testing

**Related**: [[Security/FreeIPA]], [[Infrastructure/Hardware]]

---

#### sentinel
```yaml
Hostname: sentinel.int.badger-dev.com
Type: Raspberry Pi 4 Model B
CPU: ARM64 (bcm2711)
Memory: 4GB
Storage: 64GB MicroSD card
Location: amethyst
Status: Production
```

**Purpose**: General-purpose service host and ARM64 development environment.

**Key Features**:
- ARM64 workload hosting
- Development and testing
- Service redundancy
- Edge computing capabilities

**Services**:
- Docker runtime for ARM64 containers
- Development environments
- Testing services
- Backup application hosting

**Storage Configuration**:
```bash
MicroSD (64GB): 
  ├── OS and Docker
  ├── Application data
  └── Development files
```

**Resource Profile**:
- ARM64 architecture for ARM-specific workloads
- 4GB RAM suitable for moderate workloads
- MicroSD storage (replace annually)
- Docker container hosting

**Development Role**:
- ARM64 application testing
- Container development
- CI/CD pipeline testing
- Feature validation

**Access**:
- Tailscale: 100.102.0.51:2024
- SSH: 192.168.1.51:2024 (local network)
- Ansible inventory: `sentinel`

**Use Cases**:
- ARM64 application hosting
- Development environment isolation
- Testing and validation
- Service redundancy

**Maintenance Notes**:
- Monitor MicroSD card health
- Regular system updates
- Backup critical configurations
- Performance monitoring

---

## Cloud Infrastructure

### Oracle Cloud Infrastructure (OCI)

#### oci-dmz
```yaml
Hostname: oci-dmz.badger-dev.com
Type: Oracle Cloud VM
Location: Oracle Cloud (us-ashburn-1)
Public IP: Dynamic (via DNS)
Tailscale IP: 100.102.0.30
Status: Production - Critical
```

**Purpose**: DMZ and edge security host for public-facing services.

**Key Features**:
- Public internet exposure
- Reverse proxy termination
- Security filtering
- Edge computing services

**Services**:
- Pangolin reverse proxy stack
- CrowdSec security engine
- PocketID authentication provider
- Dockflare DNS automation
- WireGuard VPN server
- Dozzle log agent
- Beszel agent
- Newt tunnel agent
- Diun image monitoring

**Security Architecture**:
```yaml
Internet → Pangolin → Internal Services
         ↘ CrowdSec (IP blocking)
         ↘ PocketID (Authentication)
```

**Network Services**:
- Pangolin (Traefik + Gerbil): Reverse proxy with tunneling
- CrowdSec: Security and IP reputation filtering
- WireGuard: Site-to-site VPN connectivity
- Dockflare: Automated Cloudflare DNS

**Authentication**:
- PocketID: OIDC/OAuth2 identity provider
- LDAP backend: FreeIPA at ipa1.int.badger-dev.com
- Multi-factor authentication support

**Access**:
- Public: https://quartz.badger-dev.com (Pangolin management)
- Tailscale: 100.102.0.30:2024
- Ansible inventory: `oci-dmz`

**Security Features**:
- Automated IP blocking via CrowdSec
- Rate limiting and DDoS protection
- SSL/TLS termination
- Web Application Firewall rules
- Geographic blocking capability

**Related**: [[Security/Security MOC]], [[Network/Network Topology]]

---

#### oci-docker
```yaml
Hostname: oci-docker.badger-dev.com
Type: Oracle Cloud VM (ARM64)
Location: Oracle Cloud (us-ashburn-1)
Public IP: Dynamic (via DNS)
Tailscale IP: 100.102.0.40
Status: Production
```

**Purpose**: Cloud-native application hosting with ARM64 optimization.

**Key Features**:
- ARM64 cloud infrastructure
- Public-facing application hosting
- Geographic distribution
- High availability services

**Services**:
- User applications (mealie, it-tools, stirling-pdf)
- AI/ML services (open-webui, openhands, qdrant)
- Development tools (omni-tools)
- Deployment tools (dock-dploy)
- Karaoke mirror (karakeep)
- Monitoring agents (Dozzle, Beszel, Diun)
- Newt tunnel agent

**Application Categories**:
```yaml
User Applications:
  - mealie: Recipe management
  - it-tools: Developer utilities
  - omni-tools: Additional utilities
  - stirling-pdf: PDF processing

AI/ML Services:
  - open-webui: LLM chat interface
  - openhands: AI coding assistant
  - qdrant: Vector database
  - dock-dploy: Deployment dashboard

Development Tools:
  - karakeep: Karaoke library (mirror)
  - Monitoring and logging agents
```

**Resource Profile**:
- ARM64 architecture for cost optimization
- Cloud storage integration
- Scalable compute resources
- High availability zones

**Access**:
- Public: Applications via Pangolin proxy
- Tailscale: 100.102.0.40:2024
- Ansible inventory: `oci-docker`

**Cloud Advantages**:
- Geographic distribution
- Managed infrastructure
- Automatic scaling
- High availability
- Backup and disaster recovery

**Related**: [[Docker/Stacks Inventory]], [[Services/Application Catalog]]

---

#### meade
```yaml
Hostname: meade.badger-dev.com
Type: Raspberry Pi 4 Model B (Remote Edge)
CPU: ARM64 (bcm2711)
Memory: 8GB
Storage: 128GB MicroSD card
Location: Remote edge (Meade residence)
Tailscale IP: 100.102.0.60
Status: Production
```

**Purpose**: Remote edge computing and monitoring host.

**Key Features**:
- Remote geographic distribution
- Edge computing capabilities
- Network monitoring
- Disaster recovery testing

**Services**:
- Docker runtime for edge services
- Beszel monitoring agent
- Dozzle log agent
- WireGuard VPN server
- Newt tunnel agent
- Diun image monitoring
- Edge-specific applications

**Edge Computing Role**:
- Geographic distribution testing
- Remote service availability
- Network performance monitoring
- Edge application deployment

**Network Configuration**:
- Residential ISP connection
- Tailscale VPN for management
- WireGuard for site-to-site VPN
- Dynamic DNS support

**Access**:
- Tailscale: 100.102.0.60:2024
- Ansible inventory: `meade`

**Remote Management**:
- Complete Tailscale VPN integration
- Secure remote access
- Automated monitoring and alerts
- Remote troubleshooting capabilities

**Edge Use Cases**:
- Geographic redundancy testing
- Remote service deployment
- Network performance monitoring
- Disaster recovery validation
- Edge computing experiments

**Considerations**:
- Limited physical access for maintenance
- Dependent on residential internet reliability
- Remote troubleshooting procedures required
- Backup power considerations

**Related**: [[Network/Network Topology]], [[Monitoring/Monitoring MOC]]

---

## Host Relationships and Dependencies

### Authentication Dependency Chain
```
All Services → FreeIPA (ipa1) → LDAP Authentication
                ↓
        User Authentication → SSH Access → Service Access
```

### Monitoring Architecture
```
apollo (Hub) ← All Agents (hercules, oci-dmz, oci-docker, synology, meade, codewizard)
     ↓
Infrastructure Metrics → Alerting → Dashboards
```

### Application Access Flow
```
Internet → oci-dmz (Pangolin) → Internal Services → Authentication (FreeIPA) → Applications
                ↓
           Security (CrowdSec) → Authorization (PocketID) → Load Balancing
```

### Data Storage Dependencies
```
Applications → postgres-svr (Database) → Synology NAS (Backups)
                ↓
            Cloud Storage (B2) → Offsite Replication
```

---

## Host Specifications Summary

### Compute Resources
| Host | CPU | Memory | Storage | Primary Use |
|------|-----|--------|---------|-------------|
| genesis | amd64 | 4GB | 64GB | Management |
| hercules | amd64 | 16GB | 256GB | Docker Production |
| codewizard | amd64 | 8GB | 128GB | Development |
| postgres-svr | amd64 | 8GB | 256GB | Database |
| homeassistant | amd64 | 2GB | 32GB | Smart Home |
| pihole-backup | amd64 | 1GB | 16GB | DNS Backup |
| apollo | arm64 | 8GB | 384GB | Monitoring |
| ipa1 | arm64 | 8GB | 256GB | Authentication |
| sentinel | arm64 | 4GB | 64GB | Services |
| oci-dmz | amd64 | 4GB | 100GB | DMZ Services |
| oci-docker | arm64 | 4GB | 100GB | Cloud Apps |
| meade | arm64 | 8GB | 128GB | Edge Computing |

### Network Configuration
| Host | Internal IP | Tailscale IP | SSH Port | Public Access |
|------|-------------|--------------|----------|---------------|
| genesis | 10.2.0.100 | 100.102.0.100 | 2024 | No |
| hercules | 10.2.0.70 | 100.102.0.70 | 2024 | No |
| codewizard | 10.2.0.140 | 100.102.0.140 | 2024 | No |
| apollo | 10.2.0.50 | 100.102.0.50 | 2024 | No |
| ipa1 | 10.2.0.53 | 100.102.0.53 | 2024 | No |
| sentinel | 10.2.0.51 | 100.102.0.51 | 2024 | No |
| oci-dmz | Dynamic | 100.102.0.30 | 2024 | Yes |
| oci-docker | Dynamic | 100.102.0.40 | 2024 | Yes |
| meade | Dynamic | 100.102.0.60 | 2024 | No |

### Service Categories
| Category | Hosts | Purpose |
|----------|-------|---------|
| **Management** | genesis | System administration |
| **Core Services** | hercules, postgres-svr, ipa1 | Essential infrastructure |
| **Development** | codewizard, sentinel | Development and testing |
| **User Services** | homeassistant, pihole-backup | User-facing applications |
| **Monitoring** | apollo | Infrastructure monitoring |
| **Cloud/Edge** | oci-dmz, oci-docker, meade | Distributed infrastructure |

---

## Access and Authentication

### SSH Access Pattern
```bash
# Standard access via Tailscale
ssh -p 2024 dan@<tailscale-ip>

# Ansible automation access
ansible <hostname> -m ping

# Emergency access (local network)
ssh -p 2024 dan@<internal-ip>
```

### Authentication Methods
1. **SSH Keys**: Primary authentication method
2. **FreeIPA LDAP**: Centralized user management
3. **Tailscale**: VPN-based secure access
4. **Emergency**: Local console access

### User Access Levels
- **Administrator**: Full access to all hosts
- **Service**: Limited service-specific accounts
- **Monitoring**: Read-only access for monitoring systems
- **Backup**: Access for backup operations

---

## Host Maintenance

### Update Strategy
- **Rolling Updates**: Non-critical hosts updated first
- **Maintenance Windows**: Scheduled for minimal impact
- **Backup Verification**: Pre-update backup verification
- **Rollback Planning**: Quick rollback procedures

### Monitoring and Health
- **Automated Alerts**: Beszel monitoring for all hosts
- **Performance Metrics**: Resource utilization tracking
- **Security Monitoring**: Log aggregation and analysis
- **Backup Status**: Continuous backup verification

### Disaster Recovery
- **Single Points of Failure**: Identified and documented
- **Recovery Procedures**: Step-by-step recovery guides
- **Backup Verification**: Regular testing and validation
- **Documentation**: Always updated after changes

---

## Related Documentation

- [[Infrastructure MOC]] - Infrastructure overview and management
- [[Infrastructure/Hardware]] - Physical hardware specifications
- [[Security/FreeIPA]] - Identity management and authentication
- [[Docker/Host Fleet]] - Docker host topology and management
- [[Network/Network Topology]] - Network architecture and connectivity
- [[Monitoring/Monitoring MOC]] - Monitoring infrastructure and alerting
- [[Backups/Backups MOC]] - Backup strategies and procedures

---

**Last Updated**: 2025-11-27
**Maintained By**: Infrastructure Team
**Review Schedule**: Monthly or on infrastructure changes
**Next Review**: 2025-12-27