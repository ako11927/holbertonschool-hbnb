#!/bin/bash
echo "=== UPDATING ALL FILES TO CONSISTENT DATA ==="

# 1. Update run_tests.sh
echo "Updating run_tests.sh..."
sed -i "s/email=test@example.com/email=11927@holbertonstudents.com/g" run_tests.sh
sed -i "s/password=test123/password=123456/g" run_tests.sh
sed -i "s/first_name=Test/first_name=John/g" run_tests.sh
sed -i "s/last_name=User/last_name=Doe/g" run_tests.sh
sed -i "s/Beautiful Apartment/Beautiful Apartment in Riyadh/g" run_tests.sh
sed -i "s/latitude=40.7128/latitude=24.7136/g" run_tests.sh
sed -i "s/longitude=-74.0060/longitude=46.6753/g" run_tests.sh

# 2. Check route files for docstrings (optional update)
echo -e "\nChecking route files for example docstrings..."
for file in presentation/api/v1/*.py; do
    if grep -q "def post" "$file" && ! grep -q "11927@holbertonstudents.com" "$file"; then
        echo "Consider adding example to: $file"
    fi
done

# 3. Verify all updates
echo -e "\n=== VERIFICATION ==="
echo "run_tests.sh now contains:"
grep "holbertonstudents.com\|123456\|Riyadh\|24.7136\|46.6753" run_tests.sh

echo -e "\n=== FINAL CHECK FOR OLD DATA ==="
echo "Files still containing 'test@example.com':"
grep -r "test@example.com" . --include="*.py" --include="*.md" --include="*.sh" 2>/dev/null | grep -v "__pycache__" | grep -v "venv"

echo -e "\nFiles still containing 'password123':"
grep -r "password123" . --include="*.py" --include="*.md" --include="*.sh" 2>/dev/null | grep -v "__pycache__" | grep -v "venv"
