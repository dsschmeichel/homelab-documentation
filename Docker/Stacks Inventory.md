---
tags:
  - docker
  - stacks
  - inventory
  - services
aliases:
  - Docker Stacks
  - Service Inventory
created: 2024-11-24
updated: 2024-11-24
---

# Docker Stacks Inventory

Complete inventory of all 36 Docker Compose stacks deployed across the Badger Development homelab infrastructure.

## Overview

| Category | Stacks | Total Instances | Purpose |
|----------|--------|-----------------|---------|
| **Applications** | 15 | 15 | User-facing services and productivity tools |
| **Infrastructure** | 11 | 18 | Platform services (includes 7 Newt instances) |
| **Monitoring** | 9 | 20 | Observability and alerting (includes 6 agents each for Beszel/Dozzle) |
| **Total** | **35 unique** | **53 instances** | Complete container platform |

**Note**: Some stacks are deployed multiple times with host-specific configuration (agents, tunnel endpoints).

## Applications

### homepage
**Host**: hercules
**Purpose**: Service dashboard and directory
**Image**: `ghcr.io/gethomepage/homepage:v1.6.1`
**Access**: https://homepage.badger-dev.com

Central dashboard providing quick access to all homelab services. Displays service status, integrates with Komodo API for deployment info, and provides bookmark management.

**Key Features**:
- Service catalog with health checks
- Docker container discovery via socket mount
- Integration with Komodo for deployment status
- Customizable layouts and widgets
- Bookmark management

**Configuration**:
- Config directory: `/home/docker/stacks/applications/homepage/config`
- Docker socket mounted read-only
- Pangolin reverse proxy integration

---

### immich
**Host**: synology-nas
**Purpose**: Self-hosted photo and video management platform
**Image**: Multiple (immich-server, immich-machine-learning, postgres, redis)
**Access**: https://immich.badger-dev.com

Google Photos alternative with ML-powered facial recognition, object detection, and automatic photo organization. Backed by NAS storage for large media libraries.

**Key Features**:
- Facial recognition and photo tagging
- Mobile app sync (iOS/Android)
- Shared albums and collaborative features
- Machine learning for object/scene detection
- Video transcoding and thumbnail generation

**Configuration**:
- Storage: Synology NAS volumes
- Database: Dedicated PostgreSQL instance
- ML: TensorFlow-based processing
- LDAP: FreeIPA integration

---

### paperless-ngx
**Host**: synology-nas
**Purpose**: Document management system with OCR
**Image**: `ghcr.io/paperless-ngx/paperless-ngx`
**Access**: https://paperless.badger-dev.com

Scan, index, and archive physical documents with full-text search. Automatic document classification and tagging using ML.

**Key Features**:
- OCR with Tesseract
- Automatic document classification
- Full-text search across scanned documents
- Mobile document scanning app
- Email import via IMAP
- Workflow automation with tags/correspondents

**Configuration**:
- Storage: NAS-backed document storage
- Redis: Task queue for async processing
- PostgreSQL: Metadata and search index
- LDAP: FreeIPA authentication

---

### ntfy
**Host**: oci-dmz (commented out in syncs)
**Purpose**: Push notification service
**Image**: `binwiederhier/ntfy`
**Access**: https://ntfy.badger-dev.com

Simple HTTP-based pub/sub notification service. Send push notifications to phone/desktop from scripts, cron jobs, and monitoring systems.

**Key Features**:
- Simple HTTP pub/sub
- Mobile apps (iOS/Android)
- Web push notifications
- Message attachments and actions
- Access control and authentication

**Configuration**:
- Currently disabled in oci-dmz deployment
- Can be re-enabled by uncommenting in `syncs/stacks-oci-dmz.toml`

---

### mealie
**Host**: oci-docker
**Purpose**: Recipe management and meal planning
**Image**: `ghcr.io/mealie-recipes/mealie`
**Access**: https://mealie.badger-dev.com

Self-hosted recipe manager with meal planning, shopping lists, and automatic recipe import from websites.

**Key Features**:
- Recipe import from URLs
- Meal planning calendar
- Automatic shopping list generation
- Recipe scaling and unit conversion
- Nutritional information tracking

