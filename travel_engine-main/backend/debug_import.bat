@echo off
cd /d c:\Users\achra\ai_agent\backend
python -c "import main; print('Import successful')" > test_output.txt 2>&1
echo Done >> test_output.txt
