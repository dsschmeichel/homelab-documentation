To create your user "Dan" and an "ansible" user for configuration with appropriate access in FreeIPA, you'll use FreeIPA commands to create users, groups, and assign permissions.

***

### Create Users

Run these commands on the FreeIPA server CLI to create the users:

```bash
# Create user Dan
ipa user-add dan --first=Dan --last=User --password

# Create ansible user for automation
ipa user-add ansible --first=Ansible --last=Automation --password
```

You will be prompted to set passwords for each user. [1][2]

***

### Create Groups

Create groups for admin and configuration roles. For example:

```bash
# A group for administrators
ipa group-add admins --desc="Administrators with full rights"

# A group for users ansible will manage (optional)
ipa group-add ansible-admins --desc="Ansible management group"
```


***

### Add Users to Groups

Add the users to their respective groups to assign roles:

```bash
# Add Dan to admins group for full admin rights
ipa group-add-member admins --users=dan

# Add ansible user to ansible-admins group or admins group if needed
ipa group-add-member ansible-admins --users=ansible
```


***

### Assign Permissions (Optional Fine-Grained)

- If you want to delegate specific FreeIPA permissions rather than full admin rights, you can create and assign roles using `ipa privilege` and `ipa role` commands to limit what the ansible user can do.

***

### Enable SSH Access and Home Directories

Ensure that when users authenticate via FreeIPA, home directories are created on first login (if you used `--mkhomedir` during install):

```bash
ipa user-mod dan --shell=/bin/bash
ipa user-mod ansible --shell=/bin/bash
```

You also need to ensure that your SSH daemon is configured to allow IPA users to login and that the SSH public keys are managed with FreeIPA if needed. [1][2]

***

This setup lets you manage user and group permissions centrally and gives the "ansible" user the ability to access hosts based on group memberships and policies, ideal for automating with Ansible.

Sources
[1] AlmaLinux 9 : FreeIPA : Configure Client - Server World https://www.server-world.info/en/note?os=AlmaLinux_9&p=freeipa&f=3
[2] Quick_Start_Guide — FreeIPA documentation https://www.freeipa.org/page/Quick_Start_Guide
