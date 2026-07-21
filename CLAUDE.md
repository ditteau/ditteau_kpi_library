# CLAUDE.md

Operating context for Claude (and Claude Code) working in this repository.
Read this before editing any file here.

## What this repo is

A KPI catalog, reference library page, and example dashboard for the
Ditteau Data Unified Platform — a multi-tenant higher-ed analytics product
built on Snowflake (Deposit → Deterge → Distribute medallion architecture,
dbt-managed from Deterge up). This repo is the KPI Library workstream:
governed KPI definitions plus a Streamlit-in-Snowflake reference dashboard
that reads from the Distribute layer. **It does not contain the dbt models
themselves** — those live in the main platform repo - ditteau_data_transform.

## Source of truth

`higher_ed_kpi_catalog_enriched.csv` is canonical. Everything else derives
from it:

- `kpi_library.html` is a browsable mirror — its `DATA` array and
  `METRIC_INFO` map must match the CSV row-for-row.
- `kpi_library_dashboard.py` should only visualize KPIs the catalog marks
  as actually computable — never one whose `Calculation Logic` reads
  `NOT YET COMPUTABLE`, `NO CONFIDENT MATCH`, or `PROPOSED`.
- `Ditteau_KPI_Dashboard_Guidelines.docx` is the process document — read
  Section E (targets/thresholds) and Section F (governance/FERPA) before
  changing how a KPI is presented.

**If you edit one of the three files above, check whether the other two
need the same edit.** They have drifted before, and reconciling that drift
was real, non-trivial work (cross-referencing dashboard query code against
catalog claims to figure out what was actually true) — don't reintroduce
the gap.

## Catalog conventions

- 138 rows, 6 Areas: Enrollment Management (32), Admissions (30),
  Financial Aid (29), Registration (27), Cross-Domain (13), Benchmarking (7).
  Each Area is a **contiguous block** in the CSV — keep it that way when
  inserting rows; don't scatter an Area's rows across the file.
- `Type` (Strategic / Operational / Compliance / Financial) is a
  governance-and-planning axis. The HTML's `cat` / Category
  (Strategic / Operational / Analytical / Tactical) is a dashboard-routing
  axis. **These are not the same taxonomy** — don't infer one from the other.
- `Time Series?` = Yes pairs only with `Indicator` = Leading or Lagging;
  `Time Series?` = No always pairs with `Indicator` = N/A.
- `FERPA Sensitive?` = Yes on any row surfacing demographic subgroups
  (URM, first-gen, Pell) or individual-level academic records, even in
  aggregate. This triggers the KKM sign-off gate — treat it as a policy
  question, not a data-classification checkbox.
- `Calculation Logic` prefixes to preserve when adding or editing rows:
  - `NOT YET COMPUTABLE — ...` — the mart/column exists in name only, not built.
  - `NO CONFIDENT MATCH — ...` — no mart currently supports this calculation as titled.
  - `COMPOSITE — ... Needs manual definition.` — a dashboard drawing on
    several underlying metrics with no single defined formula.
  - `PROPOSED — ...` — calculation logic authored by best-effort reasoning
    (e.g., from platform conventions or existing dashboard code), not
    verified against a real, built model. Use this prefix instead of
    presenting an authored definition as confirmed fact.

## Known gaps (as of the last reconciliation)

- `snap_cohort_milestone` is unbuilt — blocks the Cross-Domain dashboard
  tab and every Cross-Domain KPI that targets it.
- `mart_enrollment_demographics` is not in the documented mart inventory.
  Confirmed columns (from dashboard code): `total_headcount`, `urm_count`,
  `first_gen_count`, `fulltime_count`, by `academic_year`. No age
  dimension exists despite one catalog KPI's title implying one.
- `mart_scorecard_program_outcomes` — the entire Benchmarking area
  (7 rows) targets this mart, which doesn't exist: no schema, no dbt
  model, zero prior references anywhere in `kpi_library_dashboard.py`.
  Treat every Benchmarking KPI as Roadmap until this changes.
- `mart_retention_cohort_summary` — conflicting signals: several catalog
  rows call it unbuilt as of 2026-06-30, but `kpi_library_dashboard.py`
  queries it successfully with `program_name`, `yr1_retention_rate`,
  `yr6_grad_rate`, `cohort_size`, `has_yr1_data`. Reconcile with WDT
  before trusting either signal as-is.
- "Retention Risk Early Warning Indicators" is cataloged against
  `mart_retention_cohort_summary` (lagging, cohort-level data) but
  conceptually belongs on `mart_student_at_risk`
  (`is_at_risk`, `risk_tier`, `risk_factor_count`) — likely a
  mart-assignment error, not yet resolved.

## Governance gates — do not route around these

- **KKM** — data governance & quality. Required sign-off before any
  FERPA-flagged KPI reaches client-facing output. Also owns PII /
  `data_class` changes.
- **WDT** — systems & security/infra. Required reviewer for production
  merges; owns Snowflake provisioning; executes any Claude Code
  instructions that touch the live platform.
- **RDT** — strategic placement & marketing. Reviews peer/competitive
  content — relevant to the Benchmarking area's peer-benchmarking KPIs.
- **LVP** — architecture & strategic planning.

If a task would touch a FERPA-flagged KPI, a production merge, or
peer-benchmarking content, say so explicitly and stop rather than
proceeding — these need a named human sign-off, not just code review.

## Platform conventions that apply to any code in this repo

- Rates are stored as decimals (`0.62`, not `62`) — format as a
  percentage at the presentation layer only, never in a mart or query.
- `snake_case` columns; `COALESCE` for NULL-safe aggregation.
- `dim_student` is SCD Type 2 — never filter `is_current = true` except
  for explicit current-state tiles; point-in-time KPIs need full history.
- Snowflake GROUP BY quirk: column aliases aren't valid in `GROUP BY` —
  repeat the full expression, including full `CASE` expressions.
- No masking logic in application/dashboard SQL — masking is enforced by
  Snowflake policies on the Distribute schema only.

## When generating documents from this repo

The guidelines doc follows Serensoft/Ditteau house style: Georgia
headings (Heading 1 crimson `#740049`, Heading 2/3 blue `#4285f4`),
lettered top-level sections (A, B, C…), circle-bullet (○) sub-items,
⚠️ for warnings. Match this if asked to extend, regenerate, or reformat it.
