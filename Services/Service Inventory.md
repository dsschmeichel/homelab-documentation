---
title: Service Inventory
tags: [services, inventory, applications, catalog]
created: 2025-11-27
updated: 2025-11-27
---

# Service Inventory

Complete catalog of all services running in the Badger Development homelab infrastructure. This serves as the master index of deployed applications, infrastructure services, and their operational status.

## Service Categories

### Quick Overview

| Category | Service Count | Primary Hosts | Purpose |
|----------|---------------|---------------|---------|
| **Applications** | 15 unique | All hosts | User-facing services |
| **Infrastructure** | 11 unique | hercules, apollo, oci-dmz | Platform services |
| **Monitoring** | 9 unique | apollo, hercules | Observability |
| **Total** | **35 unique** | **Multiple hosts** | Complete infrastructure |

**Note**: Services are deployed with redundancy across hosts (agents, tunnel endpoints), resulting in 53+ total service instances.

---

## Application Services (15)

### Productivity & Content Management

#### Homepage
- **Host**: hercules
- **Access**: https://homepage.badger-dev.com
- **Purpose**: Service dashboard and directory
- **Technology**: Docker, Go
- **Status**: 🟢 Production

#### Immich
- **Host**: synology-nas
- **Access**: https://immich.badger-dev.com
- **Purpose**: Photo and video management
- **Technology**: Docker, Node.js, PostgreSQL
- **Storage**: NAS-backed media library
- **Status**: 🟢 Production

#### Paperless-ngx
- **Host**: synology-nas
- **Access**: https://paperless.badger-dev.com
- **Purpose**: Document management with OCR
- **Technology**: Docker, Python, PostgreSQL
- **Storage**: NAS-backed document storage
- **Status**: 🟢 Production

#### Mealie
- **Host**: oci-docker
- **Access**: https://mealie.badger-dev.com
- **Purpose**: Recipe management and meal planning
- **Technology**: Docker, Python, SQLite
- **Status**: 🟢 Production

### Developer Tools & Utilities

#### IT-Tools
- **Host**: oci-docker
- **Access**: https://tools.badger-dev.com
- **Purpose**: Developer utility collection
- **Technology**: Docker, Vue.js
- **Status**: 🟢 Production

#### Omni-Tools
- **Host**: oci-docker
- **Access**: Internal
- **Purpose**: Additional developer utilities
- **Technology**: Docker, Web-based
- **Status**: 🟢 Production

#### Stirling-PDF
- **Host**: oci-docker
- **Access**: https://pdf.badger-dev.com
- **Purpose**: PDF manipulation toolkit
- **Technology**: Docker, Java-based
- **Status**: 🟢 Production

#### Termix
- **Host**: hercules
- **Access**: https://term.badger-dev.com
- **Purpose**: Web-based SSH terminal
- **Technology**: Docker, Web-based SSH
- **Status**: 🟢 Production

### AI & Machine Learning

#### Open-WebUI
- **Host**: oci-docker
- **Access**: https://chat.badger-dev.com
- **Purpose**: LLM chat interface
- **Technology**: Docker, Python, Web UI
- **Authentication**: PocketID OIDC
- **Status**: 🟢 Production

#### OpenHands
- **Host**: oci-docker
- **Access**: Internal
- **Purpose**: AI-powered coding assistant
- **Technology**: Docker, AI/ML framework
- **Status**: 🟢 Production

#### Qdrant
- **Host**: oci-docker
- **Access**: API-only
- **Purpose**: Vector database for AI applications
- **Technology**: Docker, Rust-based
- **Usage**: Open-WebUI semantic search
- **Status**: 🟢 Production

### Media & Entertainment

#### Karaoke (Karakeep)
- **Hosts**: hercules, oci-docker
- **Access**: Internal
- **Purpose**: Karaoke library management
- **Technology**: Docker, Custom application
- **Deployment**: Primary + mirror
- **Status**: 🟢 Production

### Infrastructure Management

