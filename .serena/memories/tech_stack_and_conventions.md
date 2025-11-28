# Tech Stack and Conventions

## Documentation Technology Stack
- **Primary Tool**: Obsidian (Markdown-based knowledge management)
- **Storage**: iCloud sync with Git backup
- **Format**: GitHub Flavored Markdown with Obsidian extensions
- **File Encoding**: UTF-8

## Obsidian-Specific Features
- **Wiki Links**: `[[Page Name]]` for internal linking
- **Alias Links**: `[[Display Name|Actual Page]]`
- **Tag System**: `#tag` for categorization
- **Markdown Extensions**: Frontmatter, callouts, mermaid diagrams
- **Graph View**: Visual relationship mapping

## File Naming Conventions
- **MOC Files**: `Name MOC.md` (Map of Content)
- **Home Hub**: `🏠 Home.md` (emoji for primary navigation)
- **Repository Maps**: `📁 Repository Map.md` 
- **Standard Files**: `PascalCase.md` with spaces
- **Emoji Prefixes**: Used for visual hierarchy and quick identification

## Directory Structure
```
/
├── 🏠 Home.md              # Main navigation hub
├── 📁 Repository Map.md    # Repository overview
├── Ansible MOC.md          # Ansible documentation hub
├── Docker MOC.md           # Docker documentation hub
├── Infrastructure/         # Physical infrastructure docs
├── Network/               # Network configuration
├── Security/              # Security and access control
├── Services/              # Service documentation
├── Monitoring/            # Monitoring and observability
├── Backups/               # Backup procedures
├── Procedures/            # Operational guides
├── Development/           # Development environment
├── AI Tools/              # AI assistant configurations
└── FreeIPA/               # Identity management docs
```

## Frontmatter Template
```yaml
---
title: Page Title
tags: [tag1, tag2, category]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Linking Conventions
### Internal Links (Vault)
- Wiki Links: `[[Page Name]]`
- Display Links: `[[Display Text|Page Name]]`
- Section Links: `[[Page Name#Section]]`

### External Links
- Repository Files: `file:///Users/.../repository/file.ext`
- Web Resources: Standard Markdown links `[Text](URL)`
- Cross-Repo: Reference Repository Map for paths

## Tag Categories
- **Technology**: `#ansible`, `#docker`, `#network`, `#security`
- **Function**: `#infrastructure`, `#monitoring`, `#backup`, `#procedure`
- **Urgency**: `#emergency`, `#critical`, `#maintenance`
- **Host**: `#hercules`, `#oci-dmz`, `#apollo`, etc.
- **Status**: `#active`, `#planned`, `#deprecated`

## Content Standards
- **YAGNI Principle**: Document what exists, not what might exist
- **Living Documentation**: Update after infrastructure changes
- **Cross-Reference**: Link related concepts bidirectionally
- **Procedural Clarity**: Step-by-step instructions for operations
- **Emergency Focus**: Clear troubleshooting and recovery procedures

## Integration Patterns
### With Code Repositories
- Technical details stay in repository README/docs
- Architecture and cross-cutting concerns in vault
- Use `file://` links for direct repository references
- Maintain consistency between vault and repo documentation

### MOC (Map of Content) System
- Each major area has an MOC hub page
- MOC pages provide overview and navigation
- Related pages link back to their MOC
- Use consistent MOC structure across sections

## Documentation Cadence
- **Real-time**: Update during infrastructure changes
- **Weekly**: Review and update operational procedures
- **Monthly**: Audit links and check for stale content
- **Quarterly**: Major review of architecture documentation