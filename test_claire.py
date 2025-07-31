#!/usr/bin/env python3
"""
Simple CLAIRE test script to demonstrate compliance tools
"""

import sys
import os
sys.path.append('.')

def test_claire_tools():
    """Test CLAIRE's compliance tools"""
    
    print("🎯 CLAIRE (Compliance & Legal AI Risk Engine) - Tool Test")
    print("=" * 60)
    
    try:
        # Test 1: Time Tool
        print("\n1️⃣ Testing Time Tool:")
        from tools.time import get_time
        time_result = get_time.invoke({'format': 'detailed'})
        print(f"   ✅ {time_result}")
        
        # Test 2: Risk Assessment
        print("\n2️⃣ Testing Risk Assessment:")
        from tools.risk_score import assess_ai_risk
        risk_result = assess_ai_risk.invoke({
            'system_type': 'facial_recognition',
            'use_case': 'employee_attendance_tracking',
            'data_quality': 'good',
            'transparency_level': 'limited',
            'human_oversight': 'minimal'
        })
        print("   ✅ Risk Assessment Complete:")
        print("   " + "\n   ".join(risk_result.split('\n')[:8]))
        
        # Test 3: Compliance Checklist
        print("\n3️⃣ Testing Compliance Checklist:")
        from tools.checklist_gen import generate_compliance_checklist
        checklist_result = generate_compliance_checklist.invoke({
            'framework': 'EU AI Act',
            'system_type': 'biometric_identification',
            'risk_level': 'high'
        })
        print("   ✅ Checklist Generated:")
        print("   " + "\n   ".join(checklist_result.split('\n')[:6]))
        
        # Test 4: Regulatory Search
        print("\n4️⃣ Testing Regulatory Search:")
        from tools.reg_search import reg_search
        search_result = reg_search.invoke({'query': 'high-risk AI systems'})
        print("   ✅ Search Complete:")
        print(f"   {search_result}")
        
        # Test 5: List Available Frameworks
        print("\n5️⃣ Testing Framework List:")
        from tools.reg_search import list_available_frameworks
        frameworks_result = list_available_frameworks.invoke({})
        print("   ✅ Available Frameworks:")
        print(f"   {frameworks_result}")
        
        print("\n" + "=" * 60)
        print("🎉 ALL CLAIRE TOOLS TESTED SUCCESSFULLY!")
        print("🚀 CLAIRE is ready for compliance automation!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_claire_tools()
