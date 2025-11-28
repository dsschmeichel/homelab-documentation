#!/usr/bin/env python3
"""
Homelab Documentation Vault - Project Overview
This file serves as a code entry point for Serena to understand the project structure.
"""

# Project Metadata
PROJECT_TYPE = "obsidian_documentation_vault"
VAULT_NAME = "Homelab Documentation"
MAINTAINER = "Daniel Schmeichel"
CREATED = "2025-11-23"

# Repository Structure (linked directories)
ANSIBLE_REPO = "/Users/danielschmeichel/github/ansible"
DOCKER_REPO = "/Users/danielschmeichel/github/docker"
DOTFILES_REPO = "/Users/danielschmeichel/github/dotfiles"

# Main Infrastructure Components
HOSTS = [
    "hercules",      # Primary AMD64 + Komodo Core
    "oci-dmz",       # DMZ/front-door
    "oci-docker",    # ARM64 worker
    "synology-nas",  # Storage node
    "apollo",        # Monitoring hub
    "meade"          # Remote edge
]

def get_project_summary():
    """Return a structured summary of the homelab project."""
    return {
        "type": PROJECT_TYPE,
        "purpose": "Central documentation for homelab infrastructure",
        "repositories": {
            "ansible": ANSIBLE_REPO,
            "docker": DOCKER_REPO,
            "dotfiles": DOTFILES_REPO
        },
        "hosts": HOSTS,
        "key_services": [
            "FreeIPA (Identity Management)",
            "Komodo (Docker Orchestration)",
            "Beszel (Infrastructure Monitoring)",
            "Dozzle (Container Logs)"
        ]
    }

if __name__ == "__main__":
    summary = get_project_summary()
    print(f"Homelab Documentation Vault")
    print(f"Type: {summary['type']}")
    print(f"Purpose: {summary['purpose']}")
    print(f"Managed Repositories: {len(summary['repositories'])}")
    print(f"Active Hosts: {len(summary['hosts'])}")
    print(f"Key Services: {len(summary['key_services'])}")