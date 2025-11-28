---
title: Hardware Infrastructure
tags: [infrastructure, hardware, specifications]
created: 2025-01-23
updated: 2025-01-23
---

# Hardware Infrastructure

Physical hardware inventory and specifications for the Badger Development homelab infrastructure across on-premises, cloud, and edge locations.

## Quick Reference

**Total Physical Hardware**:
- 1 Proxmox hypervisor host
- 4 Raspberry Pi devices
- 1 Synology NAS
- 2 Oracle Cloud VMs (cloud infrastructure)
- Network equipment (switches, router, access points)

## Compute Hardware

### Proxmox Hypervisor Host

**Primary Virtualization Server**

```yaml
Purpose: Proxmox VE hypervisor
Location: Amethyst on-premises data center
Form Factor: Tower/Rack server
Status: Production
```

**Specifications** (Update with actual specs):
- **CPU**: Intel Xeon / AMD Ryzen (details needed)
- **Cores**: 16+ cores / 32+ threads
- **Memory**: 64GB+ DDR4 ECC RAM (expandable)
- **Storage**:
  - Boot: 256GB+ SSD (Proxmox OS)
  - VM Storage: 1TB+ NVMe/SSD (VM disks and LXC containers)
  - Backup: Network-attached (Synology NAS)
- **Network**:
  - 2x 1Gbps Ethernet (link aggregation capable)
  - or 1x 10Gbps Ethernet
- **Management**: IPMI/iLO for remote management

**Hosted Workloads**:
- 4 Virtual Machines (genesis, hercules, codewizard, +1)
- 3 LXC Containers (postgres-svr, homeassistant, pihole-backup)

**Expansion Capacity**:
- RAM slots: Available for expansion to 128GB+
- PCIe slots: Available for additional NICs, storage controllers
- Drive bays: Available for additional storage

**Power & Cooling**:
- Power Supply: Redundant PSU (if equipped)
- Power consumption: ~200-400W typical load
- Cooling: Active cooling with multiple fans
- UPS backup: Connected to UPS for power protection

See [[Proxmox]] for virtualization configuration details.

---

### Raspberry Pi Devices

#### apollo - Monitoring Hub

```yaml
Model: Raspberry Pi 4 Model B
Location: Amethyst on-premises
Purpose: Central monitoring and observability hub
Status: Production - Critical
```

**Specifications**:
- **CPU**: Broadcom BCM2711, Quad-core Cortex-A72 (ARM v8) @ 1.5GHz
- **Memory**: 8GB LPDDR4-3200 SDRAM
- **Storage**:
  - Primary: 128GB MicroSD card (A2-rated, high endurance)
  - Secondary: 256GB USB 3.0 SSD (for monitoring data)
- **Network**: Gigabit Ethernet (via USB 3.0)
- **USB**: 2x USB 3.0, 2x USB 2.0
- **GPIO**: 40-pin header (unused)
- **Power**: Official 15W USB-C power supply

**Storage Layout**:
```
MicroSD (128GB): OS and application binaries
USB SSD (256GB):
  ├── /data/beszel     # Beszel monitoring data
  ├── /data/netalertx  # Network monitoring data
  └── /data/logs       # Aggregated logs
```

**Hosted Services**:
- Beszel monitoring hub (infrastructure metrics)
- NetAlertX network monitoring
- Docker runtime
- Monitoring stack agents

**Power Consumption**: ~5-8W typical load

**Cooling**: Passive heatsink + optional fan (if case supports)

**Maintenance Notes**:
- MicroSD card: High-endurance card recommended, replace annually
- USB SSD: Monitor SMART data for health
- Regular backups of monitoring configuration

---

#### ipa1 - FreeIPA Identity Server

```yaml
Model: Raspberry Pi 4 Model B
Location: Amethyst on-premises
Purpose: FreeIPA identity management server
Status: Production - CRITICAL ⚠️
```

**Specifications**:
- **CPU**: Broadcom BCM2711, Quad-core Cortex-A72 (ARM v8) @ 1.5GHz
- **Memory**: 8GB LPDDR4-3200 SDRAM
- **Storage**:
  - Primary: 256GB USB 3.0 SSD (FreeIPA databases and CA)
  - No MicroSD: USB boot configured
- **Network**: Gigabit Ethernet (via USB 3.0)
- **USB**: SSD on USB 3.0 port
- **Power**: Official 15W USB-C power supply + UPS backup

