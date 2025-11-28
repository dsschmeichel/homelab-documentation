---
tags:
  - docker
  - komodo
  - gitops
  - orchestration
aliases:
  - Komodo Core
  - GitOps Platform
created: 2024-11-24
updated: 2024-11-24
---

# Komodo

GitOps orchestration platform managing all Docker stack deployments across the homelab infrastructure.

## Architecture

```
┌──────────────────────────────────────────────────┐
│ GitHub Repository                                │
│ github.com/dsschmeichel/docker                   │
│ - main branch (production)                       │
└────────────┬─────────────────────────────────────┘
             │
             │ Poll every 5 minutes
             ▼
┌──────────────────────────────────────────────────┐
│ Komodo Core (hercules:9120)                     │
│ - MongoDB (state/config database)                │
│ - Web UI (komodo.badger-dev.com)                 │
│ - Resource sync engine                           │
└────────────┬─────────────────────────────────────┘
             │
             │ HTTPS (port 8120)
             ▼
  ┌──────────┴──────────┬──────────────┐
  │                     │              │
  ▼                     ▼              ▼
┌──────────┐      ┌──────────┐  ┌──────────┐
│ Periphery│      │ Periphery│  │ Periphery│
│ (apollo) │ ...  │ (oci-dmz)│  │ (meade)  │
└────┬─────┘      └────┬─────┘  └────┬─────┘
     │                 │              │
     ▼                 ▼              ▼
Docker Daemon     Docker Daemon  Docker Daemon
```

**Components**:
- **Komodo Core**: Orchestration engine on hercules (port 9120)
- **MongoDB**: Configuration and state database (0.25GB WiredTiger cache)
- **Periphery Agents**: Remote Docker daemon controllers (7 hosts)
- **Resource Sync**: Git repository polling and sync (every 5 minutes)

## Repository Structure

```
/Users/danielschmeichel/github/docker/
├── stacks/                # Docker Compose stack definitions
│   ├── applications/      # User-facing services (15 stacks)
│   ├── infrastructure/    # Platform services (11 stacks)
│   ├── monitoring/        # Observability stacks (9 stacks)
│   └── _stack_archive/    # Retired stacks
├── syncs/                 # Komodo configuration
│   ├── servers.toml       # Host definitions (7 servers)
│   ├── stacks-*.toml      # Per-host stack assignments
│   └── resourcesync.toml  # Git polling configuration
├── komodo/                # Komodo deployment files
│   ├── compose.yaml       # Core deployment
│   └── periphery/         # Periphery agent configs
├── scripts/               # Operational scripts
│   ├── update-komodo.sh   # Update Core/Periphery
│   ├── health-check.sh    # Quick status check
│   ├── multi-host-check.sh # Comprehensive diagnostics
│   ├── validate-stack.sh  # Stack validation
│   ├── git-pull-all-hosts.sh # Sync Git across hosts
│   └── kopia-snapshot.sh  # Backup automation
├── docs/                  # Repository documentation
└── config/                # Shared templates
```

## Configuration Files

### servers.toml
Defines all Docker hosts and connection details:

```toml
[[server]]
name = "hercules"
[server.config]
address = "https://host.docker.internal:8120"
region = "Amethyst"
enabled = true
```

**7 registered servers**:
- hercules (10.2.0.70, via host.docker.internal)
- apollo (100.102.0.11, Tailscale)
- oci-dmz (100.90.0.90, Tailscale)
- oci-docker (100.70.1.70, Tailscale)
- synology-nas (10.2.0.200, LAN)
- meade (100.119.163.88, Tailscale)
- codewizard (10.2.0.65, LAN)

### stacks-<host>.toml
Maps stacks to hosts with per-host environment overrides:

```toml
[[stack]]
name = "dozzle-agent-hercules"
[stack.config]
server = "hercules"
project_name = "dozzle-agent"
poll_for_updates = true
auto_update = true
linked_repo = "Github-dsschmeichel"
webhook_enabled = false
run_directory = "stacks/monitoring/dozzle-agent"
environment = """
DOZZLE_HOSTNAME=hercules
"""
```

