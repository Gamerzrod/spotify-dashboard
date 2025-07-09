@echo off
REM Activate conda environment and run Streamlit app
CALL C:\Users\rodri\anaconda3\Scripts\activate.bat spotify_env
cd "C:\Users\rodri\OneDrive\Documents\spotify_project\archive"
streamlit run spotify_dashboard.py
pause
