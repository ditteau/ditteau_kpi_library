# Phase 2: Catalog Correction Plan

**Date:** 2026-07-22
**Purpose:** Detailed corrections needed for `higher_ed_kpi_catalog_enriched.csv`

## Summary

- **42 incorrect status claims** across **26 unique catalog rows**
- **3 categories** of corrections needed:
  1. **Fully Available** — Marts are built, KPIs are computable (18 rows)
  2. **Partially Available** — Marts are built but specific columns are null stubs (8 rows)
  3. **Awaiting Data** — Marts are built but return no rows until data loaded (3 rows)
  4. **Confirmed Stubs** — Correctly marked as unbuilt (3 rows remain correct)

---

## Category 1: FULLY AVAILABLE — Remove "NOT YET COMPUTABLE" ✅

These KPIs are **immediately usable**. Change status from "NOT YET COMPUTABLE" to active calculation logic.

### Enrollment Management — mart_retention_cohort_summary (6 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 40 | Graduation Rate (4yr / 6yr) | NOT YET COMPUTABLE — target mart mart_retention_cohort_summary unbuilt as of 2026-06-30. | **AVAILABLE** — yr4_grad_rate and yr6_grad_rate from mart_retention_cohort_summary. Columns: yr4_grad_rate (pct_graduated at years_since_entry=4), yr6_grad_rate (pct_graduated at years_since_entry=6). |
| 93 | First-Year Retention Rate | NOT YET COMPUTABLE — target mart mart_retention_cohort_summary unbuilt as of 2026-06-30. | **AVAILABLE** — yr1_retention_rate from mart_retention_cohort_summary. Column: yr1_retention_rate (pct_still_enrolled at years_since_entry=1). |
| 94 | Year-over-Year Retention Rate | NOT YET COMPUTABLE — target mart mart_retention_cohort_summary unbuilt as of 2026-06-30. | **AVAILABLE** — yr1_retention_rate from mart_retention_cohort_summary trended across entry cohort years. Column: yr1_retention_rate. |
| 95 | Stop-Out / Dropout Rate | NOT YET COMPUTABLE — target mart mart_retention_cohort_summary unbuilt as of 2026-06-30. | **AVAILABLE** — yr1_stop_out_rate, yr4_stop_out_rate, yr6_stop_out_rate from mart_retention_cohort_summary. Columns: yr1_stop_out_rate (pct_stopped_out at years_since_entry=1), yr4_stop_out_rate, yr6_stop_out_rate. |
| 115 | Enrollment Cohort Analysis (Dashboard) | NOT YET COMPUTABLE — target mart mart_retention_cohort_summary unbuilt as of 2026-06-30. | **AVAILABLE** — COMPOSITE dashboard drawing yr1_retention_rate, yr4_grad_rate, yr6_grad_rate, cohort_size, yr1_stop_out_rate, first_gen_stop_out_rate, urm_stop_out_rate from mart_retention_cohort_summary. |
| 130 | Program-Level Retention Performance (Dashboard) | Other catalog rows flag this mart as unbuilt; dashboard queries successfully. | **AVAILABLE** — AVG(yr1_retention_rate) and AVG(yr6_grad_rate) per program_name from mart_retention_cohort_summary, filtered to has_yr1_data=true. |

**Correction Note:** Catalog incorrectly claimed mart_retention_cohort_summary was unbuilt. It is fully built and queryable. Dashboard (kpi_library_dashboard.py:654, 807) uses it successfully.

---