**Configuration**:
- Database: SQLite (consider PostgreSQL for multi-user)
- LDAP: FreeIPA integration planned

---

### karakeep
**Host**: hercules, oci-docker
**Purpose**: Karaoke library manager
**Image**: Custom/community
**Access**: Internal

Organize and serve karaoke track libraries. Manages metadata, search, and playback of karaoke files.

**Key Features**:
- Karaoke file indexing
- Search by title/artist
- Playback integration
- Library organization

**Configuration**:
- Deployed on both hercules (primary) and oci-docker (mirror)
- Media storage on shared volumes

---

### it-tools
**Host**: oci-docker
**Purpose**: Collection of handy developer utilities
**Image**: `corentinth/it-tools`
**Access**: https://tools.badger-dev.com

All-in-one web-based toolbox for developers. Includes encoders, formatters, converters, and generators.

**Key Features**:
- Base64 encode/decode
- JSON formatter and validator
- UUID generator
- Hash generators (MD5, SHA256, etc.)
- Text diff and comparison
- RegEx tester

**Configuration**:
- Stateless container, no persistence needed
- Client-side processing (no data sent to server)

---

### omni-tools
**Host**: oci-docker
**Purpose**: Multi-purpose utility toolbox
**Image**: Community/custom
**Access**: Internal

Additional utility collection complementing it-tools with specialized functions.

**Configuration**:
- Similar to it-tools, stateless web app

---

### stirling-pdf
**Host**: oci-docker
**Purpose**: PDF manipulation and processing
**Image**: `frooodle/s-pdf`
**Access**: https://pdf.badger-dev.com

Web-based PDF toolbox for merging, splitting, converting, and editing PDFs.

**Key Features**:
- Merge/split PDFs
- Compress and optimize
- Convert to/from PDF (images, Office docs)
- OCR for scanned documents
- Add/remove watermarks
- Sign and secure PDFs

**Configuration**:
- Stateless processing (no user data retention)
- Large file support for document processing

---

### termix
**Host**: hercules
**Purpose**: Web-based terminal access
**Image**: Custom
**Access**: https://term.badger-dev.com

Browser-based terminal emulator for SSH access to homelab hosts.

**Key Features**:
- Web-based SSH client
- Multiple terminal sessions
- Session persistence
- Clipboard integration

**Configuration**:
- SSH key management
- Host access controls
- Authentication via PocketID

---

### phpipam
**Host**: apollo
**Purpose**: IP Address Management (IPAM)
**Image**: `phpipam/phpipam-www`
**Access**: https://ipam.badger-dev.com

Track and manage IP address allocation across the homelab network. Integrates with FreeIPA for authentication.

**Key Features**:
- Subnet management and visualization
- VLAN tracking
- DNS integration
- Device tracking
- API for automation
- FreeIPA LDAP authentication

**Configuration**:
- Database: MySQL/MariaDB
- LDAP: FreeIPA at `ipa1.int.badger-dev.com:389`
- Base DN: `dc=int,dc=badger-dev,dc=com`
- User DN: `uid=%login,ou=People,dc=int,dc=badger-dev,dc=com`

---

### open-webui
**Host**: oci-docker
**Purpose**: Web interface for LLM interaction
**Image**: `ghcr.io/open-webui/open-webui`
**Access**: https://chat.badger-dev.com

ChatGPT-style interface for interacting with locally-hosted or API-based LLMs.

**Key Features**:
- Multi-model support (OpenAI, Anthropic, local)
- Chat history and organization
- Prompt templates
- API key management
- Multi-user support

**Configuration**:
- Model backends configurable
- Persistent chat history
- OIDC: PocketID integration

---

### openhands
**Host**: oci-docker
**Purpose**: AI-powered coding assistant
**Image**: Community
**Access**: Internal

AI agent for code generation, debugging, and development assistance.

**Key Features**:
- Code generation
- Bug fixing assistance
- Documentation generation
- Refactoring suggestions

**Configuration**:
- LLM backend integration
- Repository access for context

---

### qdrant
**Host**: oci-docker
**Purpose**: Vector database for AI/ML applications
**Image**: `qdrant/qdrant`
**Access**: Internal API

High-performance vector similarity search engine for embeddings and semantic search.

