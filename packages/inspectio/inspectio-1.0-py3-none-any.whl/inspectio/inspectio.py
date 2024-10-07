import re
import yaml
import spacy
import argparse
import json
from datetime import datetime
import warnings
import subprocess
import pkg_resources
import sys
import time



# Suppress specific FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# inbuilt_regex = pkg_resources.resource_filename('inspectio', 'patterns.yaml')
inbuilt_regex = pkg_resources.resource_filename('inspectio', 'patterns.yaml')

def spacy_model_install():
    try:
        # Attempt to download the spaCy model
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_trf"])
        print(f"{datetime.now()}: spaCy model 'en_core_web_trf' installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        # Handle the case where the model download fails
        print(f"{datetime.now()}: Failed to install spaCy model: {e}")
        return False
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"{datetime.now()}: An error occurred: {e}")
        return False

def check_spacy_model_installation():
   # Load spaCy model
    print(f"{datetime.now()}: Loading AI Model")
    try:
        nlp = spacy.load('en_core_web_trf')
        return nlp
    except:
        try:
            print(f"{datetime.now()}: AI model loading failed. Attempting to install the model")
            installation_output = spacy_model_install()
            if installation_output:
                print(f"\n\n{datetime.now()}: Installation successful. Rerun the script again")
                sys.exit(0)
            else:
                print(f"{datetime.now()}: Installation failed. Install the model manually using : {sys.executable} -m spacy download en_core_web_trf")
                sys.exit(0)
        except Exception as e:
            print(f"{datetime.now()}: AI Model loading failed - {e}. Aborting script execution. Verify the model installation using: {sys.executable} -m spacy validate. You may also install the model again using : {sys.executable} -m spacy download en_core_web_trf")
            sys.exit(0)

# Function to load regex from YAML file
def load_regex_from_yaml(additional_regex_file):
    try:
        regex_patterns = {}
        with open(inbuilt_regex, 'r') as file:
            data = yaml.safe_load(file)
            for pattern_dict in data.get('patterns', []):
                pattern_info = pattern_dict.get('pattern')
                if pattern_info:
                    name = pattern_info.get('name')
                    regex = pattern_info.get('regex')
                    if name and regex:
                        regex_patterns[name] = regex
    except Exception as e:
        print(f"{datetime.now()}: Error loading Inbuilt regex file: {e}. Aborting the execution")
        sys.exit()

    try:
        if additional_regex_file != 'None':
            with open(additional_regex_file, 'r') as file2:
                additional_patterns = [line.strip() for line in file2 if line.strip()]
                if len(additional_patterns) <= 0:
                    print(f"{datetime.now()}: No patterns found in the additional regex file. Only default regex will be used")
                    return regex_patterns  # Return original matches in case of error
                for pattern in additional_patterns:
                    regex_patterns[f"custom_pattern_{(additional_patterns.index(pattern) + 1)}"] = pattern
        print(f"{datetime.now()}: {len(regex_patterns)} regexes loaded.")
        return regex_patterns
    except:
        print(f"{datetime.now()}: Error parsing additionally parsed regex file. Please refer documentation. Only default regex will be used")
        return regex_patterns  # Return original matches in case of error
     

def ignore_patterns_from_file(ignore_file, all_matches):
    print(f"{datetime.now()}: Ignore patterns supplied. Scanning the results and removing ignore patterns")
    try:
        with open(ignore_file, 'r') as file:
            ignore_patterns = [line.strip() for line in file if line.strip()]  # Read non-empty lines

        if len(ignore_patterns) <= 0:
            print(f"{datetime.now()}: No patterns found in the file. All results will be returned")
            return all_matches  # Return original matches in case of error

        # Compile the ignore patterns into regex objects
        compiled_patterns = [re.compile(pattern) for pattern in ignore_patterns]

        # Filter out matches that match any of the ignore patterns
        filtered_matches = [
            match for match in all_matches 
            if not any(pattern.search(str(match['identified_string'])) for pattern in compiled_patterns)
        ]

        return filtered_matches
    except Exception as e:
        print(f"{datetime.now()}: Error reading ignore patterns: {e}. All results will be returned")
        return all_matches  # Return original matches in case of error

