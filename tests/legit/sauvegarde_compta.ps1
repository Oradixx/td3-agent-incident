# Sauvegarde quotidienne du dossier comptabilité vers le partage réseau
$source = "C:\Compta"
$destination = "\\srv-backup\compta\$(Get-Date -Format 'yyyy-MM-dd')"
New-Item -ItemType Directory -Path $destination -Force | Out-Null
Copy-Item -Path "$source\*" -Destination $destination -Recurse -Force
Write-Host "Sauvegarde terminée vers $destination"
