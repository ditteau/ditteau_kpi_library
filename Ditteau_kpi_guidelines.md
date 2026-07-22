# Ditteau KPI & Dashboard Guidelines

**Higher Education KPI Library & Dashboard Standards**

---

## A. Purpose & Scope

This document sets the standard for how KPIs are defined, governed, and surfaced across every Ditteau dashboard.

**Scope** covers two deliverables: the KPI Library (governed definitions of catalog KPIs, so no two dashboards compute "yield rate" differently) and the reference dashboard built on top of existing Distribute marts. Both draw from one source of truth: `higher_ed_kpi_catalog.csv`.

**Audience:** Serensoft personnel building or reviewing a KPI-driven dashboard on the Ditteau platform.

### Catalog Coverage

| Area | Entries | Share of Catalog |
|------|---------|------------------|
| Enrollment Management | 32 | 23% |
| Admissions | 30 | 22% |
| Financial Aid | 29 | 21% |
| Registration | 27 | 20% |
| Cross-Domain | 13 | 9% |
| Benchmarking | 7 | 5% |

---

## B. What a Higher-Ed KPI Dashboard Is (and Isn't)

A KPI dashboard, a metric view, and a report solve different problems. Confusing them is the single most common reason a Ditteau dashboard build stalls in review.

| Aspect | KPI Dashboard | Metric View | Report |
|--------|---------------|-------------|--------|
| **Purpose** | Live command center for enrollment-cycle and academic-operations decisions | Ad hoc exploration for IR/analysts diagnosing a shift | Point-in-time snapshot for the Board, cabinet, or an IPEDS/accreditation submission |
| **Audience** | VP Enrollment, Registrar, Provost, CFO — people who act same-day | Institutional Research analysts | President, Board, accreditors |
| **Update cadence** | Term, Weekly, or Daily (spring) per catalog | On demand | Annual, tied to the academic calendar |
| **Best for** | Ongoing visibility during the admissions or registration cycle | Root-cause diagnosis (why did Section Fill Rate drop in Biology?) | Recapping a cohort's outcome for governance or compliance |

**Example:** a Registrar checks the Registration Holds dashboard every morning during add/drop. When holds spike in one department, they drill into a metric view segmented by hold code. At term close, IR pulls a report summarizing the term for the Provost's cabinet.

---

## C. Four Dashboard Types, Higher-Ed Audiences

Every catalog row is tagged Strategic, Operational, Analytical, or (implicitly) Tactical through its Audience and Update Frequency. Use that tag to route the KPI to the right dashboard type:

| Type | Audience | Cadence | Decisions Enabled |
|------|----------|---------|-------------------|
| **Strategic** | President, Board, CFO | Annual / Term | Resource allocation, enrollment strategy, board reporting — e.g. Enrollment Health Scorecard |
| **Operational** | Registrar, Admissions Director, Deans | Daily / Weekly | Same-cycle adjustments — e.g. Funnel Pipeline (Real-Time), Registrar Operations |
| **Analytical** | Provost, Institutional Research | On-demand | Trend and correlation investigation — e.g. Admission Profile → Retention Correlation |
| **Tactical** | Deans, Advisors, Financial Aid Director | Daily / Weekly / Term | Section scheduling, advising, aid leveraging — e.g. Student Academic Progress |

### Core Components

| Component | Definition | Ditteau Example |
|-----------|------------|-----------------|
| **KPI** | Core measure tied to an institutional objective | Admit-to-Yield Rate, Tuition Discount Rate |
| **Targets & thresholds** | Defined goals plus red/yellow/green logic | Section Fill Rate: red <60%, watch >90% capacity risk, green 60–90% |
| **Visualizations** | Chart matched to the KPI type | Line chart for Deposit Pace vs. Prior Year; gauge for Section Fill Rate |
| **Data connectors** | The governed mart feeding the tile | `mart_admissions_funnel`, `mart_aid_summary`, `snap_cohort_milestone` |
| **Ownership** | Named accountable role | Admissions Director owns Deposit Conversions; Financial Aid Director owns Aid Budget vs. Actuals |

