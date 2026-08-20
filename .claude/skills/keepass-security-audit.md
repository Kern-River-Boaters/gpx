# keepass-security-audit

> Parent Skill Definition: [keepass-security-audit](file:///home/jpino/Obsidian/Common/_Meta/Skills/keepass-security-audit/SKILL.md)

---
name: keepass-security-audit
description: "Comprehensive operational skill and heuristic rulebook for executing, auditing, categorizing, and remediating KeePass (.kdbx) password databases and 2FA coverage across federated Obsidian vaults under SYS-AGN-006 and ADR-036 Level 4 Maturity."
doc_type: skill
tags:
  - type/skill
  - topic/security
  - topic/keepass
  - topic/2fa
  - topic/governance
governing_adr: "[[SYS-AGN-006]]"
---

# KeePass & 2FA Security Audit & Family Taxonomy Skill

This skill provides standardized heuristics, family identity resolution rules, corporate lifecycle transitions, and execution directives for AI interactive environments (**Google Antigravity**, **Claude Code**, **GitHub Copilot**, **Cursor**, **OpenCode**) to audit, categorize, and remediate the **Jose Database.kdbx** password database across federated vaults.

---

## 👥 1. Family Identity & Suffix Taxonomy Rules

When classifying, scoring, or remediating credentials, agents MUST adhere to this exact family taxonomy:

| Member / Scope | Initials / Suffix Patterns | Identity & Lifecycle Role | Target KeePass Group |
| :--- | :--- | :--- | :--- |
| **Jose Luis Pino** | `JLP`, `(JLP)`, `joseluis`, `jose luis`, `jpino@`, `pino@ieee.org` | Active Primary User (Personal & Professional) | `Identity & Cloud`, `Finance`, `Work - Keysight` |
| **Lisa Maria Pino** | `LMP`, `(LMP)`, `lisapino`, `lisa pino`, `lpino@` | Active Primary User (Personal + Advising) | `Finance`, `Work - Lisa` |
| **Isabel Pino** | `MIP`, `(MIP)`, `isabel` | Active Dependent Daughter (Integrated) | `Travel`, `Healthcare`, `Government`, `Identity & Cloud` |
| **Madre (Maria Luisa Rexach)** | `Madre`, `(Madre)`, `marialuisarexach`, `maria4hope@yahoo.com` | Family Elder (Managed by Jose) | `Family - Madre/` |
| **Alister Pino (fka Susana)** | `SP`, `(SP)`, `susana`, `alister`, `8384249` | Independent Adult Kid (Trans son) | `Archive/Adult Kids/` |
| **Ana Maria Pino** | `AMP`, `(AMP)`, `anamaria`, `ana pino`, `APINO3`, `619422212` | Independent Adult Kid (Academy of Art) | `Archive/Adult Kids/` |
| **Elena Maria Pino** | `EMP`, `(EMP)`, `elenapino`, `elena pino` | Independent Adult Kid | `Archive/Adult Kids/` |
| **Eva Maria Pino** | `MEP`, `(MEP)`, `EMP`, `evampino`, `evapino`, `8137941` | Independent Adult Kid | `Archive/Adult Kids/` |
| **Household / Shared** | — | Shared streaming, utilities, shopping, IoT | `Entertainment`, `Shopping`, `Utilities` |

> [!NOTE]
> **Email Alias Rule**: `pino@ieee.org` was historically used by Jose as a permanent personal email alias/redirector. Accounts registered under `pino@ieee.org` (e.g. Travel, Shopping, Camping, Utilities) are **PERSONAL**, not work, and must be classified by their actual domain.
>
> **SSH Keys & Developer Identity Routing**:
> - **GitHub (Personal)** & `SSH Keys github` → **`Identity & Cloud/`**
> - **Keysight Work Repos** & `Keysight PC Login ssh` / `SSH jpino Key` → **`Work - Keysight/`**
> - **Local LAN / Mobile** (`SSH Android`, `Kern Ubuntu SSH`) → **`Smart Home & Network/`**

---

## 🏛️ 2. Employer Lifecycle & Corporate Spinoff / Defunct Rules

Agents MUST apply these corporate transition rules during categorization:

### A. Keysight Technologies (Active Primary Employer — Jose)
* **Status**: Current active employer (`jpino@keysight.com`, `keysight.com`).
* **Includes**: Keysight internal portals, EDA/engineering software, IEEE, Cadence, Synopsys, test & measurement platforms.
* **Target Group**: `03_Work_Keysight/`

### B. Agilent Technologies (Historical Predecessor — Jose)
* **Status**: Jose's former employer before the Keysight corporate spinoff (`jpino@agilent.com`, `agilent.com`).
* **Includes**: Historical Agilent health/life insurance, benefits, and legacy corporate accounts.
* **Target Group**: `Archive/Past_Work_Jose_Agilent/`

### C. LILA / Lycée International de Los Angeles (Active Primary Employer — Lisa)
* **Status**: Current active school employer for Lisa (`Lisa.Pino@LilaSchool.com`, `lilaschool.com`, `lila.org`).
* **Includes**: LILA school portals, Blackbaud, PowerSchool, Canvas, educator tools, and active counselor memberships.
* **Target Group**: `04_Work_LILA_and_Advising/`

### D. CollegeAdvisor (Former Employer — Lisa)
* **Status**: Lisa's former employer (`lpino@collegeadvisor.com`, `joincollegeadvisor.com`).
* **Includes**: Chase Business (Lisa), NCAA Okta, Zoom, Salesforce, and Google accounts associated with CollegeAdvisor.
* **Target Group**: `Archive/Past_Work_Lisa_CollegeAdvisor/`

### F. Civic Work: Conejo Valley USD & Community Engagement (Historical — Jose)
* **CVUSD Campaign**: Jose's past school board campaign (`jose4cvusd@gmail.com`, `jose@jose4cvusd.com`, NetFile, ActBlue, NDTC) → **`Archive/Civic - CVUSD Campaign/`**
* **LULAC & Buen Vecino**: Jose's past civic community leadership (`lulac.of.conejo.valley`, `BuenVecinoCV`, `buen.vecino.of.conejo.valley@gmail.com`) → **`Archive/Civic - LULAC & Buen Vecino/`**

### G. Out-of-Business & Defunct Services (Historical Archive)
* **Defunct Retailers**: Circuit City, CompUSA, Radio Shack, Borders Rewards, Linens-n-Things.
* **Discontinued Software & Tools**: DVD X Copy (321 Studios), PDA Defense Professional (Palm OS), Menalto Gallery, Roxio vintage.
* **Dead Web Portals & ISPs**: Adelphia Cable (`@adelphia.net`), NewsVine, Mercury Center, Free Real Time, WhisperNumber, CDDB, PackageTrackR, MySpace.
* **Target Group**: **`Archive/Defunct Services/`**

> [!IMPORTANT]
> **Heuristic Precedence Rules**:
> 1. **Delta Dental vs. Delta Air Lines**: `Delta Dental` MUST evaluate to `Healthcare/`, NOT `Travel/`. Travel keyword matching must only trigger on `delta air`, `delta.com`, or `delta flight`.
> 2. **Alumni & Education**: Jose's Georgia Tech email and alumni lists (`gatech.edu`) MUST route to `Archive/Adult Kids` or `Archive/Education`, NOT `Work - Keysight`.

---

## 🎓 3. College Board & Admissions Triage Rules

Agents MUST disambiguate College Board and university accounts using these exact criteria:

1. **Active Educator / Advising Accounts**:
   * `Lisa.Pino@LilaSchool.com` (College Board) → Active LILA Counselor (`Work - Lisa/`)
   * `lisamichellepino@gmail.com` (Common App Practice) → Active Advising (`Work - Lisa/`)
   * `joseluispino@gmail.com` (Common App Recommender) → Active Recommender (`Work - Lisa/`)
2. **Adult Kids High School SAT / IDOC / FAFSA Accounts (Archive)**:
   * Ana (`anamariapino`, `619422212`) → `Archive/Adult Kids/`
   * Elena (`elenapino`) → `Archive/Adult Kids/`
   * Eva (`evapino`, `evampino@gmail.com`, `8137941`) → `Archive/Adult Kids/`
   * Alister (`alisterpino`, `8384249`, `FAFSA Alister`) → `Archive/Adult Kids/`

---

## 🗂️ 4. Target KeePass Group Restructuring Hierarchy

The canonical, organized KeePass database hierarchy for **Jose Database.kdbx**:

```
Jose Database.kdbx
├── 🔐 Core Identity & Essentials
│   ├── Identity & Cloud/            (Google, Apple ID, Microsoft, Password Manager, AWS)
│   ├── Finance/                     (Chase, First Tech, BofA, Citi, Discover, Taxes, 529s)
│   ├── Healthcare/                  (UCLA Health [Jose, Lisa, Isabel], Cigna, Delta Dental)
│   └── Government/                  (Social Security, IRS, CA MyFTB, DMV, Passports, USCIS)
│
├── 💼 Professional & Work
│   ├── Work - Keysight/             (Keysight enterprise, EDA tools, IEEE, engineering)
│   └── Work - Lisa/                 (LILA portals, Lisa College Board, CommonApp Counselor)
│
├── 🏡 Lifestyle, Home & Hobbies
│   ├── Entertainment/               (Netflix, HBO Max, Disney+, Hulu, Spotify, YouTube, Theaters)
│   ├── Libraries/                   (TO Library, LAPL, LA County Library, OverDrive, Libby)
│   ├── Outdoors & Sports/           (Kern River Boaters, Kayaking, Strava, Garmin inReach, Camping)
│   ├── Shopping/                    (Amazon, Costco, Target, Best Buy, Sweet Maria's Coffee)
│   ├── Travel/                      (Airlines [Delta, Alaska], Hotels, Rental Cars, Amtrak)
│   └── Utilities/                   (SoCalGas, SCE, Water, Trash, Verizon, Fastrak)
│
├── 🖥️ Local Hardware & Licenses
│   ├── Smart Home & Network/        (Home router, Synology NAS, Wi-Fi networks, IoT devices)
│   └── Software Licenses/           (Active software licenses, serial numbers, product keys)
│
├── 👨‍👩‍👧 Family Care
│   ├── Family - Isabel/             (Isabel active school, medical, activities)
│   └── Family - Madre/              (Madre Apple, Microsoft, Amex, Delta, Alaska, WiFi)
│
└── 📦 Archive
    ├── Adult Kids/                  (Ana [AMP], Elena [EMP], Eva [MEP], Alister [SP] SAT/FAFSA)
    ├── Civic - CVUSD Campaign/      (Jose past school district & board campaign accounts)
    ├── Past Work - Lisa/            (CollegeAdvisor, Defunct La Reina - lpino@lareina.com)
    ├── Past Work - Jose/            (Jose Agilent pre-spinoff accounts - jpino@agilent.com)
    ├── Legacy Software/             (Obsolete serial keys: Photoshop CS, Framemaker 6, etc.)
    └── Defunct Services/            (Dead websites, old ISPs, obsolete hardware stubs)
```

---

## 🛡️ 5. Security Triage Principles & Safeguards

1. **Missing 2FA is Priority 1**: The primary danger is services supporting 2FA where no local TOTP is configured. Triage focuses on **Finance**, **Healthcare**, **Work**, and **Identity & Cloud**.
2. **Duplicate Usernames are Informational (Low Priority)**: Standard email identifiers (`joseluispino@gmail.com`, `jpino@keysight.com`) across sites are normal and must NOT trigger security alarms.
3. **Stale Passwords are Informational (NIST SP 800-63B)**: Arbitrary 365-day rotation is not required for strong, unique passwords.
4. **Zero Credential Exposure**: Passwords, OTP secrets, usernames, and notes are never passed to LLMs. Only sanitized `[UUID, Domain/Title]` pairs are transmitted.
5. **Read-Only Database Access**: `.kdbx` is opened strictly with `read_only=True` via `pykeepass`.
6. **Vault Cleanliness Guardrail**: Scripts MUST NOT create temporary batch files in permanent note folders. Output belongs in `Common/_Meta/Cache/`, `Common/_Meta/Telemetry/`, or a single curated dashboard at `Notes/Estate/Technology/KeePass Security Posture.md`.

---

## 🛠️ Operational CLI Commands

### 1. Antigravity In-Session Mode (Zero External Token Cost)
```bash
# Step 1: Export sanitized masked payload on host
python3 Common/_Meta/Scripts/keepass_audit_pipeline.py \
  --kdbx "$HOME/GoogleDrive/Household/Keepass/Jose Database.kdbx" \
  --export-masked

# Step 2: In Antigravity chat, say "Cluster masked payload"
```

### 2. Standalone Local GPU Execution (Ollama — 100% Offline)
```bash
python3 Common/_Meta/Scripts/keepass_audit_pipeline.py \
  --kdbx "$HOME/GoogleDrive/Household/Keepass/Jose Database.kdbx" \
  --provider ollama
```

### 3. Supervised Browser Remediation (Phase 4)
```bash
# Launch browser assist for top 25 priority missing-2FA accounts (skips adult kids automatically)
python3 Common/_Meta/Scripts/keepass_remediation_assist.py \
  --kdbx "$HOME/GoogleDrive/Household/Keepass/Jose Database.kdbx" \
  --limit 25
```

