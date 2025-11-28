---
title: Install FreeIPA Server
tags: [freeipa, security, authentication, dns, installation]
created: 2025-11-27
updated: 2025-11-27
---

# Install FreeIPA Server

Complete installation guide for FreeIPA identity management server on Raspberry Pi 4 with AlmaLinux 9. This deployment provides centralized authentication, LDAP directory services, Kerberos KDC, and integrated DNS management for the Badger Development homelab.

**Target System**: Raspberry Pi 4 Model B, 8GB RAM, 256GB USB SSD  
**Operating System**: AlmaLinux 9 (ARM64)  
**Realm**: `BADGER-DEV.COM`  
**DNS Domain**: `int.badger-dev.com`  
**Hostname**: `ipa1.int.badger-dev.com`  
**IP Address**: `10.2.0.53`

> **Critical Infrastructure Warning**: This server becomes the single point of failure for all authentication. Plan for high availability with a replica before production deployment.

## Installation Overview

FreeIPA provides:
- **LDAP Directory Service**: 389 Directory Server for user and group management
- **Kerberos KDC**: Centralized authentication with ticket-based security
- **Certificate Authority**: Dogtag CA for X.509 certificate management
- **DNS Integration**: BIND DNS server with automatic zone management
- **Web UI**: Administrative interface for user and service management
- **SSH Integration**: Centralized SSH key management and access control

## Prerequisites

### Hardware Requirements
- **CPU**: ARM64 (Raspberry Pi 4 recommended)
- **RAM**: Minimum 4GB, 8GB recommended for production
- **Storage**: Minimum 64GB, 256GB+ SSD recommended for database growth
- **Network**: Stable network connection with static IP

### Software Requirements
- **Operating System**: AlmaLinux 9 (ARM64)
- **Time Sync**: NTP/chrony service (critical for Kerberos)
- **Firewall**: firewalld running and enabled
- **SELinux**: Enforcing mode (recommended)

### Network Preparation
- **Static IP**: 10.2.0.53
- **DNS Resolution**: Able to resolve own hostname
- **Time Sync**: Synchronized with reliable NTP sources
- **Firewall**: Ability to open required ports

---

## Step 1: System Preparation

### Update and Reboot
```bash
# Update all packages
sudo dnf update -y

# Reboot if kernel updates were applied
sudo reboot
```

### Set Hostname
```bash
# Set the fully qualified domain name
sudo hostnamectl set-hostname ipa1.int.badger-dev.com

# Verify the hostname
hostnamectl
```

### Configure /etc/hosts
Add static mapping for the FreeIPA server (replace with actual IP):

```bash
# Backup original /etc/hosts
sudo cp /etc/hosts /etc/hosts.backup

# Add IPA server entry
echo "10.2.0.53 ipa1.int.badger-dev.com ipa1" | sudo tee -a /etc/hosts

# Verify the entry
grep ipa1 /etc/hosts
```

### Verify Network Configuration
```bash
# Check IP address
ip addr show

# Test hostname resolution
hostname -f

# Test network connectivity
ping 10.2.0.1
```

---

## Step 2: Time Synchronization (Critical)

Kerberos is extremely sensitive to time differences. Ensure proper NTP configuration:

```bash
# Check chrony status
sudo chronyc tracking

# Check time sources
sudo chronyc sources -v

# Force time sync if needed
sudo chronyc -a makestep

# Enable chrony service
sudo systemctl enable --now chronyd
```

**Time Requirements**:
- All hosts must be within 5 minutes of each other
- Recommended time accuracy: ±1 second
- Use reliable NTP sources
- Monitor time drift regularly

---

## Step 3: SELinux and Firewall Setup

### Verify SELinux Status
```bash
# Check current mode
getenforce

# Should return "Enforcing" (recommended)
```

**Do NOT disable SELinux**. FreeIPA is designed to work with SELinux enforcing and provides appropriate policies.

### Configure Firewall
Open required ports for FreeIPA services:

```bash
# Open required services
sudo firewall-cmd --add-service={http,https,dns,ntp,freeipa-ldap,freeipa-ldaps,freeipa-replication} --permanent

# Open specific ports for complex deployments
sudo firewall-cmd --add-port={53/tcp,53/udp,80/tcp,443/tcp,389/tcp,636/tcp,88/tcp,88/udp,464/tcp,464/udp,123/udp} --permanent

# Reload firewall configuration
sudo firewall-cmd --reload

# Verify opened ports
sudo firewall-cmd --list-all
```

**Port Breakdown**:
- `80/tcp`: HTTP (redirects to HTTPS)
- `443/tcp`: HTTPS (Web UI)
- `53/tcp/udp`: DNS (BIND)
- `88/tcp/udp`: Kerberos KDC
- `389/tcp`: LDAP
- `636/tcp`: LDAPS (LDAP over TLS)
- `464/tcp/udp`: Kerberos password change
- `123/udp`: NTP time sync

---

## Step 4: Install FreeIPA Server Packages

### Install Core Packages
```bash
# Install FreeIPA server with DNS support
sudo dnf install -y freeipa-server freeipa-server-dns

# This installs all dependencies:
# - freeipa-server: Core server components
# - freeipa-server-dns: BIND DNS integration
# - 389-ds-base: LDAP directory server
# - bind: DNS server
# - krb5-server: Kerberos KDC
# - dogtag-pki: Certificate Authority
# - httpd: Apache web server
```

### Verify Installation
```bash
# Check installed packages
rpm -qa | grep -E "freeipa|389|bind|krb5"

# Verify version compatibility
rpm -q freeipa-server
```

---

## Step 5: DNS Configuration (Optional but Recommended)

### Configure Forwarders
Decide on DNS forwarders for external name resolution:

```bash
# Test DNS forwarder connectivity
dig @1.1.1.1 google.com
dig @8.8.8.8 google.com
```

**Recommended Forwarders**:
- Primary: `1.1.1.1` (Cloudflare)
- Secondary: `8.8.8.8` (Google)
- Tertiary: `9.9.9.9` (Quad9)

### Create Reverse Zone File
Prepare reverse DNS zone for your network:

```bash
# For network 10.2.0.0/24, reverse zone is: 2.10.in-addr.arpa
# This will be configured during ipa-server-install
```

---

## Step 6: Run FreeIPA Server Installation

### Interactive Installation (Recommended for First Time)
```bash
# Start interactive installation
sudo ipa-server-install --setup-dns
```

**Interactive Prompts**:
1. **Continue with configuration of this server?** → `yes`
2. **Server host name** → `ipa1.int.badger-dev.com` (verify correct)
3. **Domain name** → `int.badger-dev.com`
4. **Realm name** → `BADGER-DEV.COM`
5. **Directory Manager password** → Create strong password (store securely)
6. **IPA admin password** → Create admin password (store securely)
7. **Do you want to configure integrated DNS?** → `yes`
8. **DNS forwarders** → `1.1.1.1,8.8.8.8` (or your preference)
9. **Do you want to configure reverse zone?** → `yes`
10. **Reverse zone name** → `2.10.in-addr.arpa` (for 10.2.0.0/24)
11. **Continue to configure the system with these values?** → `yes`

### Automated Installation (for Scripting)
```bash
sudo ipa-server-install \
  --setup-dns \
  --realm=BADGER-DEV.COM \
  --domain=int.badger-dev.com \
  --hostname=ipa1.int.badger-dev.com \
  --ds-password="DirectoryManagerPassword" \
  --admin-password="AdminPassword" \
  --dns-forwarder=1.1.1.1 \
  --dns-forwarder=8.8.8.8 \
  --no-reverse \
  --mkhomedir \
  --no-ntp
```

**Important Notes**:
- Replace passwords with actual strong passwords
- Store passwords securely (password manager)
- `--no-ntp` assumes chrony is already configured
- `--no-reverse` if not creating reverse zone initially

---

## Step 7: Post-Installation Verification

### Check Service Status
```bash
# Verify all FreeIPA services are running
sudo ipa-server-status

# Check individual services
sudo systemctl status ipa
sudo systemctl status httpd
sudo systemctl status named
sudo systemctl status krb5kdc
sudo systemctl status dirsrv@BADGER-DEV-COM
```