---

## D. From Institutional OKRs to Ditteau KPIs

Two different tools, often confused. Getting the distinction right decides whether a dashboard drives decisions or just decorates a status meeting.

### OKR vs. KPI: What's the Difference

An **OKR** is a goal-setting structure: an Objective (qualitative, ambitious — "strengthen first-year persistence") paired with Key Results, a small set of measurable outcomes that would prove you got there ("raise fall-to-fall retention from 78% to 82%"). It's inherently time-bound and cascading: institutional OKRs break into divisional ones, which break into departmental ones.

A **KPI** is a measurement — an ongoing metric tracked whether or not it's tied to a current goal. Section Fill Rate is a KPI whether or not anyone has set a target for it this year.

**The relationship:** a Key Result usually needs one or more KPIs to know if it's being hit, but not every KPI is in service of an active Key Result — compliance reporting and routine operational monitoring need to exist continuously, goal or no goal. The failure mode to watch for, especially in higher ed: treating the KPI list itself as the strategic plan. A dashboard full of well-tracked metrics with no Key Result behind it tells you the temperature of the room, not whether you're winning.

### Objective → Key Result → Catalog KPI

Higher-ed OKRs run on the academic calendar, not the sprint. A Key Result is checked at census date, term close, or the end of an admissions cycle — not every two weeks. Map each Key Result to a catalog KPI, not the other way around; the catalog should not grow new rows just to fit a slide.

**Three worked chains, using real catalog rows:**

- ○ **Objective:** Strengthen first-year persistence. **Key Result:** raise fall-to-fall retention from 78% to 82% by AY2028. **KPIs:** Term-to-Term Re-Enrollment Tracker (`snap_retention_term`, Leading) during the cycle; Cohort Survival & Graduation (`snap_cohort_milestone`, Lagging) to confirm the outcome a year later.

- ○ **Objective:** Improve enrollment-funnel efficiency. **Key Result:** reduce spring melt (deposit-to-enrolled loss) by 3 points. **KPIs:** Deposit Conversions and Deposit Pace vs. Prior Year (`mart_admissions_funnel` / `snap_admissions_weekly`, both Leading).

- ○ **Objective:** Protect net tuition revenue. **Key Result:** hold tuition discount rate within the 40–55% peer-benchmark band. **KPI:** Tuition Discount Rate, Net Tuition Revenue per Student — both target `mart_enrollment_census_ntr`, unbuilt as of the current snapshot. Treat this Key Result as a roadmap dependency, not a published tile, until that mart lands.

This is where the catalog's **Indicator** column earns its keep: 12 rows are tagged Leading, 44 Lagging, the remaining 82 N/A (mostly point-in-time KPIs with no trend view). A cabinet-level OKR needs at least one leading indicator so the institution can act mid-cycle, not just confirm the outcome after census.

### Vocabulary Worth Standardizing

- ○ **Melt** — loss of admitted or deposited students who never show up for census.
- ○ **Census date** — the official date (commonly day-10 or day-20 of term) enrollment counts lock for IPEDS, state, and federal reporting.
- ○ **Cohort** — the officially defined first-time, full-time (or transfer) group tracked for retention and graduation; IPEDS uses 150%-of-normal-time as the completion standard — 6 years for 4-year programs, 3 for 2-year programs.
- ○ **Discount rate** — institutional aid ÷ gross tuition revenue; the primary lever on net tuition revenue.
- ○ **Unmet need** — cost of attendance minus expected family/student contribution minus total aid awarded.

---

## E. KPI Selection Framework

Not every catalog row belongs on a dashboard tile. Run each candidate through this test before it ships:

