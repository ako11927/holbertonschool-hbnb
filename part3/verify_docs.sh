#!/bin/bash

echo "Verifying documentation files..."
echo "================================"

# Check each file
files=(
    "docs/database_diagram.md"
    "docs/README.md"
    "docs/quick_reference.md"
    "docs/generate_diagrams.sh"
    "docs/SUMMARY.md"
    "docs/diagrams.html"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        size=$(wc -l < "$file")
        echo "✅ $file - $size lines"
    else
        echo "❌ $file - MISSING"
    fi
done

echo ""
echo "Git status:"
echo "==========="
git status --porcelain docs/

echo ""
echo "File sizes:"
echo "==========="
ls -lh docs/

echo ""
echo "Documentation verification complete!"
