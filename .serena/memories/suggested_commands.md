# Suggested Commands for Homelab Documentation Project

## Essential System Commands (Darwin/macOS)

### File Navigation and Discovery
```bash
# List vault contents
ls -la "/Users/danielschmeichel/Library/Mobile Documents/iCloud~md~obsidian/Documents/Homelab Documentation"

# Find specific documentation
find . -name "*.md" -type f | grep -i "keyword"

# Search within markdown files
grep -r "search term" . --include="*.md"

# Open in Obsidian (if installed)
open -a Obsidian .
```

### Git Operations
```bash
# Check repository status
git status

# Add and commit changes
git add .
git commit -m "Update documentation"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline -10
```

### Repository Management (Multi-repo workflow)
```bash
# Update all homelab repositories
cd ~/github/ansible && git pull
cd ~/github/docker && git pull  
cd ~/github/dotfiles && git pull

# Check status across all repos
for repo in ansible docker dotfiles; do
  echo "=== $repo ==="
  cd ~/github/$repo && git status -sb
done
```

## External Repository Commands

### Ansible Repository
```bash
cd ~/github/ansible

# List hosts and groups
make list-hosts
make list-groups

# Validate configuration
make lint
make syntax-check
make check site.yml DIFF=1

# Deploy changes
make deploy site.yml TAGS=phase1
make deploy site.yml LIMIT=hostname

# Host management
python3 scripts/host_management/check_onboarding_status.py
```

### Docker Repository  
```bash
cd ~/github/docker

# List stacks and hosts
ls -la stacks/
cat syncs/servers.toml

# Komodo operations
# (Commands depend on Komodo installation)
```

### Dotfiles Repository
```bash
cd ~/github/dotfiles

# Apply dotfiles
chezmoi apply

# Check dotfile status
chezmoi status

# Update from source
chezmoi update
```

## Documentation Workflows

### Creating New Documentation
```bash
# Create new markdown file with frontmatter
cat > "New Page.md" << 'EOF'
---
title: New Page
tags: [tag1, tag2, category]
created: $(date +%Y-%m-%d)
updated: $(date +%Y-%m-%d)
---

# New Page

Content goes here...
EOF
```

### Documentation Maintenance
```bash
# Find broken links (basic check)
find . -name "*.md" -exec grep -l "\[\[.*\]\]" {} \; | head -5

# Check for orphaned pages
grep -r "\[\[Page Name\]\]" . --include="*.md" || echo "Page not referenced"

# Update timestamps in frontmatter
sed -i '' 's/updated: [0-9]*/updated: '$(date +%Y-%m-%d)'/' *.md
```

## Obsidian-Specific Workflows

### Quick Open (macOS)
```bash
# Open specific page in Obsidian
open -a Obsidian "file:///Users/danielschmeichel/Library/Mobile Documents/iCloud~md~obsidian/Documents/Homelab Documentation/Page.md"
```

### Link Validation
```bash
# Extract all wiki links for validation
grep -o -E '\[\[.+?\]\]' *.md | sort | uniq

# Find duplicate file names (potential conflicts)
find . -name "*.md" -exec basename {} \; | sort | uniq -d
```

## System Administration Commands

### Host Connectivity Checks
```bash
# Ping key infrastructure hosts
ping -c 3 hercules.local
ping -c 3 apollo.local

# Check service status (examples)
ssh hercules "docker ps"
ssh apollo "systemctl status beszel"
```

### Backup and Sync
```bash
# Ensure iCloud sync is working
brctl log --wait --shorten

# Manual Git backup
git add .
git commit -m "Backup $(date)"
git push origin main
```

## Development Environment

### AI Assistant Integration
```bash
# Update Claude Code configuration
# Edit: ~/.claude/CLAUDE.md

# Update MCP servers
claude mcp list
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server
```

### Quick Documentation Commands
```bash
# Create quick note
cat > "Quick Note $(date +%Y-%m-%d).md" << 'EOF'
# Quick Note

Notes for $(date +%Y-%m-%d)
EOF

# Search recent changes
find . -name "*.md" -newermt "1 week ago"
```

## Emergency Procedures
```bash
# Quick vault backup
tar -czf "homelab-docs-emergency-$(date +%Y%m%d).tar.gz" .

# Check last Git commit
git log -1 --stat

# Restore from Git if needed
git reset --hard HEAD~1  # Undo last change
git checkout HEAD -- file.md  # Restore specific file
```

## Monitoring and Health Checks
```bash
# Check vault size and health
du -sh .
find . -name "*.md" | wc -l

# Validate Git repository integrity
git fsck --full
```