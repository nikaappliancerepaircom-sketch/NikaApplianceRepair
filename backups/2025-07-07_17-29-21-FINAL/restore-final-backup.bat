@echo off
echo ========================================
echo Restoring FINAL Nika Appliance Repair Backup
echo From: 2025-07-07_17-29-21-FINAL
echo ========================================
echo.
echo This will restore the website to its FINAL state with all updates.
echo.
echo WARNING: This will overwrite current files!
pause

echo.
echo Restoring index.html...
copy /Y "C:\Users\petru\Documents\NikaApplianceRepair\backups\2025-07-07_17-29-21-FINAL\index.html" "C:\Users\petru\Documents\NikaApplianceRepair\index.html"

echo Restoring CSS files...
copy /Y "C:\Users\petru\Documents\NikaApplianceRepair\backups\2025-07-07_17-29-21-FINAL\css\*.css" "C:\Users\petru\Documents\NikaApplianceRepair\css\"

echo Restoring JS files...
copy /Y "C:\Users\petru\Documents\NikaApplianceRepair\backups\2025-07-07_17-29-21-FINAL\js\*.js" "C:\Users\petru\Documents\NikaApplianceRepair\js\"

echo.
echo ========================================
echo Restoration Complete!
echo ========================================
echo.
echo The website has been restored to its FINAL state with:
echo - Hero section updates (yellow text, white icons)
echo - Blue gradient footer
echo - Modern video sections
echo - How It Works with STEP 1, 2, 3
echo - Consistent dark blue headings
echo.
pause