**Key fields**:
- `server`: Target host from servers.toml
- `project_name`: Docker Compose project name
- `run_directory`: Path to compose.yaml (relative to repo root)
- `poll_for_updates`: Enable Git polling (default: true)
- `auto_update`: Automatically redeploy on changes (default: true)
- `webhook_enabled`: Allow webhook-triggered deployments (default: false)
- `environment`: Host-specific environment variables (optional)
- `reclone`: Force fresh Git clone on update (default: false)

### resourcesync.toml
Configures repository polling behavior:

```toml
[[resource_sync]]
name = "Github-dsschmeichel"
[resource_sync.config]
linked_repo = "Github-dsschmeichel"
webhook_enabled = false
resource_path = ["syncs"]
managed = true
pending_alert = false
```

**Configuration**:
- **Polling interval**: 5 minutes (default)
- **Webhook support**: Disabled (using polling only)
- **Sync paths**: `syncs/` directory
- **Managed**: Komodo controls sync state

## GitOps Workflow

### Deployment Process

1. **Edit locally**: Modify stack compose files or sync configs
2. **Validate**: Run `docker compose config` in stack directory
3. **Commit & push**: Push changes to `main` branch
4. **Auto-deployment**: Komodo polls and detects changes within 5 minutes
5. **Stack update**: Komodo redeploys affected stacks automatically
6. **Verification**: Check Komodo UI for deployment status

**Important**: `main` branch is production. Use feature branches for testing.

### Manual Deployment

When automatic deployment isn't suitable:

```bash
# Via Komodo UI
https://komodo.badger-dev.com
# Navigate to stack → Click "Deploy"

# Via SSH (emergency only)
ssh <host>
cd /home/docker/stacks/<category>/<stack-name>
docker compose pull
docker compose up -d
```

### Host-Specific Overrides

Single compose file, multiple hosts with different configs:

```toml
# stacks-hercules.toml
[[stack]]
name = "newt-hercules"
environment = """
NEWT_ID=ndqq0xnyazxkpwg
NEWT_SECRET=z932dmsmt9mq0gjy8axgo2cguokdvv101yywv8lc96e4bns6
PANGOLIN_ENDPOINT=https://quartz.badger-dev.com
"""

# stacks-apollo.toml
[[stack]]
name = "newt-apollo"
environment = """
NEWT_ID=a4ovf8gckvaukws
NEWT_SECRET=7ckhagfso1jda0tj2b5tqld4e9351wwrh4i1ykxqwvbi01oj
PANGOLIN_ENDPOINT=https://quartz.badger-dev.com
"""
```

## Operational Scripts

### update-komodo.sh
Update Komodo Core and/or Periphery agents:

```bash
cd /Users/danielschmeichel/github/docker

# Update Core only (hercules)
bash scripts/update-komodo.sh --core-only

# Update all Periphery agents
bash scripts/update-komodo.sh --periphery-only

# Update specific host
bash scripts/update-komodo.sh --host apollo

# Update everything
bash scripts/update-komodo.sh
```

### health-check.sh
Quick health status across infrastructure:

```bash
bash scripts/health-check.sh
```

Checks:
- Docker daemon status
- Komodo Core/Periphery health
- Container counts
- Resource utilization

### multi-host-check.sh
Comprehensive diagnostics across all hosts:

```bash
bash scripts/multi-host-check.sh
```

Reports:
- System metrics (CPU, memory, disk)
- Docker status and container health
- Network connectivity
- Komodo agent status
- Recent errors

### validate-stack.sh
Validate compose files and Komodo configuration:

```bash
cd /Users/danielschmeichel/github/docker
bash scripts/validate-stack.sh stacks/applications/homepage
```

Validates:
- Compose file syntax
- Environment variables
- Network definitions
- Volume mounts
- Komodo sync file references

### git-pull-all-hosts.sh
Sync Git repository across all Docker hosts:

```bash
bash scripts/git-pull-all-hosts.sh
```

Performs:
- `git pull` on each host
- Fast-forward only (safe)
- Reports sync status per host

### kopia-snapshot.sh
Trigger Kopia backups (integrated with Komodo backups):

```bash
bash scripts/kopia-snapshot.sh
```

Backs up:
- Komodo MongoDB database (dated dumps in `/backups`)
- Stack configurations
- Persistent volume data (selective)

