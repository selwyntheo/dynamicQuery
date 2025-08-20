#!/usr/bin/env python3
"""
Test enhanced formula functionality with mathematical functions
"""

import sys
import os

# Add the current directory to the path to import dynamicSubLedger
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamicSubLedger import DynamicSubLedgerProcessor

def test_enhanced_formulas():
    """
    Test the enhanced apply_formula method with various mathematical functions
    """
    print("=== Testing Enhanced Formula Functionality ===")
    
    # Create a processor instance
    processor = DynamicSubLedgerProcessor()
    
    # Test data
    test_data = {
        'bookValueBase': -150000.50,
        'netAssets': 250000.75,
        'subscriptionBalance': 1500000,
        'redemptionBalance': 500000,
        'yield': 0.0345
    }
    
    # Test cases with various formulas
    test_cases = [
        {
            'name': 'Basic multiplication',
            'formula': '[subscriptionBalance] * -1',
            'expected_type': float
        },
        {
            'name': 'ABS function with negative value',
            'formula': 'ABS([bookValueBase]) * -1',
            'expected_type': float
        },
        {
            'name': 'Multiple functions',
            'formula': 'ROUND(ABS([bookValueBase]) + [netAssets], 2)',
            'expected_type': float
        },
        {
            'name': 'MAX function',
            'formula': 'MAX([subscriptionBalance], [redemptionBalance])',
            'expected_type': float
        },
        {
            'name': 'MIN function',
            'formula': 'MIN([subscriptionBalance], [redemptionBalance])',
            'expected_type': float
        },
        {
            'name': 'Complex formula',
            'formula': 'ABS([bookValueBase]) + ROUND([netAssets] * [yield], 2)',
            'expected_type': float
        },
        {
            'name': 'CEIL function',
            'formula': 'CEIL([yield] * 100)',
            'expected_type': float
        },
        {
            'name': 'FLOOR function',
            'formula': 'FLOOR([netAssets] / 1000)',
            'expected_type': float
        },
        {
            'name': 'SQRT function',
            'formula': 'SQRT(ABS([bookValueBase]))',
            'expected_type': float
        }
    ]
    
    print(f"Test data: {test_data}")
    print(f"{'='*80}")
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"Test {i}: {test_case['name']}")
            print(f"Formula: {test_case['formula']}")
            
            result = processor.apply_formula(test_case['formula'], test_data)
            
            print(f"Result: {result}")
            print(f"Type: {type(result)}")
            print(f"Expected Type: {test_case['expected_type']}")
            
            # Verify result type
            if isinstance(result, test_case['expected_type']):
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
            
            print(f"Status: {status}")
            print(f"{'-'*80}")
            
            results.append({
                'test': test_case['name'],
                'formula': test_case['formula'],
                'result': result,
                'status': status
            })
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            print(f"{'-'*80}")
            results.append({
                'test': test_case['name'],
                'formula': test_case['formula'],
                'result': f"ERROR: {e}",
                'status': "❌ ERROR"
            })
    
    # Summary
    print(f"{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    
    passed = sum(1 for r in results if r['status'] == "✅ PASS")
    total = len(results)
    
    for result in results:
        print(f"{result['status']} {result['test']}: {result['result']}")
    
    print(f"{'='*80}")
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced formulas are working correctly.")
    else:
        print("⚠️  Some tests failed. Review the implementation.")
    
    return results

if __name__ == "__main__":
    test_enhanced_formulas()
