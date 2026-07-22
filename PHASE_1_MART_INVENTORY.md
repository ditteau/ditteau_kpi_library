# Phase 1: Mart/Snap Inventory — Ground Truth

**Date:** 2026-07-22
**Purpose:** Reconcile `higher_ed_kpi_catalog_enriched.csv` against actual dbt models in `ditteau_data_transform`

## Executive Summary

**Critical Finding:** Multiple marts the catalog claims are "unbuilt" or "NOT YET COMPUTABLE" are **actually fully built and queryable**. This represents significant catalog drift.

---

## Snapshot Models (All BUILT)

| Model | Status | Notes |
|-------|--------|-------|
| `snap_admissions_weekly` | ✅ BUILT | Powers cycle-over-cycle funnel tracking |
| `snap_aid_term` | ⚠️ BUILT BUT NO DATA | Returns zero rows until fact_aid_award has data; model structure is complete |
| `snap_cohort_milestone` | ✅ BUILT | NSC not integrated (transferred_out, nsc_verified are null stubs) but model is functional |
| `snap_enrollment_term` | ✅ BUILT | FTE column is null stub pending load_status integration |
| `snap_retention_term` | ✅ BUILT | Fully functional |

---

## Mart Status by Domain

### Admissions Domain

| Mart | Catalog Claims | **ACTUAL STATUS** | Critical Columns |
|------|----------------|-------------------|------------------|
| `mart_admissions_funnel` | BUILT | ✅ **CORRECT** | inquiry_to_app_rate, admit_rate, yield_rate, deposit_count, stealth_app_pct |
| `mart_admissions_class_profile` | BUILT | ✅ **CORRECT** | avg_hs_gpa, avg_sat_total, avg_act_composite, geographic_diversity_index, first_gen_rate, urm_rate |

### Registration Domain

| Mart | Catalog Claims | **ACTUAL STATUS** | Critical Columns |
|------|----------------|-------------------|------------------|
| `mart_section_utilization` | BUILT (with null stubs) | ✅ **CORRECT** | enrolled_count, waitlisted_count, add_drop_rate, incomplete_rate<br>⚠️ **Null stubs:** fill_rate, capacity_gap (pending section_capacity in dim_course_section) |
| `mart_academic_progress` | BUILT | ✅ **CORRECT** | credits_remaining, on_track_gpa_flag, cumulative_earned_hours, is_sap_compliant |
| `mart_registration_holds` | BUILT | ✅ **CORRECT** | is_active, blocks_registration, hold_code, hold_description |

### Financial Aid Domain

| Mart | Catalog Claims | **ACTUAL STATUS** | Critical Columns |
|------|----------------|-------------------|------------------|
| `mart_aid_summary` | BUILT | ✅ **CORRECT** | total_offered, verification_completion_rate, sap_compliance_rate, pell_recipient_pct, r2t4_rate<br>⚠️ **Null stub:** fafsa_completion_rate (fafsa_completed flag not yet surfaced) |
| `mart_aid_leveraging` | **"NOT YET COMPUTABLE — stub returning zero rows"** | ❌ **WRONG — FULLY BUILT!** | Program/term grain aid leveraging analysis. inst_aid_offered, yield by aid band, merit/need split. ⚠️ Unmet need/COA metrics null until PowerFAIDS but core model is complete. |
| `mart_financial_aid_trend` | BUILT | ✅ **CORRECT** | Time-series financial aid metrics |

### Enrollment Management Domain

