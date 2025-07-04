# Business Lead Finder Setup Script (PowerShell)
# Run with: .\setup.ps1

Write-Host "🔧 Setting up Business Lead Finder (BLF) command..." -ForegroundColor Cyan

# Get current directory
$BLF_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if already in PATH
if ($env:PATH -like "*$BLF_DIR*") {
    Write-Host "✅ BLF is already set up in your PATH!" -ForegroundColor Green
} else {
    # Add to PATH for current session
    $env:PATH = "$BLF_DIR;$env:PATH"
    
    Write-Host ""
    Write-Host "📂 Adding BLF directory to your PATH..." -ForegroundColor Yellow
    Write-Host "Directory: $BLF_DIR" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "Add to permanent PATH (requires restart)? (y/n)"
    
    if ($choice -eq "y" -or $choice -eq "Y") {
        try {
            # Get current user PATH
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
            
            # Add BLF directory if not already present
            if ($currentPath -notlike "*$BLF_DIR*") {
                $newPath = "$BLF_DIR;$currentPath"
                [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)
                Write-Host "✅ Successfully added to permanent PATH!" -ForegroundColor Green
                Write-Host "You can now run 'blf' from any directory after restart." -ForegroundColor Green
            }
        }
        catch {
            Write-Host "❌ Failed to add to permanent PATH. You may need admin rights." -ForegroundColor Red
            Write-Host "Using session PATH only." -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ Added to session PATH only." -ForegroundColor Green
        Write-Host "You can run 'blf' in this PowerShell session." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🚀 Business Lead Finder Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage examples:" -ForegroundColor Cyan
Write-Host "  blf                          # Interactive mode" -ForegroundColor Gray
Write-Host "  blf restaurants marrakech    # Quick search" -ForegroundColor Gray
Write-Host "  blf cafes casablanca        # Find cafes" -ForegroundColor Gray
Write-Host "  blf demo                    # Run demo" -ForegroundColor Gray
Write-Host ""

# Test if Python is available
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python detected" -ForegroundColor Green
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python 3 detected" -ForegroundColor Green
} else {
    Write-Host "⚠️  Python not found in PATH. Please install Python 3.8+ first." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Quick test: Try running 'blf demo' to test your setup!" -ForegroundColor Cyan

Read-Host "Press Enter to continue..."
