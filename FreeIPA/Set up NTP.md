### Configure Cloudflare as upstream on the FreeIPA server

Edit `/etc/chrony.conf` on `ipa1.int.badger-dev.com` and replace or comment out existing `pool`/`server` lines, then add Cloudflare:

```conf
# Upstream time source: Cloudflare
server time.cloudflare.com iburst

# Serve time to your LAN
allow 10.2.0.0/22
allow 100.64.0.0/10

# Optional: act as local source if WAN is down
local stratum 10

driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
leapsectz right/UTC
logdir /var/log/chrony
```

- `server time.cloudflare.com iburst` points chrony at Cloudflare’s anycast NTP service with fast initial sync. [1][2][4]
- `allow 192.168.50.0/24` lets your LAN clients use the IPA server as their NTP server. [3][5]
- `local stratum 10` is optional but keeps clients syncing even if the IPA box loses upstream connectivity. [6][7]

Then restart and verify:  

```bash
sudo systemctl restart chronyd
chronyc sources -v
chronyc tracking
```

You should see `time.cloudflare.com` as a source, typically with a low stratum and good reach. [1][8][9]

Your clients can continue to use `server ipa1.int.badger-dev.com iburst` in their own `chrony.conf` so the hierarchy becomes: Cloudflare → FreeIPA → LAN hosts.

***
### On each Linux client (chrony)

Edit `/etc/chrony.conf` and set Cloudflare as the primary server:  

```conf
# Cloudflare NTP as primary
server time.cloudflare.com iburst

# Optional: FreeIPA as secondary/local reference
server ntp.int.badger-dev.com iburst
```

- `server time.cloudflare.com iburst` makes Cloudflare your main, low‑latency time source.
- Adding your IPA server as a second `server` line gives you a local fallback and keeps the LAN consistent if Cloudflare is briefly unreachable. 

Then restart and verify on each client:  

```bash
sudo systemctl restart chronyd
chronyc sources -v
chronyc tracking
```

You should see `time.cloudflare.com` as one of the sources, usually marked as the current sync source. 