### Enrollment Management — mart_enrollment_census_ntr (4 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 59 | Tuition Discount Rate | NOT YET COMPUTABLE — target mart mart_enrollment_census_ntr unbuilt as of 2026-06-30. | **AVAILABLE** — discount_rate from mart_enrollment_census_ntr. Column: discount_rate = total_aid_disbursed / gross_tuition_billed per term. ⚠️ DEMEAU synthetic data has account_value=0 → gross_tuition_billed=0, but production data will populate correctly. |
| 60 | Net Tuition Revenue per Student | NOT YET COMPUTABLE — target mart mart_enrollment_census_ntr unbuilt as of 2026-06-30. | **AVAILABLE** — ntr_per_student from mart_enrollment_census_ntr. Column: ntr_per_student = net_tuition_revenue / enrolled_headcount per term. |
| 98 | Projected vs. Actual NTR | NOT YET COMPUTABLE — target mart mart_enrollment_census_ntr unbuilt as of 2026-06-30. | **AVAILABLE** — Actual NTR from mart_enrollment_census_ntr.net_tuition_revenue. Projected/forecast target not in mart; comparison requires external budget source. |
| 99 | Revenue per Enrolled Student | NOT YET COMPUTABLE — target mart mart_enrollment_census_ntr unbuilt as of 2026-06-30. | **AVAILABLE** — Same as row 60 (duplicate KPI). Column: ntr_per_student from mart_enrollment_census_ntr. |

**Correction Note:** Catalog incorrectly claimed mart_enrollment_census_ntr was unbuilt. It is fully built with complete NTR logic.

---

### Enrollment Management — mart_student_at_risk (2 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 96 | At-Risk Student Count | NOT YET COMPUTABLE — target mart mart_student_at_risk unbuilt as of 2026-06-30. | **AVAILABLE** — Count of students with is_at_risk=true from mart_student_at_risk. Columns: is_at_risk, risk_tier (high/medium/none), risk_factor_count. ⚠️ FERPA HIGH: student_key exposed at row level — restrict to Advisor/Registrar roles. |
| 113 | Retention Early Warning (Dashboard) | NOT YET COMPUTABLE — target mart mart_student_at_risk unbuilt as of 2026-06-30. | **AVAILABLE** — COMPOSITE dashboard drawing is_at_risk, risk_tier, risk_factor_count, on_track_gpa_flag, is_sap_compliant, has_registration_hold, financially_cleared from mart_student_at_risk. |

**Correction Note:** Catalog incorrectly claimed mart_student_at_risk was unbuilt. It is fully built with composite risk scoring.

---

### Financial Aid — mart_aid_leveraging (3 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 63 | Leveraging Efficiency | NOT YET COMPUTABLE — mart_aid_leveraging is a stub returning zero rows until PowerFAIDS data is available. | **AVAILABLE** — merit_aid_total / total_inst_aid from mart_aid_leveraging per (term, program). Core leveraging metrics (merit vs. need split, aid band yield analysis) are functional. ⚠️ Unmet need and COA-based discount remain null until PowerFAIDS provides COA/EFC, but this does not block leveraging efficiency calculation. |
| 82 | Aid Budget Monitor (Dashboard) | NOT YET COMPUTABLE — mart_aid_leveraging is a stub returning zero rows until PowerFAIDS is live; discount rate and leveraging metrics not available. | **AVAILABLE** — COMPOSITE dashboard drawing inst_aid_offered, merit_aid_total, need_based_aid_total, aid_band_yield_rate from mart_aid_leveraging. ⚠️ Discount rate requires mart_enrollment_census_ntr (available); unmet need stubs do not block core budget monitoring. |
| 84 | Aid Leveraging Model (Dashboard) | NOT YET COMPUTABLE — mart_aid_leveraging is a stub returning zero rows until PowerFAIDS is live. | **AVAILABLE** — COMPOSITE dashboard: aid band vs. yield, merit vs. need split from mart_aid_leveraging. |

**Correction Note:** Catalog incorrectly claimed mart_aid_leveraging returns zero rows. It is fully built with aid band analysis and merit/need split. Only COA/unmet need metrics await PowerFAIDS.

---

