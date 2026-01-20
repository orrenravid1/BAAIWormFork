import json
import os
from pathlib import Path

def consolidate_cell_params():
    """
    Consolidate individual cell parameter JSON files into a single JSONL file.
    Each line in the output contains one cell's parameters with a cell_name field.
    """
    # Define paths
    cell_dir = Path("eworm/components/param/cell")
    output_file = Path("eworm/components/param/cell_parameters.jsonl")

    # Check if source directory exists
    if not cell_dir.exists():
        print(f"Error: Directory {cell_dir} does not exist")
        return

    # Collect all JSON files except template.json
    json_files = sorted([f for f in cell_dir.glob("*.json") if f.name != "template.json"])

    print(f"Found {len(json_files)} JSON files to process")

    # Process files and write to JSONL
    processed_count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for json_file in json_files:
            try:
                # Read the JSON file
                with open(json_file, 'r', encoding='utf-8') as infile:
                    cell_data = json.load(infile)

                # Get cell name from filename (without .json extension)
                cell_name = json_file.stem

                # Add cell_name field to the data
                cell_data_with_name = {"cell_name": cell_name, **cell_data}

                # Write as a single line in JSONL format
                outfile.write(json.dumps(cell_data_with_name) + '\n')
                processed_count += 1

            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")

    print(f"\nSuccessfully processed {processed_count} files")
    print(f"Output written to: {output_file}")
    print(f"Output file size: {output_file.stat().st_size:,} bytes")

if __name__ == "__main__":
    consolidate_cell_params()
