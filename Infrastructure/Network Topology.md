---
title: Network Topology
tags: [infrastructure, network, topology, architecture]
created: 2025-11-27
updated: 2025-11-27
---

# Network Topology

Comprehensive network architecture documentation for the Badger Development homelab infrastructure, covering physical topology, VLANs, routing, VPN, and DNS.

## Quick Reference

**Primary Networks**:
- Management LAN: `10.2.0.0/24`
- Tailscale VPN: `100.x.x.x/16`
- WireGuard VPN: `100.90.0.0/16`
- Container Networks: `100.70.0.0/16`, `100.102.0.0/16`

**Key Infrastructure**:
- FreeIPA DNS: `ipa1.int.badger-dev.com` (10.2.0.20)
- Gateway/Router: (IP TBD)
- Primary DNS: FreeIPA (10.2.0.20)
- Secondary DNS: pihole-backup (10.2.0.12)

## Network Architecture Overview

```
                         Internet
                            │
                            │ ISP Connection
                            │
                    ┌───────▼────────┐
                    │  Gateway/Router │
                    │  (Firewall/NAT) │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
         ┌───────▼────────┐      ┌──────▼──────┐
         │  Managed Switch │      │  WiFi APs   │
         │   10.2.0.0/24   │      │             │
         └────────┬────────┘      └─────────────┘
                  │
      ┌───────────┼───────────────────────┐
      │           │                       │
┌─────▼─────┐ ┌──▼────┐        ┌─────────▼─────────┐
│ Proxmox   │ │ NAS   │        │   Raspberry Pis   │
│  Hosts    │ │       │        │  ipa1, apollo, etc│
└───────────┘ └───────┘        └───────────────────┘
      │
      │ Virtual Networks
      │
┌─────▼─────────────────────────┐
│  VMs and LXC Containers       │
│  - genesis, hercules, etc     │
│  - postgres-svr, etc          │
└───────────────────────────────┘

        Overlay Networks:
┌─────────────────────────────────┐
│  Tailscale Mesh VPN             │
│  100.x.x.x/16                   │
│  - All hosts connected          │
│  - Peer-to-peer mesh            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  WireGuard Site-to-Site         │
│  Amethyst <──> Oracle Cloud DMZ │
│  100.90.0.0/16                  │
└─────────────────────────────────┘
```

## Physical Network

### On-Premises Network (Amethyst)

**Primary LAN**: `10.2.0.0/24`
- **Gateway**: 10.2.0.1 (router)
- **DNS Primary**: 10.2.0.20 (ipa1 FreeIPA)
- **DNS Secondary**: 10.2.0.12 (pihole-backup)
- **DHCP Range**: 10.2.0.100-10.2.0.199 (if DHCP enabled)
- **Static Range**: 10.2.0.10-10.2.0.99 (infrastructure hosts)

**Network Equipment**:
- **Router**: (Model/IP TBD) - Gateway, NAT, firewall
- **Core Switch**: (Model TBD) - L2/L3 switching, VLAN support
- **Access Points**: (Model/Count TBD) - WiFi coverage

**Wiring**:
- Gigabit Ethernet (Cat5e/Cat6)
- Proxmox host: Bonded NICs (if equipped)
- Synology NAS: Bonded NICs (link aggregation)
- Raspberry Pis: Single gigabit connection

---

## IP Address Allocation

### Static IP Assignments (10.2.0.0/24)

| IP Address | Hostname | Purpose | Hardware |
|------------|----------|---------|----------|
| 10.2.0.1 | gateway | Network gateway/router | Router |
| 10.2.0.11 | apollo | Monitoring hub | Raspberry Pi 4 |
| 10.2.0.12 | pihole-backup | DNS/DHCP backup | Proxmox LXC |
| 10.2.0.20 | ipa1 | FreeIPA identity server | Raspberry Pi 4 |
| 10.2.0.21 | bucket | Reserved bucket server | Proxmox VM |
| 10.2.0.40 | homeassistant | Home automation | Proxmox LXC |
| 10.2.0.50 | sentinel | Services host | Raspberry Pi 4 |
| 10.2.0.65 | codewizard | Development Docker host | Proxmox VM |
| 10.2.0.70 | hercules | Primary Docker host | Proxmox VM |
| 10.2.0.100 | genesis | Management host | Proxmox VM |
| 10.2.0.200 | synology-nas | Network storage | Synology NAS |

