# Ditteau KPI Library

Higher-education KPI catalog and governance guidelines for the Ditteau Data
Unified Platform's Distribute layer.

**Note:** The Streamlit-in-Snowflake dashboard that visualizes these KPIs
lives in `ditteau_data_transform/streamlit/dashboards/kpi_library/`.

## Repository Structure

```
├── higher_ed_kpi_catalog_enriched.csv   # Source of truth (162 rows, 7 Areas)
├── kpi_library.html                      # Browsable HTML mirror
├── CLAUDE.md                             # Operating instructions for contributors
├── README.md
└── archive/                              # Historical reconciliation docs
```

## What's Here

### Core Artifacts

| File | What it is |
|---|---|
| `higher_ed_kpi_catalog_enriched.csv` | The canonical KPI/dashboard catalog — 162 rows across 7 Areas (Enrollment Management, Admissions, Financial Aid, Registration, Cross-Domain, Benchmarking, Finance). Single source of truth for KPI definitions, calculation logic, and governance flags (FERPA, build status). |
| `kpi_library.html` | A browsable, filterable version of the catalog (by Area / Type / Category), with calculation-logic tooltips. Mirrors the CSV — see "Keeping things in sync" below. |
| `CLAUDE.md` | Operating instructions for Claude Code and human contributors — read this before editing any file. Defines source of truth, catalog conventions, governance gates, and platform conventions. |

### Archive

The `archive/` folder contains historical documentation from the July 2026 reconciliation project (PHASE_1–5 docs, RECONCILIATION_SUMMARY) and superseded files. See `archive/README.md` for details.

## Current build status

**As of 2026-07-22 reconciliation:** 21 of 23 marts are fully functional in production.

### ✅ Functional Areas

All dashboard tabs are functional with real data:
- **Admissions** (30 KPIs) — fully functional
- **Registration** (27 KPIs) — fully functional
- **Financial Aid** (29 KPIs) — fully functional; PowerFAIDS integration pending affects unmet need calculations only
- **Enrollment Management** (32 KPIs) — fully functional
- **Benchmarking** (7 KPIs) — fully functional; College Scorecard integration complete
- **Finance** (14 KPIs) — Budget Performance and AR Aging live; remaining KPIs use proposed marts pending ERP integration

### 🟡 Known Limitations

- **Cross-Domain tab:** ~~Blocked by unbuilt `snap_cohort_milestone`~~ **CORRECTION (2026-09-26):** `snap_cohort_milestone` IS **BUILT in DEMEAU PROD** (1,138 rows). The Cross-Domain tab should be functional.
- **`mart_enrollment_census_ntr`:** Built and functional, but DEMEAU synthetic data has zero billing values (`gross_tuition_billed=0`). Logic is complete and will activate with production school data.
- **`snap_aid_term`:** PowerFAIDS integration pending affects `coa_amount`, `efc_amount` columns (unmet need calculations) in `mart_aid_leveraging`. Core leveraging metrics (merit/need split, aid band yield) are functional.
- **NSC integration:** Pending; affects transfer-out tracking in retention models. Currently transfer-outs are counted with stop-outs.

### 🔍 Previously Undocumented but Functional

The 2026-07-22 reconciliation discovered two marts that were built but not documented:
- **`mart_enrollment_demographics`** — fully functional; powers Demographics dashboard visualizations
- **`mart_scorecard_program_outcomes`** — fully functional; powers entire Benchmarking area with College Scorecard data (earnings, debt, default rates)

## Governance

Changes to this catalog aren't just a data edit — they're a governance action. See `CLAUDE.md` for the full governance model. Short version:

- **KKM** signs off before any FERPA-flagged KPI reaches client-facing output.
- **WDT** reviews production merges and owns Snowflake provisioning.
- **RDT** reviews peer/competitive content (relevant to the Benchmarking area).
- **LVP** owns architecture and strategic planning.

If a task would touch a FERPA-flagged KPI, a production merge, or peer-benchmarking content, stop and get the named human sign-off — these aren't just code review gates.

## Keeping the catalog, library page, and dashboard in sync

`higher_ed_kpi_catalog_enriched.csv` is canonical. If you add, rename, or re-categorize a KPI:

1. Update the CSV first (this repo).
2. Update the matching `DATA` entry and `METRIC_INFO` tooltip in `kpi_library.html` (this repo).
3. Update the corresponding dashboard section in `ditteau_data_transform/streamlit/dashboards/kpi_library/kpi_library_dashboard.py` — or add an honest Roadmap stub if the mart isn't built yet.
4. Re-check the Area / Type / FERPA counts in the guidelines doc if they've shifted.

**These artifacts have drifted out of sync before.** The 2026-07-22 reconciliation found 29 rows (21%) with incorrect status claims. Don't reintroduce the gap:
- Never mark a mart "NOT YET COMPUTABLE" without verifying it doesn't exist in `ditteau_data_transform`
- Never add a dashboard query without confirming the target mart/columns exist
- Never update calculation logic in one place without updating all three

## Catalog conventions

Per `CLAUDE.md`:
- **162 rows, 7 Areas:** Enrollment Management (32), Admissions (30), Financial Aid (29), Registration (27), Cross-Domain (23), Benchmarking (7), Finance (14)
- Each Area is a **contiguous block** in the CSV — keep it that way when inserting rows
- **`Type`** (Strategic / Operational / Compliance / Financial) ≠ **`Category`** in HTML (Strategic / Operational / Analytical / Tactical) — these are different taxonomies
- **`Time Series?` = Yes** pairs only with **`Indicator` = Leading or Lagging**; No always pairs with N/A
- **`FERPA Sensitive?` = Yes** on any row surfacing demographic subgroups (URM, first-gen, Pell) or individual-level academic records
- **`Calculation Logic` prefixes** to preserve:
  - `NOT YET COMPUTABLE —` the mart/column exists in name only, not built
  - `NO CONFIDENT MATCH —` no mart currently supports this calculation as titled
  - `COMPOSITE —` a dashboard drawing on several underlying metrics with no single defined formula
  - `PROPOSED —` calculation logic authored by best-effort reasoning, not verified against a real built model

## Recent changes

### 2026-09
- **Consolidated dashboards:** Removed `kpi_library_dashboard/` folder; the
  single canonical dashboard now lives in `ditteau_data_transform/streamlit/
  dashboards/kpi_library/`. This repo is now purely catalog & governance.
- Archived historical reconciliation docs to `archive/` folder
- Added `.gitignore` for cache, backup, and draft files

### 2026-08
- Added Finance domain to catalog (24 rows, 138→162 total)
- Added live Finance dashboard tab with Budget Performance and AR Aging
- Fixed Calculation Logic row-shift misalignment (rows 132-138)

### 2026-07
- Completed 4-phase reconciliation of catalog, HTML, dashboard, and dbt models
- Fixed Benchmarking tab SQL error (`debt_at_completion` → `debt_median_all`)
- Discovered and documented 2 previously undocumented marts (`mart_enrollment_demographics`, `mart_scorecard_program_outcomes`)
- Reconciliation docs now in `archive/`

## Contributing

Before making changes:
1. Read `CLAUDE.md` for source of truth, conventions, and governance gates
2. If touching FERPA-flagged content, obtain KKM sign-off first
3. Coordinate with WDT for any production deployment

## Questions?

- **Architecture & planning:** LVP
- **Data governance & FERPA:** KKM
- **Systems & Snowflake provisioning:** WDT
- **Peer/competitive benchmarking:** RDT
