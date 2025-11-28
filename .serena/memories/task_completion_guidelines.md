# Task Completion Guidelines

## When Tasks Are Completed

### Documentation Tasks
1. **Review and Update Links**
   - Verify all wiki links `[[Page]]` resolve correctly
   - Check external `file://` links to repositories
   - Ensure bidirectional linking where appropriate

2. **Validate Frontmatter**
   - Ensure `updated:` field reflects current date
   - Verify tags are accurate and consistent
   - Check title matches page content

3. **Cross-Reference Integration**
   - Update MOC (Map of Content) pages if new sections added
   - Link from related pages using consistent terminology
   - Update Repository Map if architectural changes made

4. **Git Operations**
   - Stage and commit changes with descriptive message
   - Include emoji in commit for visual clarity when appropriate
   - Push to remote repository for backup

### Infrastructure Change Tasks
1. **Update Synchronized Documentation**
   - Update inventory counts (hosts, services, etc.)
   - Record architectural decisions and their rationale
   - Update emergency procedures if new risks introduced

2. **Refresh Integration Points**
   - Update file:// links if repository structures changed
   - Verify Ansible/Docker repository documentation consistency
   - Update command examples if workflows changed

3. **Review Impact Analysis**
   - Check which other documentation pages need updates
   - Update related procedures and troubleshooting guides
   - Consider updating monitoring and backup procedures

## Quality Assurance Checklist

### Content Quality
- [ ] Content is accurate and current
- [ ] Procedures are tested and reproducible
- [ ] Emergency procedures include rollback steps
- [ ] Code examples are properly formatted and tested
- [ ] Links are functional and up-to-date

### Documentation Standards
- [ ] Frontmatter follows established template
- [ ] Tags are consistent with existing taxonomy
- [ ] File naming follows conventions
- [ ] Wiki links use correct format
- [ ] External links use appropriate protocols

### Integration Consistency
- [ ] Cross-references are bidirectional
- [ ] MOC pages reflect current structure
- [ ] Repository Map is accurate
- [ ] Command examples match actual workflows

## Post-Task Commands

### Immediate Actions (Every Task)
```bash
# 1. Stage and commit changes
git add .
git commit -m "Update documentation: brief description"

# 2. Update timestamps in modified files
# (Manual: update `updated:` in frontmatter)

# 3. Quick link validation
grep -r "\[\[.*\]\]" . --include="*.md" | grep -i "new_page_name"
```

### Periodic Actions (Weekly/Monthly)
```bash
# Comprehensive link check
find . -name "*.md" -exec grep -l "\[\[.*\]\]" {} \;

# Orphaned page identification
# (Manual: check for pages not referenced elsewhere)

# Vault health check
du -sh .
git status
```

### Emergency Recovery
```bash
# If something goes wrong during updates
git reset --hard HEAD~1  # Undo last commit
git checkout HEAD -- file.md  # Restore specific file
```

## Integration with External Repositories

### When Ansible Repository Changes
- Update host inventory in relevant documentation
- Review phase-based deployment procedures
- Update role documentation if roles modified

### When Docker Repository Changes  
- Update stack inventory and service counts
- Modify Komodo integration documentation
- Update deployment procedures if workflows changed

### When Infrastructure Changes
- Update Network Topology diagrams and descriptions
- Modify Hardware specifications if applicable
- Update Security documentation if access patterns changed

## Documentation Review Process

### Self-Review Checklist
1. **Accuracy**: Is all information technically correct?
2. **Clarity**: Is the content easy to understand?
3. **Completeness**: Are all necessary details included?
4. **Consistency**: Does it match other documentation patterns?
5. **Maintainability**: Will future updates be straightforward?

### Peer Review Triggers
- Major architectural documentation changes
- Emergency procedure updates
- New workflow documentation
- Integration point modifications

## Automation Opportunities

### Git Hooks (Potential Enhancement)
```bash
# Pre-commit hook ideas:
# - Validate markdown syntax
# - Check for broken internal links
# - Verify frontmatter format
# - Prevent large file commits
```

### Scheduled Maintenance
```bash
# Monthly cron job ideas:
# - Check for orphaned pages
# - Validate external links
# - Update statistics and inventories
# - Archive outdated content
```

## Success Metrics
- All wiki links resolve correctly
- External repository links remain accurate
- Emergency procedures are tested annually
- Documentation stays synchronized with infrastructure changes
- New team members can onboard using only the vault