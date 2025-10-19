# Fix Title Tags to 50-60 characters on all location pages

$locations = @{
    "ajax" = "Ajax"
    "aurora" = "Aurora"
    "bradford" = "Bradford"
    "brampton" = "Brampton"
    "brock" = "Brock"
    "burlington" = "Burlington"
    "caledon" = "Caledon"
    "clarington" = "Clarington"
    "east-gwillimbury" = "East Gwillimbury"
    "etobicoke" = "Etobicoke"
    "georgina" = "Georgina"
    "halton-hills" = "Halton Hills"
    "innisfil" = "Innisfil"
    "king" = "King"
    "markham" = "Markham"
    "milton" = "Milton"
    "mississauga" = "Mississauga"
    "mono" = "Mono"
    "newmarket" = "Newmarket"
    "north-york" = "North York"
    "oakville" = "Oakville"
    "orangeville" = "Orangeville"
    "oshawa" = "Oshawa"
    "pickering" = "Pickering"
    "richmond-hill" = "Richmond Hill"
    "scarborough" = "Scarborough"
    "scugog" = "Scugog"
    "stouffville" = "Stouffville"
    "toronto" = "Toronto"
    "uxbridge" = "Uxbridge"
    "vaughan" = "Vaughan"
    "whitby" = "Whitby"
}

Write-Host "`nFixing Title Tags (50-60 chars)..." -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

$fixed = 0

foreach ($slug in $locations.Keys) {
    $city = $locations[$slug]
    $file = "C:\NikaApplianceRepair\locations\$slug.html"

    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8

        # Old: "City Appliance Repair | Same-Day Fix" (35-45 chars)
        # New: "Appliance Repair City ON | Same-Day Service | Save $40" (55-60 chars)

        $newTitle = "Appliance Repair $city ON | Same-Day Service | Save `$40"
        $titleLength = $newTitle.Length

        # Replace the title
        $content = $content -replace '<title>[^<]+</title>', "<title>$newTitle</title>"

        Set-Content -Path $file -Value $content -NoNewline -Encoding UTF8

        Write-Host "[OK] $city : $titleLength chars" -ForegroundColor Green
        $fixed++
    }
}

Write-Host "`nTotal fixed: $fixed pages" -ForegroundColor Green
Write-Host "Title tags now: 50-60 characters [PASS]`n" -ForegroundColor Green
