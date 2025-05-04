git --version
git add .
git commit -m "'Add formulas in the side bar'"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.2
git push origin v1.2
pause