#### Dock-Dploy
- **Host**: oci-docker
- **Access**: Internal
- **Purpose**: Deployment dashboard
- **Technology**: Docker, Custom
- **Status**: 🟢 Production

---

## Infrastructure Services (11)

### Orchestration & Management

#### Komodo Core
- **Host**: hercules
- **Access**: https://komodo.badger-dev.com
- **Purpose**: GitOps orchestration platform
- **Technology**: Docker, MongoDB
- **Role**: Central deployment manager
- **Status**: 🟢 Critical

#### Semaphore
- **Host**: hercules
- **Access**: https://semaphore.badger-dev.com
- **Purpose**: Ansible automation web UI
- **Technology**: Docker, MySQL
- **Role**: Ansible playbook execution
- **Status**: 🟢 Production

#### N8N
- **Host**: hercules
- **Access**: https://n8n.badger-dev.com
- **Purpose**: Workflow automation
- **Technology**: Docker, Node.js, PostgreSQL
- **Role**: Business process automation
- **Status**: 🟢 Production

### Networking & Security

#### Pangolin
- **Host**: oci-dmz
- **Access**: https://quartz.badger-dev.com
- **Purpose**: Reverse proxy with tunneling
- **Technology**: Docker, Traefik, WireGuard
- **Components**: 
  - Pangolin: Configuration management
  - Gerbil: WireGuard tunnel termination
  - Traefik: Reverse proxy
  - Middleware Manager: Dynamic rules
- **Status**: 🟢 Critical

#### PocketID
- **Host**: oci-dmz
- **Access**: https://idp.badger-dev.com
- **Purpose**: OIDC/OAuth2 identity provider
- **Technology**: Docker, Go
- **Role**: Modern SSO bridge to FreeIPA
- **Status**: 🟢 Critical

#### CrowdSec
- **Host**: oci-dmz
- **Access**: API-only
- **Purpose**: Security engine and intrusion prevention
- **Technology**: Docker, Go
- **Role**: IP blocking and threat intelligence
- **Status**: 🟢 Critical

#### Dockflare
- **Host**: oci-dmz
- **Access**: Background service
- **Purpose**: Cloudflare DNS automation
- **Technology**: Docker, Go
- **Role**: Automated DNS record management
- **Status**: 🟢 Production

#### WireGuard
- **Hosts**: oci-dmz, meade
- **Access**: VPN-only
- **Purpose**: Site-to-site VPN tunnels
- **Technology**: Docker, Linux
- **Role**: Secure connectivity
- **Status**: 🟢 Production

#### Newt (7 instances)
- **Hosts**: ALL hosts (hercules, apollo, oci-dmz, oci-docker, synology-nas, meade, codewizard)
- **Access**: Background service
- **Purpose**: Pangolin tunnel agents
- **Technology**: Docker, WireGuard
- **Role**: Internal service tunneling to Pangolin
- **Status**: 🟢 Critical (7 instances)

### Database & Identity

#### PostgreSQL
- **Host**: postgres-svr (LXC, not Docker)
- **Access**: Internal only
- **Purpose**: Centralized database server
- **Technology**: Native PostgreSQL
- **Role**: Application data storage
- **Status**: 🟢 Critical

#### FreeIPA
- **Host**: ipa1
- **Access**: https://ipa1.int.badger-dev.com
- **Purpose**: Identity and authentication management
- **Technology**: Native Linux, 389 Directory, Kerberos
- **Role**: Central authentication authority
- **Status**: 🟢 Critical (SPOF)

---

## Monitoring Services (9)

### Infrastructure Monitoring

#### Beszel
- **Host**: apollo
- **Access**: https://beszel.badger-dev.com
- **Purpose**: Infrastructure monitoring hub
- **Technology**: Docker, Go
- **Role**: Central metrics collection
- **Agents**: 6 Beszel agents deployed
- **Status**: 🟢 Critical

#### Beszel-Agent (6 instances)
- **Hosts**: hercules, oci-dmz, oci-docker, synology-nas, meade, codewizard
- **Access**: Background service
- **Purpose**: System and container metrics collection
- **Technology**: Docker, Go
- **Role**: Metrics reporting to Beszel hub
- **Status**: 🟢 Production

