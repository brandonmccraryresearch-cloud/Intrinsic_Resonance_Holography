#!/bin/bash
# Phase E: Repository-Wide Cleanup Script

# Move root-level summaries to archive
mv ALPHA_VERIFICATION_SUMMARY.md archive/summaries_dec2025/
mv AUDIT_SUMMARY_FOR_USER.md archive/summaries_dec2025/
mv CONSOLIDATION_SUMMARY.md archive/summaries_dec2025/
mv DEPLOYMENT_SUMMARY.md archive/summaries_dec2025/
mv FINAL_IMPLEMENTATION_SUMMARY.md archive/summaries_dec2025/
mv FINAL_SESSION_SUMMARY.md archive/summaries_dec2025/
mv IRH_v21.4_MERGER_SUMMARY.md archive/summaries_dec2025/
mv WORKFLOW_FIX_SUMMARY.md archive/summaries_dec2025/

# Move cloud/deployment docs to docs/deployment/
mkdir -p docs/deployment
mv CLOUD_RUN_DEPLOYMENT.md docs/deployment/
mv CLOUD_RUN_QUICKREF.md docs/deployment/
mv QUICKSTART_CLOUD_RUN.md docs/deployment/

# Move status/implementation docs to docs/status/
mv IMPLEMENTATION_STATUS.md docs/status/
mv COPILOT_SETUP_VALIDATION.md docs/status/

# Move user guides to docs/guides/
mkdir -p docs/guides
mv COMPLIANCE_USER_GUIDE.md docs/guides/

# Move development docs to docs/development/
mkdir -p docs/development
mv FIGURE_SPECIFICATIONS.md docs/development/
mv LATEX_COMPILATION_GUIDE.md docs/development/
mv LATEX_CONVERSION_README.md docs/development/
mv ML_SURROGATE_IMPLEMENTATION_INSTRUCTIONS.md docs/development/

# Move continuation_guide.md to docs (consolidate with CONTINUATION_GUIDE.md)
# Note: Will need to merge these two files

echo "Root directory cleanup complete"