**Storage Layout**:
```
USB SSD (256GB):
  ├── /var/lib/dirsrv     # 389 Directory Server data
  ├── /var/lib/ipa        # FreeIPA data
  ├── /var/kerberos       # Kerberos KDC data
  └── /var/lib/pki        # Dogtag CA certificates
```

**Critical Infrastructure Role**:
- **SPOF Warning**: Single point of failure for authentication
- All 13 hosts depend on this server for authentication
- Loss of this host breaks login for entire infrastructure

**Hosted Services**:
- FreeIPA server (identity management)
- 389 Directory Server (LDAP)
- Kerberos KDC
- Dogtag CA (certificate authority)
- BIND DNS server
- Apache HTTP Server (web UI)

**Power Consumption**: ~6-10W typical load

**High Availability Considerations**:
- **Current**: Single instance (no replica)
- **Recommended**: Add ipa2 replica on Proxmox LXC
- **Backup Strategy**: Daily ipa-backup + offsite replication

**Cooling**: Active cooling recommended (fan + heatsink)

**Maintenance Notes**:
- SSD health monitoring: Critical (monthly SMART checks)
- UPS protection: Required
- Backup verification: Weekly
- Disaster recovery testing: Monthly

See [[Security/FreeIPA]] for complete FreeIPA documentation.

---

#### sentinel - Services Host

```yaml
Model: Raspberry Pi 4 Model B
Location: Amethyst on-premises
Purpose: General-purpose service host
Status: Production
```

**Specifications**:
- **CPU**: Broadcom BCM2711, Quad-core Cortex-A72 (ARM v8) @ 1.5GHz
- **Memory**: 4GB LPDDR4-3200 SDRAM
- **Storage**: 64GB MicroSD card (A2-rated)
- **Network**: Gigabit Ethernet (via USB 3.0)
- **Power**: Official 15W USB-C power supply

**Hosted Services**:
- Docker runtime
- Containerized services
- ARM64 workload testing

**Power Consumption**: ~4-6W typical load

**Cooling**: Passive heatsink

---

#### meade - Remote Edge Host

```yaml
Model: Raspberry Pi 4 Model B
Location: Remote edge location (Meade)
Purpose: Remote monitoring and edge computing
Status: Production
```

**Specifications**:
- **CPU**: Broadcom BCM2711, Quad-core Cortex-A72 (ARM v8) @ 1.5GHz
- **Memory**: 8GB LPDDR4-3200 SDRAM
- **Storage**: 128GB MicroSD card (A2-rated, high endurance)
- **Network**: Gigabit Ethernet (residential ISP)
- **Power**: Official 15W USB-C power supply

**Hosted Services**:
- Docker runtime
- Beszel agent (reports to apollo)
- Dozzle agent (reports to hercules)
- Edge-specific services

**Power Consumption**: ~5-8W typical load

**Remote Considerations**:
- No physical access for troubleshooting
- Dependent on residential internet
- Tailscale VPN for connectivity

**Cooling**: Passive heatsink

---

## Storage Hardware

### Synology NAS

```yaml
Model: Synology DiskStation DS920+ (or similar)
Location: Amethyst on-premises
Purpose: Network-attached storage, Docker host
Status: Production - High Priority
```

**Hardware Specifications**:
- **CPU**: Intel Celeron J4125, Quad-core @ 2.0-2.7GHz
- **Memory**: 8GB DDR4 SO-DIMM (upgradeable to 16GB+)
- **Drive Bays**: 4x 3.5" SATA HDD bays
- **M.2 Slots**: 2x M.2 2280 NVMe slots (SSD cache)
- **Network**: 2x Gigabit Ethernet (link aggregation capable)
- **USB**: 2x USB 3.2 Gen 1
- **eSATA**: 1x eSATA port (expansion)

**Storage Configuration**:

**Installed Drives** (Update with actual configuration):
```
Bay 1: 8TB WD Red Plus (CMR)
Bay 2: 8TB WD Red Plus (CMR)
Bay 3: 8TB WD Red Plus (CMR)
Bay 4: 8TB WD Red Plus (CMR)

RAID Configuration: SHR-1 (Synology Hybrid RAID with 1-disk fault tolerance)
  - Usable Capacity: ~22TB (after RAID overhead)
  - Redundancy: 1-disk failure tolerance
  - Performance: Balanced read/write

M.2 Cache:
  - Slot 1: 500GB NVMe SSD (read/write cache)
  - Slot 2: 500GB NVMe SSD (read/write cache - mirrored)
```