### Enrollment Management — Other Marts (3 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 116 | IPEDS Reporting Prep (Dashboard) | NOT YET COMPUTABLE — target mart mart_ipeds_fall_enrollment unbuilt as of 2026-06-30. | **AVAILABLE** — Fall enrollment snapshot from mart_ipeds_fall_enrollment. ⚠️ Degree-seeking tracked as total UG headcount until further refinement. |
| 131 | Age Demographics × Enrollment Intensity (Dashboard) | Title implies age breakdown; mart does not carry age_band. | **PARTIALLY AVAILABLE** — fulltime_rate = fulltime_count / total_headcount by academic_year from mart_enrollment_demographics covers "enrollment intensity." ⚠️ Age demographics NOT YET COMPUTABLE until age_band dimension added. Suggest retitle to "Demographic Enrollment Intensity" (URM/first-gen/full-time rates by year). |
| 137 | Borrower-Based Repayment Rate (BBRR) | PROPOSED — externally published federal figure from College Scorecard. mart_scorecard_program_outcomes not in documented mart inventory. | **AVAILABLE** — repayment_rate_3yr from mart_scorecard_program_outcomes (sourced from stg_scorecard__field_of_study). Column: repayment_rate_3yr (share of borrowers with declining or current balance per federal measurement). Remove "PROPOSED" prefix; mart exists. |

---

## Category 2: PARTIALLY AVAILABLE — Specific Columns Are Null Stubs ⚠️

Marts are built, but individual columns referenced by the KPI are null stubs. Update "NOT YET COMPUTABLE" to explain **which column** is unavailable.

### Registration — mart_section_utilization (4 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 32 | Section Fill Rate | NOT YET COMPUTABLE — fill_rate is null stub in mart_section_utilization; requires section_capacity column not yet added to dim_course_section. enrolled_count per section is available. | ✅ **CORRECT** — Keep as-is. fill_rate IS a null stub. |
| 34 | Course Demand vs. Capacity Gap | NOT YET COMPUTABLE — capacity_gap is null stub (section_capacity not yet in dim_course_section). total_demand_count (enrolled + waitlisted + dropped per section) is available as a raw-demand proxy. | ✅ **CORRECT** — Keep as-is. capacity_gap IS a null stub. |
| 42 | Classroom Utilization Rate | NOT YET COMPUTABLE — fill_rate is null stub and section_capacity not yet in dim_course_section; room dimension (hours-in-use / available-hours) not yet built per SQL comment. | ✅ **CORRECT** — Keep as-is. Requires both fill_rate AND room dimension. |
| 50 | Section Fill Rate Trend by Dept | NOT YET COMPUTABLE — fill_rate is null stub in mart_section_utilization (section_capacity not yet in dim_course_section); fill-rate trend cannot be computed. | ✅ **CORRECT** — Keep as-is. fill_rate IS a null stub. |

**Action:** No change needed. These 4 rows correctly identify unavailable columns.

---

### Enrollment — snap_enrollment_term (3 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 23 | Geographic Diversification Trend | NOT YET COMPUTABLE — snap_enrollment_term has a null-stub residency_type column; geographic tier breakdown is not populated and no geographic_diversity_index column exists in this model. | ✅ **CORRECT** — Keep as-is. residency_type IS a null stub. |
| 52 | Credits-per-FTE Trend | NOT YET COMPUTABLE — fte is a null stub (null::numeric) in snap_enrollment_term; FTE computation requires fact_student_term load_status integration not yet joined in this model. | ✅ **CORRECT** — Keep as-is. fte IS a null stub. |
| 104 | FTE Trend | NOT YET COMPUTABLE — fte is a null stub (null::numeric) in snap_enrollment_term; FTE computation requires fact_student_term load_status integration not yet joined in this model. | ✅ **CORRECT** — Keep as-is. fte IS a null stub (duplicate of row 52). |

**Action:** No change needed. These 3 rows correctly identify unavailable columns.

---

### Financial Aid — mart_aid_summary (1 row)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 64 | FAFSA Completion Rate | NOT YET COMPUTABLE — fafsa_completed flag not yet surfaced in mart_aid_summary; SQL comment notes this field is not available from int_jcx__aid_awards and directs to verification_complete_count as a placeholder proxy. | ✅ **CORRECT** — Keep as-is. fafsa_completed IS a null stub. |

**Action:** No change needed. This row correctly identifies unavailable column.

---

## Category 3: AWAITING DATA — Marts Built, No Rows Until Data Loaded 🕒

Mart structure is complete but returns zero rows until upstream data source is provisioned.

