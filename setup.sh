#!/bin/bash

echo "🔧 Setting up Business Lead Finder (BLF) command..."

# Get current directory
BLF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make sure blf script is executable
chmod +x "$BLF_DIR/blf" 2>/dev/null

# Function to detect Python
detect_python() {
    # Try standard commands first
    for cmd in python3 python; do
        if command -v "$cmd" &> /dev/null; then
            # Skip Windows Store stub
            if "$cmd" --version 2>&1 | grep -q "Microsoft Store"; then
                continue
            fi
            if "$cmd" --version &> /dev/null; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    
    # Try common installation paths
    local python_paths=(
        "/usr/bin/python3"
        "/usr/local/bin/python3"
        "/c/Python*/python.exe"
        "/c/Program Files/Python*/python.exe"
    )
    
    for path_pattern in "${python_paths[@]}"; do
        for python_path in $path_pattern; do
            if [[ -f "$python_path" ]] && "$python_path" --version &> /dev/null; then
                echo "$python_path"
                return 0
            fi
        done
    done
    
    return 1
}

# Test if blf command works
echo "🔍 Testing BLF command..."
PYTHON_FOUND=$(detect_python)

if [[ -n "$PYTHON_FOUND" ]]; then
    echo "✅ Python detected: $PYTHON_FOUND"
    
    # Test the blf script
    if "$BLF_DIR/blf" --help &>/dev/null; then
        echo "✅ BLF script is working!"
        
        # Check if it's globally accessible
        if command -v blf &>/dev/null && blf --help &>/dev/null; then
            echo "✅ BLF command is available globally!"
            echo ""
            echo "🚀 Setup is already complete!"
            echo ""
            echo "Usage examples:"
            echo "  blf demo                     # Run demo"
            echo "  blf restaurants marrakech    # Quick search"
            exit 0
        else
            echo "🔧 BLF works locally but not globally. Setting up PATH..."
        fi
    else
        echo "⚠️  BLF script needs configuration..."
    fi
else
    echo "❌ Python not found in common locations."
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "  • Windows: https://python.org/downloads/"
    echo "  • macOS: https://python.org/downloads/ or 'brew install python'"
    echo "  • Linux: 'sudo apt install python3' or equivalent"
    echo ""
    echo "After installing Python, run this setup again."
    exit 1
fi

# Add to PATH for current session
export PATH="$BLF_DIR:$PATH"
    
    echo ""
    echo "📂 Adding BLF directory to your PATH..."
    echo "Directory: $BLF_DIR"
    echo ""
    
    # Determine shell config file
    if [[ -n "$ZSH_VERSION" ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
        SHELL_NAME="zsh"
    elif [[ -n "$BASH_VERSION" ]]; then
        if [[ -f "$HOME/.bashrc" ]]; then
            SHELL_CONFIG="$HOME/.bashrc"
        else
            SHELL_CONFIG="$HOME/.bash_profile"
        fi
        SHELL_NAME="bash"
    else
        SHELL_CONFIG="$HOME/.profile"
        SHELL_NAME="shell"
    fi
    
    echo "Detected $SHELL_NAME shell, config file: $SHELL_CONFIG"
    echo ""
    
    read -p "Add to permanent PATH in $SHELL_CONFIG? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Add to permanent PATH
        echo "" >> "$SHELL_CONFIG"
        echo "# Business Lead Finder PATH" >> "$SHELL_CONFIG"
        echo "export PATH=\"$BLF_DIR:\$PATH\"" >> "$SHELL_CONFIG"
        
        echo "✅ Successfully added to $SHELL_CONFIG!"
        echo "Please run 'source $SHELL_CONFIG' or restart your terminal."
    else
        echo "✅ Added to session PATH only."
        echo "You can run 'blf' in this terminal session."
    fi

echo ""
echo "🚀 Business Lead Finder Setup Complete!"
echo ""
echo "Usage examples:"
echo "  blf                          # Interactive mode"
echo "  blf restaurants marrakech    # Quick search"
echo "  blf cafes casablanca        # Find cafes"
echo "  blf demo                    # Run demo"
echo ""
echo "🎯 Quick test: Try running 'blf demo' to test your setup!"
