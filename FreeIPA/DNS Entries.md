ipa dnsrecord-add int.badger-dev.com _kerberos._udp --srv-rec="0 100 88 ipa1.int.badger-dev.com"
ipa dnsrecord-add int.badger-dev.com _kerberos._tcp --srv-rec="0 100 88 ipa1.int.badger-dev.com"
ipa dnsrecord-add int.badger-dev.com _ldap._tcp     --srv-rec="0 100 389 ipa1.int.badger-dev.com"
ipa dnsrecord-add int.badger-dev.com _ldaps._tcp    --srv-rec="0 100 636 ipa1.int.badger-dev.com"

ipa dnsrecord-add 0.2.10.in-addr.arpa 20 --ptr-rec=ipa1.int.badger-dev.com

ipa dnsrecord-add int.badger-dev.com ipa1 --a-ip-address=10.2.0.20

ipa dnsrecord-add int.badger-dev.com ntp --a-ip-address=10.2.0.20