| Criteria | Question to Ask | Pass/Fail |
|----------|----------------|-----------|
| **Alignment** | Does it trace to a strategic-plan objective or an accreditation/compliance requirement? | Required |
| **Controllability** | Can the named Audience actually act on it? | Required |
| **Timeliness** | Does Update Frequency match the decision cycle it serves? | Required |
| **Leading vs. lagging** | Is the Indicator Leading, Lagging, or N/A — does the bundle balance both? | Balance |
| **Clarity** | Can a Dean read the tile without a footnote? | Required |
| **Computability** | Does Calculation Logic resolve to a real column, or say NOT YET COMPUTABLE / NO CONFIDENT MATCH? | Required — see Section E |

### A completed example, pulled straight from the catalog:

| Objective | KPI | Mart / View | Audience | Cadence |
|-----------|-----|-------------|----------|---------|
| Reduce spring melt | Deposit Pace vs. Prior Year | `snap_admissions_weekly` | Admissions Director, VP Enrollment | Daily (spring) |
| Right-size course sections | Section Fill Rate | `mart_section_utilization` | Registrar, Deans | Term — currently a null stub; flag as Roadmap |
| Protect first-gen completion | First-Gen Enrollment % | `mart_admissions_class_profile` | VP Enrollment, Financial Aid | Term — FERPA-sensitive, KKM gate applies |

---

## F. Targets, Thresholds & Status Logic

Rates in every Ditteau mart are stored as decimals (0.62, not 62). Format the percentage at the presentation layer — never inside the mart.

Higher ed is cyclical, not continuous, so baseline the way `snap_admissions_weekly` already does: index everything to `snapshot_week_num` (weeks since October 1 of the entry-year cycle) and compare the current cycle to the same week in prior cycles, rather than a trailing rolling average that smooths right through the admissions season's real peaks and troughs. The same logic applies to any December enrollment push — compare this December to last December, not to November, or every cycle looks like a spike.

| Element | How to Set It | Example |
|---------|---------------|---------|
| **Baseline** | Prior-cycle value at the same `snapshot_week_num` | Fall 2025 fill rate at week 6 |
| **Green** | Within the healthy operating band | 60–90% capacity |
| **Yellow** | Under-enrolled; watch for consolidation | 50–59% capacity |
| **Red** | Under-enrolled (waste) or over-capacity (compliance/safety risk) | <50% or >90% |

---

## G. Governance, FERPA & Change Management

The catalog's **Calculation Logic** column is the KPI dictionary. A dashboard tile never recalculates a KPI locally — it renders exactly what the governed mart returns.

| Governance Element | What It Means | Ditteau Example |
|--------------------|---------------|-----------------|
| **Data lineage** | Every tile shows its Mart/View, Primary Source System, and last-refresh time | Section Fill Rate cites `mart_section_utilization`, Jenzabar:Workday:Banner, Term |
| **FERPA gate** | KKM sign-off required before any FERPA-flagged KPI reaches client-facing output | 34 of 138 catalog rows are flagged FERPA Sensitive — First-Gen %, URM %, Student Academic Progress, FAFSA/Verification Completion, URM Equity & Retention Gap Analysis, and Pell vs. Non-Pell Earnings Gap among them |
| **Access enforcement** | Masking and row-access policies applied only in the Distribute schema, never as a dashboard-level filter | `mart_academic_progress` exposes `student_key` at row grain; RBAC is mandatory before client-facing delivery |
| **Change management** | Known Caveats is the changelog trigger | Resolving a caveat (e.g., populating `section_capacity`) updates the catalog row and the dashboard tile together, versioned |

⚠️ **That's the whole test, really:** if KKM hasn't signed off and the mart isn't masked at the Distribute layer, a FERPA-flagged KPI does not go client-facing.

---

## H. Visualization Playbook

Match the KPI type to the chart, not the other way around:

| KPI Type | Chart | Ditteau Example |
|----------|-------|-----------------|
| **Progress-to-target** | Gauge or bullet chart | Section Fill Rate against the 60–90% band |
| **Rate over time** | Line chart with target band | Deposit Pace vs. Prior Year, indexed to `snapshot_week_num` |
| **Part-to-whole** | Stacked bar (not pie) | Institutional aid by fund type in `mart_aid_summary` |
| **Comparison across categories** | Sorted horizontal bar | Fill rate by department |
| **Distribution** | Histogram | Admitted-cohort GPA/test-score distribution in `mart_admissions_class_profile` |