#### Pulse
- **Host**: apollo
- **Access**: https://pulse.badger-dev.com
- **Purpose**: Proxmox hypervisor monitoring
- **Technology**: Docker, Custom
- **Role**: VM/LXC resource monitoring
- **Status**: 🟢 Production

#### Uptime Kuma
- **Host**: apollo
- **Access**: https://status.badger-dev.com
- **Purpose**: Service uptime monitoring
- **Technology**: Docker, Node.js, SQLite
- **Role**: External service availability checks
- **Status**: 🟢 Production

### Log Management

#### Dozzle
- **Host**: hercules
- **Access**: https://logs.badger-dev.com
- **Purpose**: Docker log aggregation hub
- **Technology**: Docker, Go
- **Role**: Central log streaming and search
- **Agents**: 6 Dozzle agents deployed
- **Status**: 🟢 Critical

#### Dozzle-Agent (6 instances)
- **Hosts**: hercules, apollo, oci-dmz, oci-docker, synology-nas, meade
- **Access**: Background service
- **Purpose**: Container log collection
- **Technology**: Docker, Go
- **Role**: Log streaming to Dozzle hub
- **Status**: 🟢 Production

### Network & Image Monitoring

#### NetAlertX
- **Host**: apollo
- **Access**: https://netalertx.badger-dev.com
- **Purpose**: Network device discovery and tracking
- **Technology**: Docker, Python
- **Role**: Network security and inventory
- **Status**: 🟢 Production

#### Diun (7 instances)
- **Hosts**: ALL Docker hosts
- **Access**: Background service
- **Purpose**: Docker image update monitoring
- **Technology**: Docker, Go
- **Role**: Update notifications for containers
- **Status**: 🟢 Production

---

## Service Architecture Patterns

### Hub-Agent Architectures

**Beszel Monitoring**:
- **Hub**: apollo (central metrics collection)
- **Agents**: 6 hosts reporting system and container metrics
- **Protocol**: SSH-based secure communication

**Dozzle Logging**:
- **Hub**: hercules (central log aggregation)
- **Agents**: 6 hosts streaming container logs
- **Protocol**: Real-time log streaming over network

**Pangolin/Newt Tunneling**:
- **Hub**: oci-dmz (Pangolin + Gerbil)
- **Agents**: 7 hosts with secure WireGuard tunnels
- **Protocol**: WireGuard encrypted tunnels

---

### Authentication Integration

**FreeIPA LDAP Integration**:
- Used by: phpipam, semaphore, n8n, paperless-ngx, immich
- Provides: Centralized user management, SSH key auth
- Backend: 389 Directory Server

**PocketID OIDC Integration**:
- Used by: open-webui, komodo, beszel, dozzle
- Provides: Modern OAuth2/OIDC SSO
- Backend: LDAP bridge to FreeIPA

---

### External Access Patterns

**Public-Facing Services** (via Pangolin/Tailscale):
- Homepage, Immich, Paperless-ngx, Mealie
- IT-Tools, Stirling-PDF, Open-WebUI
- Komodo, Semaphore, Beszel, Dozzle

**Internal-Only Services**:
- PostgreSQL (database only)
- FreeIPA (internal authentication)
- Monitoring agents and internal APIs

**VPN-Required Access**:
- Internal services via Tailscale
- Management interfaces
- Debug and troubleshooting tools

---

## Service Dependencies

### Critical Dependencies

**Authentication Dependency Chain**:
```
All Services → FreeIPA (ipa1) → LDAP Authentication → User Access
All SSO Services → PocketID → FreeIPA → LDAP → OIDC
```

**Infrastructure Dependencies**:
```
Applications → Docker → Komodo (deployment) → GitOps
Services → FreeIPA → Authentication → LDAP
Monitoring → Agents → Services → Metrics Collection
```

**Storage Dependencies**:
```
Applications → PostgreSQL → Data Storage → Backups (Kopia)
Files → Synology NAS → NFS/SMB → User Access
```