### Tailscale VPN (100.x.x.x/16)

| Tailscale IP | Hostname | Physical Location | Notes |
|--------------|----------|-------------------|-------|
| 100.102.0.11 | apollo | Amethyst | Monitoring hub |
| 100.102.0.30 | oci-dmz | Oracle Cloud | DMZ/Proxy host |
| 100.102.0.40 | oci-docker | Oracle Cloud | ARM64 app node |
| 100.102.0.50 | sentinel | Amethyst | Services host |
| 100.102.0.51 | ipa1 | Amethyst | FreeIPA server |
| 100.102.0.60 | meade | Remote Edge | Edge host |
| 100.102.0.70 | hercules | Amethyst | Primary Docker host |
| 100.102.0.100 | genesis | Amethyst | Management host |
| 100.102.0.140 | codewizard | Amethyst | Development host |
| 100.102.1.200 | postgres-svr | Amethyst | Database server |

**Tailscale Configuration**:
- Mesh VPN connecting all infrastructure
- Automatic peer-to-peer connections
- MagicDNS enabled: `<hostname>.tail<domain>.ts.net`
- ACL policies restrict access between hosts
- Exit nodes: Not configured (uses direct routing)

See [[Network/VPN#Tailscale]] for detailed Tailscale configuration.

### WireGuard VPN (100.90.0.0/16)

| WireGuard IP | Hostname | Physical Location | Role |
|--------------|----------|-------------------|------|
| 100.90.0.90 | oci-dmz | Oracle Cloud | VPN endpoint |
| TBD | gateway | Amethyst | Site-to-site peer |

**WireGuard Configuration**:
- Site-to-site VPN: Amethyst ↔ Oracle Cloud DMZ
- Persistent tunnel for OCI DMZ access
- Routes Amethyst traffic through OCI DMZ
- Used for public-facing services

See [[Network/VPN#WireGuard]] for detailed WireGuard configuration.

---

## DNS Infrastructure

### Primary DNS: FreeIPA (ipa1)

**Server**: ipa1.int.badger-dev.com (10.2.0.20)

**Capabilities**:
- Authoritative DNS for `int.badger-dev.com` domain
- Dynamic DNS updates (from DHCP/clients)
- DNSSEC support (if configured)
- DNS forwarding to upstream resolvers
- Integrated with LDAP and Kerberos

**DNS Zone**: `int.badger-dev.com`

**DNS Records** (Sample):
```
A Records:
ipa1.int.badger-dev.com.        IN A    10.2.0.20
apollo.int.badger-dev.com.      IN A    10.2.0.11
hercules.int.badger-dev.com.    IN A    10.2.0.70
synology-nas.int.badger-dev.com. IN A   10.2.0.200

CNAME Records:
freeipa.int.badger-dev.com.     IN CNAME ipa1.int.badger-dev.com.
nas.int.badger-dev.com.         IN CNAME synology-nas.int.badger-dev.com.

SRV Records (Kerberos, LDAP):
_kerberos._tcp.int.badger-dev.com.  IN SRV 0 100 88 ipa1.int.badger-dev.com.
_ldap._tcp.int.badger-dev.com.      IN SRV 0 100 389 ipa1.int.badger-dev.com.
```

**DNS Management**:
```bash
# Add DNS record
ipa dnsrecord-add int.badger-dev.com newhost --a-rec 10.2.0.50

# Show DNS zone
ipa dnszone-show int.badger-dev.com

# Find DNS records
ipa dnsrecord-find int.badger-dev.com
```

**Upstream Forwarders**:
- Primary: 1.1.1.1 (Cloudflare)
- Secondary: 8.8.8.8 (Google)
- Or ISP DNS servers

See [[Security/FreeIPA#DNS]] for detailed FreeIPA DNS documentation.

---

### Secondary DNS: Pi-hole (pihole-backup)

**Server**: pihole-backup.int.badger-dev.com (10.2.0.12)

**Capabilities**:
- Backup DNS resolver
- Ad-blocking DNS (Pi-hole)
- DNS caching
- DHCP server (backup role)
- Unbound recursive resolver

**Configuration**:
- Forwards to FreeIPA (10.2.0.20) for `int.badger-dev.com` queries
- Uses Unbound for external DNS resolution
- Gravity ad-blocking enabled
- Synced with primary Pi-hole (if exists)

**Access**:
- Web UI: http://pihole-backup.int.badger-dev.com/admin
- DNS port: 53
- DHCP: Enabled (backup, not primary)

---

## VLAN Configuration

**Current VLANs** (Update if configured):

| VLAN ID | Name | Subnet | Purpose |
|---------|------|--------|---------|
| 1 | Default | 10.2.0.0/24 | Management and infrastructure |
| TBD | Servers | TBD | Server VLAN (if segregated) |
| TBD | IoT | TBD | IoT devices (isolation) |
| TBD | Guest | TBD | Guest WiFi (isolated) |

**VLAN Strategy** (if implemented):
- VLAN 1: Management and trusted infrastructure
- VLAN 10: Server infrastructure (Proxmox, NAS, databases)
- VLAN 20: IoT devices (smart home, cameras) - isolated
- VLAN 30: Guest network - internet only, no LAN access

**Inter-VLAN Routing**:
- Handled by router or L3 switch
- Firewall rules restrict cross-VLAN traffic
- Explicit allow rules for required services

---

## Routing & Firewall

### Default Gateway

**Router/Gateway**: 10.2.0.1 (Model TBD)

**Routing Functions**:
- NAT (Network Address Translation) for internet access
- Default route to ISP
- Static routes to VPN networks (Tailscale, WireGuard)
- Port forwarding (minimal, prefer VPN)

**Firewall Rules** (Conceptual):

**WAN → LAN** (Inbound from Internet):
- **Default**: DENY all
- **Allow**: Only explicitly configured (VPN endpoints)
- **NAT Port Forwards**: Minimal (prefer Tailscale/WireGuard)

**LAN → WAN** (Outbound to Internet):
- **Default**: ALLOW all
- **Block**: Known malicious IPs (if configured)

**Inter-VLAN** (if configured):
- Default: DENY cross-VLAN
- Allow: Specific services (DNS, monitoring)

---

## VPN Infrastructure

### Tailscale Mesh VPN

**Architecture**: Mesh VPN connecting all infrastructure hosts

**Deployment**:
- Installed on all 13 hosts
- Automatic peer discovery and connection
- NAT traversal (works behind firewalls)
- End-to-end encryption

**Use Cases**:
- Remote access to infrastructure
- Host-to-host communication across locations
- FreeIPA connectivity for remote hosts (oci-docker, meade)
- Monitoring traffic (Beszel, Dozzle)

**Configuration File**: `/etc/default/tailscaled` (per host)

**Management**:
- Tailscale admin console (web)
- ACL policies for access control
- DNS: MagicDNS for automatic hostname resolution

**Security**:
- Device authorization required
- Key expiry: 180 days (configurable)
- ACL policies restrict traffic
- No default routes (split tunnel)

See [[Network/VPN#Tailscale]] for complete Tailscale documentation.

---

### WireGuard Site-to-Site VPN

**Purpose**: Persistent VPN tunnel between Amethyst and Oracle Cloud DMZ

**Topology**:
```
Amethyst (10.2.0.0/24) ←─WireGuard─→ OCI DMZ (100.90.0.90)
                                         ↓
                                    Internet Access
                                    (Public Services)
```

**Endpoints**:
- **Amethyst Peer**: Gateway router or hercules (TBD)
- **OCI DMZ Peer**: oci-dmz (100.90.0.90)

**Tunnel Configuration**:
- Tunnel interface: wg0
- Tunnel IP range: 100.90.0.0/16
- Persistent keepalive: 25 seconds
- Allowed IPs: Amethyst subnet and OCI DMZ

**Use Cases**:
- OCI DMZ access to Amethyst services
- Expose select Amethyst services via OCI DMZ
- Backup route for internet access (if configured)

**Configuration Files**:
- Amethyst: `/etc/wireguard/wg0.conf`
- OCI DMZ: `/etc/wireguard/wg0.conf`

See [[Network/VPN#WireGuard]] for complete WireGuard documentation.

---

## Container Networking

### Docker Networks

**Docker Host: hercules**

**Network Modes**:
- **Bridge**: Default isolated network per container
- **Host**: Container shares host network stack (rare use)
- **Macvlan**: Container gets own MAC/IP on LAN
- **Custom Bridge**: Named networks for stack isolation

**Common Docker Networks**:
```
docker network ls

NAME                DRIVER    SCOPE
bridge              bridge    local     # Default
host                host      local
komodo_net          bridge    local     # Komodo orchestration
traefik_net         bridge    local     # Reverse proxy
monitoring_net      bridge    local     # Monitoring stack
```

**External Access**:
- Traefik reverse proxy (HTTPS ingress)
- Published ports (e.g., 8080:80)
- VPN access via Tailscale

---

## Network Monitoring

### Monitoring Tools

**Beszel** (apollo, 10.2.0.11):
- Infrastructure host monitoring
- Network bandwidth tracking
- Connection state monitoring

**Dozzle** (hercules, 10.2.0.70):
- Docker container network logs
- Connection tracking for containers

**NetAlertX** (apollo, 10.2.0.11):
- Network device discovery
- Port scanning and monitoring
- MAC address tracking
- Rogue device detection

**Uptime Kuma** (hercules, 10.2.0.70):
- HTTP/HTTPS endpoint monitoring
- DNS resolution checks
- Ping monitoring
- TCP port checks

See [[Monitoring/Monitoring MOC]] for comprehensive monitoring documentation.

---

### Network Metrics

**Key Metrics Tracked**:
- Bandwidth utilization (in/out)
- Packet loss and latency
- Connection counts (established, time_wait, etc.)
- DNS query times
- VPN tunnel status

**Alerting Thresholds**:
- Bandwidth >80% sustained for 5 minutes
- Packet loss >1% for 10 minutes
- DNS resolution failures
- VPN tunnel down >5 minutes

---

## Network Security

### Firewall Rules

**Host-Based Firewalls (UFW)**:
- Deployed on all hosts via Ansible
- Default: DENY incoming, ALLOW outgoing
- Explicit ALLOW rules for required services

**Example UFW Rules** (hercules):
```bash
# SSH
ufw allow 2024/tcp comment 'SSH'

# Docker API (internal only)
ufw allow from 10.2.0.0/24 to any port 2375

# HTTP/HTTPS (Traefik)
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Komodo
ufw allow from 10.2.0.0/24 to any port 9120
ufw allow from 10.2.0.0/24 to any port 8120

# Monitoring
ufw allow from 10.2.0.11 to any port 9100 comment 'Beszel agent'
```

---

### Network Segmentation

**Current Segmentation**:
1. **Management Network** (10.2.0.0/24): Trusted infrastructure
2. **VPN Networks**: Tailscale and WireGuard
3. **Docker Internal Networks**: Isolated per stack

**Future Segmentation** (if VLANs deployed):
1. **Server VLAN**: Infrastructure hosts
2. **IoT VLAN**: Smart home devices (isolated)
3. **Guest VLAN**: Guest WiFi (internet only)
4. **DMZ VLAN**: Public-facing services (if needed)

---

### Access Control

**Network Access Policies**:
- FreeIPA enforces host-based access control (HBAC)
- SSH key-based authentication only (no passwords)
- VPN required for external access
- Fail2ban on all internet-facing hosts
- Rate limiting on reverse proxy (Traefik)

**Service Exposure**:
- Internal services: Accessible only via VPN
- Public services: Exposed through OCI DMZ via WireGuard
- Minimal port forwarding on primary router

---

## Bandwidth & Performance

### ISP Connection

**Primary Internet**:
- Provider: (ISP name)
- Speed: (Download / Upload, e.g., 1Gbps / 1Gbps fiber)
- IP: Dynamic or static?
- IPv6: Supported?

**Performance**:
- Typical latency: <10ms to ISP, ~30-50ms to internet
- Typical throughput: 95%+ of advertised speeds
- Uptime: 99.9%+ (typical residential/business)

---

### Internal Network Performance

**LAN Performance**:
- Switch backplane: Gigabit (1Gbps) or 10Gbps?
- Typical throughput: 900-950Mbps (gigabit)
- Latency: <1ms local LAN
- Bonded NICs: 2Gbps aggregate (Proxmox, NAS)

**Storage Network (NFS)**:
- Synology NAS → Docker hosts
- Throughput: 100-200MB/s typical (gigabit)
- With M.2 cache: 200-400MB/s reads
- Bonded NICs improve aggregate throughput

**VPN Performance**:
- Tailscale: Near-native speeds (direct peer-to-peer)
- WireGuard: 500-900Mbps (depending on CPU)

---

## Network Topology Documentation

### Logical Topology Diagram

```
                          Internet
                             ▲
                             │
                    ┌────────┴────────┐
                    │   Gateway/NAT   │
                    │    Firewall     │
                    └────────┬────────┘
                             │ 10.2.0.1
                    ┌────────┴────────┐
                    │  Core Switch    │
                    │  10.2.0.0/24    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌─────▼─────┐       ┌─────▼──────┐
   │ Proxmox │         │    NAS    │       │ Pi Devices │
   │  Host   │         │ 10.2.0.200│       │ 10.2.0.x   │
   └────┬────┘         └───────────┘       └────────────┘
        │
        │ VMs/LXCs
        │
   ┌────▼──────────────────────────┐
   │  VMs: genesis, hercules, etc  │
   │  LXCs: postgres, homeassist   │
   └───────────────────────────────┘

   Overlay: Tailscale Mesh (100.x.x.x/16)
   ┌──────────────────────────────────────┐
   │ All 13 hosts in encrypted mesh       │
   │ Includes: OCI Cloud, Remote Edge     │
   └──────────────────────────────────────┘

   Site-to-Site: WireGuard (100.90.0.0/16)
   ┌──────────────────────────────────────┐
   │ Amethyst Gateway ↔ OCI DMZ           │
   │ Persistent tunnel for public services│
   └──────────────────────────────────────┘
```

---

### Physical Topology

```
ISP Modem/ONT
      │
      │ Fiber/Ethernet
      │
   Gateway
   Router
      │
      ├─── Core Switch ──┬─── Proxmox Host (bonded NICs)
      │                  ├─── Synology NAS (bonded NICs)
      │                  ├─── Raspberry Pis (single NIC each)
      │                  ├─── Access Point 1 (PoE)
      │                  └─── Access Point 2 (PoE)
      │
      └─── Workstations, Printers, etc.
```

---

## Network Configuration Files

### Key Configuration Locations

**Router/Gateway**:
- Configuration: Web UI or CLI (model-specific)
- Backup: Regular config exports

**Hosts (Ubuntu/Debian)**:
- Network config: `/etc/netplan/*.yaml` (Ubuntu)
- Or: `/etc/network/interfaces` (Debian)
- DNS config: `/etc/resolv.conf` (managed by systemd-resolved)

**FreeIPA DNS**:
- Zone data: LDAP-backed (not flat files)
- Management: `ipa dnszone-*`, `ipa dnsrecord-*` commands

**Tailscale**:
- Service: `/etc/default/tailscaled`
- State: `/var/lib/tailscale/`

**WireGuard**:
- Config: `/etc/wireguard/wg0.conf` (per host)
- Service: `wg-quick@wg0.service`

**Docker Networks**:
- Docker Compose: `networks:` section in compose files
- CLI: `docker network create ...`

---

## Troubleshooting

### Network Connectivity Issues

**Check Network Status**:
```bash
# Interface status
ip addr show
ip link show

# Routing table
ip route show

# DNS resolution
nslookup ipa1.int.badger-dev.com
dig ipa1.int.badger-dev.com

# Ping gateway
ping 10.2.0.1

# Ping external
ping 1.1.1.1

# Traceroute
traceroute google.com
```

**Check Firewall Rules**:
```bash
# UFW status
sudo ufw status verbose

# List iptables rules
sudo iptables -L -n -v
```

**Check VPN Status**:
```bash
# Tailscale
sudo tailscale status
sudo tailscale ping <hostname>

# WireGuard
sudo wg show
sudo wg show wg0
```

**DNS Troubleshooting**:
```bash
# Check DNS servers
cat /etc/resolv.conf

# Test DNS resolution
dig @10.2.0.20 ipa1.int.badger-dev.com
nslookup ipa1.int.badger-dev.com 10.2.0.20

# Check FreeIPA DNS
ssh ipa1.int.badger-dev.com
sudo ipa dnszone-show int.badger-dev.com
```

---

### Performance Issues

**Check Bandwidth**:
```bash
# iperf3 test (between two hosts)
# Server:
iperf3 -s

# Client:
iperf3 -c <server-ip>

# Network statistics
netstat -i
ip -s link

# Monitor real-time traffic
sudo iftop
sudo nethogs
```

**Check Latency**:
```bash
# Ping local gateway
ping -c 10 10.2.0.1

# Ping DNS server
ping -c 10 10.2.0.20

# MTR (My TraceRoute)
mtr google.com
```

---

## Change Management

### Network Change Procedures

1. **Plan Change**:
   - Document change details
   - Identify affected systems
   - Plan rollback procedure

2. **Schedule Maintenance**:
   - Notify users/stakeholders
   - Schedule during low-traffic window
   - Ensure physical access if needed

3. **Implement Change**:
   - Execute changes systematically
   - Test connectivity after each step
   - Monitor for issues

4. **Verify**:
   - Test affected services
   - Verify monitoring metrics
   - Confirm rollback procedure

5. **Document**:
   - Update network documentation
   - Record change in change log
   - Update network diagrams if needed

---

### Maintenance Schedule

**Daily** (Automated):
- Monitor VPN tunnel status
- DNS resolution checks
- Network device availability

**Weekly**:
- Review network metrics and bandwidth
- Check firewall logs for anomalies
- Verify backup VPN routes

**Monthly**:
- Review and optimize firewall rules
- Update network documentation
- Check for firmware updates (router, switches)

**Quarterly**:
- Network capacity planning
- Security audit (firewall, VPN configs)
- Update network topology diagrams

---

## Related Documentation

- [[Infrastructure MOC]] - Infrastructure overview
- [[Hosts Inventory]] - Host inventory and IPs
- [[Security/Security MOC]] - Network security
- [[Network/VPN]] - VPN configuration details
- [[Network/DNS]] - DNS infrastructure details
- [[Security/Firewall Rules]] - Firewall configuration
- [[Monitoring/Monitoring MOC]] - Network monitoring

---

**Last Updated**: 2025-11-27
**Network Baseline**: Established 2025-11-27
**Maintained By**: Infrastructure Team
**Review Schedule**: Quarterly or on network changes