**Volume Layout**:
```
/volume1/ (22TB usable)
  ├── docker/               # Docker volumes (~5TB)
  │   ├── hercules/        # Volumes for primary host
  │   ├── codewizard/      # Development volumes
  │   └── synology/        # Local NAS containers
  ├── backups/             # Kopia repository (~8TB)
  │   ├── kopia-repo/      # Encrypted backup repository
  │   └── snapshots/       # BTRFS snapshots
  ├── media/               # Media library (~5TB)
  │   ├── photos/
  │   ├── videos/
  │   └── music/
  └── shares/              # User shares (~2TB)
      ├── documents/
      └── archives/
```

**Network Configuration**:
- Link aggregation (802.3ad / LACP)
- Bonded NICs: 2x 1Gbps = 2Gbps aggregate
- NFS server for Docker volumes
- SMB/CIFS for user shares

**Performance Specifications**:
- Sequential Read: ~220 MB/s (HDD), 400+ MB/s (with cache)
- Sequential Write: ~200 MB/s (HDD), 350+ MB/s (with cache)
- Random IOPS: Significantly improved with M.2 cache
- Network throughput: 2Gbps (bonded)

**Power & Cooling**:
- Power consumption:
  - Idle: ~30W
  - Active (all drives): ~60W
  - Peak: ~90W
- Cooling: Multiple 92mm fans (automatic speed control)
- UPS backup: Connected for graceful shutdown

**Backup Strategy**:
- **RAID protection**: SHR-1 (1-disk fault tolerance)
- **Snapshots**: BTRFS snapshots (hourly/daily/weekly)
- **Off-site**: Critical data synced to Backblaze B2
- **Kopia repository**: Hosts backup repo for all infrastructure

**Disk Health Monitoring**:
- SMART monitoring enabled
- Email alerts for disk warnings/failures
- Monthly SMART extended tests
- Annual disk replacement strategy

**Expansion Options**:
- DX517 expansion unit (5 additional bays)
- eSATA or USB 3.2 for external storage
- M.2 cache expansion (if not already installed)

See [[Backups/Backups MOC]] for backup configuration details.

---

## Network Hardware

### Router

```yaml
Device: (Update with actual router model)
Location: Amethyst network edge
Purpose: Gateway, routing, VPN
Status: Production
```

**Specifications** (Example - update with actual):
- **Model**: UniFi Dream Machine Pro / pfSense box / EdgeRouter
- **Routing Performance**: 1-10Gbps
- **WAN**: 1Gbps fiber
- **LAN**: Multi-gigabit switch integration
- **VPN**: WireGuard, OpenVPN support
- **Features**:
  - VLAN support
  - QoS (Quality of Service)
  - Firewall rules
  - NAT/PAT
  - DHCP server
  - DNS forwarding to FreeIPA

**Network Segments**:
```
WAN: ISP connection
LAN: 10.2.0.0/24 (management)
VLANs: (if configured)
  - VLAN 10: Servers
  - VLAN 20: IoT devices
  - VLAN 30: Guest network
```

---

### Switch(es)

```yaml
Device: (Update with actual switch model/count)
Location: Amethyst network core
Purpose: Layer 2/3 switching
Status: Production
```

**Specifications** (Example - update with actual):
- **Model**: UniFi Switch 24 PoE / managed switch
- **Ports**: 24x Gigabit Ethernet
- **PoE**: 802.3af/at on select ports
- **Uplink**: 2x SFP+ 10Gbps (optional)
- **Management**: Web UI, SNMP, CLI
- **Features**:
  - VLAN support
  - Link aggregation (LACP)
  - Port mirroring
  - Spanning tree protocol
  - PoE budget: 150-250W

**Port Allocation** (Example):
```
Port 1-4:   Proxmox host (bonded/LACP)
Port 5-6:   Synology NAS (bonded/LACP)
Port 7:     Router uplink
Port 8-11:  Raspberry Pi devices
Port 12-15: Access points (PoE)
Port 16-24: Workstations, printers, misc
```

---

### Wireless Access Points

```yaml
Device: (Update with actual AP model/count)
Location: Distributed across premises
Purpose: WiFi coverage
Status: Production
```

