call E:\ProgramData\Anaconda3\condabin\conda_hook.bat
call conda activate deep
set PYTHONPATH=%PYTHONPATH%;%cd%
cd front_end_tests && behave