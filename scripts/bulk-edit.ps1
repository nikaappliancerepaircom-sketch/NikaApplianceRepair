# PowerShell Bulk HTML Editor
# Массовое редактирование HTML файлов

# Пример 1: Замена текста во всех location pages
function Replace-InLocationPages {
    param(
        [string]$OldText,
        [string]$NewText
    )

    Get-ChildItem -Path ".\locations\*.html" | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $content = $content -replace [regex]::Escape($OldText), $NewText
        Set-Content -Path $_.FullName -Value $content -NoNewline
        Write-Host "Updated: $($_.Name)"
    }
}

# Пример 2: Замена текста во всех service pages
function Replace-InServicePages {
    param(
        [string]$OldText,
        [string]$NewText
    )

    Get-ChildItem -Path ".\services\*.html" | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $content = $content -replace [regex]::Escape($OldText), $NewText
        Set-Content -Path $_.FullName -Value $content -NoNewline
        Write-Host "Updated: $($_.Name)"
    }
}

# Пример 3: Замена во ВСЕХ HTML файлах
function Replace-InAllPages {
    param(
        [string]$OldText,
        [string]$NewText
    )

    Get-ChildItem -Path "." -Filter "*.html" -Recurse | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -match [regex]::Escape($OldText)) {
            $content = $content -replace [regex]::Escape($OldText), $NewText
            Set-Content -Path $_.FullName -Value $content -NoNewline
            Write-Host "Updated: $($_.FullName)"
        }
    }
}

# Пример 4: Удаление секции между двумя маркерами
function Remove-SectionBetweenMarkers {
    param(
        [string]$StartMarker,
        [string]$EndMarker,
        [string]$Path = ".\locations\*.html"
    )

    Get-ChildItem -Path $Path | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $pattern = "(?s)$([regex]::Escape($StartMarker)).*?$([regex]::Escape($EndMarker))"
        $content = $content -replace $pattern, ""
        Set-Content -Path $_.FullName -Value $content -NoNewline
        Write-Host "Processed: $($_.Name)"
    }
}

# Пример 5: Добавить CSS файл во все страницы
function Add-CssLink {
    param(
        [string]$CssPath,
        [string]$HtmlPattern = "*.html"
    )

    $cssLink = "<link rel=`"stylesheet`" href=`"$CssPath`">"

    Get-ChildItem -Path "." -Filter $HtmlPattern -Recurse | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -notmatch [regex]::Escape($CssPath)) {
            $content = $content -replace "</head>", "    $cssLink`n</head>"
            Set-Content -Path $_.FullName -Value $content -NoNewline
            Write-Host "Added CSS link to: $($_.FullName)"
        }
    }
}

# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

# Заменить телефон во всех файлах:
# Replace-InAllPages -OldText "437-747-6737" -NewText "NEW-PHONE"

# Заменить текст только в location pages:
# Replace-InLocationPages -OldText "старый текст" -NewText "новый текст"

# Удалить секцию из всех location pages:
# Remove-SectionBetweenMarkers -StartMarker '<div class="old-section">' -EndMarker '</div>' -Path ".\locations\*.html"

# Добавить CSS файл:
# Add-CssLink -CssPath "css/new-styles.css"

Write-Host "PowerShell bulk edit script loaded. Use the functions above to make changes."
Write-Host ""
Write-Host "Available functions:"
Write-Host "  Replace-InLocationPages"
Write-Host "  Replace-InServicePages"
Write-Host "  Replace-InAllPages"
Write-Host "  Remove-SectionBetweenMarkers"
Write-Host "  Add-CssLink"