**Key Features**:
- Vector similarity search
- Real-time indexing
- REST and gRPC APIs
- Filtering and payload storage
- Horizontal scaling

**Configuration**:
- Persistent vector storage
- Used by open-webui for semantic search
- API-only access (no web UI)

---

### dock-dploy
**Host**: oci-docker
**Purpose**: Deployment dashboard and monitoring
**Image**: Custom
**Access**: Internal

Dashboard for tracking deployment status and managing releases.

**Configuration**:
- Integration with Komodo API
- GitHub Actions hooks

---

## Infrastructure

### komodo
**Host**: hercules
**Purpose**: GitOps orchestration platform (Core)
**Image**: `ghcr.io/moghtech/komodo-core:latest`
**Access**: https://komodo.badger-dev.com

Central orchestration platform managing all Docker stacks via GitOps. Polls GitHub repository every 5 minutes and automatically deploys changes.

**Key Components**:
- **Komodo Core**: Main orchestration engine (port 9120)
- **MongoDB**: Configuration and state database

**Key Features**:
- GitOps-driven deployment
- Multi-host stack management
- Per-host environment overrides
- Webhook support (optional)
- Built-in backup system
- Web UI for manual interventions

**Configuration**:
- Database: MongoDB with 0.25GB WiredTiger cache
- Backups: `/backups` directory for dated database dumps
- Sync files: `/syncs` directory mounted from repository
- Network: `pangolin-tunnel` for external access
- Special labels: `komodo.skip` prevents auto-stop

**See**: [[Docker/Komodo]] for comprehensive Komodo documentation

---

### n8n
**Host**: hercules
**Purpose**: Workflow automation platform
**Image**: `n8nio/n8n`
**Access**: https://n8n.badger-dev.com

Self-hosted alternative to Zapier/IFTTT. Automates workflows between services, APIs, and databases.

**Key Features**:
- 200+ service integrations
- Visual workflow editor
- Webhook triggers
- Scheduled workflows
- JavaScript/Python code nodes
- Database query nodes

**Configuration**:
- PostgreSQL backend for workflows
- Webhook endpoint for external triggers
- LDAP: FreeIPA authentication
- Persistent workflow storage

**Example Workflows**:
- GitHub webhook → Komodo deployment trigger
- Uptime Kuma alerts → ntfy notifications
- Scheduled backups → health checks

---

### postgres
**Host**: postgres-svr (LXC container, not Docker)
**Purpose**: Centralized PostgreSQL database cluster
**Note**: Deployed via Ansible, not Komodo

Centralized PostgreSQL server providing databases for multiple services (n8n, Immich, Paperless-ngx, etc.).

