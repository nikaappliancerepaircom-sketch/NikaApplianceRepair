# Remove booking-form-optimized.css link from all HTML files

$filesChanged = 0

Get-ChildItem -Path "C:\NikaApplianceRepair" -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw

    if ($content -match 'booking-form-optimized\.css') {
        # Remove the CSS link line
        $newContent = $content -replace '<link[^>]*booking-form-optimized\.css[^>]*>\s*\n?', ''

        Set-Content -Path $_.FullName -Value $newContent -NoNewline
        Write-Host "Removed from: $($_.Name)" -ForegroundColor Green
        $filesChanged++
    }
}

Write-Host ""
Write-Host "Total files updated: $filesChanged" -ForegroundColor Cyan
