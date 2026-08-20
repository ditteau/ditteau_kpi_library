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

- 162 rows, 7 Areas: Enrollment Management (32), Admissions (30),
  Financial Aid (29), Registration (27), Cross-Domain (23), Benchmarking (7),
  Finance (14). Each Area is a **contiguous block** in the CSV — keep it that
  way when inserting rows; don't scatter an Area's rows across the file.
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

## Known gaps (as of 2026-07-22 reconciliation)

**Unbuilt / Stub Models:**
- `snap_cohort_milestone` — unbuilt; blocks Cross-Domain dashboard tab
  and all Cross-Domain KPIs that target it.
- `mart_ipeds_reporting` — stub returning zero rows; awaiting
  stg_ipeds__peer_benchmarks provisioning.

**Data Gaps in Built Models:**
- `snap_aid_term` — PowerFAIDS integration pending; affects
  `coa_amount`, `efc_amount` (unmet need calculations) in
  `mart_aid_leveraging`. Core leveraging metrics (merit/need split, aid
  band yield) are functional.
- `mart_enrollment_census_ntr` — DEMEAU synthetic data has zero billing
  values (`account_value=0` in sbcust_rec → `gross_tuition_billed=0`),
  but model logic is complete and will activate with production school data.
- NSC integration pending — affects transfer-out tracking in
  `snap_cohort_milestone` and `mart_retention_cohort_summary`. Currently
  transfer-outs are counted with stop-outs.

**Schema Gaps:**
- Age demographics — `mart_enrollment_demographics` exists and is
  functional (columns: `total_headcount`, `urm_count`, `first_gen_count`,
  `fulltime_count` by `academic_year`), but no `age_band` dimension
  exists. Row 131 title implies age breakdown but only enrollment intensity
  (full-time rate) is computable.

**Previously Undocumented but Functional:**
- `mart_enrollment_demographics` — built and functional; not in prior
  mart inventory.
- `mart_scorecard_program_outcomes` — built and functional; powers
  Benchmarking dashboard tab with College Scorecard data (earnings, debt,
  default rates by program).

## Finance Domain Integration — Standing Decisions (LVP, 2026-08)

The following decisions are settled and should not be relitigated:

1. **Category 1 candidates are `Cross-Domain`, not `Finance`.** The ten KPIs
   that join Finance data to Enrollment, Admissions, Registration, or
   Financial Aid data take `Area = Cross-Domain`.

2. **Finance is one Area.** `student_accounts` does not become a separate
   sub-area. G/L, Student Accounts (AR), and A/P all live under
   `Area = Finance`, with separation carried by the `Primary Source System`
   column instead. This matches the single `FINANCE` value already reserved
   by the `DATA_DOMAIN` governance tag.

3. **The catalog is aspirational as well as descriptive.** Category 3
   (ERP-native) rows enter the governed catalog now, before per-client ERP
   feasibility is confirmed. The `PROPOSED —` prefix carries that status.
   A row with no ingested source is legitimate catalog content.

4. **The HTML library is authoritative at 162 rows.** CSV and HTML are now
   synchronized. (Prior reconciliation closed the 127→138 gap; Finance
   integration added 24 rows for 162 total.)

## Finance Vocabulary Additions (2026-08)

**Area:** `Finance` added to `AREA_ORDER` in `kpi_library.html` and to
`st.radio` Area list in `kpi_library_dashboard.py`.

**Update Frequency:** `Monthly` — twelve of the 24 Finance rows use this;
finance operates on fiscal periods rather than academic terms. Do not
coerce to `Term`.

**Primary Source System:** Three new values:
- `Jenzabar:Workday:Banner (Finance)` — mirrors existing interchangeable-SIS
  convention
- `Student Accounts (AR)`
- `A/P`

**Audience:** Three new values:
- `Controller`
- `A/P Manager`
- `VP Student Affairs`

(`Bursar` and `CFO` already exist in the vocabulary.)

## Proposed Finance Marts (not yet designed)

The following `(proposed) mart_*` names appear in the Finance rows. These
are **not built models** — do not create dbt models for them without an
LVP decision. The `(proposed)` prefix distinguishes them from built marts
at a glance.

- `(proposed) mart_program_economics`
- `(proposed) mart_student_value`
- `(proposed) mart_finance_ratios`
- `(proposed) mart_finance_budget_variance`
- `(proposed) mart_ar_aging`
- `(proposed) mart_ap_performance`
- `(proposed) mart_auxiliary_revenue`

## Finance Integration Findings — Pending Human Decision

These require human decisions. Do not act on them; record and surface.

**1. Six Finance candidates overlap existing catalog rows.**
   The dedupe decision is LVP's. Overlaps identified:
   - *Net Tuition Revenue per FTE by Program/Major* overlaps *Net Tuition
     Revenue per Student* (Financial Aid) and *Revenue per Enrolled Student*
     (Enrollment Management). All three depend on `mart_enrollment_census_ntr`.
   - *Customer Acquisition Cost vs. LTV* — its CAC numerator is the existing
     Admissions row *Cost Per Enrolled Student*.
   - *Discount Rate by Student Segment* overlaps *Tuition Discount Rate* and
     *Tuition Discount Rate Trend (5-Year)*.
   - *Aid Leveraging ROI (Extended)* is a scope expansion of the existing
     `mart_aid_leveraging` stub, not a new mart.
   - *Retention-Adjusted Revenue Forecast* is blocked by the same missing NTR
     dependency that already produced the `NO CONFIDENT MATCH` flag on
     *Revenue per Completed Student*.

**2. `Cost Per Enrolled Student` declares `Slate / GL` as its source system.**
   The catalog asserts a `GL` source for a system the platform does not
   ingest. Either the bare `GL` token retires in favor of the new
   finance-ERP vocabulary, or that row is reflagged `PROPOSED` alongside
   the Finance set. Do not change it without LVP decision.

**3. Possible undocumented AR data in the platform.**
   RDT reports that Jenzabar CX's `sbcust_rec` billing table already feeds
   `mart_enrollment_census_ntr`. If correct, student-account data is flowing
   without a `DATA_DOMAIN = FINANCE` tag and without having passed KKM
   review. **This is a governance exposure.** Do not trace, modify, or
   retag the lineage yourself. Surface to KKM and LVP.

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
