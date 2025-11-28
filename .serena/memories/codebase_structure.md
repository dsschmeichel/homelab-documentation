# Codebase Structure and Architecture

## Overall Architecture

This is an **Obsidian documentation vault** organized as a knowledge management system for a multi-repository homelab infrastructure. The structure follows MOC (Map of Content) methodology with hierarchical organization.

## Vault Structure Overview

### Root Level Navigation
```
/
├── 🏠 Home.md                    # Main navigation hub and entry point
├── 📁 Repository Map.md          # Overview of three main repositories
├── README.md                     # Basic project description
├── Welcome.md                    # Obsidian default (can be removed)
├── project_overview.py           # Serena entry point file
└── Ansible MOC.md                # Ansible documentation hub
```

### Primary Documentation Areas

#### Infrastructure Documentation
```
Infrastructure/
├── Hardware.md                   # Physical hardware specifications
├── Network Topology.md          # Network design and layout
└── [Future: Hosts Inventory.md] # Individual host documentation
```

#### Network Configuration
```
Network/
├── Network Overview.md           # Network architecture summary
└── [Future: DNS.md, VPN.md]      # Network service details
```

#### Security and Access Control
```
Security/
└── FreeIPA.md                    # Identity management documentation
```

#### Service Documentation
```
Services/
└── Service Inventory.md          # Catalog of deployed services
```

#### Container Platform
```
Docker/
├── Docker MOC.md                 # Docker documentation hub
├── Stacks Inventory.md           # All deployed Docker stacks
├── Komodo.md                     # Orchestration platform docs
└── Host Fleet.md                 # Docker host topology
```

#### Identity Management
```
FreeIPA/
├── Install FreeIPA server.md     # Server setup procedures
├── Add Users.md                  # User management
├── DNS Entries.md               # DNS configuration
├── Set up NTP.md                # Time synchronization
└── Install FreeIPA Client and Enroll.md  # Client setup
```

#### AI Assistant Integration
```
AI Tools/
├── MCP Servers/
│   └── Serena.md                # Serena MCP server info
├── Claude Code/
│   └── Add Serena MCP Server to Project.md  # Setup instructions
├── Zed/                         # Zed editor configurations
├── Github Copilot/              # Copilot integration
└── Goose/                       # Goose AI assistant
```

## Key Architectural Patterns

### MOC (Map of Content) System
- Each major domain has a dedicated MOC hub page
- MOC pages provide overview, navigation, and quick access
- Related pages link back to their domain MOC
- Consistent structure across all MOC pages

### Three-Tier Repository Integration
1. **Ansible Repository** (`~/github/ansible`)
   - Configuration management and orchestration
   - 19 roles in risk-based phases (0-9)
   - Host management and deployment procedures

2. **Docker Repository** (`~/github/docker`)
   - Containerized application deployment
   - Komodo orchestration and management
   - Infrastructure and application stacks

3. **Dotfiles Repository** (`~/github/dotfiles`)
   - Personal development environment
   - Shell configurations and CLI tools
   - AI assistant integrations

### Linking Strategy
- **Internal Wiki Links**: `[[Page Name]]` for vault navigation
- **Display Links**: `[[Display Text|Page Name]]` for user-friendly text
- **External File Links**: `file:///path/to/repo/file` for repository references
- **Web Links**: Standard Markdown for external resources
- **Bidirectional References**: Related pages link to each other

### Tag-Based Organization
- **Technology Tags**: `#ansible`, `#docker`, `#network`, `#security`
- **Function Tags**: `#infrastructure`, `#monitoring`, `#backup`, `#procedure`
- **Host Tags**: `#hercules`, `#oci-dmz`, `#apollo`, etc.
- **Status Tags**: `#active`, `#planned`, `#deprecated`

## Documentation Content Types

### Procedural Documentation
- Step-by-step guides with command examples
- Emergency procedures with rollback steps
- Troubleshooting guides with diagnostic steps
- Deployment workflows with validation checks

### Reference Documentation
- Configuration specifications and examples
- Architecture diagrams and descriptions
- Service inventories and dependencies
- Host specifications and capabilities

### Operational Documentation
- Maintenance schedules and procedures
- Monitoring and alerting configurations
- Backup and recovery procedures
- Security policies and access controls

## Integration Points

### Cross-Repository References
- Ansible roles referenced in infrastructure documentation
- Docker stacks linked from service documentation
- Network configurations reference Ansible variables
- Development tools documented across repositories

### External System Links
- Direct file references to repository files
- Web links to official documentation
- Server and service URL references
- Monitoring dashboard links

## Content Management Patterns

### Living Documentation
- Updated immediately after infrastructure changes
- Version controlled with Git backup
- Cross-referenced with actual implementations
- Regularly reviewed for accuracy

### Scalable Structure
- Modular organization supporting growth
- Consistent naming and formatting conventions
- Hierarchical navigation with clear taxonomy
- Searchable content with comprehensive tagging

## Future Expansion Areas
- Monitoring documentation section
- Backup and recovery procedures
- Development environment setup
- Additional service documentation
- Performance tuning guides
- Security audit procedures