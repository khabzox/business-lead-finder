# 🔧 Business Lead Finder - Setup Guide

This guide provides setup instructions for all operating systems and environments.

## 🚀 Quick Setup (Choose Your Method)

### Windows Users

#### Option A: Command Prompt

```cmd
setup.bat
```

#### Option B: PowerShell

```powershell
.\setup.ps1
```

#### Option C: Git Bash/WSL

```bash
chmod +x setup.sh
./setup.sh
```

### Linux Users

```bash
chmod +x setup.sh
./setup.sh
```

### macOS Users

```bash
chmod +x setup.sh
./setup.sh
```

## 🧪 Quick Test

After setup, test your installation:

```bash
blf demo                     # Test all features
blf restaurants marrakech    # Quick search test
blf --help                   # Show all options
```

## 📋 Prerequisites

- **Python 3.8+** installed and accessible
- **Internet connection** for business searches
- **Terminal/Command Prompt** access

## 🛠️ Manual Setup (If Automated Setup Fails)

### Option 1: Add to PATH

1. **Find your BLF directory** (where you downloaded/cloned the project)
2. **Add to system PATH:**
   - **Windows:** Add the directory to your PATH environment variable
   - **Linux/macOS:** Add `export PATH="/path/to/business-lead-finder:$PATH"` to your shell config file

### Option 2: Use Direct Commands

Instead of global `blf` command, use platform-specific commands:

#### Windows Command Prompt

```cmd
blf.bat restaurants marrakech
blf.bat demo
```

#### Windows PowerShell

```powershell
.\blf.ps1 restaurants marrakech
.\blf.ps1 demo
```

#### Linux/macOS/WSL/Git Bash

```bash
./blf restaurants marrakech
./blf demo
```

### Option 3: Python Direct Method

```bash
python main.py restaurants marrakech
python main.py demo
python main.py --help
```

## 🔧 Troubleshooting

### "command not found" error

#### Windows

- **Command Prompt:** Use `setup.bat`
- **PowerShell:** Use `.\setup.ps1`
- **Git Bash:** Use `chmod +x setup.sh && ./setup.sh`

#### Linux/macOS

- Run `chmod +x setup.sh` first
- Then run `./setup.sh`
- Make sure you're in the project directory

### Permission errors

#### Windows

- Run Command Prompt or PowerShell as Administrator
- Or use the session-only setup option

#### Linux/macOS

- Run `chmod +x setup.sh blf`
- Make sure you have write permissions to your home directory

### Python not found

1. **Install Python 3.8+** from [python.org](https://python.org/downloads/)
2. **Add Python to PATH:**
   - **Windows:** Check "Add Python to PATH" during installation
   - **Linux:** Usually installed in PATH by default
   - **macOS:** May need to update PATH manually
3. **Restart terminal/command prompt**
4. **Test:** Run `python --version` or `python3 --version`

### Setup script fails

Use the **Python Direct Method** as a fallback:

```bash
python main.py restaurants marrakech
python main.py demo
```

This method works on any system with Python installed, regardless of PATH configuration.

## 🔄 Updating

To update your installation:

1. **Pull latest changes** (if using git)
2. **Run setup again:**
   ```bash
   # Your platform's setup command
   setup.bat           # Windows CMD
   .\setup.ps1         # Windows PowerShell
   ./setup.sh          # Linux/macOS
   ```

## 📞 Support

If you're still having issues:

1. **Check the [HOW_TO_RUN.md](docs/HOW_TO_RUN.md)** guide
2. **Try the Python Direct Method:** `python main.py demo`
3. **Check Python installation:** `python --version`
4. **Verify you're in the correct directory**

The Python Direct Method (`python main.py`) should work on any system with Python installed.
