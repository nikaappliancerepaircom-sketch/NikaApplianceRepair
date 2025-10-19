# Fix UTF-8 encoding issues (hieroglyphs) in HTML files

param(
    [string]$FilePath = "C:\NikaApplianceRepair\locations\east-gwillimbury.html"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "FIX ENCODING ISSUES (HIEROGLYPHS)" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if (-not (Test-Path $FilePath)) {
    Write-Host "[ERROR] File not found: $FilePath" -ForegroundColor Red
    exit 1
}

# Read file as UTF-8
$content = Get-Content $FilePath -Raw -Encoding UTF8

Write-Host "[INFO] Checking: $FilePath" -ForegroundColor Cyan
Write-Host ""

$originalContent = $content
$issuesFixed = 0

# Fix common UTF-8 encoding issues (double-encoded characters)

# Fix bullet points
if ($content -match 'â€¢') {
    $count = ([regex]::Matches($content, 'â€¢')).Count
    $content = $content -replace 'â€¢', '•'
    Write-Host "[FIXED] $count bullet points (â€¢ → •)" -ForegroundColor Green
    $issuesFixed++
}

# Fix star emoji
if ($content -match 'â­') {
    $count = ([regex]::Matches($content, 'â­')).Count
    $content = $content -replace 'â­', '⭐'
    Write-Host "[FIXED] $count star emojis (â­ → ⭐)" -ForegroundColor Green
    $issuesFixed++
}

# Fix lightning emoji
if ($content -match 'âš¡') {
    $count = ([regex]::Matches($content, 'âš¡')).Count
    $content = $content -replace 'âš¡', '⚡'
    Write-Host "[FIXED] $count lightning emojis (âš¡ → ⚡)" -ForegroundColor Green
    $issuesFixed++
}

# Fix copyright symbol
if ($content -match 'Â©') {
    $count = ([regex]::Matches($content, 'Â©')).Count
    $content = $content -replace 'Â©', '©'
    Write-Host "[FIXED] $count copyright symbols (Â© → ©)" -ForegroundColor Green
    $issuesFixed++
}

# Fix shield emoji (common in warranty/security sections)
if ($content -match 'ðŸ›¡ï¸') {
    $count = ([regex]::Matches($content, 'ðŸ›¡ï¸')).Count
    $content = $content -replace 'ðŸ›¡ï¸', '🛡️'
    Write-Host "[FIXED] $count shield emojis (ðŸ›¡ï¸ → 🛡️)" -ForegroundColor Green
    $issuesFixed++
}

# Fix wrench emoji
if ($content -match 'ðŸ"§') {
    $count = ([regex]::Matches($content, 'ðŸ"§')).Count
    $content = $content -replace 'ðŸ"§', '🔧'
    Write-Host "[FIXED] $count wrench emojis (ðŸ"§ → 🔧)" -ForegroundColor Green
    $issuesFixed++
}

# Fix trophy emoji
if ($content -match 'ðŸ†') {
    $count = ([regex]::Matches($content, 'ðŸ†')).Count
    $content = $content -replace 'ðŸ†', '🏆'
    Write-Host "[FIXED] $count trophy emojis (ðŸ† → 🏆)" -ForegroundColor Green
    $issuesFixed++
}

# Fix money bag emoji
if ($content -match 'ðŸ'°') {
    $count = ([regex]::Matches($content, 'ðŸ'°')).Count
    $content = $content -replace 'ðŸ'°', '💰'
    Write-Host "[FIXED] $count money bag emojis (ðŸ'° → 💰)" -ForegroundColor Green
    $issuesFixed++
}

# Fix house emoji
if ($content -match 'ðŸ ') {
    $count = ([regex]::Matches($content, 'ðŸ ')).Count
    $content = $content -replace 'ðŸ ', '🏠'
    Write-Host "[FIXED] $count house emojis (ðŸ  → 🏠)" -ForegroundColor Green
    $issuesFixed++
}

# Fix technician emoji
if ($content -match 'ðŸ'¨â€ðŸ"§') {
    $count = ([regex]::Matches($content, 'ðŸ'¨â€ðŸ"§')).Count
    $content = $content -replace 'ðŸ'¨â€ðŸ"§', '👨‍🔧'
    Write-Host "[FIXED] $count technician emojis (ðŸ'¨â€ðŸ"§ → 👨‍🔧)" -ForegroundColor Green
    $issuesFixed++
}

# Fix money emoji
if ($content -match 'ðŸ'µ') {
    $count = ([regex]::Matches($content, 'ðŸ'µ')).Count
    $content = $content -replace 'ðŸ'µ', '💵'
    Write-Host "[FIXED] $count money emojis (ðŸ'µ → 💵)" -ForegroundColor Green
    $issuesFixed++
}

# Fix calendar emoji
if ($content -match 'ðŸ"…') {
    $count = ([regex]::Matches($content, 'ðŸ"…')).Count
    $content = $content -replace 'ðŸ"…', '📅'
    Write-Host "[FIXED] $count calendar emojis (ðŸ"… → 📅)" -ForegroundColor Green
    $issuesFixed++
}

# Fix water droplet emoji
if ($content -match 'ðŸ'§') {
    $count = ([regex]::Matches($content, 'ðŸ'§')).Count
    $content = $content -replace 'ðŸ'§', '💧'
    Write-Host "[FIXED] $count water droplet emojis (ðŸ'§ → 💧)" -ForegroundColor Green
    $issuesFixed++
}

# Fix building emoji
if ($content -match 'ðŸ¢') {
    $count = ([regex]::Matches($content, 'ðŸ¢')).Count
    $content = $content -replace 'ðŸ¢', '🏢'
    Write-Host "[FIXED] $count building emojis (ðŸ¢ → 🏢)" -ForegroundColor Green
    $issuesFixed++
}

# Fix cooking pot emoji
if ($content -match 'ðŸ¥˜') {
    $count = ([regex]::Matches($content, 'ðŸ¥˜')).Count
    $content = $content -replace 'ðŸ¥˜', '🥘'
    Write-Host "[FIXED] $count cooking pot emojis (ðŸ¥˜ → 🥘)" -ForegroundColor Green
    $issuesFixed++
}

# Fix checkmark emoji
if ($content -match 'âœ"') {
    $count = ([regex]::Matches($content, 'âœ"')).Count
    $content = $content -replace 'âœ"', '✓'
    Write-Host "[FIXED] $count checkmark emojis (âœ" → ✓)" -ForegroundColor Green
    $issuesFixed++
}

# Save file if changes were made
if ($content -ne $originalContent) {
    # Remove BOM if present and save as UTF-8 without BOM
    Set-Content -Path $FilePath -Value $content -NoNewline -Encoding UTF8

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "[SUCCESS] Fixed $issuesFixed encoding issue types" -ForegroundColor Green
    Write-Host "[SAVED] $FilePath" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
} else {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "[INFO] No encoding issues found!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
}