### Verify Kerberos Authentication
```bash
# Obtain Kerberos ticket for admin user
kinit admin

# Verify ticket
klist

# Test kadmin (Kerberos admin interface)
kadmin.local -q "listprincs"
```

### Verify DNS Functionality
```bash
# Test forward DNS resolution
dig @localhost ipa1.int.badger-dev.com A

# Test reverse DNS resolution
dig @localhost -x 10.2.0.53

# Test DNS services
dig @localhost _kerberos._udp.int.badger-dev.com SRV
dig @localhost _ldap._tcp.int.badger-dev.com SRV
```

### Test LDAP Service
```bash
# Test LDAP directory service
ldapsearch -x -H ldap://ipa1.int.badger-dev.com -s base "(objectclass=*)"

# Test LDAP over TLS (if certificate is configured)
ldapsearch -x -H ldaps://ipa1.int.badger-dev.com -s base "(objectclass=*)"
```

---

## Step 8: Access Web Interface

### Browser Access
Open web browser and navigate to:
```
https://ipa1.int.badger-dev.com/ipa/ui
```

**Login Credentials**:
- Username: `admin`
- Password: Admin password set during installation

**Web Interface Features**:
- User and group management
- Host enrollment and management
- DNS zone management
- Certificate management
- Policy configuration
- Audit log viewing

### Certificate Warning
You'll see a certificate warning because FreeIPA uses a self-signed certificate by default. This is expected. Add an exception in your browser or import the CA certificate.

```bash
# Export CA certificate for browser import
sudo cp /etc/ipa/ca.crt /tmp/
# Copy /tmp/ca.crt to your workstation and import into browser
```

---

## Step 9: Initial Configuration

### Set Up DNS Zones
```bash
# DNS management via command line
ipa dnszone-find
ipa dnsrecord-add int.badger-dev.com www --a-rec 10.2.0.70
ipa dnsrecord-add int.badger-dev.com hercules --a-rec 10.2.0.70
```

### Create Initial Users
```bash
# Create a regular user
ipa user-add daniel \
  --first=Daniel \
  --last=Schmeichel \
  --email=daniel@badger-dev.com \
  --loginshell=/bin/bash

# Set user password
ipa user-mod daniel --password
```

### Create Groups
```bash
# Create administrative group
ipa group-add it-admins --desc="IT Administrators"

# Add user to group
ipa group-add-member it-admins --users=daniel
```

### SSH Key Management
```bash
# Add SSH key to user
# Generate SSH key on client first, then:
ssh-keygen -t rsa -b 4096 -C "daniel@badger-dev.com"

# Add public key to FreeIPA user account
ipa user-mod daniel --sshpubkey="ssh-rsa AAAAB3... daniel@badger-dev.com"
```

---

## Step 10: Client Enrollment Preparation

### Prerequisites for Client Enrollment
Each client needs:
1. DNS resolution pointing to FreeIPA server
2. Network connectivity to FreeIPA server
3. Proper time synchronization
4. Appropriate client packages

### Create Enrollment Host Group
```bash
# Create host group for servers
ipa hostgroup-add servers --desc="Server hosts"

# Create host group for clients
ipa hostgroup-add clients --desc="Client workstations"
```

### Prepare DNS for Client Enrollment
Ensure client hostnames resolve properly:
```bash
# Add DNS record for client
ipa dnsrecord-add int.badger-dev.com client1 --a-rec 10.2.0.100
```

---

## Step 11: Backup and Recovery

### Directory Manager Backup
```bash
# Create directory backup (as root)
sudo ipa-backup

# Verify backup
ls -la /var/lib/ipa/backup/
```

### Configuration Backup
```bash
# Backup key configuration files
sudo tar -czf /root/ipa-config-backup.tar.gz \
  /etc/ipa/ \
  /etc/dirsrv/ \
  /etc/named.* \
  /var/named/ \
  /etc/krb5.* \
  /etc/httpd/conf.d/ipa.conf
```

### Document Critical Information
Store the following securely:
- Directory Manager password
- Admin password  
- Kerberos realm information
- DNS configuration details
- Backup locations

---

