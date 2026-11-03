# Inventaire matériel envoyé au service informatique
$info = @{
    ComputerName = $env:COMPUTERNAME
    OSVersion = [Environment]::OSVersion.VersionString
    Architecture = (Get-WmiObject Win32_OperatingSystem).OSArchitecture
    Bios = (Get-WmiObject Win32_BIOS).Manufacturer
    RAM = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory
}
$info | ConvertTo-Json | Out-File "C:\Inventaire\$env:COMPUTERNAME.json"
