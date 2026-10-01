# CLAUDE.md

Operating context for Claude (and Claude Code) working in this repository.
Read this before editing any file here.

## What this repo is

A KPI catalog and reference library page for the Ditteau Data Unified
Platform — a multi-tenant higher-ed analytics product built on Snowflake
(Deposit → Deterge → Distribute medallion architecture, dbt-managed from
Deterge up). This repo is the KPI Library workstream: governed KPI
definitions and the browsable HTML reference. **It does not contain the
dbt models or the Streamlit dashboard** — those live in
`ditteau_data_transform` (dbt models in `/models`, dashboard in
`/streamlit/dashboards/kpi_library`).

## Source of truth

`higher_ed_kpi_catalog_enriched.csv` is canonical. Everything else derives
from it:

- `kpi_library.html` is a browsable mirror — its `DATA` array and
  `METRIC_INFO` map must match the CSV row-for-row.
- The Streamlit dashboard (`ditteau_data_transform/streamlit/dashboards/
  kpi_library/kpi_library_dashboard.py`) should only visualize KPIs the
  catalog marks as actually computable — never one whose `Calculation Logic`
  reads `NOT YET COMPUTABLE`, `NO CONFIDENT MATCH`, or `PROPOSED`.
- `Ditteau_KPI_Dashboard_Guidelines.docx` is the process document — read
  Section E (targets/thresholds) and Section F (governance/FERPA) before
  changing how a KPI is presented.

**If you edit the CSV or HTML here, check whether the dashboard in
`ditteau_data_transform` needs the same edit.** These artifacts have drifted
before, and reconciling that drift was real, non-trivial work — don't
reintroduce the gap.

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

## Known gaps (as of 2026-09-26 correction pass)

**⚠️ CORRECTION (2026-09-26):** `snap_cohort_milestone` IS **BUILT in DEMEAU PROD** (1,138 rows in DEMEAU_DD_PROD, also in DEV/TEST). The Cross-Domain tab should be functional.

**Unbuilt / Stub Models:**
- `mart_ipeds_reporting` — stub returning zero rows; awaiting
  stg_ipeds__peer_benchmarks provisioning.
- `mart_aid_leveraging` — 2 rows in DEMEAU PROD `[SNOWFLAKE-VERIFIED
  2026-10-01]`. Still a stub; row 145 is a scope expansion of it, not a new mart.

**⚠️ Finance lineage (added to this section 2026-10-01 — it predated the GL
work entirely and said nothing about it):**

- **The General Ledger IS ingested on the Jenzabar CX arm.** Several catalog
  rows asserted "no G/L source ingested"; that was false and rows 140 and 141
  have been corrected. Measured in `DEMEAU_DD_PROD` 2026-10-01:

  | Model | Rows |
  |---|---|
  | `int_gl_account_balances` | 2,975,685 (154,384 accounts, 19 fiscal years) |
  | `int_subsidiary_balances` | 921,770 |

  345 GL accounts carry `is_cash_account`; `net_asset_type_code` is populated
  (`U`/`T`/`P`).

- ⚠️ **Scope the claim by source arm.** This is **Jenzabar CX**, which arrives
  by Snowflake share. The **J1** arm — Merrimack's and DEMEAU's primary SIS —
  has six `stg_j1__*` finance staging models built over **empty** deposit
  tables and no intermediate at all. "G/L is ingested" is true of the platform
  and **false of Merrimack**. Never write the unqualified form.

- ⚠️ **`seed_gl_object_classification` does not exist, and it is the single
  highest-leverage gap in the Finance set.** Nothing in the platform knows
  which GL object codes are revenue, expense, asset or liability. One seed
  blocks or materially limits **seven** KPIs: 143, 144, 150, 152, 155, 156, 160.

  Both built finance marts name this gap and refuse to guess —
  `mart_finance_budget_variance` calls `object_code_leading_digit` "AN
  OBSERVATION, NOT A CLASSIFICATION", and `mart_ar_aging` declines the DSO
  denominator for the same reason. `docs/designs/mart_finance_cash_position_design.md`
  in `ditteau_data_transform` reaches the same conclusion independently.

  It is a **governance seed, not a lookup table** — same class as
  `seed_hold_domain_crosswalk`. Every row records a human accounting
  classification and carries its classifier and date. It is also
  **tenant-specific**: a chart of accounts is an institutional artifact and
  DEMEAU's classification does not transfer to Merrimack.

- ⚠️ `gasb_category_code` is null on all GL rows at DEMEAU and that is
  **expected, not a gap** — DEMEAU is pseudonymised Anselm data and Anselm
  reports under FASB. **Do not build a CFI on it.**

