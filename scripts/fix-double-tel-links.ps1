# Fix double-nested tel: links that were created by previous script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "FIX DOUBLE TEL: LINKS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$locationPages = Get-ChildItem -Path "C:\NikaApplianceRepair\locations" -Filter "*.html"
$fixed = 0

foreach ($page in $locationPages) {
    $content = Get-Content $page.FullName -Raw -Encoding UTF8
    $originalContent = $content

    # Fix pattern: <a href="tel:...">...<a href="tel:...">...</a></a>
    # Replace with: <a href="tel:...">...</a>

    # Pattern 1: <a href="tel:4377476737" style="..."><a href="tel:4377476737">TEXT</a></a>
    $content = $content -replace '<a href="tel:4377476737"([^>]*)><a href="tel:4377476737">([^<]+)</a></a>', '<a href="tel:4377476737"$1>$2</a>'

    # Pattern 2: Any remaining nested tel: links
    $content = $content -replace '<a href="tel:([^"]+)"[^>]*><a href="tel:\1">([^<]+)</a></a>', '<a href="tel:$1">$2</a>'

    if ($content -ne $originalContent) {
        Set-Content -Path $page.FullName -Value $content -NoNewline -Encoding UTF8
        Write-Host "[FIXED] $($page.Name)" -ForegroundColor Green
        $fixed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Total pages fixed: $fixed" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
