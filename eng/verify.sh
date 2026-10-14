#!/usr/bin/env bash
# Full local and CI verification. Keep in sync with eng/verify.ps1.
# Every step must pass. The script stops at the first failure with a nonzero exit code.
set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repository_root"

solution="Sonumio.slnx"
configuration="Release"
results_directory="${repository_root}/TestResults"

step() {
    printf '\n=== %s ===\n' "$1"
}

fail() {
    printf 'VERIFY FAILED: %s\n' "$1" >&2
    exit 1
}

step "Prerequisites"
command -v git >/dev/null 2>&1 || fail "git is not on PATH (Nerdbank.GitVersioning needs git history)."
command -v dotnet >/dev/null 2>&1 || fail "dotnet is not on PATH. Install the SDK version in global.json."
required_sdk="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' global.json | head -n 1)"
active_sdk="$(dotnet --version)" || fail "No installed SDK satisfies global.json (requires ${required_sdk}, rollForward latestPatch)."
echo "global.json SDK: ${required_sdk}; active SDK: ${active_sdk}"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "Not a git work tree."
[ "$(git rev-parse --is-shallow-repository)" = "false" ] || fail "Shallow clone. Nerdbank.GitVersioning needs full history (fetch-depth: 0)."

export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1

step "Locked restore"
dotnet restore "$solution" --locked-mode

step "Vulnerable package check"
vulnerability_report="$(dotnet package list --project "$solution" --vulnerable --include-transitive --no-restore)"
echo "$vulnerability_report"
if echo "$vulnerability_report" | grep -q "has the following vulnerable packages"; then
    fail "Vulnerable packages found."
fi

step "Formatting and code style"
dotnet format "$solution" --verify-no-changes --no-restore --severity info

step "Build (warnings as errors)"
dotnet build "$solution" --configuration "$configuration" --no-restore --warnaserror

step "Tests with results and coverage"
rm -rf "$results_directory"
dotnet test --solution "$solution" --configuration "$configuration" --no-build \
    --results-directory "$results_directory" \
    --report-xunit-trx \
    --coverlet --coverlet-output-format cobertura

step "Architecture checks executed"
count_architecture_outcome() {
    # grep exits 1 when nothing matches; that is a valid count of 0.
    { cat "$results_directory"/*.trx | grep -o "testName=\"[^\"]*ArchitectureTests[^\"]*\"[^>]*outcome=\"$1\"" || true; } | wc -l | tr -d ' '
}
ls "$results_directory"/*.trx >/dev/null 2>&1 || fail "No TRX test results were produced."
ls "$results_directory"/coverage.cobertura.*.xml >/dev/null 2>&1 || fail "No coverage files were produced."
architecture_passed="$(count_architecture_outcome Passed)"
[ "$architecture_passed" -gt 0 ] || fail "No passed architecture tests were found in the TRX results."
architecture_failed="$(count_architecture_outcome Failed)"
[ "$architecture_failed" -eq 0 ] || fail "Architecture tests failed."
echo "Architecture tests passed: ${architecture_passed}"

step "Verification succeeded"
echo "Results: ${results_directory}"
