#!/bin/bash
echo "Starting git add, commit, and push..."

# Show current status
echo -e "\n1. Current git status:"
git status

# Add all files
echo -e "\n2. Adding files..."
git add .

# Commit
echo -e "\n3. Committing changes..."
git commit -m "Implement Place and Review endpoints

- Complete Place model with validation
- Complete Review model with validation  
- Implement Place endpoints (GET, POST, PUT, GET reviews)
- Implement Review endpoints (GET, POST, PUT, DELETE)
- Update HBnBFacade with CRUD operations
- Add sample data and test scripts
- Fix import issues and circular dependencies
- Add proper error handling and validation"

# Show commit
echo -e "\n4. Last commit:"
git log -1 --oneline

# Push
echo -e "\n5. Pushing to remote..."
git push origin main

echo -e "\nDone!"