## Step 12: Monitoring and Maintenance

### System Monitoring
Monitor these critical metrics:
- **Disk Space**: `/var/lib/dirsrv` grows with user data
- **Memory**: FreeIPA can use significant RAM
- **CPU**: LDAP queries and Kerberos operations
- **Network**: DNS and authentication traffic
- **Time Sync**: Critical for Kerberos operation

### Regular Maintenance Tasks
```bash
# Weekly: Check service health
sudo ipa-server-status

# Weekly: Review logs
sudo journalctl -u ipa --since "1 week ago"
sudo tail -f /var/log/dirsrv/slapd-BADGER-DEV-COM/errors

# Monthly: Check disk usage
sudo du -sh /var/lib/dirsrv/
sudo du -sh /var/log/

# Quarterly: Backup verification
sudo ipa-backup --data --online
```

### Log Locations
- **FreeIPA Logs**: `/var/log/ipa/`
- **Directory Server Logs**: `/var/log/dirsrv/slapd-BADGER-DEV-COM/`
- **Kerberos Logs**: `/var/log/krb5kdc/`
- **DNS Logs**: `/var/log/named/`
- **Apache Logs**: `/var/log/httpd/`

---

## Troubleshooting

### Common Installation Issues

**SELinux Denials**:
```bash
# Check for SELinux issues
sudo ausearch -m avc -ts recent

# Check if SELinux is blocking FreeIPA
sudo semanage fcontext -a -t cert_t "/etc/ipa/ca.crt(/.*)?"
sudo restorecon -R -v /etc/ipa/
```

**Time Synchronization Issues**:
```bash
# Force time sync
sudo chronyc -a makestep

# Check time drift
sudo chronyc tracking

# Restart chrony if needed
sudo systemctl restart chronyd
```

**DNS Resolution Issues**:
```bash
# Check DNS configuration
cat /etc/resolv.conf

# Test DNS resolution
dig ipa1.int.badger-dev.com
dig @localhost ipa1.int.badger-dev.com

# Check BIND status
sudo systemctl status named
sudo named-checkconf
```

**Service Failures**:
```bash
# Check all FreeIPA services
sudo ipa-server-status

# Restart individual services
sudo systemctl restart ipa
sudo systemctl restart httpd
sudo systemctl restart named
sudo systemctl restart krb5kdc
```

### Configuration Issues

**Certificate Problems**:
```bash
# Check certificate status
sudo getcert list

# Renew certificates if needed
sudo getcert resubmit -i (cert-id)
```

**Replication Issues** (when adding replica):
```bash
# Check replication status
ipa-replica-manage list -v ipa1.int.badger-dev.com

# Force replication if needed
ipa-replica-manage force-sync ipa1.int.badger-dev.com
```

---

## Security Considerations

### Network Security
- Firewall configured correctly
- Only expose necessary ports
- Use VPN or private network for management
- Monitor for unauthorized access attempts

### Password Security
- Strong Directory Manager password
- Strong admin password
- Password policies configured
- Regular password rotation for service accounts

### Certificate Management
- Monitor certificate expiration
- Regular certificate renewal
- Secure private key storage
- Proper CA certificate distribution

### Access Control
- Principle of least privilege
- Regular access reviews
- Administrative access limited
- Audit logging enabled

---

## Performance Optimization

### Hardware Optimization
- **SSD Storage**: Use SSD for LDAP database
- **Adequate RAM**: 8GB+ for production workloads
- **CPU**: Multi-core for concurrent authentication
- **Network**: Gigabit for fast LDAP responses

### Database Optimization
```bash
# Tune 389 Directory Server
sudo ldapmodify -D "cn=directory manager" -W <<EOF
dn: cn=config
changetype: modify
replace: nsslapd-cachememsize
nsslapd-cachememsize: 20971520
EOF
```

### DNS Optimization
- Configure appropriate DNS forwarders
- Enable DNS cache
- Monitor DNS query performance
- Consider DNS load balancing for larger deployments

---

## Next Steps

### Immediate (Post-Installation)
1. **Create user accounts** for all administrators
2. **Configure password policies**
3. **Set up group structure**
4. **Test client enrollment** on a test host
5. **Configure backup procedures**

