# Phase 5: Reconciliation & Correction Plan

**Date:** 2026-07-22
**Purpose:** Systematic application of all corrections identified in Phases 1-4

## Correction Summary

- **CSV catalog:** 29 rows requiring Calculation Logic updates
- **HTML DATA array:** 1 mart assignment fix (row 100)
- **HTML METRIC_INFO:** 19 entries requiring flag and/or calc text updates
- **Dashboard:** 1 tab requiring activation (Benchmarking)
- **CLAUDE.md:** Update "Known gaps" section with accurate findings

---

## Priority 1: Critical Corrections (Highest Impact)

### A. mart_retention_cohort_summary (6 catalog rows)

**Impact:** First-Year Retention Rate, Graduation Rates marked unavailable when they ARE available

**CSV rows to update:** 40, 93, 94, 95, 115, 130

**Current (incorrect):** "NOT YET COMPUTABLE — target mart mart_retention_cohort_summary unbuilt as of 2026-06-30."

**Corrected:**
- **Row 40 (Graduation Rate 4yr/6yr):** "yr4_grad_rate and yr6_grad_rate from mart_retention_cohort_summary. Columns: yr4_grad_rate (pct_graduated at years_since_entry=4), yr6_grad_rate (pct_graduated at years_since_entry=6). Pivots snap_cohort_milestone to IPEDS-standard grain."

- **Row 93 (First-Year Retention Rate):** "yr1_retention_rate from mart_retention_cohort_summary. Column: yr1_retention_rate (pct_still_enrolled at years_since_entry=1). Grain: one row per (institution_id, entry_cohort_year, program_key, cohort_type)."

- **Row 94 (Year-over-Year Retention Rate):** "yr1_retention_rate from mart_retention_cohort_summary trended across entry cohort years. Query across multiple entry_acad_year_int values to show year-over-year comparison."

- **Row 95 (Stop-Out / Dropout Rate):** "yr1_stop_out_rate, yr4_stop_out_rate, yr6_stop_out_rate from mart_retention_cohort_summary. Columns: yr1_stop_out_rate (pct_stopped_out at years_since_entry=1), yr4_stop_out_rate, yr6_stop_out_rate. Stopped-out students include transfer-outs until NSC integration."

- **Row 115 (Enrollment Cohort Analysis):** "COMPOSITE — draws yr1_retention_rate, yr4_grad_rate, yr6_grad_rate, cohort_size, yr1_stop_out_rate, first_gen_stop_out_rate, urm_stop_out_rate from mart_retention_cohort_summary at (institution_id, entry_cohort_year, program_key, cohort_type) grain. Needs manual definition."

- **Row 130 (Program-Level Retention Performance):** "AVG(yr1_retention_rate) and AVG(yr6_grad_rate) per program_name from mart_retention_cohort_summary, filtered to has_yr1_data=true, ranked descending (top 10 shown). Dashboard query: `SELECT program_name, AVG(yr1_retention_rate) AS yr1_rate, AVG(yr6_grad_rate) AS yr6_rate, AVG(cohort_size) AS avg_cohort_size FROM mart_retention_cohort_summary WHERE has_yr1_data = TRUE GROUP BY program_name ORDER BY yr1_rate DESC LIMIT 10`."

**HTML flags:** Change from `flag:"nyc"` to `flag:null` for rows 40, 93, 94, 95

---

### B. mart_enrollment_census_ntr (4 catalog rows)

**Impact:** Tuition Discount Rate, NTR metrics marked unavailable when they ARE available

**CSV rows to update:** 59, 60, 98, 99

**Current (incorrect):** "NOT YET COMPUTABLE — target mart mart_enrollment_census_ntr unbuilt as of 2026-06-30."

**Corrected:**
- **Row 59 (Tuition Discount Rate):** "discount_rate from mart_enrollment_census_ntr. Column: discount_rate = total_aid_disbursed / gross_tuition_billed per term. Grain: one row per (institution_id, term_key). ⚠️ DEMEAU synthetic data: account_value=0 → gross_tuition_billed=0, but production data will populate correctly."

- **Row 60 (Net Tuition Revenue per Student):** "ntr_per_student from mart_enrollment_census_ntr. Column: ntr_per_student = net_tuition_revenue / enrolled_headcount per term. Denominator from mart_enrollment_census aggregated to (institution, term) grain."