**Specifications** (Example - update with actual):
- **Model**: UniFi AP-AC-PRO / similar
- **Count**: 2-3 units
- **Standards**: 802.11ac Wave 2 (WiFi 5) or 802.11ax (WiFi 6)
- **Bands**: Dual-band (2.4GHz + 5GHz)
- **Power**: PoE (802.3af/at)
- **Management**: UniFi Controller / standalone

**Coverage**:
- AP 1: Main area
- AP 2: Secondary area
- AP 3: Guest/IoT network

---

## Power Infrastructure

### Uninterruptible Power Supply (UPS)

```yaml
Purpose: Power protection and graceful shutdown
Location: Amethyst data center
Status: Critical Infrastructure
```

**Specifications** (Update with actual):
- **Model**: APC Back-UPS / CyberPower / Tripp Lite
- **Capacity**: 1500VA / 900W (example)
- **Runtime**: 15-30 minutes at 50% load
- **Outlets**: 8-10 outlets (battery backup + surge only)
- **Communication**: USB monitoring to management host
- **Features**:
  - Automatic voltage regulation (AVR)
  - Pure sine wave output
  - LCD display
  - Audible alarms

**Protected Equipment**:
- Proxmox hypervisor host
- Synology NAS
- Network equipment (router, switches)
- FreeIPA server (ipa1) - CRITICAL
- apollo monitoring hub

**UPS Monitoring**:
- Connected to genesis or hercules via USB
- NUT (Network UPS Tools) for monitoring
- Automated graceful shutdown on low battery
- Email/SMS alerts for power events

**Battery Maintenance**:
- Expected battery life: 3-5 years
- Annual battery load test
- Replacement schedule: Every 3 years or as needed

**Power Event Procedures**:
1. **Short outage (<15 min)**: UPS provides power, no action needed
2. **Extended outage (>15 min)**: Automated graceful shutdown sequence
3. **Post-outage**: Manual verification and restart procedures

---

### Power Distribution

**Primary Power**:
- Dedicated 20A circuit for server equipment
- Separate circuits for network equipment
- Surge protection at panel and UPS

**Power Consumption Summary**:
```
Proxmox Host:      ~300W typical, 500W peak
Synology NAS:      ~60W typical, 90W peak
Raspberry Pis (4): ~24W total typical
Network Equipment: ~50W typical
Total Load:        ~450W typical, ~700W peak
UPS Capacity:      900W (example)
```

---

## Cooling & Environmental

### Cooling Strategy

**Active Cooling**:
- Equipment room AC or ventilation
- Individual device fans (automatic speed control)
- Rack ventilation (if rack-mounted)

**Temperature Monitoring**:
- Proxmox host: CPU, motherboard sensors
- Synology NAS: Drive temps, system temp
- Raspberry Pis: CPU temperature monitoring
- Network equipment: Built-in sensors

**Target Temperatures**:
- Ambient room: 18-24°C (64-75°F)
- Equipment operating: <70°C CPU, <50°C drives
- Alert thresholds: >80°C CPU, >60°C drives

**Monitoring**:
- Beszel collects temperature metrics
- SMART data for drive temperatures
- Automated alerts for high temps

---

## Hardware Lifecycle Management

### Warranty & Support

| Device | Purchase Date | Warranty | End of Life | Replacement Plan |
|--------|---------------|----------|-------------|------------------|
| Proxmox Host | TBD | 3-5 years | TBD | TBD |
| Synology NAS | TBD | 3 years | TBD+7 years | 2030+ |
| Raspberry Pis | TBD | 1 year | N/A | Replace as needed |
| Network Equipment | TBD | 1-3 years | TBD | TBD |

### Maintenance Schedule

**Monthly**:
- Review SMART data for all drives
- Check UPS battery status
- Verify cooling and temperatures
- Physical inspection of equipment

**Quarterly**:
- Clean dust from equipment
- Verify all fans operational
- Check cable management
- Update hardware inventory

**Annually**:
- Deep clean of equipment
- Thermal paste replacement (if needed)
- UPS battery load test
- Firmware updates for all devices
- Review and update documentation

### Hardware Refresh Cycle

