#!/bin/bash
# Cleanup docs/ directory

# Move session summaries to docs/handoff/
mv docs/ML_SURROGATE_SESSION_*_SUMMARY.md docs/handoff/ 2>/dev/null || true
mv docs/UPDATE_SUMMARY_DEC_2025.md docs/handoff/
mv docs/CONTINUATION_INSTRUCTIONS.md docs/handoff/

# Move phase status to docs/status/
mv docs/PHASE_4_5_STATUS.md docs/status/
mv docs/PHASE_4_5_COMPLETION_SUMMARY.md docs/status/

# Move analysis/findings to docs/analysis/
mkdir -p docs/analysis
mv docs/NOTEBOOK_05_ANALYSIS.md docs/analysis/
mv docs/NOTEBOOK_05_EXECUTIVE_SUMMARY.md docs/analysis/
mv docs/NOTEBOOK_05_IMPLEMENTATION_PLAN.md docs/analysis/
mv docs/NOTEBOOK_FINDINGS.md docs/analysis/
mv docs/NOTEBOOK_UPDATE_SUMMARY.md docs/analysis/
mv docs/FRAMEWORK_AUDIT_REPORT.md docs/analysis/
mv docs/ALPHA_INVERSE_VERIFICATION_REPORT.md docs/analysis/

echo "docs/ directory cleanup complete"