- **Row 98 (Projected vs. Actual NTR):** "Actual NTR from mart_enrollment_census_ntr.net_tuition_revenue per term. Projected/forecast target not in mart; comparison requires external budget source. Column: net_tuition_revenue (gross_tuition_billed - total_aid_disbursed)."

- **Row 99 (Revenue per Enrolled Student):** "Same as row 60. Column: ntr_per_student from mart_enrollment_census_ntr."

**HTML flags:** Change from `flag:"nyc"` to `flag:null` for rows 59, 60, 98, 99

---

### C. mart_student_at_risk (2 catalog rows)

**Impact:** At-Risk Count and Early Warning dashboard marked unavailable when they ARE available

**CSV rows to update:** 96, 113

**Current (incorrect):** "NOT YET COMPUTABLE — target mart mart_student_at_risk unbuilt as of 2026-06-30."

**Corrected:**
- **Row 96 (At-Risk Student Count):** "Count of students with is_at_risk=true from mart_student_at_risk. Columns: is_at_risk, risk_tier (high/medium/none), risk_factor_count. Composite risk based on 4 dimensions: GPA (on_track_gpa_flag=false), SAP (is_sap_compliant=false), holds (has_registration_hold=true), financial clearing (financially_cleared=false). ⚠️ FERPA HIGH: student_key exposed at row level — restrict to Advisor/Registrar roles only."

- **Row 113 (Retention Early Warning):** "COMPOSITE — draws is_at_risk, risk_tier, risk_factor_count, on_track_gpa_flag, is_sap_compliant, has_registration_hold, financially_cleared from mart_student_at_risk at student row grain. Grain: one row per currently enrolled student per program. ⚠️ FERPA HIGH: student-level data. Needs manual definition."

**HTML flags:** Change from `flag:"nyc"` to `flag:null` for rows 96, 113

---

### D. mart_aid_leveraging (3 catalog rows)

**Impact:** Aid leveraging marked unavailable when core metrics ARE available

**CSV rows to update:** 63, 82, 84

**Current (incorrect):** "NOT YET COMPUTABLE — mart_aid_leveraging is a stub returning zero rows until PowerFAIDS data is available."

**Corrected:**
- **Row 63 (Leveraging Efficiency):** "merit_aid_total / total_inst_aid from mart_aid_leveraging per (term_key, program_key). Core leveraging metrics (merit vs. need split, aid band yield analysis) are functional. Columns: inst_aid_offered, merit_aid_total, need_based_aid_total, yield by aid_band. ⚠️ Unmet need and COA-based discount remain null until PowerFAIDS provides COA/EFC fields, but this does not block leveraging efficiency calculation."

- **Row 82 (Aid Budget Monitor):** "COMPOSITE — draws inst_aid_offered, merit_aid_total, need_based_aid_total, aid_band_yield_rate from mart_aid_leveraging at (term_key, program_key) grain. Discount rate requires mart_enrollment_census_ntr (available). ⚠️ Unmet need stubs do not block core budget monitoring. Needs manual definition."

- **Row 84 (Aid Leveraging Model):** "COMPOSITE — aid band vs. yield, merit vs. need split from mart_aid_leveraging. Aid bands: band_zero ($0), band_1_5k ($1–$5k), band_5_10k ($5,001–$10k), band_10_15k ($10,001–$15k), band_15_20k ($15,001–$20k), band_20k_plus ($20,001+). Needs manual definition."

**HTML flags:** Change from `flag:"nyc"` to `flag:null` for rows 63, 82, 84

---

### E. mart_scorecard_program_outcomes (7 catalog rows — Benchmarking area)

**Impact:** Entire Benchmarking area (rows 132–138) marked "PROPOSED" when mart IS built

**CSV rows to update:** 132, 133, 134, 135, 136, 137, 138

**Current (incorrect):** All start with "PROPOSED —" prefix

**Corrected:** Remove "PROPOSED —" prefix from all 7 rows:

- **Row 132 (Program Earnings vs. Debt ROI):** "COMPOSITE dashboard: earn_median_4yr / debt_at_completion by program and credential level from mart_scorecard_program_outcomes. Columns: earn_median_4yr (median earnings 4 years post-completion), debt_at_completion (median debt at graduation), earn_vs_national_pct (earnings vs. national median). Grain: one row per institution × cip_code × credential_level_code × data_year. Sources from stg_scorecard__field_of_study. Needs manual definition."