# Function to detect sensitive information using regex
def detect_with_regex(logs, regex_patterns):
    print(f"{datetime.now()}: Regex Scanning initiated")
    matches = []
    for i, line in enumerate(logs):
        for name, pattern in regex_patterns.items():
            try:
                found_matches = re.findall(pattern, line, re.IGNORECASE)
                for identified_string in found_matches:
                    matches.append({
                        "category": name,
                        "line_number": i + 1,
                        "identified_string": identified_string,
                        "log_snippet": line.strip()
                    })
            except re.error as e:
                print(f"{datetime.now()}: Regex error in category {name}: {e}")
    return matches

# Function to detect sensitive information using spaCy model
def detect_with_spacy(logs,nlp):
    try:
        print(f"{datetime.now()}: Scanning using AI model")
        matches = []
        # Define sensitive entity types
        sensitive_entity_types = {"PERSON", "NORP", "FAC", "ORG", "GPE", "LOC","DATE","CARDINAL"}

        for i, line in enumerate(logs):
            doc = nlp(line)
            for ent in doc.ents:
                if ent.label_ in sensitive_entity_types:
                    matches.append({
                        "category": ent.label_,
                        "line_number": i+1,
                        "identified_string": ent.text,
                        "log_snippet": line.strip()
                    })
        return matches
    except:
        print(f"{datetime.now()}: Scanning with AI model failed. Results would only have regex output.")
        return []

# Function to save output in different formats
def save_output(matches, output_format, output_path):
    if output_format == 'json':
        try:
            with open(output_path, 'w') as f:
                json.dump(matches, f, indent=4)
            print(f"{datetime.now()}: Output saved to {output_path}")
        except Exception as e:
            print(f"{datetime.now()}: Error saving JSON output: {e}")

    elif output_format == 'html':
        try:
            print(f"{datetime.now()}: Generating HTML output")
            # Get current datetime for report generation
            report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Start building the HTML content
            html_content = f"""
            <html>
            <head>
                <title>Inspectio Report</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }}
                    h1 {{
                        color: #004080;
                        text-align: center;
                    }}
                    p {{
                        text-align: center;
                        font-size: 14px;
                        color: #555;
                    }}
                    table {{
                        width: 100%;
                        max-width: 100%;
                        border-collapse: collapse;
                        table-layout: fixed;
                        margin: 20px 0;
                        font-size: 14px;
                        word-wrap: break-word;
                    }}
                    table, th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #004080;
                        color: white;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f2f2f2;
                    }}
                    .center {{
                        text-align: center;
                    }}
                </style>
            </head
            >
            <body>
                <h1>Inspectio: Automated Secure Log Review Report</h1>
                <p>Generated on: {report_time}</p>
                <table>
                    <tr>
                        <th style="width: 5%;">Sl No.</th>
                        <th style="width: 10%;">Log Line Number</th>
                        <th style="width: 15%;">Category</th>
                        <th style="width: 20%;">Sensitive Value</th>
                        <th style="width: 50%;">Log Snippet</th>
                    </tr>
            """

            # Loop through the matches and populate the table rows
            for index, match in enumerate(matches, start=1):
                html_content += f"""
                <tr>
                    <td class="center" style="width: 5%;">{index}</td>
                    <td class="center" style="width: 10%;">{match['line_number']}</td>
                    <td style="width: 15%;">{match['category']}</td>
                    <td style="width: 20%;">{match['identified_string']}</td>
                    <td style="width: 50%;">{match['log_snippet']}</td>
                </tr>
                """

            # Close the HTML structure
            html_content += """
                </table>
            </body>
            </html>
            """

            # Write the HTML content to the output file
            with open(output_path, 'w') as file:
                file.write(html_content)
            
            print(f"{datetime.now()}: HTML report successfully saved to {output_path}")
        
        except Exception as e:
            print(f"{datetime.now()}: Error generating HTML report: {e}")


    else:
        raw_output = ""
        for match in matches:
            raw_output += (f"Log line number: {match['line_number']}\n")
            raw_output += (f"Category of sensitive field identified: {match['category']}\n")
            raw_output += (f"Sensitive value found: {match['identified_string']}\n")
            raw_output += (f"Log snippet: {match['log_snippet']}\n")
            raw_output += ("-" * 40)  # Separator for clarity
        if output_path:
            with open(output_path, 'w') as file:
                file.write(raw_output)
            print(f"{datetime.now()}: Output saved to {output_path}")
        else:
            print("\n\n")
            print(raw_output)

