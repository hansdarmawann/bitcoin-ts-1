@echo off
REM ============================================
REM Run Streamlit App - Bitcoin Time Series
REM ============================================

REM Move to project root
cd /d "%~dp0"

REM Activate conda environment
call conda activate bitcoin-ts-1

REM Run Streamlit
streamlit run sources\streamlit_app.py

pause
