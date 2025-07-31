"""
Risk Scoring Tool for CLAIRE
Evaluates AI systems against compliance risk criteria
"""

from langchain.tools import tool
import yaml
import os
from typing import Dict, Any
import logging

def load_risk_rubric() -> Dict[str, Any]:
    """Load the risk assessment rubric from YAML configuration"""
    try:
        rubric_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'risk_rubric.yaml')
        with open(rubric_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading risk rubric: {e}")
        return {}

@tool
def assess_ai_risk(
    system_type: str,
    use_case: str, 
    data_quality: str = "unknown",
    transparency_level: str = "unknown",
    human_oversight: str = "unknown"
) -> str:
    """
    Assess compliance risk for an AI system based on key characteristics.
    
    Args:
        system_type: Type of AI system (e.g., "biometric_identification", "chatbot", "credit_scoring")
        use_case: Specific use case description
        data_quality: Data governance level ("poor", "fair", "good", "excellent", "unknown") 
        transparency_level: Model transparency ("black_box", "limited", "moderate", "high", "unknown")
        human_oversight: Level of human control ("none", "minimal", "moderate", "full", "unknown")
    
    Returns:
        Detailed risk assessment with score and recommendations
    """
    try:
        rubric = load_risk_rubric()
        if not rubric:
            return "Error: Could not load risk assessment rubric. Please check configuration."
        
        # Calculate risk score based on rubric
        total_score = 0
        category_scores = {}
        risk_factors = []
        
        # 1. AI System Risk Level (25% weight)
        system_risk_score = classify_system_risk(system_type, rubric)
        category_scores["AI System Classification"] = system_risk_score
        total_score += system_risk_score * 0.25
        
        # 2. Data Governance (20% weight) 
        if data_quality != "unknown":
            data_score = get_data_governance_score(data_quality, rubric)
            category_scores["Data Governance"] = data_score
            total_score += data_score * 0.20
        else:
            category_scores["Data Governance"] = "Not assessed"
            
        # 3. Transparency (15% weight)
        if transparency_level != "unknown":
            transparency_score = get_transparency_score(transparency_level, rubric)
            category_scores["Transparency"] = transparency_score
            total_score += transparency_score * 0.15
        else:
            category_scores["Transparency"] = "Not assessed"
            
        # 4. Human Oversight (15% weight)
        if human_oversight != "unknown":
            oversight_score = get_oversight_score(human_oversight, rubric)
            category_scores["Human Oversight"] = oversight_score
            total_score += oversight_score * 0.15
        else:
            category_scores["Human Oversight"] = "Not assessed"
        
        # Default scores for unassessed categories
        category_scores["Security & Robustness"] = "Not assessed (assumes medium risk)"
        category_scores["Impact Scope"] = "Not assessed (assumes medium risk)"
        total_score += 50 * 0.15  # Security default
        total_score += 50 * 0.10  # Impact default
        
        # Determine risk level
        risk_level = determine_risk_level(total_score, rubric)
        
        # Generate recommendations
        recommendations = get_recommendations(risk_level, rubric)
        
        # Format output
        result = f"""## AI System Risk Assessment

**System:** {system_type}
**Use Case:** {use_case}
**Overall Risk Score:** {total_score:.0f}/100 ({risk_level.upper()})

### Category Breakdown:
"""
        for category, score in category_scores.items():
            if isinstance(score, (int, float)):
                result += f"• {category}: {score:.0f}/100\n"
            else:
                result += f"• {category}: {score}\n"
        
        result += f"""
### Key Risk Factors:
{get_risk_factors(system_type, total_score)}

### Recommended Actions:
{chr(10).join(f'• {rec}' for rec in recommendations)}

### Regulatory Framework Alignment:
{get_framework_alignment(system_type, total_score)}

⚠️ **Disclaimer:** This is an automated assessment. Consult legal counsel for definitive compliance guidance.
"""
        
        return result
        
    except Exception as e:
        logging.error(f"Error in assess_ai_risk: {e}")
        return f"Error performing risk assessment: {str(e)}"

def classify_system_risk(system_type: str, rubric: Dict) -> int:
    """Classify AI system risk level based on type"""
    system_type_lower = system_type.lower()
    
    # Check against rubric categories
    risk_categories = rubric.get('risk_categories', {}).get('ai_system_risk_level', {}).get('criteria', {})
    
    for level, data in risk_categories.items():
        examples = data.get('examples', [])
        if any(example in system_type_lower for example in examples):
            return data.get('score', 50)
    
    # Default to limited risk if not found
    return 40

def get_data_governance_score(quality: str, rubric: Dict) -> int:
    """Get data governance risk score"""
    mapping = {"excellent": 10, "good": 30, "fair": 60, "poor": 80}
    return mapping.get(quality, 50)

def get_transparency_score(level: str, rubric: Dict) -> int:
    """Get transparency risk score"""
    mapping = {"high": 20, "moderate": 40, "limited": 60, "black_box": 90}
    return mapping.get(level, 50)

def get_oversight_score(oversight: str, rubric: Dict) -> int:
    """Get human oversight risk score"""
    mapping = {"full": 15, "moderate": 40, "minimal": 70, "none": 95}
    return mapping.get(oversight, 50)

def determine_risk_level(score: float, rubric: Dict) -> str:
    """Determine risk level based on score"""
    thresholds = rubric.get('risk_thresholds', {})
    if score >= thresholds.get('critical', 80):
        return "critical"
    elif score >= thresholds.get('high', 60):
        return "high" 
    elif score >= thresholds.get('medium', 40):
        return "medium"
    elif score >= thresholds.get('low', 25):
        return "low"
    else:
        return "minimal"

def get_recommendations(risk_level: str, rubric: Dict) -> list:
    """Get recommendations based on risk level"""
    recs = rubric.get('recommendations', {})
    return recs.get(risk_level, ["Consult compliance team for guidance"])

def get_risk_factors(system_type: str, score: float) -> str:
    """Generate risk factors based on system characteristics"""
    factors = []
    
    if score >= 80:
        factors.append("High regulatory scrutiny expected")
        factors.append("Potential for significant penalties if non-compliant")
    
    if "biometric" in system_type.lower():
        factors.append("Subject to strict EU AI Act prohibitions/restrictions")
    
    if any(term in system_type.lower() for term in ["employment", "credit", "healthcare"]):
        factors.append("Impacts fundamental rights and opportunities")
    
    if not factors:
        factors.append("Standard compliance monitoring recommended")
    
    return "\n".join(f"• {factor}" for factor in factors)

def get_framework_alignment(system_type: str, score: float) -> str:
    """Get framework-specific guidance"""
    alignment = []
    
    if score >= 60:
        alignment.append("**EU AI Act:** Likely high-risk system requiring conformity assessment")
        alignment.append("**NIST AI RMF:** Comprehensive GOVERN and MANAGE controls needed")
    else:
        alignment.append("**EU AI Act:** May qualify for limited risk transparency obligations")
        alignment.append("**NIST AI RMF:** Standard risk management practices recommended")
    
    return "\n".join(alignment)

@tool
def quick_risk_check(system_description: str) -> str:
    """
    Perform a quick risk assessment based on a natural language description.
    
    Args:
        system_description: Natural language description of the AI system
    
    Returns:
        Quick risk assessment and guidance
    """
    description_lower = system_description.lower()
    
    # High-risk indicators
    high_risk_terms = [
        "biometric", "facial recognition", "credit scoring", "hiring", "employment", 
        "medical diagnosis", "criminal justice", "law enforcement", "autonomous vehicle",
        "critical infrastructure", "border control"
    ]
    
    # Prohibited indicators
    prohibited_terms = [
        "social scoring", "manipulation", "subliminal", "dark pattern", 
        "exploitation", "vulnerable groups"
    ]
    
    risk_score = 20  # Base score
    risk_factors = []
    
    # Check for prohibited uses
    for term in prohibited_terms:
        if term in description_lower:
            risk_score = 100
            risk_factors.append(f"Potentially prohibited use detected: {term}")
    
    # Check for high-risk applications
    if risk_score < 100:
        for term in high_risk_terms:
            if term in description_lower:
                risk_score = max(risk_score, 80)
                risk_factors.append(f"High-risk application detected: {term}")
    
    # Determine level
    if risk_score >= 80:
        level = "HIGH/CRITICAL"
        action = "Immediate legal review required before proceeding"
    elif risk_score >= 40:
        level = "MEDIUM"
        action = "Detailed compliance assessment recommended"
    else:
        level = "LOW"
        action = "Standard monitoring practices sufficient"
    
    result = f"""## Quick Risk Assessment

**System Description:** {system_description}
**Estimated Risk Level:** {level} ({risk_score}/100)

**Key Findings:**
{chr(10).join(f'• {factor}' for factor in risk_factors) if risk_factors else '• No obvious high-risk indicators detected'}

**Immediate Action:** {action}

💡 **Next Step:** Use assess_ai_risk() for detailed analysis with specific parameters.
"""
    
    return result