- ⚠️ **C-22 is a live defect**, not a future risk. `stg_jcx__subsidiary_balances`
  casts four columns to boolean on an assumed, unverified `Y`/`N` domain —
  `hld_pmt`, `disc_taken`, `single_ck`, `interest_wvd`. Anything reading those
  booleans today may be reading nulls, with no error. Row 163 depends on
  `is_discount_taken` and is flagged accordingly.

**Full gap analysis:** `ditteau_data_transform/docs/kpi_catalog/finance_kpi_support_gap_analysis.md`
(2026-10-01) — all 24 finance KPIs traced to the facts, dimensions, staging
models and seeds they need, with a recommended build sequence.

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
`st.radio` Area list in the dashboard (`ditteau_data_transform`).

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

## Finance Marts — built vs. proposed

**⚠️ CORRECTED 2026-10-01.** Two of the seven names below were built and
deployed to DEMEAU PROD and this list had not caught up. The CSV already knew —
rows 154, 156, 157 and 160 carry bare mart names — so the CSV was right and this
section was the stale one, which is the ordering the source-of-truth rule
predicts.

**Built and deployed** `[SNOWFLAKE-VERIFIED 2026-10-01, role DEMEAU_DBT_PROD]`:

| Mart | Rows in `DEMEAU_DD_PROD` | Serves |
|---|---|---|
| `mart_finance_budget_variance` | 57,005 | Rows 154, 156 |
| `mart_ar_aging` | 5 | Rows 146, 157, 160 |

⚠️ Both read Deterge intermediates directly — there is **no finance fact or
dimension** in the lineage. `dim_fiscal_period` exists in DEMEAU **DEV only**
(785 rows); it is **not in PROD**.

**Still proposed — not built models.** Do not create dbt models for these
without an LVP decision. The `(proposed)` prefix distinguishes them at a glance.

- `(proposed) mart_program_economics`
- `(proposed) mart_student_value`
- `(proposed) mart_finance_ratios`
- `(proposed) mart_ap_performance`
- `(proposed) mart_auxiliary_revenue`

⚠️ **`mart_ap_performance` is blocked on absent data, not on effort.** The CX
A/P archive is settled: 794,634 `financial`-domain balance rows, **80** with a
non-zero amount `[SNOWFLAKE-VERIFIED 2026-10-01]`. There is no payables position
to age, no payment-date column, and `purchase_order_number`'s modal value is
`'0'`. Do not sequence its four KPIs (158, 159, 161, 162, 163) as though effort
were the constraint.

⚠️ **`mart_auxiliary_revenue` needs a housing/residence-life source that is not
in the platform's source inventory at all.** Defer until one is scoped.

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

**3. ~~Possible undocumented AR data in the platform.~~ RESOLVED 2026-10-01 —
   but one live gap carries forward; read on before closing this.**

   ~~RDT reports that Jenzabar CX's `sbcust_rec` billing table already feeds
   `mart_enrollment_census_ntr`. If correct, student-account data is flowing
   without a `DATA_DOMAIN = FINANCE` tag and without having passed KKM
   review.~~

   The lineage is **not undocumented**. `int_subsidiary_balances` is an
   explicitly domain-tagged model: it emits a `data_domain` column routing
   student receivables to `student_accounts` and institutional payables to
   `financial`, and `mart_ar_aging` filters `where data_domain =
   'student_accounts'` downstream. `[REPO-VERIFIED 2026-10-01]` The model header
   documents the split at length, including why employee-facing subsidiaries
   (`W/P`, `E/P`, `FSMP`) have no home in the domain grid.

   ⚠️ **DO NOT CLOSE THIS ITEM WITHOUT CARRYING FORWARD THE GAP INSIDE IT.**
   There is **no `rap_student_accounts` row access policy.** The account holds
   four RAPs — `student_academic`, `admissions`, `financial_aid`,
   `student_health` — and none for receivables. `mart_ar_aging` works around
   this by publishing no `account_holder_id` at all, aggregating to
   subsidiary × aging bucket precisely because student-level balances are an
   education record.

   This is the hard blocker on rows **141** (Student LTV), **146** (Bad-Debt
   Risk Score) and any AR drill-through. **The RAP comes first — it is not a
   modelling detail and must not be resolved by adding `student_id` to
   `mart_ar_aging`.** Owner: **KKM**.

   ⚠️ Row 146 carries a second question beyond FERPA: predictive delinquency
   scoring joined to academic-risk signals raises a **use-limitation** issue
   (risk of adverse action against students). KKM review before it leaves draft.

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
