#!/usr/bin/env python3
"""
Test dynamic ledger account resolution functionality
"""

import sys
import os

# Add the current directory to the path to import dynamicSubLedger
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamicSubLedger import DynamicSubLedgerProcessor

def test_dynamic_ledger_accounts():
    """
    Test the dynamic ledger account resolution functionality
    """
    print("=== Testing Dynamic Ledger Account Resolution ===")
    
    # Create a processor instance
    processor = DynamicSubLedgerProcessor()
    
    # Test data simulating MongoDB aggregation results
    test_data_samples = [
        {
            '_id': {'valuationDt': '2024-08-19', 'account': 'ACC123'},
            'eagleEntityId': 'ENT_001',
            'subscriptionBalance': 1500000,
            'accountCode': '3002000110',
            'accountType': 'ASSET',
            'categoryCode': '200'
        },
        {
            '_id': {'valuationDt': '2024-08-19', 'account': 'ACC456'},
            'eagleEntityId': 'ENT_002', 
            'subscriptionBalance': 2500000,
            'accountCode': '3002000120',
            'accountType': 'LIABILITY',
            'categoryCode': '150'
        }
    ]
    
    # Test cases for different ledger account patterns
    test_cases = [
        {
            'name': 'Static ledger account',
            'ledger_definition': '3002000110',
            'description': 'Fixed account number'
        },
        {
            'name': 'Dynamic account from field',
            'ledger_definition': '[accountCode]',
            'description': 'Use accountCode field value directly'
        },
        {
            'name': 'Prefix + dynamic field',
            'ledger_definition': '300[categoryCode]001',
            'description': 'Combine prefix, field value, and suffix'
        },
        {
            'name': 'Complex pattern',
            'ledger_definition': '[accountType]_[categoryCode]_LEDGER',
            'description': 'Multiple field references with text'
        }
    ]
    
    print("Test Data Samples:")
    for i, sample in enumerate(test_data_samples, 1):
        print(f"Sample {i}: Account={sample['_id']['account']}, "
              f"AccountCode={sample['accountCode']}, "
              f"AccountType={sample['accountType']}, "
              f"CategoryCode={sample['categoryCode']}")
    
    print(f"\n{'='*80}")
    
    # Test each ledger definition pattern
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Ledger Definition: '{test_case['ledger_definition']}'")
        print(f"{'-'*60}")
        
        for i, data in enumerate(test_data_samples, 1):
            resolved = processor.resolve_ledger_account(test_case['ledger_definition'], data)
            print(f"  Sample {i} -> Resolved: '{resolved}'")
        
        print()
    
    # Test field extraction for ledger definitions
    print(f"{'='*80}")
    print("Field Extraction Test:")
    print(f"{'='*80}")
    
    ledger_patterns = [
        '3002000110',
        '[accountCode]', 
        '300[categoryCode]001',
        '[accountType]_[categoryCode]_LEDGER',
        'CASH_[accountCode]_[accountType]'
    ]
    
    for pattern in ledger_patterns:
        fields = processor.extract_fields_from_formula(pattern)
        print(f"Pattern: '{pattern}' -> Fields: {fields}")

def test_integration_with_processing():
    """
    Test how dynamic ledger accounts work in the full processing pipeline
    """
    print(f"\n{'='*80}")
    print("Integration Test - Simulated Processing")
    print(f"{'='*80}")
    
    processor = DynamicSubLedgerProcessor()
    
    # Mock ledger definition with dynamic account
    mock_definition = {
        'ruleName': 'Dynamic Account Test',
        'sourceTable': 'dataNAV',
        'ledgerDefinition': '300[categoryCode]001',  # Dynamic pattern
        'dataDefinition': '[subscriptionBalance] * -1',
        'filter': 'none'
    }
    
    # Mock query result
    mock_result = {
        '_id': {'valuationDt': '2024-08-19T00:00:00.000Z', 'account': 'ACC123'},
        'eagleEntityId': 'ENT_001',
        'subscriptionBalance': 1500000,
        'categoryCode': '200'
    }
    
    print(f"Mock Definition: {mock_definition}")
    print(f"Mock Result: {mock_result}")
    print()
    
    # Test the resolution process
    resolved_account = processor.resolve_ledger_account(
        mock_definition['ledgerDefinition'], 
        mock_result
    )
    
    calculated_value = processor.apply_formula(
        mock_definition['dataDefinition'],
        mock_result
    )
    
    print(f"Original Ledger Definition: '{mock_definition['ledgerDefinition']}'")
    print(f"Resolved Ledger Account: '{resolved_account}'")
    print(f"Calculated Value: {calculated_value:,.2f}")
    
    # Show what the final ledger entry would look like
    print(f"\nFinal Ledger Entry Preview:")
    entry = {
        'ruleName': mock_definition['ruleName'],
        'account': mock_result['_id']['account'],
        'valuationDt': mock_result['_id']['valuationDt'],
        'eagleLedgerAcct': resolved_account,  # This is now dynamic!
        'calculatedValue': calculated_value,
        'dataDefinition': mock_definition['dataDefinition'],
        'ledgerDefinition': mock_definition['ledgerDefinition']
    }
    
    for key, value in entry.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_dynamic_ledger_accounts()
    test_integration_with_processing()
