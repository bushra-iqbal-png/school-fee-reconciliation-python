import pandas as pd

def reconcile_fees(file_path):
    # Data load karna
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: '{file_path}' file nahi mili!")
        return None
    
    results = []
    seen_transactions = set()
    
    for index, row in df.iterrows():
        s_id = row['student_id']
        name = row['student_name']
        invoice = row['invoice_amount']
        payment = row['payment_received']
        txn_id = str(row['transaction_id']).strip()
        
        status = ""
        remarks = "Normal"
        balance = 0
        
        # 1. Invalid Record Check (Negative amounts)
        if invoice < 0 or payment < 0:
            status = "Invalid Record"
            remarks = "Negative amount detected."
            balance = invoice - payment
            
        else:
            # 2. Outstanding Balance Calculation
            balance = invoice - payment
            
            # 3. Duplicate / Suspicious Payment Check
            if txn_id != "NONE" and txn_id in seen_transactions:
                status = "Suspicious / Duplicate"
                remarks = f"Duplicate Transaction ID: {txn_id}"
            else:
                if txn_id != "NONE":
                    seen_transactions.add(txn_id)
                
                # 4. Status Classifications
                if payment == invoice:
                    status = "Fully Paid"
                elif payment == 0:
                    status = "Unpaid"
                elif payment < invoice:
                    status = "Partially Paid"
                elif payment > invoice:
                    status = "Overpaid"
                    remarks = "Extra amount paid by student."
        
        results.append({
            "Student ID": s_id,
            "Name": name,
            "Invoice Amount": invoice,
            "Payment Received": payment,
            "Outstanding Balance": balance,
            "Status": status,
            "Remarks": remarks
        })
        
    # Final Report DataFrame
    report_df = pd.DataFrame(results)
    return report_df

if __name__ == "__main__":
    input_file = "fees_data.csv"
    print("--- School Fee Reconciliation Report ---\n")
    
    report = reconcile_fees(input_file)
    
    if report is not None:
        print(report)
        
        # Report ko Excel/CSV file mein save karna
        output_file = "reconciliation_report.csv"
        report.to_csv(output_file, index=False)
        print(f"\n[Success] Report successfully '{output_file}' ke naam se save ho gayi hai!")