- **Row 133 (Post-Graduation Earnings Benchmarking):** "COMPOSITE dashboard: earn_median_4yr vs. earn_median_4yr_national, earn_p25_4yr_national, earn_p75_4yr_national from mart_scorecard_program_outcomes. Benchmarks own-institution program earnings against College Scorecard national medians by CIP code and credential level. Needs manual definition."

- **Row 134 (Pell vs. Non-Pell Earnings Gap):** "earn_median_pell_4yr vs. earn_median_nopell_4yr from mart_scorecard_program_outcomes by program. Earnings equity measure: gap = earn_median_nopell_4yr - earn_median_pell_4yr. No join to mart_aid_summary needed; Pell/non-Pell earnings already segmented in this mart. Column: earn_pell_vs_nopell_ratio (earn_median_pell_4yr / earn_median_nopell_4yr)."

- **Row 135 (Student Debt Burden vs. Peers):** "COMPOSITE dashboard: debt_at_completion by program from mart_scorecard_program_outcomes, benchmarked against College Scorecard national and peer-group medians for matching CIP code and credential level. Columns: debt_at_completion, debt_vs_national_pct. Needs manual definition."

- **Row 136 (Loan Default Rate — College Scorecard):** "cdr_3yr from mart_scorecard_program_outcomes. Published 3-year cohort default rate from U.S. Dept. of Education via College Scorecard, ingested as-is (not computed). Column: cdr_3yr (borrowers who defaulted within 3 years / all borrowers who entered repayment). ⚠️ This is program-level CDR from Scorecard; row 67 CDR is institution-level from NSC (stub). Both are valid but serve different purposes."

- **Row 137 (Borrower-Based Repayment Rate — BBRR):** "repayment_rate_3yr from mart_scorecard_program_outcomes. Share of a program's borrower cohort with declining or current loan balance within the federal measurement window, per Financial Value Transparency / Gainful Employment rules. Published via College Scorecard and ingested as-is. Column: repayment_rate_3yr."

- **Row 138 (Earnings-to-Debt Ratio by Program):** "earn_median_4yr / debt_at_completion from mart_scorecard_program_outcomes by program (inverse framing of federal debt-to-earnings ratio used in gainful employment determinations). Higher ratio = stronger program ROI. Column: earn_to_debt_ratio (computed as earn_median_4yr / NULLIF(debt_at_completion, 0))."

**HTML flags:** Change from `flag:"nyc"` to `flag:null` for rows 132, 136, 137, 138
**HTML flags:** Rows 133, 135 already have `flag:null` (no change needed)
**HTML flags:** Row 134 has `flag:"nyc"` → change to `flag:null`

---

## Priority 2: Medium-Impact Corrections

### F. Other Available KPIs (3 rows)

**Row 116 (IPEDS Reporting Prep):**
- **Current:** "NOT YET COMPUTABLE — target mart mart_ipeds_fall_enrollment unbuilt as of 2026-06-30."
- **Corrected:** "Fall enrollment snapshot from mart_ipeds_fall_enrollment. Grain: one row per institution per survey_year. Columns: headcount by level (UG/Grad), race/ethnicity composition, gender breakdown. ⚠️ Degree-seeking tracked as total UG headcount until further refinement."
- **HTML flag:** Change from `flag:"nyc"` to `flag:null`

**Row 131 (Age Demographics × Enrollment Intensity):**
- **Current:** "NOT YET COMPUTABLE — title implies age breakdown; mart does not carry age_band."
- **Corrected:** "fulltime_rate = fulltime_count / total_headcount by academic_year from mart_enrollment_demographics covers 'enrollment intensity.' Columns: total_headcount, urm_count, first_gen_count, fulltime_count by academic_year. ⚠️ Age demographics NOT YET COMPUTABLE until age_band dimension added. Suggest retitle to 'Demographic Enrollment Intensity' (URM/first-gen/full-time rates by year) OR add age_band to mart."
- **HTML flag:** Keep `flag:"nyc"` (age dimension is legitimately unavailable)
- **HTML calc:** Update to clarify that enrollment intensity IS available but age demographics are not