**Expected Lifespan**:
- **Proxmox Host**: 5-7 years
- **Synology NAS**: 7-10 years (drives: 3-5 years)
- **Raspberry Pis**: 3-5 years (MicroSD: 1-2 years)
- **Network Equipment**: 5-7 years
- **UPS Batteries**: 3-5 years

**Replacement Triggers**:
- End of manufacturer support
- Insufficient performance for workloads
- Frequent hardware failures
- No longer cost-effective to maintain

---

## Expansion Planning

### Current Capacity Utilization

**Compute**:
- Proxmox Host: ~60% CPU, ~70% RAM utilized
- Capacity for 2-3 additional VMs or 5-10 LXC containers

**Storage**:
- Synology NAS: ~40% utilized (~9TB used of 22TB)
- Expansion option: DX517 (5 additional bays)

**Network**:
- Switch ports: ~60% utilized
- Bandwidth: Adequate for current workloads

### Planned Expansions

**Short Term (1 year)**:
- Add FreeIPA replica (ipa2) on Proxmox LXC
- Additional M.2 cache for Synology (if not installed)
- UPS capacity expansion if needed

**Medium Term (2-3 years)**:
- Proxmox host RAM upgrade (if needed)
- Additional Raspberry Pi for testing/development
- Network upgrade to 2.5Gbps or 10Gbps (selective)

**Long Term (3-5 years)**:
- Proxmox host replacement or clustering
- Synology NAS capacity expansion (DX517)
- Network equipment refresh

---

## Troubleshooting

### Common Hardware Issues

**Proxmox Host Issues**:
```bash
# Check hardware health
sensors  # Temperature sensors
smartctl -a /dev/sda  # Disk health
dmesg | grep -i error  # Kernel errors
journalctl -xe  # System logs

# Memory test (from boot)
# Add memtest86+ to GRUB menu
```

**Synology NAS Issues**:
- **Dashboard**: Monitor drives, temperature, resource usage
- **SMART Data**: Storage Manager → HDD/SSD → Health Info
- **Logs**: Log Center for system and hardware events
- **Beep codes**: Refer to Synology beep code guide

**Raspberry Pi Issues**:
```bash
# Check temperature
vcgencmd measure_temp

# Check throttling
vcgencmd get_throttled

# Check power supply
vcgencmd get_throttled  # 0x0 = good, 0x50000 = under-voltage

# Storage health (MicroSD/SSD)
sudo badblocks -v /dev/mmcblk0  # Check for bad blocks
```

**Network Equipment Issues**:
- Check link lights and port status
- Review switch logs for errors
- Verify VLAN configuration
- Check for firmware updates

---

## Disaster Recovery

### Critical Hardware Failures

**Proxmox Host Failure**:
1. Restore VMs from Proxmox backups to new host
2. Expected recovery time: 4-6 hours
3. Critical VMs: hercules, postgres-svr, ipa1 (if VM-based)

**Synology NAS Failure**:
1. **Single disk failure**: Replace disk, RAID rebuild
2. **Complete failure**: New NAS + restore from Kopia/B2
3. Expected recovery time: 8-24 hours (depends on data size)

**FreeIPA Server (ipa1) Failure**:
1. Restore from ipa-backup to new Raspberry Pi or VM
2. Restore FreeIPA configuration and data
3. Update DNS records if IP changed
4. Re-enroll clients if necessary
5. Expected recovery time: 2-4 hours
6. **CRITICAL**: All authentication depends on this

**Network Equipment Failure**:
1. Replace with spare or new equipment
2. Restore configuration from backup
3. Verify connectivity and VLANs
4. Expected recovery time: 1-2 hours

### Hardware Spares

**Recommended Spare Parts**:
- 1x Spare HDD (matching NAS drives)
- 1x Spare MicroSD card (pre-imaged)
- 1x Spare Raspberry Pi (optional but recommended)
- 1x Spare power supply (Raspberry Pi USB-C)
- Network cables and adapters

---

## Related Documentation

- [[Infrastructure MOC]] - Infrastructure overview
- [[Hosts Inventory]] - Host inventory and specifications
- [[Proxmox]] - Virtualization platform
- [[Network Topology]] - Network architecture
- [[Backups/Backups MOC]] - Backup strategy
- [[Monitoring/Monitoring MOC]] - Hardware monitoring

---

**Last Updated**: 2025-01-23
**Maintained By**: Infrastructure Team
**Review Schedule**: Quarterly or on hardware changes
**Next Hardware Review**: TBD
