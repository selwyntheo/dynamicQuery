#!/usr/bin/env python3
"""
Test script for Dynamic Sub Ledger functionality
"""

from dynamicSubLedger import DynamicSubLedgerProcessor

def test_formula_parsing():
    """Test formula parsing functionality"""
    print("=== Testing Formula Parsing ===")
    
    processor = DynamicSubLedgerProcessor("dummy.csv")
    
    test_formulas = [
        "[subscriptionBalance] * -1",
        "[redemptionBalance] + [redemptionPayBase]",
        "[netAssets] / [sharesOutstanding]",
        "[capstock] + [settleCapstock] - [distribution]",
        "[dailyYeild] * 365 * 100"
    ]
    
    for formula in test_formulas:
        fields = processor.extract_fields_from_formula(formula)
        print(f"Formula: {formula}")
        print(f"Fields: {fields}\n")

def test_formula_calculation():
    """Test formula calculation with sample data"""
    print("=== Testing Formula Calculation ===")
    
    processor = DynamicSubLedgerProcessor("dummy.csv")
    
    test_data = {
        'subscriptionBalance': 1000000,
        'redemptionBalance': 500000,
        'redemptionPayBase': 200000,
        'netAssets': 50000000,
        'sharesOutstanding': 1000000,
        'dailyYeild': 0.025
    }
    
    test_cases = [
        ("[subscriptionBalance] * -1", -1000000),
        ("[redemptionBalance] + [redemptionPayBase]", 700000),
        ("[netAssets] / [sharesOutstanding]", 50.0),
        ("[dailyYeild] * 100", 2.5)
    ]
    
    for formula, expected in test_cases:
        result = processor.apply_formula(formula, test_data)
        status = "✓" if abs(result - expected) < 0.01 else "✗"
        print(f"{status} Formula: {formula}")
        print(f"   Expected: {expected}, Got: {result}\n")

def test_mongodb_query_building():
    """Test MongoDB query building"""
    print("=== Testing MongoDB Query Building ===")
    
    processor = DynamicSubLedgerProcessor("dummy.csv")
    
    test_cases = [
        ("dataNAV", "", ["subscriptionBalance"]),
        ("dataNAV", "shareClass='A'", ["netAssets"]),
        ("dataNAV", "isComposite=true", ["capstock", "settleCapstock"]),
        ("dataNAV", "accountBaseCurrency='USD'", ["dailyYeild"])
    ]
    
    for source_table, filter_condition, fields in test_cases:
        query = processor.build_mongodb_query(source_table, filter_condition, fields)
        print(f"Source: {source_table}")
        print(f"Filter: {filter_condition}")
        print(f"Fields: {fields}")
        print(f"Query: {query}\n")

def create_test_csv():
    """Create a test CSV file with various scenarios"""
    print("=== Creating Test CSV ===")
    
    test_csv_content = """ruleName,sourceTable,ledgerDefinition,dataDefinition,filter
Simple Multiplication,dataNAV,3001000100,"[subscriptionBalance] * 2",none
Addition Formula,dataNAV,3001000200,"[redemptionBalance] + [redemptionPayBase]",none
Division Formula,dataNAV,3001000300,"[netAssets] / [sharesOutstanding]",none
Filtered by Class,dataNAV,3001000400,"[netAssets]","shareClass='A'"
Filtered by Currency,dataNAV,3001000500,"[dailyYeild] * 365","accountBaseCurrency='USD'"
Boolean Filter,dataNAV,3001000600,"[capstock] + [settleCapstock]","isComposite=true"
Complex Formula,dataNAV,3001000700,"([incomeDistribution] - [ltcglDistribution]) * 1.2",none"""
    
    with open('/Volumes/D/Ai/python/dataset/test_dynamicSubledger.csv', 'w') as f:
        f.write(test_csv_content)
    
    print("Test CSV created: test_dynamicSubledger.csv")

def run_test_scenario():
    """Run a complete test scenario"""
    print("=== Running Complete Test Scenario ===")
    
    create_test_csv()
    
    # Process the test CSV
    processor = DynamicSubLedgerProcessor(
        csv_file_path="/Volumes/D/Ai/python/dataset/test_dynamicSubledger.csv"
    )
    
    results = processor.process_all_definitions()
    
    # Generate summary
    summary = processor.generate_summary_report()
    print(summary)
    
    # Save test results
    processor.save_results_to_json("/Volumes/D/Ai/python/dataset/test_ledger_results.json")

if __name__ == "__main__":
    print("=== Dynamic Sub-Ledger Test Suite ===\n")
    
    test_formula_parsing()
    test_formula_calculation()
    test_mongodb_query_building()
    run_test_scenario()
