import pdfplumber
import pandas as pd
import os
import re

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, "../../historical_data/pdf/")
output_folder = os.path.join(script_dir, "../../historical_data/csv/")

# Extract lottery data
def extract_lottery_data(pdf_file, output_file):
    draws = []
    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):  # Track page numbers for debugging
            text = page.extract_text()
            for line_num, line in enumerate(text.split("\n"), start=1):  # Track line numbers for debugging
                # Debug: Print the raw line
                print(f"[DEBUG] Page {page_num}, Line {line_num}: {line}")
                
                # Use regex to extract the first date and the next 7 numbers
                match = re.search(r"^(\d{4}-\d{2}-\d{2}).*?((\d{1,2}) - (\d{1,2}) - (\d{1,2}) - (\d{1,2}) - (\d{1,2}) (\d{1,2}) (\d{1,2}))", line)
                if match:
                    date = match.group(1)  # First date
                    numbers = match.group(2)  # All 7 numbers as a single string
                    
                    # Split the numbers into individual fields
                    number_list = re.split(r" - | ", numbers)
                    
                    # Append cleaned data (date and split numbers)
                    draws.append([date] + number_list)
                    
                    # Debug: Print the cleaned data
                    print(f"[DEBUG] Cleaned Data: {[date] + number_list}")
    
    # Save to CSV with headers
    columns = ["Date", "Number1", "Number2", "Number3", "Number4", "Number5", "Bonus", "Multiplier"]
    df = pd.DataFrame(draws, columns=columns)
    df.to_csv(output_file, index=False)

# Process all PDFs in the input folder
def process_all_pdfs(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            csv_path = os.path.join(output_folder, filename.replace(".pdf", ".csv"))
            print(f"Processing {filename}...")
            extract_lottery_data(pdf_path, csv_path)
    print("All PDFs processed successfully!")

# Run the script
if __name__ == "__main__":
    process_all_pdfs(input_folder, output_folder)
