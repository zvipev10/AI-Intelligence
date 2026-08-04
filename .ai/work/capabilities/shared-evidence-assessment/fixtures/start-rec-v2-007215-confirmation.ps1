$ErrorActionPreference = "Stop"

$auditPath = Join-Path $env:TEMP "mcp_audit_moshe_rec_v2_007215.jsonl"
$proposal = (
    Get-Content -LiteralPath $auditPath -Encoding UTF8 |
        ForEach-Object { $_ | ConvertFrom-Json } |
        Where-Object tool -eq "prepare_workstream_indication_proposal" |
        Select-Object -Last 1
).result.workstream_proposal

$confirmationPrompt = [System.Text.RegularExpressions.Regex]::Unescape(
    "@\u05de\u05e9\u05d4, \u05d0\u05e0\u05d9 \u05de\u05d0\u05e9\u05e8 \u05d0\u05ea \u05d4\u05d4\u05e6\u05e2\u05d4 \u05db\u05e4\u05d9 \u05e9\u05d4\u05d5\u05e6\u05d2\u05d4. \u05e9\u05de\u05d5\u05e8 \u05d0\u05d5\u05ea\u05d4 \u05d1\u05d6\u05e8\u05dd \u05d4\u05e2\u05d1\u05d5\u05d3\u05d4."
)
$request = [ordered]@{
    prompt = $confirmationPrompt
    routing_prompt = $confirmationPrompt
    history = @()
    investigation_id = "investigation-final-validation-rec-v2-007215-20260728"
    workstream_context = [ordered]@{
        workstream_id = "ws_20260728_042407_9611560e"
        pending_proposal = $proposal
        current_turn_message_id = "validation-moshe-confirm-turn-3"
    }
}

$requestPath = Join-Path $env:TEMP "rec-v2-007215-confirm-request.json"
$outputPath = Join-Path $env:TEMP "rec-v2-007215-confirm-response.json"
$errorPath = Join-Path $env:TEMP "rec-v2-007215-confirm-error.txt"
[System.IO.File]::WriteAllText(
    $requestPath,
    ($request | ConvertTo-Json -Depth 30),
    (New-Object System.Text.UTF8Encoding($false))
)

$process = Start-Process -FilePath "curl.exe" -ArgumentList @(
    "--silent",
    "--show-error",
    "--max-time",
    "600",
    "--header",
    "Content-Type:application/json",
    "--data-binary",
    "@$requestPath",
    "http://151.145.93.180/api/investigate"
) -RedirectStandardOutput $outputPath -RedirectStandardError $errorPath -WindowStyle Hidden -PassThru

[pscustomobject]@{
    pid = $process.Id
    request = $requestPath
    output = $outputPath
    error = $errorPath
} | ConvertTo-Json
