# Création d'une tâche planifiée de nettoyage des fichiers temporaires
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Scripts\nettoyage.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
Register-ScheduledTask -TaskName "NettoyageTemp" -Action $action -Trigger $trigger
