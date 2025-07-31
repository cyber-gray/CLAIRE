"""
Checklist Generator Tool for CLAIRE
Creates compliance checklists and evidence tables for audits
"""

from langchain.tools import tool
from datetime import datetime
import os
from typing import Dict, List
import logging

@tool
def generate_compliance_checklist(
    framework: str = "EU AI Act",
    system_type: str = "general",
    risk_level: str = "high"
) -> str:
    """
    Generate a compliance checklist for a specific regulatory framework and AI system.
    
    Args:
        framework: Regulatory framework ("EU AI Act", "NIST AI RMF", "ISO 42001")
        system_type: Type of AI system (e.g., "biometric", "chatbot", "credit_scoring")
        risk_level: Risk level ("critical", "high", "medium", "low")
    
    Returns:
        Formatted compliance checklist with action items and evidence requirements
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate framework-specific checklist
        if framework.upper() == "EU AI ACT":
            checklist = generate_eu_ai_act_checklist(system_type, risk_level)
        elif framework.upper() == "NIST AI RMF":
            checklist = generate_nist_rmf_checklist(system_type, risk_level)
        elif framework.upper() == "ISO 42001":
            checklist = generate_iso_42001_checklist(system_type, risk_level)
        else:
            checklist = generate_general_checklist(system_type, risk_level)
        
        result = f"""# Compliance Checklist: {framework}

**Generated:** {timestamp}  
**System Type:** {system_type}  
**Risk Level:** {risk_level.upper()}  

---

{checklist}

---

## Evidence Collection Guidelines

### Documentation Requirements
- [ ] Maintain detailed records of all compliance activities
- [ ] Document risk assessments and mitigation measures
- [ ] Keep audit trail of system changes and updates
- [ ] Record all human oversight and intervention instances

### Audit Preparation
- [ ] Organize evidence by regulatory requirement
- [ ] Prepare executive summary of compliance status
- [ ] Identify any gaps or areas needing attention
- [ ] Schedule regular compliance reviews

### Export Options
💡 Use `export_checklist()` to generate PDF or Markdown versions for formal documentation.

**⚠️ Disclaimer:** This checklist provides general guidance. Consult legal experts for definitive compliance requirements.
"""
        
        return result
        
    except Exception as e:
        logging.error(f"Error generating checklist: {e}")
        return f"Error generating compliance checklist: {str(e)}"

def generate_eu_ai_act_checklist(system_type: str, risk_level: str) -> str:
    """Generate EU AI Act specific checklist"""
    
    if risk_level.lower() in ["critical", "high"]:
        return """## EU AI Act High-Risk System Requirements

### Article 9 - Risk Management System
- [ ] Establish continuous risk management process
- [ ] Document known and foreseeable risks
- [ ] Implement risk mitigation measures
- [ ] Test risk controls regularly
- [ ] **Evidence:** Risk management documentation, test reports

### Article 10 - Data and Data Governance
- [ ] Assess training data quality and relevance
- [ ] Implement data governance measures
- [ ] Address bias and discrimination risks
- [ ] Document data lineage and provenance
- [ ] **Evidence:** Data quality reports, bias testing results

### Article 11 - Technical Documentation
- [ ] Create comprehensive technical documentation
- [ ] Include system architecture and algorithms
- [ ] Document performance metrics and limitations
- [ ] Maintain version control and change logs
- [ ] **Evidence:** Technical documentation package

### Article 12 - Record-Keeping
- [ ] Implement automatic logging capabilities
- [ ] Record all AI system operations
- [ ] Ensure logs are tamper-proof
- [ ] Retain records for appropriate period
- [ ] **Evidence:** Log samples, retention policies

### Article 13 - Transparency and Information
- [ ] Provide clear user information
- [ ] Ensure instructions are understandable
- [ ] Communicate system capabilities and limitations
- [ ] Include contact information for support
- [ ] **Evidence:** User documentation, training materials

### Article 14 - Human Oversight
- [ ] Design for meaningful human control
- [ ] Enable human intervention capabilities
- [ ] Provide oversight tools and interfaces
- [ ] Train human operators appropriately
- [ ] **Evidence:** Oversight procedures, training records