### Short Term (1-2 weeks)
1. **Enroll all infrastructure hosts**
2. **Set up SSH key management**
3. **Configure sudo rules** via FreeIPA HBAC
4. **Set up monitoring** for FreeIPA services
5. **Document operational procedures**

### Medium Term (1-3 months)
1. **Deploy FreeIPA replica** for high availability
2. **Configure certificate** for external services
3. **Set up automated backups**
4. **Implement multi-factor authentication**
5. **Plan for disaster recovery**

### Long Term (3+ months)
1. **Scale infrastructure** as needed
2. **Advanced security policies**
3. **Integration with external systems**
4. **Regular security audits**
5. **Capacity planning**

---

## Related Documentation

- [[FreeIPA/DNS Entries]] - DNS configuration and management
- [[FreeIPA/Add Users]] - User account management
- [[FreeIPA/Set up NTP]] - Time synchronization setup
- [[FreeIPA/Install FreeIPA Client and Enroll]] - Client enrollment procedures
- [[Security/FreeIPA]] - Complete FreeIPA documentation
- [[Infrastructure/Network Topology]] - Network architecture
- [[Infrastructure/Hosts Inventory]] - Host specifications

---

**Installation Date**: 2025-11-27
**FreeIPA Version**: 4.x (AlmaLinux 9 default)
**Realm**: BADGER-DEV.COM
**DNS Domain**: int.badger-dev.com
**Maintained By**: Infrastructure Team
**Next Review**: 2025-12-27

**Critical Infrastructure Notice**: This FreeIPA server is essential for all authentication services. Plan redundancy and ensure robust backup procedures before production deployment.

***

### 1. Design and assumptions

FreeIPA strongly recommends using an upper‑case Kerberos realm that matches the primary DNS domain, but it is supported to use a different realm like `BADGER-DEV.COM` with DNS domain `int.badger-dev.com`. [3][6][4]
This means your users will authenticate as `user@BADGER-DEV.COM` while hosts and services live under the `int.badger-dev.com` DNS zone managed by the IPA DNS server. [3][6][5]

***

### 2. Prepare AlmaLinux and hostname

Update the server and reboot if there are kernel updates:  

```bash
sudo dnf update -y
sudo reboot
```
  
Set the FQDN and verify it:  

```bash
sudo hostnamectl set-hostname ipa1.int.badger-dev.com
hostnamectl
```
  
Ensure `/etc/hosts` has a static mapping for the IPA server’s IP (replace with your real IP):  

```bash
echo "192.168.50.10 ipa1.int.badger-dev.com ipa1" | sudo tee -a /etc/hosts
```
  

Make sure the server has a static IP configured and reliable time sync (Kerberos is very time‑sensitive), usually via `chronyd` which AlmaLinux 9 uses by default. [2][5]

***

### 3. Check SELinux and firewall baseline

FreeIPA is designed to run with SELinux enforcing, and modern docs recommend leaving SELinux enabled rather than disabling it. [7][5]
Verify mode with:  

```bash
getenforce
```

and only use permissive temporarily for troubleshooting if you hit a specific SELinux denial during install. [8][7]

If you are using `firewalld`, keep it enabled; you will open the required services after the install. [8][7]

***

### 4. Install FreeIPA server and DNS packages

On AlmaLinux 9, FreeIPA is available from the standard repositories. [1][2]
Install the server and DNS components:  

```bash
sudo dnf install -y freeipa-server freeipa-server-dns
```
  

This pulls in IPA server, Dogtag CA, 389‑DS, Apache, bind‑DNS integration, and required dependencies. [9][1][5]

***

### 5. Open required firewall ports

If `firewalld` is running, allow the FreeIPA and DNS services and reload:  

```bash
sudo firewall-cmd --add-service={http,https,dns,ntp,freeipa-ldap,freeipa-ldaps,freeipa-replication} --permanent
sudo firewall-cmd --reload
```
  

These services cover the web UI, LDAP/LDAPS, replication, DNS, and time sync used by FreeIPA deployments. [2][8][5]

***

### 6. Run ipa-server-install with integrated DNS

