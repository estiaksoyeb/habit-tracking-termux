#!/data/data/com.termux/files/usr/bin/bash
set -e

# Program install dir
TARGET_DIR="$HOME/.programs/habits"

echo "📦 Installing Habits program..."

# --- Step 1: Check & install requirements ---
if ! command -v python >/dev/null 2>&1; then
    echo "🐍 Python not found. Installing..."
    pkg install -y python
fi

if ! command -v sqlite3 >/dev/null 2>&1; then
    echo "📂 sqlite3 not found. Installing..."
    pkg install -y sqlite
fi

# --- Step 2: Copy program files ---
mkdir -p "$TARGET_DIR"
cp -r ./* "$TARGET_DIR"
echo "✅ Program files copied to $TARGET_DIR"

# --- Step 3: Create bin launcher ---
BIN_FILE="$PREFIX/bin/habit"

cat > "$BIN_FILE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
python $TARGET_DIR/main.py "\$@"
EOF

chmod +x "$BIN_FILE"
echo "✅ Added command 'habit' in $PREFIX/bin"

echo ""
echo "🎉 Installation complete!"
echo "➡️ You can now run: habit"