## Komodo Core Deployment

### compose.yaml Structure

```yaml
services:
  mongo:
    image: mongo
    command: --quiet --wiredTigerCacheSizeGB 0.25
    labels:
      komodo.skip:  # Prevent Komodo from self-stopping
    volumes:
      - mongo-data:/data/db
      - mongo-config:/data/configdb
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${KOMODO_DB_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${KOMODO_DB_PASSWORD}

  core:
    image: ghcr.io/moghtech/komodo-core:latest
    labels:
      komodo.skip:  # Prevent Komodo from self-stopping
    depends_on:
      - mongo
    ports:
      - 9120:9120
    environment:
      KOMODO_DATABASE_ADDRESS: mongo:27017
      KOMODO_DATABASE_USERNAME: ${KOMODO_DB_USERNAME}
      KOMODO_DATABASE_PASSWORD: ${KOMODO_DB_PASSWORD}
    volumes:
      - ${COMPOSE_KOMODO_BACKUPS_PATH}:/backups
      - ./syncs:/syncs
    networks:
      - pangolin-tunnel
    extra_hosts:
      - host.docker.internal:host-gateway
```

**Special labels**:
- `komodo.skip`: Prevents Komodo from managing itself (avoid self-stop)

**Volumes**:
- `/backups`: Dated MongoDB backups
- `/syncs`: Mounted from repository for resource sync

**Networks**:
- `pangolin-tunnel`: External access via Pangolin proxy

**Host mapping**:
- `host.docker.internal`: Allows Core to connect to local Periphery

### Periphery Agent Deployment

Periphery agents run as systemd services (not Docker containers), deployed via Ansible:

```bash
# Check Periphery status
ssh <host>
sudo systemctl status komodo-periphery

# View Periphery logs
sudo journalctl -u komodo-periphery -f

# Restart Periphery
sudo systemctl restart komodo-periphery
```

**Connection**:
- Port 8120 (HTTPS)
- Passkey authentication
- TLS encryption

**Deployment**:
- Managed by Ansible `docker` role (Phase 4)
- Configuration: `/etc/komodo/periphery.config.toml`
- Binary: `/usr/local/bin/komodo-periphery`

