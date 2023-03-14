import os
import json
import csv
import re
import shutil
import logging as log
import pandas as pd
import subprocess

# Setting up the basic logging configuration for logging
log.basicConfig(filename='logging.log', level=log.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

#Converting csv to json for better readability 
def write_csv_to_json(file):
    """
    This function reads a CSV file and creates a JSON file from it.

    Arguments:
    file -- the CSV file to be scanned.
  
    """
    log.info("Starting writing CSV to JSON...")
    endcoding = "utf-8"
    #Open the CSV file
    with open(file, 'r', encoding=endcoding) as f:
            #Open the output JSON file
            current_directory = os.getcwd()
            with open(os.path.join(current_directory, 'fields_as_json.json'), 'w') as json_file:
                #Read the CSV file in chunks and write each row to the JSON file to ensure that there are no memory leaks
                reader = csv.reader(f, delimiter='|', quotechar='~')
                for row in reader:
                    try:
                        if len(row) >= 2:
                            id = row[0]
                            log.info(f"Alive and working on reading CSV. At ID: {id} right now")
                            body = re.sub(r'[\\]|<p>.*?</p>|<li>.*?</li>', '', row[1])
                            json.dump({'id': id, 'body': body}, json_file)
                            json_file.write('\n')
                        else:
                            log.warning(f"Skipped row {row} with {len(row)} fields")
                    except csv.Error:
                        log.warning(f"Error processing CSV")


def generate_json_for_every_id():
    """
    This function accesses the previously generated JSON file and creates a separate JSON file for each ID.
    """
    log.info("Starting generating JSONS for every ID...")
    current_directory = os.getcwd()
    try:
        #Open the JSON file
        with open(f'{current_directory}/fields_as_json.json', 'r') as in_file:
            #Open json file record by record to ensure that there are no memory leaks
            for row in in_file:
                #loads the record
                record = json.loads(row)
                id = record['id']
                id = id.replace("~", "")
                id = id.replace("\n", "")
                if not id.isdigit():
                    log.warning(f"Skipping ID {id} as it is not a number.")
                    continue
                body = record['body']
                #Create a new JSON file for each id in the json file
                with open(f'{current_directory}/jsons/{id}.json', 'w') as out_file:
                    json.dump({'id': id, 'body': body}, out_file)
                    log.info(f"Generated JSON for ID: {id}")
    except Exception as e:
        log.critical(f"Error generating JSONs: {e}")

#extract javascript from the json file one by one to avoid memory leaks 
def extract_javascript_from_json_files():
    '''
    This function extracts Javascript code snippets from JSON files.
    
    '''
    log.info("Extracting JavaScript code from JSONs...")
    #Get current directory path
    current_directory = os.getcwd()
    #Change to the specified directory
    os.chdir(f'{current_directory}/jsons')
    #Get the list of JSON files in the specified directory
    json_files = [f for f in os.listdir() if f.endswith('.json')]
    #Loop through the JSON files
    for file in json_files:
        #Extract the name of the JSON file without the .json extension at the end
        file_name = os.path.splitext(file)[0]
        #Load the JSON file
        with open(file, 'r') as f:
            # Load the JSON data for this file
            data = json.load(f)

            #Extract the JavaScript code from the body field
            match = re.search(r'<script(.*?)</script>', data['body'], re.DOTALL)
            if match:
                log.info(f'Match found for file: {file}')
                code = match.group(1)
                # Write the code to a JavaScript file in a separate directory
                directory = f'{current_directory}/semgrep_to_scan'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                with open(f'{directory}/{file_name}.js', 'w') as f:
                    f.write(code)
            else:
                # Print an error message if the regular expression didn't match
                log.info(f'No match found for file: {file}')

        #deleting the data from the memory to avoid memory leaks
        del data
    #change back to root directory 
    os.chdir("..")

def extract_vulnerabilities():
    '''
    This function extracts vulnerabilities from a the semgrep_results.json.
    '''

    log.info("Getting Data from Semgrep results..")
    filename = "semgrep_to_scan/current/semgrep_results.json"
    with open(filename, 'r') as file_read:
        # Open the output CSV files
        with open('semgrep_ids_with_vulnerabilities.csv', 'a', newline='') as id_file, open('semgrep_data_results.csv', 'a', newline='') as data_file:
            id_writer = csv.writer(id_file)
            data_writer = csv.writer(data_file)
            for line in file_read:
                try:
                    record = json.loads(line.strip())
                    results = record['results']
                    if results:
                        for result in results:
                            id = result.get("path", "")
                            id = id.split(".")[0]
                            extra = result.get('extra', {})
                            message = extra.get('message', '')
                            metadata = extra.get('metadata', {})
                            cwe = metadata.get('cwe', '')
                            id_writer.writerow([id])
                            data_writer.writerow([id, message, cwe])
                except Exception as e:
                    log.critical(f'Something went wrong... ({e})')

def clear_directory():
    log.info("Clearing directory...")
    if os.path.exists("fields_as_json.json"):
        os.remove("fields_as_json.json")
        log.info("Deleted fields_as_json.json")

    if os.path.exists("jsons"):
        shutil.rmtree("jsons")
        log.info("Deleted jsons directory")

    if os.path.exists("semgrep_to_scan"):
        shutil.rmtree("semgrep_to_scan")
        log.info("Deleted semgrep_to_scan directory")
    log.info("Finished clearing directory.")


def scan_files_with_semgrep():
    '''
    This function scans 500 files in a batch with semgrep
    '''
    directory = os.getcwd() + "/semgrep_to_scan"
    current_dir = os.path.join(directory, "current")
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    #Loop until all files are scannend with semgrep
    while True:
        files_to_scan = os.listdir(directory)
        if len(files_to_scan) == 1:
            break

        #Move 500 files to scan 
        files_to_move = files_to_scan[:500]
        for filename in files_to_move:
            if not filename.endswith('.js'):
                continue
            jsfilepath = os.path.join(directory, filename)
            shutil.move(jsfilepath, current_dir)
            print(f"Moved file {filename} to {current_dir}")

        #Scan the files with semgrep
        command = ["docker", "run", "--rm", "-v", f"{current_dir}:/src", "returntocorp/semgrep", "semgrep", "--config=auto", "--max-memory", "10240", "-o", "semgrep_results.json", "--json"]
        semgrep_process = subprocess.Popen(command)
        semgrep_process.communicate()
        #extracting vulnerabilites
        extract_vulnerabilities()

        #Delete the scanned files from the directory and then repeat
        for filename in files_to_move:
            if not filename.endswith('.js'):
                continue
            jsfilepath = os.path.join(current_dir, filename)
            os.remove(jsfilepath)
            print(f"Removed file {filename} from {current_dir}")
        print("Scanned files with Semgrep")