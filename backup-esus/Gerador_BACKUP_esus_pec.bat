@echo off
set nfile=%date:~6,4%%date:~3,2%%date:~0,2%%time:~0,2%%time:~3,2%%time:~6,2%
set nfile=%nfile: =0%
set PGPASSWORD=
"C:\Program Files\e-SUS\database\postgresql-9.6.13-4-windows-x64\bin\pg_dump.exe" -d esus -h localhost -p 5433 -U postgres -F c -b -f C:\bk\%nfile%-acresc-esus-postgres.backup
echo "Realizando Backup E-SUS PEC..."
pause