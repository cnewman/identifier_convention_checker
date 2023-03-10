import identifier_analysis_src.scan_identifiers as identifier_analysis
import sys, subprocess, csv, argparse
VERSION = "1.0.0"

if __name__ == '__main__':
    command_line_parser = argparse.ArgumentParser()
    command_line_parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    command_line_parser.add_argument("--target")
    args = command_line_parser.parse_args()
    
    srcml_process = subprocess.Popen(['srcml', '--position', args.target], stdout=subprocess.PIPE)
    srcml_out = srcml_process.communicate()
    
    extract_identifiers_process = subprocess.Popen(['checkidentifiers'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    extract_identifiers_process.stdin.write(srcml_out[0])
    extract_identifiers_process_out = extract_identifiers_process.communicate()
    
    identifier_csv_reader = csv.DictReader(extract_identifiers_process_out[0].decode('utf-8').strip().splitlines())
    
    for row in identifier_csv_reader:
        identifierAppraisal = identifier_analysis.CheckLocalIdentifier(row)
        if identifierAppraisal != None:
            sys.stdout.write(str(identifierAppraisal))
