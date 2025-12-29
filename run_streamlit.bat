@echo off
REM ============================================
REM Run Streamlit App - Bitcoin Time Series
REM ============================================

REM Pindah ke root project
cd /d "%~dp0"

REM Aktifkan conda environment
call conda activate bitcoin-ts-1

REM Jalankan Streamlit
streamlit run sources\streamlit_app.py

pause
