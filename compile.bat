pyinstaller -y -F --log-level DEBUG --hidden-import pkg_resources.py2_warn --add-binary "./facilities/LKCSB_GSR.csv;./facilities" --add-binary "./facilities/SIS_GSR.csv;./facilities" --add-binary "./facilities/SOA_GSR.csv;./facilities" --add-binary "./facilities/SOE_GSR.csv;./facilities" --add-binary "./facilities/SOL_GSR.csv;./facilities" "FBS Auto Booker v1.0.py"