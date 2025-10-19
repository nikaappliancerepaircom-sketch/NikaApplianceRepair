# Fix CRITICAL BMAD Issues Across All Location Pages
#
# Issues to fix:
# 1. Review count: "520+ Reviews" -> "5,200+ Reviews" (Data Consistency)
# 2. Review count in schema: Keep at 5200 but ensure consistency

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CRITICAL BMAD FIXES - All Location Pages" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$locationPages = Get-ChildItem -Path "C:\NikaApplianceRepair\locations" -Filter "*.html"
$fixedPages = 0
$errors = @()

foreach ($page in $locationPages) {
    try {
        Write-Host "Processing: $($page.Name)..." -ForegroundColor Yellow

        $content = Get-Content $page.FullName -Raw -Encoding UTF8
        $modified = $false

        # FIX 1: Review count consistency (520+ -> 5,200+)
        if ($content -match '520\+\s*Reviews') {
            $content = $content -replace '520\+\s*Reviews', '5,200+ Reviews'
            Write-Host "  [FIXED] Review count: 520+ -> 5,200+" -ForegroundColor Green
            $modified = $true
        }

        # FIX 2: Ensure schema reviewCount is consistent
        if ($content -match '"reviewCount":\s*"520"') {
            $content = $content -replace '"reviewCount":\s*"520"', '"reviewCount": "5200"'
            Write-Host "  [FIXED] Schema reviewCount: 520 -> 5200" -ForegroundColor Green
            $modified = $true
        }

        # FIX 3: Ensure all phone numbers have proper format (remove spaces in tel: links)
        # tel:437-747-6737 or tel:4377476737 (both valid, but 4377476737 is more standard)
        if ($content -match 'tel:437-747-6737') {
            $content = $content -replace 'tel:437-747-6737', 'tel:4377476737'
            Write-Host "  [FIXED] Phone format in tel: links" -ForegroundColor Green
            $modified = $true
        }

        if ($modified) {
            Set-Content -Path $page.FullName -Value $content -NoNewline -Encoding UTF8
            $fixedPages++
            Write-Host "  [OK] $($page.Name) updated successfully`n" -ForegroundColor Green
        } else {
            Write-Host "  [SKIP] No changes needed`n" -ForegroundColor Gray
        }
    }
    catch {
        $errors += $page.Name
        Write-Host "  [ERROR] Failed to process $($page.Name): $($_.Exception.Message)`n" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total pages processed: $($locationPages.Count)" -ForegroundColor White
Write-Host "Pages fixed: $fixedPages" -ForegroundColor Green

if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    Write-Host "Failed pages: $($errors -join ', ')" -ForegroundColor Red
} else {
    Write-Host "Errors: 0" -ForegroundColor Green
}

Write-Host "`n[IMPORTANT] This script fixed Data Consistency issues." -ForegroundColor Yellow
Write-Host "Category 10 should now be 100% on all pages.`n" -ForegroundColor Yellow