**Configuration**:
- Dedicated LXC container on Proxmox
- Managed via Ansible `postgres` role
- Not part of Docker infrastructure
- See [[../Infrastructure/Hosts Inventory#postgres-svr]]

---

### pocketid
**Host**: oci-dmz
**Purpose**: OIDC/OAuth2 authentication provider
**Image**: `stonith404/pocket-id`
**Access**: https://idp.badger-dev.com, https://auth.badger-dev.com

Modern OIDC identity provider for SSO across homelab services. Acts as bridge between FreeIPA LDAP and modern OAuth2/OIDC applications.

**Key Features**:
- OIDC/OAuth2 provider
- LDAP backend (FreeIPA)
- Multi-factor authentication
- User self-service portal
- Application registration and management

**Configuration**:
- LDAP: FreeIPA at `ipa1.int.badger-dev.com`
- Webhook: Auto-deployment enabled
- Domains: idp.badger-dev.com, auth.badger-dev.com
- Proxied via Pangolin/Gerbil

---

### crowdsec
**Host**: oci-dmz
**Purpose**: Security engine and intrusion prevention
**Image**: `crowdsecurity/crowdsec`
**Access**: API-only

Community-powered threat intelligence and intrusion prevention system. Analyzes Pangolin/Traefik logs and blocks malicious IPs.

**Key Features**:
- Real-time log analysis
- Community threat intelligence
- Automatic IP banning
- Integration with firewall/reverse proxy
- Scenario-based detection

**Configuration**:
- LAPI Key: Shared with Pangolin for bouncer integration
- Log source: Pangolin Traefik access logs
- Configuration: `/home/docker/stacks/infrastructure/pangolin/config`

---

### pangolin
**Host**: oci-dmz
**Purpose**: Traefik-based reverse proxy with tunneling
**Image**: `fosrl/pangolin:1.12.2`
**Access**: https://quartz.badger-dev.com

Sophisticated reverse proxy stack combining Traefik, Gerbil (WireGuard tunneling), and middleware management. Handles all external traffic to homelab services.

**Key Components**:
- **Pangolin**: Configuration management API
- **Gerbil**: WireGuard tunnel termination (ports 51820, 21820)
- **Traefik**: Reverse proxy and load balancer (ports 80, 443)
- **Middleware Manager**: Dynamic middleware configuration
- **Log Dashboard**: Traefik access log visualization
- **Error Pages**: Custom error page handler

**Key Features**:
- Let's Encrypt automatic TLS certificates
- CrowdSec bouncer integration
- Dynamic middleware management
- Multi-tunnel support (Newt agents)
- Access log analytics
- Custom error pages

**Configuration**:
- Cloudflare DNS integration via Dockflare
- Config directory: `/home/docker/stacks/infrastructure/pangolin/config`
- Domains: `badger-dev.com`, `quartz.badger-dev.com`, `api-quartz.badger-dev.com`
- Webhook: Auto-deployment enabled

**Ports**:
- 80: HTTP (redirect to HTTPS)
- 443: HTTPS (TLS termination)
- 51820/UDP: Pangolin WireGuard VPN
- 21820/UDP: Client VPN
- 3456: Middleware Manager UI

**See Also**: [[Docker/Stacks Inventory#newt|Newt]] for tunnel agent details

---

### dockflare
**Host**: oci-dmz
**Purpose**: Cloudflare DNS automation
**Image**: `containeroo/dockflare`
**Access**: Background service

Automatically updates Cloudflare DNS records for Docker containers based on labels. Monitors Gerbil container for domain assignments.

**Key Features**:
- Label-based DNS automation
- Multi-domain support
- A/CNAME record management
- Automatic record cleanup

**Configuration**:
- Cloudflare API Token: `CF_API_TOKEN`
- Account ID: `CF_ACCOUNT_ID`
- Zone ID: `CF_ZONE_ID`
- Monitors: Gerbil container labels

---

### wireguard
**Host**: oci-dmz, meade
**Purpose**: Site-to-site VPN tunnels
**Image**: `linuxserver/wireguard`
**Access**: VPN-only

WireGuard VPN for site-to-site connectivity and remote access. Separate from Tailscale mesh (100.x.x.x/16).

**Deployments**:
- **oci-dmz**: External VPN access point
- **meade**: Remote edge connectivity

**Key Features**:
- Modern VPN protocol (fast, secure)
- Point-to-point tunneling
- Low overhead
- Kernel-integrated

**Configuration**:
- Webhook: Auto-deployment enabled (oci-dmz)
- Peer management via config files
- Complements Tailscale for specific use cases

---

### netbox
**Host**: apollo
**Purpose**: Infrastructure documentation and DCIM
**Image**: `netboxcommunity/netbox`
**Access**: https://netbox.badger-dev.com

Data center infrastructure management (DCIM) and network documentation. Source of truth for physical/virtual infrastructure inventory.

**Key Features**:
- Device and rack management
- Cable/connection tracking
- IP address management (IPAM)
- Virtual machine inventory
- Circuit management
- API for automation

**Configuration**:
- PostgreSQL database
- Redis cache
- FreeIPA LDAP integration
- API tokens for automation

---

### nebula-sync
**Host**: apollo
**Purpose**: Configuration synchronization service
**Image**: Custom
**Access**: Internal API

Synchronizes configuration files across homelab hosts. Ensures consistency of shared configs.

**Key Features**:
- File synchronization
- Version tracking
- Conflict detection

**Configuration**:
- Sync targets configurable
- File watch for automatic sync

---

### newt
**Hosts**: ALL (hercules, apollo, oci-dmz, oci-docker, synology-nas, meade, codewizard)
**Purpose**: Pangolin tunnel agents
**Image**: Custom/Pangolin
**Access**: Background service

Gerbil tunnel agents that establish secure WireGuard connections from internal hosts to the Pangolin reverse proxy on oci-dmz. Enables external access to internal services without exposing them directly.

**Deployments** (7 instances):
| Host | Instance Name | Newt ID | Purpose |
|------|--------------|---------|---------|
| hercules | newt-hercules | ndqq0xnyazxkpwg | Primary services tunnel |
| apollo | newt-apollo | a4ovf8gckvaukws | Monitoring tunnel |
| oci-dmz | newt-oci-dmz | 35dmk50gyw1edkp | DMZ self-tunnel |
| oci-docker | newt-oci-docker | TBD | Cloud services tunnel |
| synology-nas | newt-synology | TBD | Storage services tunnel |
| meade | newt-meade | TBD | Remote edge tunnel |
| codewizard | newt-codewizard | TBD | Development tunnel |

**Key Features**:
- Secure WireGuard tunneling to Pangolin
- Automatic reconnection
- Per-host identification
- Integrated with Gerbil on oci-dmz

**Configuration**:
- Endpoint: `https://quartz.badger-dev.com`
- Per-host Newt ID and Secret
- Reclone enabled for auto-updates

---

### semaphore
**Host**: hercules
**Purpose**: Ansible automation web UI
**Image**: `semaphoreui/semaphore`
**Access**: https://semaphore.badger-dev.com

Web-based UI for running Ansible playbooks. Provides scheduling, logging, and access control for Ansible automation.

**Key Features**:
- Ansible playbook execution
- Scheduled playbook runs
- Inventory management
- Task history and logging
- RBAC and team management
- FreeIPA LDAP integration

**Configuration**:
- Database: MySQL/PostgreSQL
- LDAP: FreeIPA authentication
- SSH key management for Ansible
- Webhook: Auto-deployment disabled (manual control preferred)

**Integration**:
- Manages Ansible repository at `/Users/danielschmeichel/github/ansible`
- Executes phase-based deployments
- See [[../Infrastructure/Ansible]] for playbook details

---

## Monitoring

### beszel
**Host**: apollo
**Purpose**: Infrastructure monitoring hub
**Image**: `henrygd/beszel:0.16.1`
**Access**: https://beszel.badger-dev.com

Central monitoring hub collecting system metrics from Beszel agents across all Docker hosts.

**Key Features**:
- CPU, memory, disk, network monitoring
- Container-level metrics
- Historical data retention
- Alerting and notifications
- Dashboard customization
- Multi-system overview

**Configuration**:
- Port: 8090
- Pangolin tunnel integration
- Health checks every 30s
- Persistent data in `beszel_data` volume

**Agents**: 6 agents deployed (see beszel-agent)

---

### beszel-agent
**Hosts**: hercules, oci-dmz, oci-docker, synology-nas, meade, codewizard
**Purpose**: Beszel monitoring agents
**Image**: `henrygd/beszel-agent`
**Access**: Background service

Lightweight monitoring agents that report system and container metrics to Beszel hub on apollo.

**Deployments** (6 agents):
- beszel-agent-hercules
- beszel-agent-oci-dmz
- beszel-agent-oci-docker
- beszel-agent-synology
- beszel-agent-meade
- beszel-agent-codewizard

**Key Features**:
- Low resource footprint
- Real-time metrics collection
- Docker socket integration
- Automatic hub registration

**Configuration**:
- Hub: Beszel on apollo
- SSH key authentication
- Per-host identification

**See Also**: [[../Monitoring/Beszel]] for comprehensive monitoring setup

---

### dozzle
**Host**: hercules
**Purpose**: Docker log aggregation hub
**Image**: `amir20/dozzle`
**Access**: https://logs.badger-dev.com

Central log aggregation hub collecting container logs from Dozzle agents across all Docker hosts. Provides real-time log streaming and search.

**Key Features**:
- Real-time log streaming
- Multi-host log aggregation
- Full-text search across all logs
- Container filtering
- Log export
- Automatic container discovery

**Configuration**:
- Port: 8080
- Pangolin tunnel integration
- Agent-based architecture

**Agents**: 6 agents deployed (see dozzle-agent)

---

### dozzle-agent
**Hosts**: hercules, apollo, oci-dmz, oci-docker, synology-nas, meade
**Purpose**: Dozzle log collection agents
**Image**: `amir20/dozzle`
**Access**: Background service

Log collection agents that stream container logs to Dozzle hub on hercules.

**Deployments** (6 agents):
| Host | Instance Name | Hostname Label |
|------|--------------|----------------|
| hercules | dozzle-agent-hercules | DOZZLE_HOSTNAME=hercules |
| apollo | dozzle-agent-apollo | DOZZLE_HOSTNAME=apollo |
| oci-dmz | dozzle-agent-oci-dmz | DOZZLE_HOSTNAME=oci-dmz |
| oci-docker | dozzle-agent-oci-docker | DOZZLE_HOSTNAME=oci-docker |
| synology-nas | dozzle-agent-synology | DOZZLE_HOSTNAME=synology |
| meade | dozzle-agent-meade | DOZZLE_HOSTNAME=meade |

**Key Features**:
- Docker socket log streaming
- Per-host identification
- Automatic hub connection
- Real-time log forwarding

**Configuration**:
- Hub: Dozzle on hercules
- Environment: `DOZZLE_HOSTNAME` for host identification
- Docker socket: Mounted read-only

**See Also**: [[../Monitoring/Dozzle]] for log management details

---

### pulse
**Host**: apollo
**Purpose**: Proxmox hypervisor monitoring
**Image**: Community
**Access**: https://pulse.badger-dev.com

Monitoring dashboard specifically for Proxmox VE. Tracks VM/LXC resource usage, node health, and cluster status.

**Key Features**:
- Proxmox API integration
- VM/LXC resource tracking
- Node health monitoring
- Cluster status overview
- Storage monitoring

**Configuration**:
- Proxmox Host: `https://proxmox-server:8006`
- API Token: `PROXMOX_API_TOKEN_ID`, `PROXMOX_API_TOKEN_SECRET`
- Port: 7655

---

### uptime-kuma
**Host**: apollo
**Purpose**: Service uptime monitoring and status pages
**Image**: `louislam/uptime-kuma`
**Access**: https://status.badger-dev.com

Monitors service availability via HTTP/TCP checks and provides public/private status pages.

**Key Features**:
- HTTP/HTTPS monitoring
- TCP port checks
- Ping monitoring
- Keyword monitoring
- Status pages (public/private)
- Notification integrations (ntfy, email, webhooks)
- Certificate expiration alerts

**Configuration**:
- Persistent SQLite database
- Multi-user support
- Notification channels configured for critical services

---

### netalertx
**Host**: apollo
**Purpose**: Network device discovery and tracking
**Image**: `jokobsk/netalertx`
**Access**: https://netalertx.badger-dev.com

Scans local network for new/unknown devices and provides alerting for network changes.

**Key Features**:
- Network device discovery
- MAC address tracking
- New device alerts
- Vendor identification (OUI lookup)
- Historical device tracking

**Configuration**:
- Network: Bridge mode for direct network access
- Alerts: Integration with ntfy for notifications

---

### diun
**Hosts**: ALL (hercules, apollo, oci-dmz, oci-docker, synology-nas, meade, codewizard)
**Purpose**: Docker image update notifications
**Image**: `crazymax/diun`
**Access**: Background service

Monitors Docker images for updates and sends notifications when new versions are available. Runs on every Docker host.

**Deployments** (7 instances):
- diun-hercules
- diun-apollo
- diun-oci-dmz
- diun-oci-docker
- diun-synology
- diun-meade
- diun-codewizard

**Key Features**:
- Registry polling for image updates
- Per-container update tracking
- Notification via ntfy/webhooks
- Renovate integration

**Configuration**:
- Docker socket mounted read-only
- Registry credentials for private images
- Notification endpoints

---

### alertmanager
**Host**: TBD
**Purpose**: Alert routing and management
**Image**: `prom/alertmanager`
**Access**: Internal

Handles alerts from Prometheus and other monitoring systems. Routes, deduplicates, and silences alerts.

**Key Features**:
- Alert routing rules
- Notification templates
- Alert grouping and deduplication
- Silence management
- Integration with multiple receivers

**Configuration**:
- Alert sources: Prometheus, custom webhooks
- Receivers: ntfy, email, PagerDuty (if configured)

---

## Stack Deployment Matrix

| Host | Applications | Infrastructure | Monitoring | Total |
|------|--------------|----------------|------------|-------|
| **hercules** | homepage, karakeep, termix | komodo, n8n, semaphore, newt | dozzle, dozzle-agent, diun | 11 |
| **apollo** | phpipam | netbox, nebula-sync, newt | beszel, pulse, uptime-kuma, netalertx, dozzle-agent, diun | 10 |
| **synology-nas** | immich, paperless-ngx | newt | beszel-agent, dozzle-agent, diun | 6 |
| **codewizard** | TBD | newt | beszel-agent, diun | 3+ |
| **oci-dmz** | - | pangolin, crowdsec, pocketid, dockflare, wireguard, newt | dozzle-agent, diun | 9 |
| **oci-docker** | karakeep, mealie, it-tools, omni-tools, stirling-pdf, open-webui, openhands, qdrant, dock-dploy | newt | dozzle-agent, diun | 12 |
| **meade** | - | wireguard, newt | beszel-agent, dozzle-agent, diun | 5 |
| **Total** | **15 unique** | **11 unique (18 instances)** | **9 unique (20 instances)** | **53 instances** |

## Stack Categories by Purpose

### External-Facing Services (via Pangolin)
Services accessible from the internet through oci-dmz:
- homepage
- immich
- paperless-ngx
- mealie
- it-tools
- stirling-pdf
- phpipam
- open-webui
- pocketid (auth)
- komodo
- semaphore
- beszel
- dozzle
- uptime-kuma

### Internal-Only Services
Services accessible only via Tailscale VPN:
- postgres (LXC, not Docker)
- netbox
- nebula-sync
- qdrant (API-only)
- alertmanager
- All agent instances (beszel-agent, dozzle-agent, newt, diun)

### Hub-Agent Architectures
Services using centralized hub + distributed agents:

**Beszel** (Infrastructure Monitoring):
- Hub: apollo
- Agents: hercules, oci-dmz, oci-docker, synology-nas, meade, codewizard

**Dozzle** (Log Aggregation):
- Hub: hercules
- Agents: hercules, apollo, oci-dmz, oci-docker, synology-nas, meade

**Pangolin/Newt** (Reverse Proxy Tunneling):
- Hub: oci-dmz (Pangolin + Gerbil)
- Agents: ALL hosts (7 Newt instances)

### Authentication Integration

**OIDC (via PocketID)**:
- open-webui
- komodo
- beszel
- dozzle
- (others configurable)

**LDAP (via FreeIPA)**:
- phpipam
- semaphore
- pocketid (backend)
- paperless-ngx
- immich
- n8n

## Common Configuration Patterns

### Environment Variables
Most stacks use these common variables:
- `PUID` / `PGID`: User/group IDs for file permissions
- `TZ`: Timezone (typically UTC)
- `DOMAIN_NAME`: Base domain (badger-dev.com)

### Networks
Common Docker networks:
- `pangolin-tunnel`: External access via Pangolin proxy
- `default` / `<stack-name>`: Stack-isolated networks
- `cloudflare-net`: Dockflare DNS automation

### Volumes
Volume patterns:
- Named volumes: For persistent data (e.g., `beszel_data`)
- Host mounts: For configuration (e.g., `/home/docker/stacks/<path>`)
- NAS mounts: For large media storage (Synology NFS)

### Health Checks
Most production stacks include:
- Interval: 30s (standard)
- Timeout: 10s
- Retries: 3
- Start period: 30-40s

## Related Documentation

- **[[Docker/Docker MOC]]** - Docker infrastructure overview
- **[[Docker/Komodo]]** - Komodo orchestration details
- **[[Docker/Host Fleet]]** - Docker host topology
- **[[../Services/Application Catalog]]** - User-facing application details
- **[[../Services/Service Dependencies]]** - Service dependency mapping
- **[[../Monitoring/Beszel]]** - Beszel monitoring setup
- **[[../Monitoring/Dozzle]]** - Dozzle log aggregation setup

## External References

- **Docker Repository**: /Users/danielschmeichel/github/docker
- **Stack Configurations**: /Users/danielschmeichel/github/docker/stacks/
- **Sync Files**: /Users/danielschmeichel/github/docker/syncs/