### Article 15 - Accuracy, Robustness and Cybersecurity
- [ ] Achieve appropriate accuracy levels
- [ ] Test system robustness thoroughly
- [ ] Implement cybersecurity measures
- [ ] Plan for resilience and recovery
- [ ] **Evidence:** Testing reports, security assessments"""
    
    else:
        return """## EU AI Act Limited Risk System Requirements

### Article 50 - Transparency Obligations
- [ ] Inform users of AI system interaction
- [ ] Provide clear and understandable information
- [ ] Enable users to make informed decisions
- [ ] **Evidence:** User interface screenshots, information notices

### General Compliance
- [ ] Monitor for changes in risk classification
- [ ] Stay updated on regulatory guidance
- [ ] Document compliance measures taken
- [ ] **Evidence:** Monitoring logs, compliance documentation"""

def generate_nist_rmf_checklist(system_type: str, risk_level: str) -> str:
    """Generate NIST AI RMF checklist"""
    return """## NIST AI Risk Management Framework

### GOVERN Function
- [ ] **GOVERN-1.1:** Establish AI governance structure
- [ ] **GOVERN-1.2:** Define AI risk tolerance
- [ ] **GOVERN-1.3:** Document AI governance policies
- [ ] **GOVERN-2.1:** Assign AI risk management roles
- [ ] **GOVERN-3.1:** Integrate AI risks into enterprise risk management
- [ ] **Evidence:** Governance documentation, policies, role definitions

### MAP Function
- [ ] **MAP-1.1:** Document AI system context and purpose
- [ ] **MAP-2.1:** Categorize AI system characteristics
- [ ] **MAP-3.1:** Identify AI risks and impacts
- [ ] **MAP-4.1:** Map risks to potential harms
- [ ] **MAP-5.1:** Assess impact of AI system failures
- [ ] **Evidence:** System documentation, risk registers, impact assessments

### MEASURE Function
- [ ] **MEASURE-1.1:** Establish AI system performance metrics
- [ ] **MEASURE-2.1:** Implement bias testing procedures
- [ ] **MEASURE-3.1:** Monitor AI system performance
- [ ] **MEASURE-4.1:** Assess AI system trustworthiness
- [ ] **Evidence:** Performance reports, bias testing results, monitoring dashboards

### MANAGE Function
- [ ] **MANAGE-1.1:** Implement risk response strategies
- [ ] **MANAGE-2.1:** Document risk treatment decisions
- [ ] **MANAGE-3.1:** Establish incident response procedures
- [ ] **MANAGE-4.1:** Monitor risk treatment effectiveness
- [ ] **Evidence:** Risk treatment plans, incident response procedures, monitoring reports"""

def generate_iso_42001_checklist(system_type: str, risk_level: str) -> str:
    """Generate ISO 42001 checklist"""
    return """## ISO 42001 AI Management System

### Clause 4 - Context of the Organization
- [ ] Understand organizational context for AI
- [ ] Identify interested parties and requirements
- [ ] Determine AIMS scope and boundaries
- [ ] **Evidence:** Context analysis, stakeholder mapping

### Clause 5 - Leadership
- [ ] Demonstrate leadership commitment to AI management
- [ ] Establish AI policy and objectives
- [ ] Define roles and responsibilities
- [ ] **Evidence:** AI policy, role definitions, leadership communications

### Clause 6 - Planning
- [ ] Identify AI risks and opportunities
- [ ] Establish AI objectives and planning
- [ ] Plan for achieving AI objectives
- [ ] **Evidence:** Risk assessments, objective planning, action plans

### Clause 7 - Support
- [ ] Determine required resources for AI management
- [ ] Ensure AI competence requirements
- [ ] Establish AI awareness programs
- [ ] Control documented information
- [ ] **Evidence:** Resource allocation, competency records, training materials

### Clause 8 - Operation
- [ ] Plan and control AI operations
- [ ] Implement AI system development lifecycle
- [ ] Manage AI system performance
- [ ] **Evidence:** Operational procedures, lifecycle documentation

