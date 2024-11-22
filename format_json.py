def format_json(data: dict) -> dict:
    # Extract GCPF/FPSC number from the details section
    details_text = data["details"]["text"]
    gcpf_number = None
    lines = details_text.split("\n")
    for line in lines:
        if "GCPF / FPSC" in line:
            gcpf_number = int(line.split()[-1].strip())

    # Extract recipient name, vendor number, program, and agreement
    recipient_name = None
    vendor_number = None
    program = None
    agreement = None
    for row in data["tables"][0]:
        if "Recipient Name" in row.get("Column_0", ""):
            recipient_name = row["Column_0"].split(":")[1].strip().replace("\n", "")
            vendor_number = int(row.get("Column_1", "").split(":")[-1].strip())
            program = row.get("Column_2", "").split(":")[-1].strip().replace("\n", "")
            agreement = row.get("Column_3", "").split(":")[-1].strip().replace("\n", "")

    # Extract grant contribution details from the table
    fiscal_years_data = {}  # Dictionary to group data by fiscal year
    total_payment_issued = 0.0  # Initialize total payment issued

    for page in data['tables']:
        for row in page:
            fiscal_year = row.get("Column_0", "").strip()

            # Check if the row contains fiscal year data
            if fiscal_year and "Funds Commitment Number" not in fiscal_year:
                try:
                    # Ensure the fiscal year is in the correct format (e.g., "2023-2024")
                    if "-" in fiscal_year and len(fiscal_year) == 9:
                        entry = {
                            "funds_commitment_number": int(row.get("Column_1", "").strip()),
                            "fund_centre": int(row.get("Column_2", "").strip()),
                            "authority_code": row.get("Column_3", "").strip(),
                            "gl_account": int(row.get("Column_4", "").strip()),
                            "internal_order": int(row.get("Column_5", "").strip()),
                            "description": row.get("Column_6", "").replace("\n", ""),
                            "amount": float(
                                row.get("Column_7", "0").split()[-1].replace(",", "").replace("$", "").strip())
                        }

                        # Add the entry to the fiscal year's list
                        if fiscal_year not in fiscal_years_data:
                            fiscal_years_data[fiscal_year] = []
                        fiscal_years_data[fiscal_year].append(entry)
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}. Error: {e}")

            # Check if the row contains the total payment issued
            if "Total Payment Issued" in row.get("Column_0", ""):
                try:
                    total_payment_issued = float(
                        row.get("Column_1", "0").split()[-1].replace(",", "").replace("$", "").strip())
                except (ValueError, IndexError) as e:
                    print(f"Error processing total payment issued: {row}. Error: {e}")

    # Convert fiscal years data into a list format for JSON output
    grant_contribution_details = [
        {"fiscal_year": fiscal_year, "grant_data": entries}
        for fiscal_year, entries in fiscal_years_data.items()
    ]

    # Organize data into the required structure
    final_data = {
        "gcpf_number": gcpf_number,
        "grant_contribution_details": grant_contribution_details,
        "total_payment_issued": total_payment_issued,
        "recipient_name": recipient_name,
        "vendor_number": vendor_number,
        "program": program,
        "agreement": agreement
    }

    return final_data
