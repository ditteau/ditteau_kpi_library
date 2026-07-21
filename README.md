# Ditteau KPI Library & Reference Dashboard

Higher-education KPI catalog, governance guidelines, and an example
Streamlit-in-Snowflake dashboard, built on the Ditteau Data Unified
Platform's Distribute layer.

## What's here

| File | What it is |
|---|---|
| `higher_ed_kpi_catalog_enriched.csv` | The canonical KPI/dashboard catalog — 138 rows across 6 Areas (Enrollment Management, Admissions, Financial Aid, Registration, Cross-Domain, Benchmarking). Single source of truth for KPI definitions, calculation logic, and governance flags (FERPA, build status). |
| `kpi_library.html` | A browsable, filterable version of the catalog (by Area / Type / Category), with calculation-logic tooltips. Mirrors the CSV — see "Keeping things in sync" below. |
| `kpi_library_dashboard.py` | Streamlit-in-Snowflake reference dashboard, one tab per Area, showing live examples of catalog KPIs against the `DEMEAU_DD_DEV` demo data. |
| `Ditteau_KPI_Dashboard_Guidelines.docx` | The governance document: KPI/dashboard type definitions, OKR-to-KPI alignment, target/threshold conventions, the FERPA gate, role-based KPI bundles, and the pre-publish checklist. Read this before adding or changing a KPI. |

## Current build status

- Most catalog rows have real, verified calculation logic drawn from built dbt models.
- Rows marked `NOT YET COMPUTABLE`, `NO CONFIDENT MATCH`, or `PROPOSED` in `Calculation Logic` are Roadmap, not production tiles — don't wire a dashboard to one of these and don't present it as authoritative.
- Known gaps worth knowing before you touch this repo:
  - **`snap_cohort_milestone` is unbuilt** — blocks the Cross-Domain dashboard tab and every Cross-Domain KPI that depends on it.
  - **`mart_enrollment_demographics`** isn't in the documented mart inventory, and has no age dimension despite one catalog KPI's title implying one.
  - **`mart_scorecard_program_outcomes`** (the whole Benchmarking area, 7 rows) doesn't exist yet — no schema, no dashboard code. The dashboard's Benchmarking tab is an honest "Roadmap" stub, not fabricated data.
  - **`mart_retention_cohort_summary`** — some catalog rows call it unbuilt; `kpi_library_dashboard.py` queries it successfully. Reconcile with data engineering before trusting either signal.

## Running the dashboard

This is a Streamlit-in-Snowflake app. It expects:
- A Snowpark session via `get_active_session()` — falls back gracefully (no Snowflake calls) if run outside Snowflake.
- `DB = "DEMEAU_DD_DEV"`, `SCHEMA = "DISTRIBUTE"` — update these constants near the top of `kpi_library_dashboard.py` to point at a different target.

To preview locally with `streamlit run kpi_library_dashboard.py`, you'll need network access to a Snowflake account with those objects, or you'll want to stub out `run_query`.

## Governance

Changes to this catalog aren't just a data edit — they're a governance action. See the guidelines doc, Section F, for the full model. Short version:

- **KKM** signs off before any FERPA-flagged KPI reaches client-facing output.
- **WDT** reviews production merges and owns Snowflake provisioning.
- **RDT** reviews peer/competitive content (relevant to the Benchmarking area).
- **LVP** owns architecture and strategic planning.

## Keeping the catalog, library page, and dashboard in sync

`higher_ed_kpi_catalog_enriched.csv` is canonical. If you add, rename, or re-categorize a KPI:

1. Update the CSV first.
2. Update the matching `DATA` entry and `METRIC_INFO` tooltip in `kpi_library.html`.
3. Update the corresponding dashboard section in `kpi_library_dashboard.py` — or add an honest Roadmap stub if the mart isn't built yet.
4. Re-check the Area / Type / FERPA counts in the guidelines doc if they've shifted.

These three artifacts have drifted out of sync before. Don't let it happen again.
