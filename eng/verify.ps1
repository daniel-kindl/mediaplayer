#!/usr/bin/env pwsh
# Full local and CI verification. Keep in sync with eng/verify.sh.
# Every step must pass. The script stops at the first failure with a nonzero exit code.
#Requires -Version 7.2
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$repositoryRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repositoryRoot

$solution = 'Sonumio.slnx'
$configuration = 'Release'
$resultsDirectory = Join-Path $repositoryRoot 'TestResults'

function Write-Step([string] $name) {
    Write-Host ""
    Write-Host "=== $name ==="
}

function Stop-Verification([string] $message) {
    Write-Error "VERIFY FAILED: $message" -ErrorAction Continue
    exit 1
}

Write-Step 'Prerequisites'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Stop-Verification 'git is not on PATH (Nerdbank.GitVersioning needs git history).' }
if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) { Stop-Verification 'dotnet is not on PATH. Install the SDK version in global.json.' }
$requiredSdk = (Get-Content global.json -Raw | ConvertFrom-Json).sdk.version
$activeSdk = & dotnet --version
Write-Host "global.json SDK: $requiredSdk; active SDK: $activeSdk"
if ((& git rev-parse --is-shallow-repository) -ne 'false') { Stop-Verification 'Shallow clone. Nerdbank.GitVersioning needs full history (fetch-depth: 0).' }

$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$env:DOTNET_NOLOGO = '1'

Write-Step 'Locked restore'
& dotnet restore $solution --locked-mode

Write-Step 'Vulnerable package check'
$vulnerabilityReport = & dotnet package list --project $solution --vulnerable --include-transitive --no-restore | Out-String
Write-Host $vulnerabilityReport
if ($vulnerabilityReport -match 'has the following vulnerable packages') { Stop-Verification 'Vulnerable packages found.' }

Write-Step 'Formatting and code style'
& dotnet format $solution --verify-no-changes --no-restore --severity info

Write-Step 'Build (warnings as errors)'
& dotnet build $solution --configuration $configuration --no-restore --warnaserror

Write-Step 'Tests with results and coverage'
if (Test-Path $resultsDirectory) { Remove-Item $resultsDirectory -Recurse -Force }
& dotnet test --solution $solution --configuration $configuration --no-build `
    --results-directory $resultsDirectory `
    --report-xunit-trx `
    --coverlet --coverlet-output-format cobertura

Write-Step 'Architecture checks executed'
$trxFiles = @(Get-ChildItem $resultsDirectory -Filter '*.trx')
if ($trxFiles.Count -eq 0) { Stop-Verification 'No TRX test results were produced.' }
if (@(Get-ChildItem $resultsDirectory -Filter 'coverage.cobertura.*.xml').Count -eq 0) { Stop-Verification 'No coverage files were produced.' }
$architectureResults = foreach ($file in $trxFiles) {
    # Projects without tests produce a TRX file with no result nodes.
    ([xml](Get-Content $file.FullName -Raw)).SelectNodes("//*[local-name()='UnitTestResult']") |
        Where-Object { $_.GetAttribute('testName') -like '*ArchitectureTests*' }
}
$passed = @($architectureResults | Where-Object { $_.GetAttribute('outcome') -eq 'Passed' }).Count
$failed = @($architectureResults | Where-Object { $_.GetAttribute('outcome') -eq 'Failed' }).Count
if ($passed -eq 0) { Stop-Verification 'No passed architecture tests were found in the TRX results.' }
if ($failed -ne 0) { Stop-Verification 'Architecture tests failed.' }
Write-Host "Architecture tests passed: $passed"

Write-Step 'Verification succeeded'
Write-Host "Results: $resultsDirectory"
