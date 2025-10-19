# Check word counts for all 20 new location pages

$newLocations = @(
    "etobicoke", "north-york", "scarborough",
    "aurora", "whitby", "newmarket", "stouffville", "caledon", "clarington",
    "halton-hills", "bradford", "east-gwillimbury", "king", "georgina",
    "innisfil", "orangeville", "uxbridge", "scugog", "brock", "mono"
)

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "WORD COUNT CHECK - 20 NEW LOCATION PAGES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Target: 2,000-2,500 words (visible content)`n" -ForegroundColor Yellow

$results = @()
$passCount = 0
$lowCount = 0
$highCount = 0

foreach ($location in $newLocations) {
    $file = "C:\NikaApplianceRepair\locations\$location.html"

    if (Test-Path $file) {
        # Use Node.js script to count words
        $output = & node "C:\NikaApplianceRepair\tools\count-visible-words.js" $file 2>&1

        # Extract word count from output
        if ($output -match 'VISIBLE WORD COUNT:\s*(\d+)\s*words') {
            $wordCount = [int]$matches[1]

            $status = ""
            $color = "White"

            if ($wordCount -ge 2000 -and $wordCount -le 2500) {
                $status = "PERFECT"
                $color = "Green"
                $passCount++
            }
            elseif ($wordCount -lt 2000) {
                $needed = 2000 - $wordCount
                $status = "LOW (-$needed)"
                $color = "Yellow"
                $lowCount++
            }
            else {
                $excess = $wordCount - 2500
                $status = "HIGH (+$excess)"
                $color = "Magenta"
                $highCount++
            }

            $cityName = (Get-Culture).TextInfo.ToTitleCase($location.Replace("-", " "))
            Write-Host ("{0,-20} {1,5} words  [{2}]" -f $cityName, $wordCount, $status) -ForegroundColor $color

            $results += [PSCustomObject]@{
                City = $cityName
                Words = $wordCount
                Status = $status
            }
        }
    }
}

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Total pages checked: $($newLocations.Count)" -ForegroundColor White
Write-Host "Perfect range (2,000-2,500): $passCount" -ForegroundColor Green
Write-Host "Below 2,000: $lowCount" -ForegroundColor Yellow
Write-Host "Above 2,500: $highCount" -ForegroundColor Magenta

$avgWords = ($results | Measure-Object -Property Words -Average).Average
Write-Host "`nAverage word count: $([int]$avgWords) words" -ForegroundColor Cyan

if ($lowCount -gt 0) {
    Write-Host "`n[ACTION NEEDED] $lowCount pages need more content" -ForegroundColor Yellow
}

if ($highCount -gt 0) {
    Write-Host "`n[REVIEW] $highCount pages exceed target (may need reduction)" -ForegroundColor Magenta
}

Write-Host "`n"
