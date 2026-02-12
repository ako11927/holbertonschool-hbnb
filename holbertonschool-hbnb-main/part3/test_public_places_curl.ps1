# Test public GET /api/v1/places endpoints without JWT (cURL-style, using Invoke-WebRequest).
# Run from part3 with API server on http://127.0.0.1:5000
# Usage: .\test_public_places_curl.ps1

$Base = "http://127.0.0.1:5000/api/v1"

Write-Host "=============================================="
Write-Host "1. GET /api/v1/places/ (list) - no Authorization"
Write-Host "=============================================="
$r1 = Invoke-WebRequest -Uri "$Base/places/" -Method GET -UseBasicParsing
Write-Host $r1.Content
Write-Host "HTTP Status: $($r1.StatusCode)"
Write-Host ""

Write-Host "=============================================="
Write-Host "2. GET /api/v1/places/<place_id> (detail) - no Authorization"
Write-Host "=============================================="
$list = ($r1.Content | ConvertFrom-Json)
$placeId = if ($list -is [array] -and $list.Count -gt 0) { $list[0].id } else { "00000000-0000-0000-0000-000000000001" }
try {
    $r2 = Invoke-WebRequest -Uri "$Base/places/$placeId" -Method GET -UseBasicParsing -ErrorAction Stop
    Write-Host $r2.Content
    Write-Host "HTTP Status: $($r2.StatusCode)"
} catch {
    $status = $_.Exception.Response.StatusCode.value__
    Write-Host "HTTP Status: $status"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        Write-Host $reader.ReadToEnd()
    }
}
Write-Host ""

Write-Host "=============================================="
Write-Host "Done. Expected: list 200 + JSON array; detail 200 (found) or 404 (not found)."
Write-Host "=============================================="