# Main function to process log files
def process_log_file(input_file, output_format, output_path, regex_yaml,ignore_regex,model):
    try:
        print(f"{datetime.now()}: Scanning Log file")
        with open(input_file, 'r') as file:
            logs = file.readlines()
    except FileNotFoundError:
        print(f"{datetime.now()}: Error: File {input_file} not found.")
        return

    # Load regex patterns
    regex_patterns = load_regex_from_yaml(regex_yaml)
    
    # Detect sensitive info with regex
    regex_matches = detect_with_regex(logs, regex_patterns)
    
    # Detect sensitive info with spaCy
    spacy_matches = detect_with_spacy(logs,model)
    
    # Combine matches
    all_matches = regex_matches + spacy_matches

    unique_matches = []
    seen_values = set()

    # Filter unique matches based on sensitive values
    for match in all_matches:
        sensitive_value = match['identified_string']
        if sensitive_value not in seen_values:
            unique_matches.append(match)
            seen_values.add(sensitive_value)

    # Sort unique matches by line number
    unique_matches.sort(key=lambda x: x['line_number'])

    all_matches = unique_matches
    if ignore_regex:
        all_matches = ignore_patterns_from_file(ignore_regex, all_matches)

    # Save or print output
    save_output(all_matches, output_format, output_path)

def printBanner():
    banner = '''
    
██╗███╗   ██╗███████╗██████╗ ███████╗ ██████╗████████╗██╗ ██████╗ 
██║████╗  ██║██╔════╝██╔══██╗██╔════╝██╔════╝╚═██╔══╝██║██╔═══██╗
██║██╔██╗ ██║███████╗██████╔╝█████╗  ██║        ██║   ██║██║   ██║
██║██║╚██╗██║╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██║██║   ██║
██║██║ ╚████║███████║██║     ███████╗╚██████╗   ██║   ██║╚██████╔╝
╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ 
                                                                  
                   An Automated Secure Log Review Tool
                   '''
    print(banner)

# Set up argparse
def main():
    printBanner()
    parser = argparse.ArgumentParser(description='Secure Log Review Tool')
    parser.add_argument('-l', '--log', required=True, help='Input log file path')
    parser.add_argument('-f', '--format', choices=['json', 'raw', 'html'], default='raw', help='Output format (json, raw, html)')
    parser.add_argument('-o', '--output', help='Output file path (required if format is html or json)')
    parser.add_argument('-r', '--regex', default='None', help='Additional Regex  file path (Line separated. Any other format will fail and corrupt the output)')
    parser.add_argument('-i', '--ignore', help='File path containing ignore patterns (Line separated. Any other format will fail and corrupt the output)')

    args = parser.parse_args()
    
    if (args.format == 'html' and not args.output) or (args.format == 'json' and not args.output):
        print(f"{datetime.now()}: Error: Output file path is required for HTML/Json formats.")
        return
    
    model = check_spacy_model_installation()
    
    process_log_file(args.log, args.format, args.output, args.regex,args.ignore,model)

if __name__ == '__main__':
    main()