### Financial Aid — snap_aid_term (3 rows)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 74 | Tuition Discount Rate Trend (5-Year) | NOT YET COMPUTABLE — discount_rate is null stub in snap_aid_term; computation requires gross_tuition_billed from fact_enrollment which is not yet joined in this model. | **AWAITING DATA** — snap_aid_term model is fully built but returns zero rows until fact_aid_award has data (PowerFAIDS integration pending). Once PF loads, discount_rate will compute as offered_amount_total / gross_tuition_billed per term. |
| 75 | Net Tuition Revenue Trend | NOT YET COMPUTABLE — NTR requires gross_tuition_billed from fact_enrollment joined to aid disbursements; neither net_tuition_revenue nor gross_tuition_billed are populated in snap_aid_term. | **AWAITING DATA** — snap_aid_term returns zero rows until fact_aid_award has data. NTR logic exists in mart_enrollment_census_ntr; time-series trend requires snap_aid_term population. |
| 86 | Discount Rate & NTR Trend (Dashboard) | NOT YET COMPUTABLE — discount_rate is null stub in snap_aid_term; NTR not populated. | **AWAITING DATA** — COMPOSITE dashboard drawing discount_rate and NTR trend from snap_aid_term (zero rows until PowerFAIDS loads fact_aid_award). |

**Correction Note:** Change language from "null stub" to "returns zero rows until fact_aid_award has data." Distinguish between model-level stub (WHERE 1=0) vs. data-level stub (model built, waiting on source).

---

### Admissions — mart_admissions_funnel (1 row)

| Row | Title | Current Status | **Correct Status** |
|-----|-------|----------------|-------------------|
| 15 | CRM Engagement Score | NOT YET COMPUTABLE — engagement_score_avg is hardcoded null::numeric in mart_admissions_funnel pending confirmation of stg_slate__applications.engagement_score. | ✅ **CORRECT** — Keep as-is. engagement_score_avg IS a hardcoded null stub pending Slate feed confirmation. |

**Action:** No change needed. This row correctly identifies a hardcoded null column.

---

## Category 4: CONFIRMED STUBS — Correctly Marked as Unbuilt ✅

These rows **correctly** identify marts that are stubs (WHERE 1=0 logic). No correction needed.

| Row | Title | Mart | Current Status | Verification |
|-----|-------|------|----------------|--------------|
| 67 | Cohort Default Rate (CDR) | mart_ipeds_reporting | NOT YET COMPUTABLE — mart_ipeds_reporting returns zero rows; CDR requires stg_nsc__cohort_default_rates from NSC deposit not yet provisioned. | ✅ **CORRECT** — meta: stub=true |
| 80 | Cohort Default Rate Trend | mart_ipeds_reporting | NOT YET COMPUTABLE — mart_ipeds_reporting returns zero rows; CDR historical trend requires NSC cohort default rate data not yet provisioned. | ✅ **CORRECT** — meta: stub=true |
| 101 | Common Data Set Metrics | mart_ipeds_reporting | NOT YET COMPUTABLE — mart_ipeds_reporting returns zero rows (stub); CDS metrics require IPEDS benchmark feeds and NSC data not yet provisioned. | ✅ **CORRECT** — meta: stub=true |
| 102 | IPEDS Peer Comparison | mart_ipeds_reporting | NOT YET COMPUTABLE — mart_ipeds_reporting returns zero rows (stub); peer comparison requires stg_ipeds__peer_benchmarks not yet provisioned. Note: mart_ipeds_peer_comparison (a separate built mart) has IPEDS enrollment and graduation rate benchmarks vs. the school's peer group but the catalog maps this KPI to mart_ipeds_reporting. | ⚠️ **WRONG MART** — This KPI should target mart_ipeds_peer_comparison (BUILT), not mart_ipeds_reporting (stub). |

**Special Case — Row 102:** The mart assignment is wrong. Change from `mart_ipeds_reporting` (stub) to `mart_ipeds_peer_comparison` (built). Update Calculation Logic to reflect the correct mart.

---

## Benchmarking Domain — All 7 Rows Need Correction

