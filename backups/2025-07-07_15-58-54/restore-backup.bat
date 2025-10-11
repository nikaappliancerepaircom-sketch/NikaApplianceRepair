@echo off
echo ========================================
echo Restoring Nika Appliance Repair Backup
echo From: 2025-07-07_15-58-54
echo ========================================
echo.
echo WARNING: This will overwrite current files!
pause

echo Restoring index.html...
copy /Y "C:\Users\petru\Documents\NikaApplianceRepair\backups\2025-07-07_15-58-54\index.html" "C:\Users\petru\Documents\NikaApplianceRepair\index.html"

echo Restoring CSS files...
copy /Y "C:\Users\petru\Documents\NikaApplianceRepair\backups\2025-07-07_15-58-54\css\*.css" "C:\Users\petru\Documents\NikaApplianceRepair\css\"

echo Restoring JS files...
copy /Y "C:\Users\petru\Documents\NikaApplianceRepair\backups\2025-07-07_15-58-54\js\*.js" "C:\Users\petru\Documents\NikaApplianceRepair\js\"

echo.
echo ========================================
echo Restoration Complete!
echo ========================================
pause