| Mart | Catalog Claims | **ACTUAL STATUS** | Critical Columns |
|------|----------------|-------------------|------------------|
| `mart_enrollment_census` | BUILT (with null stubs) | ✅ **CORRECT** | headcount, fte, student_type, load_status, credits_per_fte, withdraw_rate<br>⚠️ **Null stubs:** gross_tuition_billed, net_tuition_revenue, discount_rate, ntr_per_student |
| `mart_enrollment_census_ntr` | **"NOT YET COMPUTABLE — unbuilt as of 2026-06-30"** | ❌ **WRONG — FULLY BUILT!** | gross_tuition_billed, net_tuition_revenue, discount_rate, ntr_per_student. ⚠️ DEMEAU synthetic data: account_value = 0 → gross billed = 0, but model is complete. |
| `mart_enrollment_demographics` | **Not in documented mart inventory per CLAUDE.md** | ✅ **BUILT — UNDOCUMENTED!** | total_headcount, urm_count, first_gen_count, fulltime_count by academic_year. Powers Demographics tab in DEMEAU dashboard v2. ⚠️ Residency null stubs. |
| `mart_retention_cohort_summary` | **"NOT YET COMPUTABLE — unbuilt as of 2026-06-30"** | ❌ **WRONG — FULLY BUILT!** | yr1_retention_rate, yr4_grad_rate, yr6_grad_rate, cohort_size, yr1_stop_out_rate, first_gen_stop_out_rate, urm_stop_out_rate, has_yr1_data. Pivots snap_cohort_milestone to IPEDS-standard grain. |
| `mart_student_at_risk` | **"NOT YET COMPUTABLE — unbuilt as of 2026-06-30"** | ❌ **WRONG — FULLY BUILT!** | is_at_risk, risk_tier, risk_factor_count, student-level early warning flags. ⚠️ FERPA HIGH: student_key exposed at row level. |
| `mart_executive_summary` | **"unbuilt as of 2026-06-30"** | ✅ **BUILT** | Composite metrics. ⚠️ Discount rate and NTR components stubbed pending billing fact. |
| `mart_ipeds_reporting` | **"NOT YET COMPUTABLE — returns zero rows (stub)"** | ✅ **CORRECT — CONFIRMED STUB** | meta = stub: true. Returns WHERE 1=0 for all CTEs. Blocked on NSC deposit (CDR) and IPEDS benchmark feed (peer comparison, CDS metrics). |
| `mart_ipeds_fall_enrollment` | Marked as unbuilt in some catalog rows | ✅ **BUILT** | Fall enrollment snapshot. ⚠️ Degree-seeking tracked as total UG headcount until further refinement. |
| `mart_ipeds_peer_comparison` | Separate from mart_ipeds_reporting | ✅ **BUILT** | IPEDS enrollment and graduation rate benchmarks vs. peer group. |

### Benchmarking Domain

| Mart | Catalog Claims | **ACTUAL STATUS** | Critical Columns |
|------|----------------|-------------------|------------------|
| `mart_scorecard_program_outcomes` | **"does not appear in documented mart inventory" per CLAUDE.md** | ✅ **BUILT — UNDOCUMENTED!** | earn_median_4yr, debt_at_completion, earn_vs_national_pct, earn_median_pell_4yr, earn_median_nopell_4yr, cdr_3yr, repayment_rate_3yr. Sources from stg_scorecard__field_of_study. All 7 Benchmarking KPIs (rows 132–138) can be computed. |

---

## Catalog Misalignments Requiring Immediate Fix

### 🔴 HIGH PRIORITY — Marts Incorrectly Marked "Unbuilt"

1. **mart_retention_cohort_summary** (affects 4 catalog KPIs)
   - Catalog rows 39, 92, 93, 94, 114 claim "NOT YET COMPUTABLE — unbuilt"
   - **Reality:** Fully built table. Dashboard queries it successfully (kpi_library_dashboard.py:654, 807)
   - **Impact:** First-Year Retention Rate, Year-over-Year Retention Rate, Stop-Out Rate, Graduation Rate (4yr/6yr) all marked as unavailable when they ARE available

2. **mart_enrollment_census_ntr** (affects 4 catalog KPIs)
   - Catalog rows 58, 59, 97, 98 claim "NOT YET COMPUTABLE — unbuilt"
   - **Reality:** Fully built table with complete NTR logic
   - **Caveat:** DEMEAU synthetic data has account_value = 0 → gross_tuition_billed = 0, but model structure is complete
   - **Impact:** Tuition Discount Rate, Net Tuition Revenue per Student, Projected vs. Actual NTR, Revenue per Enrolled Student

3. **mart_student_at_risk** (affects 2 catalog KPIs)
   - Catalog rows 95, 112 claim "NOT YET COMPUTABLE — unbuilt"
   - **Reality:** Fully built table with risk scoring
   - **Impact:** At-Risk Student Count, Retention Early Warning dashboard