See [[../Infrastructure/Ansible#Phase 4 Docker]] for Periphery deployment details.

## Common Tasks

### View Komodo Core Status

```bash
ssh hercules
cd /home/docker/komodo
docker compose ps
docker compose logs -f core
```

### Check MongoDB Health

```bash
ssh hercules
cd /home/docker/komodo
docker compose logs -f mongo
docker compose exec mongo mongosh --eval "db.adminCommand('ping')"
```

### Restart Komodo Core

```bash
ssh hercules
cd /home/docker/komodo
docker compose restart core
```

### Force Stack Redeployment

```bash
# Via Komodo UI
https://komodo.badger-dev.com
# Stack → Deploy (button)

# Via API
curl -X POST https://komodo.badger-dev.com/api/stack/<stack-id>/deploy \
  -H "Authorization: Bearer <token>"
```

### View Stack Deployment History

```bash
# Via Komodo UI
https://komodo.badger-dev.com
# Stack → History tab

# Via SSH on target host
ssh <host>
cd /home/docker/stacks/<category>/<stack>
docker compose ps
docker compose logs --tail=50
```

### Check Resource Sync Status

```bash
# Via Komodo UI
https://komodo.badger-dev.com
# Settings → Resources → Github-dsschmeichel

# Via Core logs
ssh hercules
cd /home/docker/komodo
docker compose logs -f core | grep -i sync
```

## Troubleshooting

### Core Not Polling Repository

1. Check resource sync configuration:
```bash
ssh hercules
cd /home/docker/komodo
docker compose logs core | grep -i "resource sync"
```

2. Verify GitHub connection:
```bash
# Check Core can reach GitHub
ssh hercules
curl -I https://github.com
```

3. Check sync timing (5-minute intervals):
```bash
# Wait up to 5 minutes for next poll
# Or manually trigger via UI: Resources → Sync Now
```

### Stack Deployment Failures

1. Check Komodo UI for error messages
2. Verify Periphery agent connectivity:
```bash
ssh <host>
sudo systemctl status komodo-periphery
sudo journalctl -u komodo-periphery -n 50
```

3. Validate compose file locally:
```bash
cd /Users/danielschmeichel/github/docker
cd stacks/<category>/<stack>
docker compose config
```

4. Check for missing environment variables:
```bash
# Review syncs/stacks-<host>.toml
# Ensure all required vars are defined
```

5. Manual deployment if needed:
```bash
ssh <host>
cd /home/docker/stacks/<category>/<stack>
docker compose pull
docker compose up -d
```

### Periphery Agent Unreachable

1. Check agent service status:
```bash
ssh <host>
sudo systemctl status komodo-periphery
```

2. Verify port 8120 is listening:
```bash
sudo ss -tlnp | grep 8120
```

3. Check firewall rules:
```bash
sudo iptables -L -n | grep 8120
```

4. Verify Tailscale connectivity (if applicable):
```bash
tailscale status
ping <host-tailscale-ip>
```

5. Restart Periphery:
```bash
sudo systemctl restart komodo-periphery
sudo journalctl -u komodo-periphery -f
```

### MongoDB Issues

1. Check MongoDB logs:
```bash
ssh hercules
cd /home/docker/komodo
docker compose logs mongo
```

2. Verify database connectivity:
```bash
docker compose exec core sh -c 'wget -O- mongo:27017'
```

3. Check disk space (MongoDB writes to `/var/lib/docker/volumes`):
```bash
df -h /var/lib/docker
```

4. Restart MongoDB (safe, Core will reconnect):
```bash
docker compose restart mongo
```

### Stack Not Auto-Updating

1. Verify `auto_update` is enabled in stack config:
```bash
grep -A 10 "name = \"<stack-name>\"" syncs/stacks-<host>.toml
# Ensure: auto_update = true
```

2. Check `poll_for_updates` is enabled:
```bash
# Should be: poll_for_updates = true
```

3. Verify recent changes were pushed to `main` branch
4. Wait for next polling interval (up to 5 minutes)
5. Check Core logs for sync activity:
```bash
ssh hercules
cd /home/docker/komodo
docker compose logs core | grep -i "<stack-name>"
```

## Security Considerations

### Passkey Management
- Periphery agents use passkeys for authentication
- Passkeys stored in `komodo/periphery/compose.yaml` (not committed)
- Rotate passkeys periodically via Ansible re-deployment

### Network Security
- Core accessible via Pangolin tunnel (TLS)
- Periphery agents use TLS on port 8120
- No direct internet exposure (Tailscale/private networks)

### Access Control
- Web UI authentication via PocketID (OIDC)
- API tokens for automation
- Role-based access control (admin/operator/viewer)

### Backup Strategy
- MongoDB backups: Dated dumps in `/backups` directory
- Automatic backup via Komodo internal scheduler
- Manual backups: `bash scripts/kopia-snapshot.sh`
- Retention: 7 daily, 4 weekly, 3 monthly

## Integration with Other Systems

### Ansible
- **Phase 4**: Docker installation and Periphery agent deployment
- **Relationship**: Ansible provisions hosts, Komodo manages containers
- See [[../Infrastructure/Ansible]]

### Monitoring
- **Beszel**: Infrastructure metrics (Komodo monitored via beszel-agent)
- **Dozzle**: Container logs (Komodo Core/Mongo logs aggregated)
- **Uptime Kuma**: HTTP checks on Komodo UI availability

### Authentication
- **PocketID**: OIDC provider for Komodo web UI
- **FreeIPA**: Underlying LDAP (via PocketID)

## Related Documentation

- **[[Docker/Docker MOC]]** - Docker infrastructure overview
- **[[Docker/Host Fleet]]** - Docker host details
- **[[Docker/Stacks Inventory]]** - All 36 stack configurations
- **[[../Infrastructure/Ansible]]** - Ansible automation (Periphery deployment)
- **[[../Procedures/Deployment]]** - Deployment procedures
- **[[../Procedures/Troubleshooting]]** - Troubleshooting guide

## External References

- **Komodo Documentation**: https://komo.do/docs
- **Komodo UI**: https://komodo.badger-dev.com
- **Repository**: /Users/danielschmeichel/github/docker
- **GitHub**: github.com/dsschmeichel/docker