You can run `ipa-server-install` interactively, but with your specifics it is convenient to supply the main options on the command line. [1][3][10]
Example (adjust passwords and any DNS forwarders to your needs):  

```bash
sudo ipa-server-install \
  --setup-dns \
  --realm=BADGER-DEV.COM \
  --domain=int.badger-dev.com \
  --hostname=ipa1.int.badger-dev.com \
  --mkhomedir
```
  

Key points during the prompts (if not fully specified on the CLI): [1][2][5]

- Directory Manager password: set a strong LDAP Directory Manager password (used rarely). [2][5]
- IPA admin password: this becomes the `admin` user’s password for Web UI and CLI. [2][5]
- Integrated DNS: answer “yes” to configuring integrated DNS when prompted. [1][10]
- DNS forwarders: specify one or more upstream resolvers (e.g., 1.1.1.1, 9.9.9.9) or choose no forwarders if you want a root‑resolving server. [2][10]
- Reverse zone: when asked, provide the reverse zone for your server’s subnet, for example `50.168.192.in-addr.arpa` for `192.168.50.0/24`. [4][19]

The installer configures the CA, KDC, LDAP, HTTP, NTP integration, and bind DNS zone for `int.badger-dev.com` and the reverse zone. [9][1][5]

***

### 7. Verify services and basic Kerberos

After installation completes, confirm the IPA services are healthy:  

```bash
sudo ipa-server-status
```
  
Obtain a Kerberos ticket for the `admin` user and list it:  

```bash
kinit admin
klist
```
  

A valid TGT for `admin@BADGER-DEV.COM` indicates Kerberos is functioning correctly. [3][5]

***

### 8. Verify DNS from a client

Point a test machine (or the server itself) to use the IPA server as its DNS and test resolution. [2][11]

On the IPA server:  

```bash
dig ipa1.int.badger-dev.com A
dig -x 192.168.50.10
```
  

You should see forward and reverse records matching the hostname and IP created by the installer. [2][11][5]

***

### 9. Access the Web UI

From a browser that can reach your server, go to:  

```text
https://ipa1.int.badger-dev.com/ipa/ui
```
  

Log in as `admin` with the password you set during `ipa-server-install`, and you will see the FreeIPA web interface for managing users, groups, hosts, DNS, and policies. [9][1][5]

***

### 10. Enroll AlmaLinux (or other) clients

On each client you want to join to FreeIPA, first ensure its DNS points to the IPA server so SRV records can be discovered. [11][12]

```bash
# example using NetworkManager
sudo nmcli connection modify eth0 ipv4.dns 192.168.50.10
sudo nmcli connection up eth0
```
  

Then install the IPA client package and enroll:  

```bash
sudo dnf install -y freeipa-client

sudo ipa-client-install \
  --server=ipa1.int.badger-dev.com \
  --domain=int.badger-dev.com \
  --realm=BADGER-DEV.COM \
  --mkhomedir
```
  

When prompted, confirm the detected realm/domain, allow time sync, and provide `admin` credentials to enroll the client into the realm. [11][12][5]

***

### 11. First checks and basic management

Create a test user and try SSH login from a client. [11][12][5]

```bash
# on IPA server
ipa user-add jdoe --first=John --last=Doe

# on client (after enrollment)
ssh jdoe@client-hostname
```
  

If home directories are created at first login via `--mkhomedir`, you should get a shell as `jdoe` authenticated against FreeIPA. [11][12][5]

***

### 12. Notes on AlmaLinux 9.x quirks

Some AlmaLinux 9.5 users have reported needing to create or adjust `/etc/ipa/custodia` configuration files if the installer fails with custodia‑related errors, which is documented in AlmaLinux FreeIPA troubleshooting threads. [13]
If you hit an unexpected `custodia.conf` or similar error during install, check recent AlmaLinux FreeIPA notes and apply any recommended workarounds before re‑running `ipa-server-install`. [11]

***

If you share the exact AlmaLinux major/minor (for example 9.3 vs 9.5) and your LAN IP scheme, a follow‑up can include concrete forward and reverse zones, plus hardened DNS and certificate settings tailored to your network.