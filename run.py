from scanner_source import *
import sys, subprocess

if __name__ == '__main__':
    srcml_process = subprocess.Popen(['srcml', '--position', sys.argv[1]], stdout=subprocess.PIPE)
    srcml_out = srcml_process.communicate()
    
    extract_identifiers_process = subprocess.Popen(['build/bin/checkidentifiers', srcml_out[0].decode('utf-8').strip()], stdout=subprocess.PIPE)
    extract_identifiers_process_out = extract_identifiers_process.communicate()

    
    print(extract_identifiers_process_out[0].decode('utf-8').strip())