---

## Service Status Matrix

| Service | Category | Host | Access Type | Authentication | Status |
|---------|----------|------|-------------|----------------|--------|
| Komodo | Infrastructure | hercules | Public | PocketID | 🟢 Critical |
| Pangolin | Infrastructure | oci-dmz | Public | Internal | 🟢 Critical |
| FreeIPA | Infrastructure | ipa1 | Internal | LDAP | 🟢 Critical (SPOF) |
| Beszel | Monitoring | apollo | Public | PocketID | 🟢 Critical |
| Dozzle | Monitoring | hercules | Public | PocketID | 🟢 Critical |
| Homepage | Application | hercules | Public | None | 🟢 Production |
| Immich | Application | synology-nas | Public | LDAP | 🟢 Production |
| Open-WebUI | Application | oci-docker | Public | PocketID | 🟢 Production |
| PostgreSQL | Infrastructure | postgres-svr | Internal | LDAP | 🟢 Critical |

---

## Service Deployment Methods

### GitOps via Komodo
- **Primary Method**: Komodo polls GitHub repository
- **Sync Files**: `stacks-*.toml` files define per-host deployments
- **Auto-Deployment**: Changes pushed to GitHub auto-deploy
- **Configuration**: Environment-specific overrides

### Ansible Configuration
- **System Configuration**: Ansible playbooks for host setup
- **Application Integration**: Some services configured via Ansible
- **Identity Management**: FreeIPA setup and user enrollment

### Manual Configuration
- **Legacy Services**: Some services still require manual setup
- **Emergency Changes**: Quick fixes applied manually
- **Testing**: New services often start manually before GitOps

---

## Service Maintenance

### Update Strategies

**Automated Updates**:
- Diun monitors Docker images for updates
- Komodo automatically deploys stack updates
- Security patches via Ansible schedules

**Manual Updates**:
- Major version upgrades planned and tested
- Configuration changes require careful coordination
- Database migrations and data preservation

**Rollback Procedures**:
- Git-based rollback for Komodo deployments
- Database backups for application data
- Configuration versioning and testing

---

### Monitoring and Health

**Health Checks**:
- Container health checks in Docker Compose
- External service monitoring via Uptime Kuma
- Internal metrics collection via Beszel
- Log aggregation and analysis via Dozzle

**Alerting**:
- Critical service failures via ntfy notifications
- Performance degradation alerts
- Security events via CrowdSec
- Resource utilization monitoring

---

## Service Scaling

### Current Capacity

**Compute Resources**:
- Docker hosts: 7 hosts across 3 locations
- Total container instances: 53+
- CPU utilization: Average 30-40%
- Memory utilization: Average 50-60%

**Storage Resources**:
- Primary storage: Synology NAS (22TB usable)
- Database storage: postgres-svr (dedicated)
- Backup storage: Cloud replication

**Network Resources**:
- Internal network: 10.2.0.0/24 (1Gbps)
- VPN mesh: Tailscale (100.x.x.x/16)
- External bandwidth: ISP connection limits

### Scaling Plans

**Short Term**:
- Add monitoring capacity (if needed)
- Optimize resource allocation
- Implement service redundancy

**Medium Term**:
- Add FreeIPA replica (high availability)
- Expand monitoring capabilities
- Service geographic distribution

**Long Term**:
- Container orchestration upgrades
- Multi-region deployment
- Advanced service mesh

---

## Related Documentation

- [[Docker/Stacks Inventory]] - Detailed stack configurations
- [[Infrastructure/Hosts Inventory]] - Host specifications and locations
- [[Security/FreeIPA]] - Identity management configuration
- [[Docker/Komodo]] - Orchestration platform details
- [[Monitoring/Monitoring MOC]] - Monitoring infrastructure
- [[Network/Network Topology]] - Network architecture and access

---

**Last Updated**: 2025-11-27
**Service Count**: 35 unique services, 53+ total instances
**Maintained By**: Infrastructure Team
**Review Schedule**: Monthly or on service changes
**Next Review**: 2025-12-27