---

## I. Role-Based KPI Bundles

Bundles below map directly to the catalog's **Audience** column. Pick five to ten per dashboard — more than that and nobody scans past the first row.

### President / Board — Strategic

Enrollment Health Score (Composite), Enrollment Health Scorecard, 10-Year Enrollment Trend, Tuition Discount Rate, Cohort Survival & Graduation.

**Action trigger:** If the Enrollment Health Score composite drops two consecutive terms, add a standing agenda item to the next Board finance & enrollment committee meeting.

### VP Enrollment / Admissions Director — Funnel & Yield

Inquiry-to-Application Rate, Application-to-Admit Rate, Admit-to-Yield Rate, Deposit Conversions, Stealth Applicant %, Year-over-Year Funnel Comparison.

**Action trigger:** If Deposit Pace falls more than 5 points behind the same week last cycle, escalate to VP Enrollment to revisit aid leveraging before the next disbursement window.

### Registrar / Deans — Registration Operations

Section Fill Rate, Waitlist Volume Trend, Registrar Operations (holds), Room & Faculty Utilization.

**Action trigger:** If a section's fill rate holds below 60% two terms running, route to the Dean for a consolidation or cancellation decision before the next term's schedule builds.

### Financial Aid Director / CFO — Aid & Revenue

Tuition Discount Rate, Net Tuition Revenue per Student, Aid Budget vs. Actuals, Avg Institutional Award per Student, FAFSA Completion Rate, Verification Completion Rate.

**Action trigger:** If Verification Completion Rate drops below target inside the FAFSA season window, alert the Financial Aid Director with the list of students still in selected/pending status.

### Provost / Institutional Research — Compliance & Cohort Analytics

Cohort Survival & Graduation, IPEDS Reporting Prep, First-Gen Enrollment %, Underrepresented Minority %, Enrollment Cohort Analysis.

**Action trigger:** If a cohort's stop-out share exceeds the prior three-cohort average at the same years-since-entry mark, flag it for the retention committee's next review.

### CFO / Provost / Financial Aid Director — Benchmarking (Roadmap)

Program Earnings vs. Debt ROI, Post-Graduation Earnings Benchmarking, Pell vs. Non-Pell Earnings Gap, Student Debt Burden vs. Peers, Loan Default Rate (College Scorecard), Borrower-Based Repayment Rate (BBRR), Earnings-to-Debt Ratio by Program.

**Action trigger:** None yet — every KPI in this bundle targets `mart_scorecard_program_outcomes`, which isn't built. Treat the whole bundle as Roadmap (Section E) until data engineering confirms the schema and source feed (College Scorecard / NSLDS).

---

## J. Pre-Publish Checklist

Run every KPI or dashboard tile through this checklist before it ships:

### Build & Design

1. KPI traces to a strategic-plan objective or accreditation requirement (Section D).
2. Update Frequency matches the decision cycle it serves.
3. Chart type matches the KPI type (Section H).
4. Dashboard holds five to ten KPIs, not more.

### Governance & FERPA

5. Calculation Logic is fully resolved — no NOT YET COMPUTABLE, NO CONFIDENT MATCH, or Needs manual definition.
6. FERPA Sensitive? confirmed; KKM sign-off obtained if Yes.
7. Masking and row-access enforced at the Distribute layer, not the dashboard.
8. Mart/View, Primary Source System, and last-refresh time are visible on the tile.

### Action & Adoption

9. Named owner (from Audience) assigned with an escalation path.
10. Threshold band set (green/yellow/red) with a documented baseline.
11. Action trigger written in plain language for at least the Strategic and Operational bundles.
12. Known Caveats footnoted on the tile, not buried in the catalog alone.
