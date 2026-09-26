#!/usr/bin/env python3
"""
Fix Calculation Logic misalignment in KPI Library CSV.

Based on Richard's analysis in KPI Library Analytic Type Review v0.1:
- Section E.1: Rows 132-138 are shifted by one (each has logic of the next row)
- Section E.2: Several rows have duplicated logic from adjacent entries

Run from ditteau_kpi_library directory:
    python fix_calculation_logic.py
"""

import csv
from pathlib import Path

INPUT_FILE = Path("higher_ed_kpi_catalog_enriched.csv")
OUTPUT_FILE = Path("higher_ed_kpi_catalog_enriched.csv")
BACKUP_FILE = Path("higher_ed_kpi_catalog_enriched.csv.bak")

# Correct Calculation Logic for each affected entry
# Key = Title, Value = (correct_calculation_logic, correct_known_caveats, correct_mart_view or None)

CORRECTIONS = {
    # Section E.1: Shifted by one row (rows 132-139)
    "Retention Risk Early Warning Indicators": (
        "COMPOSITE dashboard: draws is_at_risk, risk_tier (high/medium/none), risk_factor_count, is_gpa_at_risk, is_sap_at_risk, is_hold_at_risk, is_financial_at_risk from mart_student_at_risk. Risk tier based on count of 4 dimensions: GPA (on_track_gpa_flag=false), SAP (is_sap_compliant=false), holds (has_registration_hold=true), financial (student_billing_cleared=false). Grain: one row per currently enrolled student per program. Needs manual definition.",
        "FERPA HIGH: student_key exposed at row level. Rule-based composite, not model-scored.",
        "mart_student_at_risk"
    ),
    "Program Earnings vs. Debt ROI": (
        "COMPOSITE dashboard: earn_median_4yr / debt_at_completion by program and credential level from mart_scorecard_program_outcomes. Columns: earn_median_4yr (median earnings 4 years post-completion), debt_at_completion (median debt at graduation), earn_vs_national_pct (earnings vs. national median). Grain: one row per institution × cip_code × credential_level_code × data_year. Sources from stg_scorecard__field_of_study. Needs manual definition.",
        "is_suppressed = true when ED withheld values; ROI calculation skips suppressed rows.",
        None
    ),
    "Post-Graduation Earnings Benchmarking": (
        "COMPOSITE dashboard: earn_median_4yr vs. earn_median_4yr_national, earn_p25_4yr_national, earn_p75_4yr_national from mart_scorecard_program_outcomes. Benchmarks own-institution program earnings against College Scorecard national medians by CIP code and credential level. Needs manual definition.",
        "Peer ranks are NULL when <3 non-suppressed peers exist — avoids misleading 'rank 1 of 1.'",
        None
    ),
    "Pell vs. Non-Pell Earnings Gap": (
        "earn_median_pell_4yr vs. earn_median_nopell_4yr from mart_scorecard_program_outcomes by program. Earnings equity measure: gap = earn_median_nopell_4yr - earn_median_pell_4yr. No join to mart_aid_summary needed; Pell/non-Pell earnings already segmented in this mart. Column: earn_pell_vs_nopell_ratio (earn_median_pell_4yr / earn_median_nopell_4yr).",
        "is_suppressed flag applies; equity gap calculation skips suppressed program rows.",
        None
    ),
    "Student Debt Burden vs. Peers": (
        "COMPOSITE dashboard: debt_at_completion by program from mart_scorecard_program_outcomes, benchmarked against College Scorecard national and peer-group medians for matching CIP code and credential level. Columns: debt_at_completion, debt_vs_national_pct. Needs manual definition.",
        "Peer ranks NULL when <3 non-suppressed peers; is_suppressed flag applies.",
        None
    ),
    "Loan Default Rate (College Scorecard)": (
        "cdr_3yr from mart_scorecard_program_outcomes. Published 3-year cohort default rate from U.S. Dept. of Education via College Scorecard, ingested as-is (not computed). Column: cdr_3yr (borrowers who defaulted within 3 years / all borrowers who entered repayment). This is program-level CDR from Scorecard; row 67 CDR is institution-level from NSC (stub). Both are valid but serve different purposes.",
        "Program-level CDR from Scorecard; differs from institution-level CDR in row 67 (NSC-based, currently stub).",
        None
    ),
    "Borrower-Based Repayment Rate (BBRR)": (
        "repayment_rate_3yr from mart_scorecard_program_outcomes. Share of a program's borrower cohort with declining or current loan balance within the federal measurement window, per Financial Value Transparency / Gainful Employment rules. Published via College Scorecard and ingested as-is. Column: repayment_rate_3yr.",
        "Externally published federal figure, not Ditteau-computed.",
        None
    ),
    # Row 139 (Earnings-to-Debt Ratio) already has correct logic - no change needed

    # Section E.2: Duplicated from adjacent entry
    "On-Track Graduation %": (
        "pct_on_track = count of students with on_track_gpa_flag=true AND cumulative_earned_hours >= expected_credits_at_level divided by total enrolled students per program. on_track_gpa_flag based on cumulative_gpa >= 2.0 (UG) or >= 3.0 (Grad). expected_credits_at_level maps class level to milestone: FR=0, SO=30, JR=60, SR=90. Column: pct_on_track.",
        "Credit-pace rule uses default credits_to_degree (120 UG, 36 GR, 18 cert) when dim_program.required_hours not populated; GPA threshold is configurable via var('min_gpa_undergrad', 2.0).",
        None
    ),
    "Aid Budget vs. Actuals": (
        "Sum of total_inst_disbursed (institutional aid disbursed) vs. budget target per (program, term) from mart_aid_summary. Budget target not in mart — requires external budget input for vs-goal comparison. Columns: total_inst_disbursed, total_inst_offered.",
        "Budget denominator not in mart; full KPI requires external budget data source.",
        None
    ),
    "FAFSA Completion Rate": (
        "Count of distinct students with has_fafsa=true (at least one aid row with fafsa_filed_flag=true via boolor_agg) divided by enrolled_headcount per (program, term). Column: fafsa_completion_rate.",
        "has_fafsa derives from boolor_agg across aid rows — any single FAFSA-flagged row triggers the student-level flag; denominator is all enrolled students, not just aid applicants.",
        None
    ),
    "Compliance Status Board": (
        "COMPOSITE — draws fafsa_completion_rate, sap_compliance_rate, verification_completion_rate, r2t4_rate from mart_aid_summary at (program, term) grain. Also surfaces verification_status breakdown and packaging_status breakdown. Needs manual definition.",
        "All compliance metrics are at aided-student level except fafsa_completion_rate which uses full enrolled headcount as denominator.",
        None
    ),
    "Student Debt Load Report": (
        "COMPOSITE — draws avg_loan_amount (sum of total_loan_disbursed / loan_recipient_count), pell_recipient_pct, avg_unmet_need from mart_aid_summary. CDR from mart_scorecard_program_outcomes (program-level) or mart_ipeds_reporting (institution-level, stub). Needs manual definition.",
        "avg_unmet_need is null until PowerFAIDS is live; CDR sources differ — program-level from Scorecard, institution-level from NSC (stub).",
        None
    ),
    "Re-Enrollment Rate (Continuing)": (
        "re_enrollment_rate = registered_next_term / eligible_continuing per (from_term, to_term, program, student_type) from snap_retention_term. Columns: re_enrollment_rate, eligible_continuing, registered_next_term, prior_yr_re_enroll_rate, rate_delta_yoy.",
        "eligible_continuing excludes new/transfer students via enrollment_status filter; filter logic has redundancy noted in SQL comment.",
        None
    ),
    "Enrollment Forecast Accuracy": (
        "Compares forecast_headcount to actual_headcount at census date. Columns: forecast_error (actual - forecast), forecast_error_pct ((actual - forecast) / forecast * 100), abs_error. Grain: institution × term. Forecast source: TBD pending ADR-011 (Cortex FORECAST pipeline). Actual from mart_enrollment_census.",
        "Forecast mart not yet built; requires Cortex FORECAST pipeline from ADR-011. Until then, forecast_headcount must come from external budget source.",
        "TBD — requires forecast pipeline (ADR-011)"
    ),
    "Executive Enrollment Summary": (
        "COMPOSITE — draws headcount and fte from mart_enrollment_census; net_tuition_revenue and discount_rate from mart_enrollment_census_ntr; yr1_retention_rate, yr4_grad_rate, yr6_grad_rate from mart_retention_cohort_summary. NTR forecast component requires Cortex FORECAST pipeline (ADR-011). Needs manual definition.",
        "NTR forecast component not yet available; mart_executive_summary not built as of 2026-06-30.",
        None
    ),
    "10-Year Enrollment Trend": (
        "Time-series view of headcount — count of enrollment records (count(*)) per (program, student_type, load_status) per term from snap_enrollment_term queried across annual fall terms over 10 years. Peer benchmark overlay requires mart_ipeds_peer_comparison.",
        "headcount in snap_enrollment_term uses count(*) (row count from fact_enrollment), not count(distinct student_id); duplicate enrollment records for the same student-term would inflate counts. Peer overlay blocked until IPEDS feeds provisioned.",
        None
    ),
}


def main():
    # Read the CSV
    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Create backup
    with open(BACKUP_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Backup created: {BACKUP_FILE}")

    # Apply corrections
    corrections_made = 0
    for row in rows:
        title = row.get("Title", "")
        if title in CORRECTIONS:
            calc_logic, known_caveats, mart_view = CORRECTIONS[title]

            old_logic = row.get("Calculation Logic", "")[:50]
            row["Calculation Logic"] = calc_logic
            row["Known Caveats"] = known_caveats
            if mart_view is not None:
                row["Mart / View"] = mart_view

            corrections_made += 1
            print(f"Fixed: {title}")
            print(f"  Old logic started: {old_logic}...")
            print(f"  New logic starts:  {calc_logic[:50]}...")
            print()

    # Write the corrected CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Corrections made: {corrections_made}")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
