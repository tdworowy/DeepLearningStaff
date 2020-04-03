call C:\ProgramData\Anaconda3\condabin\conda_hook.bat
call conda activate conda1
set PYTHONPATH=%PYTHONPATH%;%cd%
cd front_end_tests && behave