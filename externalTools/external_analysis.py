import externalTools.external_analysis_functions as f
import os
import glob
import subprocess
import datetime
import shutil

# INFO: RUN THE SCRIPT IN THE DIRECTORY WHERE THE CSV FILE IS LOCATED 
f.log.info("Starting Extern Analysis...")

f.log.info("Generating directories...")
directories_to_generate = ['jsons', 'semgrep_to_scan']
csv_files = glob.glob('*.csv')

f.log.info("Looking for CSV...")
if not csv_files:
    print("No CSV files found in the current directory.")
else:
    for directory in directories_to_generate:
       if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"{directory} has been created.")
            except OSError as e:
                if 'File exists' not in str(e):
                    raise
       else:
        print(f"{directory} already exists.")

    latest_csv = max(csv_files, key=os.path.getmtime)
    full_path = os.path.abspath(latest_csv)
    f.log.info(f"Latest CSV file is: {full_path}")
    time = os.path.getmtime(full_path)
    time_object = datetime.datetime.fromtimestamp(time)
    f.log.info(f"Latest CSV file modification time: {time_object.date()}:{time_object.time()}")

    f.write_csv_to_json(full_path)
    f.generate_json_for_every_id()
    f.extract_javascript_from_json_files()
    f.scan_files_with_semgrep()
    