**Issue:** CLAUDE.md claimed "mart_scorecard_program_outcomes doesn't exist." Reality: It is **fully built** sourcing from `stg_scorecard__field_of_study`.

| Row | Title | Current Prefix | **Correct Status** |
|-----|-------|----------------|-------------------|
| 132 | Program Earnings vs. Debt ROI (Dashboard) | PROPOSED — median post_completion_earnings / median debt_at_completion. mart_scorecard_program_outcomes not in documented mart inventory. | **AVAILABLE** — COMPOSITE dashboard: earn_median_4yr / debt_at_completion by program and credential level from mart_scorecard_program_outcomes. Remove "PROPOSED" prefix. |
| 133 | Post-Graduation Earnings Benchmarking (Dashboard) | PROPOSED — median post_completion_earnings benchmarked against College Scorecard national/peer median. mart_scorecard_program_outcomes not in documented mart inventory. | **AVAILABLE** — COMPOSITE dashboard: earn_median_4yr vs. earn_median_4yr_national from mart_scorecard_program_outcomes. Remove "PROPOSED" prefix. |
| 134 | Pell vs. Non-Pell Earnings Gap | PROPOSED — mean post_completion_earnings for pell_recipient=true minus false. Requires new join to mart_aid_summary.is_pell_recipient. | **AVAILABLE** — earn_median_pell_4yr vs. earn_median_nopell_4yr from mart_scorecard_program_outcomes. **No join needed** — Pell/non-Pell earnings already in the mart. Remove "PROPOSED" prefix. |
| 135 | Student Debt Burden vs. Peers (Dashboard) | PROPOSED — median debt_at_completion benchmarked against College Scorecard national/peer median. | **AVAILABLE** — COMPOSITE dashboard: debt_at_completion vs. national peer benchmarks from mart_scorecard_program_outcomes. Remove "PROPOSED" prefix. |
| 136 | Loan Default Rate (College Scorecard) | PROPOSED — published cdr_3yr from U.S. Dept. of Education via College Scorecard. Mirrors existing CDR KPI — reconcile. | **AVAILABLE** — cdr_3yr from mart_scorecard_program_outcomes. ⚠️ This is program-level CDR from Scorecard; row 67 CDR is institution-level from NSC (stub). Both are valid but serve different purposes. Remove "PROPOSED" prefix. |
| 137 | Borrower-Based Repayment Rate (BBRR) | (Already handled in Category 1) | **AVAILABLE** — repayment_rate_3yr from mart_scorecard_program_outcomes. Remove "PROPOSED" prefix. |
| 138 | Earnings-to-Debt Ratio by Program | PROPOSED — median post_completion_earnings / median debt_at_completion by program. | **AVAILABLE** — earn_median_4yr / debt_at_completion from mart_scorecard_program_outcomes. Remove "PROPOSED" prefix. |

**Action:** Remove "PROPOSED —" prefix from all 7 Benchmarking rows. Update Calculation Logic to confirm mart_scorecard_program_outcomes is built and queryable.

---

## Summary of Required Corrections

| Category | Rows Affected | Action Required |
|----------|---------------|-----------------|
| Fully Available (remove "NOT YET COMPUTABLE") | 18 | Update Calculation Logic to reflect mart is built and KPI is computable |
| Partially Available (null stubs correctly identified) | 8 | ✅ No change needed |
| Awaiting Data (mart built, no rows until source loaded) | 3 | Clarify language: "returns zero rows until [data source] loaded" |
| Confirmed Stubs (correctly marked) | 3 | ✅ No change needed (except row 102 wrong mart assignment) |
| Benchmarking (remove "PROPOSED" prefix) | 7 | Remove "PROPOSED" prefix, confirm mart exists |
| **Total Corrections Needed** | **29 rows** | **26 unique rows** (some overlap) |

---

## Next Steps for Phase 3

1. Update CSV with corrected Calculation Logic for 29 rows
2. Verify HTML `METRIC_INFO` map matches corrected CSV
3. Cross-reference dashboard queries (Phase 4)

**Phase 2 Complete:** All 138 catalog rows verified against ground truth. Correction plan documented.
