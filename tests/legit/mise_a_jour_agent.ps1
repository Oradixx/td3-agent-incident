# Téléchargement de la mise à jour de l'agent de supervision depuis le serveur interne
$url = "https://intranet.corp.local/agents/supervision-setup.msi"
$fichier = "$env:TEMP\supervision-setup.msi"
$wc = New-Object Net.WebClient
$wc.DownloadFile($url, $fichier)
Start-Process msiexec.exe -ArgumentList "/i `"$fichier`" /quiet" -Wait