4. **mart_aid_leveraging** (affects 3 catalog KPIs)
   - Catalog rows 62, 81, 83 claim "NOT YET COMPUTABLE — stub returning zero rows"
   - **Reality:** Fully built table with aid band analysis and merit/need split
   - **Caveat:** Unmet need and COA-based discount remain null until PowerFAIDS provides COA/EFC, but core leveraging metrics exist
   - **Impact:** Leveraging Efficiency, Aid Budget Monitor, Aid Leveraging Model

5. **mart_enrollment_demographics** (affects 1 catalog KPI)
   - CLAUDE.md: "not in the documented mart inventory"
   - Dashboard: uses it successfully (kpi_library_dashboard.py:787)
   - **Reality:** Fully built, powers Demographics tab in DEMEAU dashboard v2
   - **Impact:** Age Demographics × Enrollment Intensity (row 130)
   - **Issue:** Title claims "age demographics" but no age_band column exists; only URM/first-gen/full-time rates

6. **mart_scorecard_program_outcomes** (affects ALL 7 Benchmarking KPIs)
   - CLAUDE.md: "does not exist: no schema, no dbt model, zero prior references"
   - Catalog rows 132–138 (entire Benchmarking area) target this mart
   - **Reality:** Fully built table sourcing from stg_scorecard__field_of_study
   - **Impact:** All 7 Benchmarking KPIs (Program Earnings vs. Debt ROI, Post-Graduation Earnings Benchmarking, Pell vs. Non-Pell Earnings Gap, Student Debt Burden vs. Peers, Loan Default Rate, BBRR, Earnings-to-Debt Ratio)

### 🟡 MEDIUM PRIORITY — Correct Status, Missing Columns

7. **mart_section_utilization**
   - Catalog correctly flags fill_rate and capacity_gap as "NOT YET COMPUTABLE"
   - Blocked on section_capacity column not yet in dim_course_section
   - **Impact:** Section Fill Rate (row 31), Course Demand vs. Capacity Gap (row 33), Classroom Utilization Rate (row 41)

8. **snap_enrollment_term**
   - FTE column is null stub (null::numeric)
   - Blocked on fact_student_term load_status integration not yet joined
   - **Impact:** FTE Trend (row 103), Credits-per-FTE Trend (row 51)

9. **snap_aid_term**
   - Returns zero rows until fact_aid_award has data
   - Model structure is complete; waiting on PowerFAIDS deposit
   - **Impact:** Multiple Financial Aid trend KPIs (rows 73–80, 85–86)

10. **mart_aid_summary**
    - fafsa_completion_rate is NOT YET COMPUTABLE (fafsa_completed flag not surfaced)
    - All other metrics functional
    - **Impact:** FAFSA Completion Rate (row 63)

---

## Recommendations

### Immediate Actions (Phase 2)

1. **Update catalog** to mark the 6 incorrectly-flagged-as-unbuilt marts as BUILT
2. **Document mart_enrollment_demographics** and **mart_scorecard_program_outcomes** in platform inventory
3. **Verify dashboard queries** against actual column names (Phase 4)
4. **Recalculate KPI availability**: ~23 catalog rows currently marked "NOT YET COMPUTABLE" should be reclassified as AVAILABLE

### CLAUDE.md Updates Required

Replace "Known gaps" section with accurate findings:
- ❌ "mart_retention_cohort_summary unbuilt" → ✅ Built and queryable
- ❌ "mart_enrollment_demographics not in documented inventory" → ✅ Built, document it
- ❌ "mart_scorecard_program_outcomes doesn't exist" → ✅ Built with full College Scorecard integration

### WDT Coordination Points

1. Confirm actual data availability in production Snowflake vs. DEMEAU synthetic data
2. Validate PowerFAIDS integration roadmap (affects snap_aid_term, unmet need metrics)
3. Confirm NSC deposit timeline (affects mart_ipeds_reporting CDR section, snap_cohort_milestone transfer-out tracking)

---

**Phase 1 Complete:** Ground truth inventory established.
**Next:** Phase 2 — Catalog accuracy check (systematic verification of 138 rows against this inventory)