### Clause 9 - Performance Evaluation
- [ ] Monitor and measure AI performance
- [ ] Conduct internal audits
- [ ] Perform management reviews
- [ ] **Evidence:** Performance metrics, audit reports, review records

### Clause 10 - Improvement
- [ ] Address nonconformities
- [ ] Implement continual improvement
- [ ] **Evidence:** Corrective action records, improvement plans"""

def generate_general_checklist(system_type: str, risk_level: str) -> str:
    """Generate general AI compliance checklist"""
    return """## General AI System Compliance

### Risk Assessment
- [ ] Conduct comprehensive risk assessment
- [ ] Document potential impacts and harms
- [ ] Identify mitigation strategies
- [ ] **Evidence:** Risk assessment reports

### Documentation
- [ ] Maintain system documentation
- [ ] Document decision-making processes
- [ ] Keep records of system changes
- [ ] **Evidence:** Documentation package

### Testing and Validation
- [ ] Test system performance thoroughly
- [ ] Validate against requirements
- [ ] Document test results
- [ ] **Evidence:** Test reports, validation records

### Monitoring and Maintenance
- [ ] Implement ongoing monitoring
- [ ] Plan for system maintenance
- [ ] Review performance regularly
- [ ] **Evidence:** Monitoring reports, maintenance logs"""

@tool
def export_checklist(checklist_content: str, format: str = "markdown", filename: str = None) -> str:
    """
    Export a compliance checklist to file.
    
    Args:
        checklist_content: The checklist content to export
        format: Export format ("markdown" or "pdf")
        filename: Optional custom filename
    
    Returns:
        Status message with export location
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename is None:
            filename = f"compliance_checklist_{timestamp}"
        
        # Ensure exports directory exists
        exports_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        if format.lower() == "markdown":
            filepath = os.path.join(exports_dir, f"{filename}.md")
            with open(filepath, 'w') as f:
                f.write(checklist_content)
            return f"✅ Checklist exported to: {filepath}"
        
        elif format.lower() == "pdf":
            # For now, create a text file (PDF generation would require additional dependencies)
            filepath = os.path.join(exports_dir, f"{filename}.txt")
            with open(filepath, 'w') as f:
                f.write(checklist_content)
            return f"✅ Checklist exported to: {filepath} (PDF export will be available in future version)"
        
        else:
            return f"❌ Unsupported format: {format}. Use 'markdown' or 'pdf'."
            
    except Exception as e:
        logging.error(f"Error exporting checklist: {e}")
        return f"Error exporting checklist: {str(e)}"

@tool
def list_checklist_templates() -> str:
    """
    List available checklist templates and frameworks.
    
    Returns:
        List of available templates with descriptions
    """
    templates = {
        "EU AI Act": {
            "description": "European Union Artificial Intelligence Act compliance",
            "risk_levels": ["high", "limited", "minimal"],
            "best_for": "EU market deployment, high-risk AI systems"
        },
        "NIST AI RMF": {
            "description": "US National Institute of Standards AI Risk Management Framework",
            "functions": ["GOVERN", "MAP", "MEASURE", "MANAGE"],
            "best_for": "US federal agencies, risk-based approach"
        },
        "ISO 42001": {
            "description": "International AI Management System standard",
            "clauses": ["Context", "Leadership", "Planning", "Support", "Operation", "Performance", "Improvement"],
            "best_for": "Organizational AI governance, international compliance"
        }
    }
    
    result = "Available Compliance Checklist Templates:\n\n"
    
    for framework, details in templates.items():
        result += f"## {framework}\n"
        result += f"**Description:** {details['description']}\n"
        
        if 'risk_levels' in details:
            result += f"**Risk Levels:** {', '.join(details['risk_levels'])}\n"
        if 'functions' in details:
            result += f"**Functions:** {', '.join(details['functions'])}\n"
        if 'clauses' in details:
            result += f"**Clauses:** {', '.join(details['clauses'])}\n"
            
        result += f"**Best For:** {details['best_for']}\n\n"
    
    result += "💡 Use `generate_compliance_checklist(framework='Framework Name')` to create a specific checklist."
    
    return result
