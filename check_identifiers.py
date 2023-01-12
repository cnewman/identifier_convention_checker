import identifier_analysis_src.scan_identifiers as identifier_analysis
import sys, subprocess, csv

if __name__ == '__main__':
    srcml_process = subprocess.Popen(['srcml', '--position', sys.argv[1]], stdout=subprocess.PIPE)
    srcml_out = srcml_process.communicate()
    
    extract_identifiers_process = subprocess.Popen(['checkidentifiers'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    extract_identifiers_process.stdin.write(srcml_out[0])
    extract_identifiers_process_out = extract_identifiers_process.communicate()
    
    identifier_csv_reader = csv.DictReader(extract_identifiers_process_out[0].decode('utf-8').strip().splitlines())
    
    for row in identifier_csv_reader:
        identifierAppraisal = identifier_analysis.CheckLocalIdentifier(row)
        if identifierAppraisal != None:
            sys.stdout.write(str(identifierAppraisal))