**Row 137 (BBRR):** Already covered in section E above

---

### G. Row 100 Mart Assignment Error (HTML only)

**Impact:** IPEDS Peer Comparison assigned to wrong mart

**CSV row 100:**
- **Current:** `Mart / View` = mart_ipeds_reporting
- **Corrected:** `Mart / View` = mart_ipeds_peer_comparison
- **Calculation Logic:** Change from "NOT YET COMPUTABLE — mart_ipeds_reporting returns zero rows (stub); peer comparison requires stg_ipeds__peer_benchmarks not yet provisioned. Note: mart_ipeds_peer_comparison (a separate built mart) has IPEDS enrollment and graduation rate benchmarks vs. the school's peer group but the catalog maps this KPI to mart_ipeds_reporting." → "Side-by-side enrollment and graduation rate benchmarks from mart_ipeds_peer_comparison. Columns: headcount_total, cnt_urm_proxy, headcount_men, headcount_women (enrollment); yr4_grad_rate, yr6_grad_rate (completion) per institution × survey_year × lstudy_code. School-scoped via var('school_code'). Sources from stg_ipeds__fall_enrollment and stg_ipeds__graduation_rates."

**HTML DATA (line ~243):**
- **Current:** `mart:"mart_scorecard_program_outcomes"`
- **Corrected:** `mart:"mart_ipeds_peer_comparison"`

**HTML METRIC_INFO (line ~387):**
- **Current:** `ref:"mart_scorecard_program_outcomes.ipeds_peer_comparison"`
- **Corrected:** `ref:"mart_ipeds_peer_comparison.ipeds_peer_comparison"`
- **calc:** Use CSV corrected text above
- **flag:** Change from `"nyc"` to `null`

---

## Priority 3: Data-Awaiting Clarifications

### H. snap_aid_term (3 rows) — Awaiting PowerFAIDS Data

**CSV rows:** 74, 75, 86

**Current language:** "NOT YET COMPUTABLE — discount_rate is null stub" (confusing — implies model-level stub)

**Clarified language:** "Returns zero rows until fact_aid_award has data (PowerFAIDS integration pending). Model structure is complete. Once PF loads..."

- **Row 74 (Tuition Discount Rate Trend 5-Year):** "snap_aid_term model is fully built but returns zero rows until fact_aid_award has data (PowerFAIDS integration pending). Once PF loads, discount_rate will compute as offered_amount_total / gross_tuition_billed per term × aid_type. Time-series view of Tuition Discount Rate by term."

- **Row 75 (Net Tuition Revenue Trend):** "snap_aid_term returns zero rows until fact_aid_award has data. NTR logic exists in mart_enrollment_census_ntr; time-series trend requires snap_aid_term population. Once PF loads, NTR trend will derive from term-by-term aid disbursement totals."

- **Row 86 (Discount Rate & NTR Trend):** "COMPOSITE dashboard drawing discount_rate and NTR trend from snap_aid_term (zero rows until PowerFAIDS loads fact_aid_award). Model is built; waiting on source data. Needs manual definition."

**HTML flags:** Keep `flag:"nyc"` (legitimately unavailable until data loads) but update calc text for clarity

---

## Summary: Files to Update

### 1. higher_ed_kpi_catalog_enriched.csv
- **29 rows** requiring `Calculation Logic` column updates
- **1 row** (100) requiring `Mart / View` column update

### 2. kpi_library.html
- **1 entry** in DATA array (line ~243, row 100 mart assignment)
- **19 entries** in METRIC_INFO map (calc text and/or flag updates)

### 3. kpi_library_dashboard.py
- **1 section** (Benchmarking tab, lines ~830–840) — remove stub message, add queries

### 4. CLAUDE.md
- **"Known gaps" section** — replace with accurate findings from Phase 1

---

## Execution Sequence

**Step 1:** Update CSV catalog (29 + 1 = 30 rows)
**Step 2:** Update HTML DATA array (1 entry)
**Step 3:** Update HTML METRIC_INFO (19 entries)
**Step 4:** Update dashboard Benchmarking tab
**Step 5:** Update CLAUDE.md
**Step 6:** Verify synchronization across all 3 artifacts

---

**Phase 5 Correction Plan Complete.** Ready to begin applying changes.
