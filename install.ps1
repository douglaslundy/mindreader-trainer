$ErrorActionPreference = "Stop"
$src = Split-Path -Parent $MyInvocation.MyCommand.Path
$base = if ($env:OPENJARVIS_HOME) { $env:OPENJARVIS_HOME } else { Join-Path $HOME ".openjarvis" }
$dest = Join-Path $base "skills\mindreader-trainer-v2"
$state = Join-Path $base "mindreader-trainer-v2"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = "$dest.backup-$stamp"

New-Item -ItemType Directory -Force -Path (Split-Path $dest -Parent) | Out-Null
New-Item -ItemType Directory -Force -Path $state | Out-Null

if (Test-Path $dest) {
    Move-Item -Force $dest $backup
    Write-Host "Backup da skill anterior criado em: $backup"
}

Copy-Item -Recurse -Force $src $dest
Write-Host "Instalado em: $dest"
Write-Host "Diretório de progresso preservado em: $state"

try {
    jarvis skill info mindreader-trainer-v2
    Write-Host "Para iniciar: jarvis chat --agent orchestrator"
    Write-Host "Dentro do chat, use: /mente"
} catch {
    Write-Host "O comando jarvis não está no PATH desta sessão."
    Write-Host "Depois, confirme com: jarvis skill list; jarvis skill info mindreader-trainer-v2"
}
