import pandas as pd
import json
import requests
import io
import time

def fetch_public_gsheet_csv(spreadsheet_url):
    try:
        response = requests.get(spreadsheet_url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), on_bad_lines='skip')
        print("Kolom yang ditemukan:", df.columns)
        return df
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca Google Sheets: {e}")
        return None

def check_row_completeness(row, idx):
    """
    Check if a row has empty required fields.
    Returns a tuple of (is_complete, list of error messages)
    """
    errors = []
    
    # Check tag
    if pd.isna(row['tag']) or str(row['tag']).strip() == '':
        errors.append(f"Empty tag at row {idx}")
    
    # Check patterns
    if pd.isna(row['patterns']) or str(row['patterns']).strip() == '':
        errors.append(f"Empty patterns at row {idx}")
    else:
        patterns = str(row['patterns']).split('|')
        if not any(pattern.strip() for pattern in patterns):
            errors.append(f"All patterns are empty at row {idx}")
    
    # Check responses
    if pd.isna(row['responses']) or str(row['responses']).strip() == '':
        errors.append(f"Empty responses at row {idx}")
    else:
        responses = str(row['responses']).split('|')
        if not any(response.strip() for response in responses):
            errors.append(f"All responses are empty at row {idx}")
    
    return len(errors) == 0, errors

def dataframe_to_json(df, output_file):
    try:
        if 'patterns' not in df.columns or 'responses' not in df.columns:
            return False, ["Kolom 'patterns' atau 'responses' tidak ditemukan dalam DataFrame."]
        
        all_errors = []
        intents = []
        
        for idx, row in df.iterrows():
            is_complete, errors = check_row_completeness(row, idx + 2)  # +2 because spreadsheet rows start at 1 and header is row 1
            
            if errors:
                all_errors.extend(errors)
                continue
                
            patterns = row['patterns'].split('|') if pd.notna(row['patterns']) else []
            responses = row['responses'].split('|') if pd.notna(row['responses']) else []
            intents.append({
                "tag": row['tag'],
                "patterns": patterns,
                "responses": responses
            })
        
        if all_errors:
            return False, all_errors
            
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump({"intents": intents}, json_file, indent=4, ensure_ascii=False)
            
        return True, ["Data berhasil dikonversi ke JSON"]

    except Exception as e:
        return False, [f"Terjadi kesalahan saat mengonversi data ke JSON: {e}"]

def main():
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-vU-qVPt77la8GaWSIp-HDxxZawbknDTat_tXHCJpbgHP1kHO-W4Mx69cNqgVnM5wk-nbegpkH-Me/pub?output=csv"
    output_json_file = "intents.json"
    
    df = fetch_public_gsheet_csv(spreadsheet_url)
    if df is not None:
        success, messages = dataframe_to_json(df, output_json_file)
        if not success:
            print("\n".join(messages))
            sys.exit(1)
        print("\n".join(messages))
        return True
    else:
        print("Gagal membaca data dari Google Sheets.")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
