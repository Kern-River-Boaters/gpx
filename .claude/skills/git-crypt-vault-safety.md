# git-crypt-vault-safety

> Parent Skill Definition: [git-crypt-vault-safety](file:///home/jpino/Obsidian/Common/_Meta/Skills/git-crypt-vault-safety/SKILL.md)

---
name: git_crypt_vault_safety
description: "|   Guardrails for working with git-crypt encrypted Obsidian vaults (Notes, Genealogy, Notes_test).   Trigger this skill when: cloning a vault, pulling from remote, processing medical/genealogy PDFs,   debugging invalid pdf header or \x00GITCRYPT errors, or developing import/sync agents."
---

# Git-Crypt Vault Safety Guardrails

## Encrypted Repos

| Repo | GitHub Remote | Encrypted Paths |
|------|--------------|-----------------|
| Notes | joseluispino/Household-Notes | `Medical/**`, `Estate/**`, `Personal/Journal/**` |
| Genealogy | joseluispino/Genealogy | `/*.md`, `Drafts/**`, `Sources/**` |
| Notes_test | (test fork) | Same as Notes |

Non-encrypted repos: `Common`, `KRB`, `Cookbook` — never write PII here.

---

## CRITICAL: .git/config Must Use Clean Syntax

**Known Bug (2026-07-27):** Escaped quotes in `.git/config` silently break the smudge filter.

### ❌ Broken (do NOT use):
```ini
[filter "git-crypt"]
    smudge = \"git-crypt\" smudge
```

### ✅ Correct:
```ini
[filter "git-crypt"]
    smudge = git-crypt smudge
    clean = git-crypt clean
    required = true
[diff "git-crypt"]
    textconv = git-crypt diff
```

If you see `invalid pdf header: b'\x00GITC'` errors — check `.git/config` first.

---

## Pre-Flight Checklist for Encrypted Vault Operations

Before processing any encrypted file:

```bash
# 1. Verify .git/config syntax
grep "smudge" [[config]]
# Must show: smudge = git-crypt smudge (no backslash-quotes)

# 2. Unlock the repo
cd [[Notes]]
git-crypt unlock /home/jpino/notes-vault-production.key

# 3. Force re-smudge if needed
git checkout -f HEAD -- .

# 4. Verify a binary file is decrypted
python3 -c "
with open('Medical/Isabel/Sources/some.pdf', 'rb') as f:
    h = f.read(10)
    assert b'GITCRYPT' not in h, f'Still encrypted! Header: {h}'
    print('OK:', h[:4])
"

# 5. Run regression tests
python3 [[test_git_crypt_and_import.py]]
```

---

## Detecting Ciphertext Stubs

```python
def is_gitcrypt_stub(path):
    """Returns True if file is a raw ciphertext stub (not decrypted)."""
    try:
        with open(path, 'rb') as f:
            header = f.read(10)
            return b'GITCRYPT' in header or b'\x00GITC' in header
    except Exception:
        return False
```

---

## Repairing .git/config Programmatically

```python
clean_gc_block = '''[filter "git-crypt"]
\tsmudge = git-crypt smudge
\tclean = git-crypt clean
\trequired = true
[diff "git-crypt"]
\ttextconv = git-crypt diff
'''

config_path = Path('[[config]]')
lines = config_path.read_text().splitlines()
# Strip any existing git-crypt filter lines
clean = [l for l in lines if 'git-crypt' not in l
         and '[filter' not in l and '[diff' not in l]
config_path.write_text('\n'.join(clean).rstrip() + '\n\n' + clean_gc_block)
```

---

## Key File Location

```
/home/jpino/notes-vault-production.key
```

This key unlocks Notes, Genealogy, and Notes_test. The same key bytes are stored at `.git/git-crypt/keys/default` inside each repo after unlock.

---

## Test Suite

Always run before and after changes to vault sync/import code:

```bash
python3 [[test_git_crypt_and_import.py]]
```

Tests:
1. `.git/config` syntax across all encrypted repos
2. Binary file header integrity scan (zero ciphertext stubs)
3. Medical import agent quarantine false-positive regression

---

## Medical Import Agent HIPAA Quarantine — Known False Positives

The `is_other_patient_record()` function in `medical_import_agent.py` must NOT quarantine files where the regex extracts form field labels like `DATE/TIME OF PROCEDURE` as patient names.

Ignore list in `is_other_patient_record()` must include:
```python
["yes", "no", "self", "parent", "spouse", "child",
 "date", "time", "dob", "mrn", "csn", "age", "sex",
 "gender", "provider", "physician", "doctor"]
```

---

## References

- [Postmortem](file:///home/jpino/.gemini/antigravity-ide/knowledge/git-crypt-smudge-filter-bug/artifacts/git_crypt_smudge_postmortem.md)
- [[Test Suite]]
- [[Directive 6 SOP]]
- [[medical_import_agent.py]]

