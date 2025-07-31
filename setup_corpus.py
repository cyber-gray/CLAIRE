#!/usr/bin/env python3
"""
CLAIRE Corpus Manager
Tool to help you populate and manage your AI policy document corpus
"""

import os
import shutil
from pathlib import Path
import requests
import zipfile
import tempfile

def create_corpus_directories():
    """Create organized corpus directory structure"""
    corpus_path = Path("./corpus")
    corpus_path.mkdir(exist_ok=True)
    
    # Create subdirectories for different frameworks
    subdirs = [
        "eu_ai_act",
        "nist_ai_rmf", 
        "iso_standards",
        "oecd_principles",
        "ieee_standards",
        "general_ai_policy",
        "custom_policies"
    ]
    
    for subdir in subdirs:
        (corpus_path / subdir).mkdir(exist_ok=True)
    
    print("📁 Created corpus directory structure:")
    for subdir in subdirs:
        print(f"   - corpus/{subdir}/")

def add_sample_documents():
    """Add comprehensive sample documents to corpus"""
    corpus_path = Path("./corpus")
    
    # EU AI Act sample
    eu_ai_act_content = """# EU AI Act - Key Provisions

## Article 5: Prohibited AI Practices

The following artificial intelligence practices shall be prohibited:

1. **Subliminal techniques**: AI systems that deploy subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques to distort a person's behaviour where such techniques are likely to cause that person or another person physical or psychological harm.

2. **Exploitation of vulnerabilities**: AI systems that exploit any of the vulnerabilities of a specific group of persons due to their age, physical or mental disability, in order to distort their behaviour where such techniques are likely to cause that person or another person physical or psychological harm.

3. **Social scoring**: AI systems that evaluate or classify individuals based on their social behaviour or known, inferred or predicted personal characteristics, with the social score leading to either or both of the following:
   - Detrimental or unfavourable treatment of certain natural persons or whole groups in social contexts which are unrelated to the contexts in which the data was originally generated
   - Detrimental or unfavourable treatment that is unjustified or disproportionate to their social behaviour

4. **Real-time remote biometric identification**: The use of real-time remote biometric identification systems in publicly accessible spaces for the purpose of law enforcement, unless and in as far as such use is strictly necessary for specific purposes.

## Article 6: Classification Rules for High-Risk AI Systems

1. Irrespective of whether an AI system is placed on the market or put into service independently from the products listed in points (a) and (b), that AI system shall be considered high-risk where both of the following conditions are fulfilled:
   - The AI system is intended to be used as a safety component of a product, or the AI system is itself a product, covered by the Union harmonisation legislation listed in Annex II
   - The product whose safety component pursuant to point (a) is the AI system, or the AI system itself as a product, is subject to a third-party conformity assessment with a view to placing that product on the market or putting it into service

2. AI systems referred to in Annex III shall be considered high-risk.

## Article 9: Risk Management System

1. A risk management system shall be established, implemented, documented and maintained in relation to high-risk AI systems.

2. The risk management system shall be understood as a continuous iterative process planned and run throughout the entire lifecycle of a high-risk AI system, requiring regular systematic updating.

3. The risk management system shall comprise the following steps:
   - Identification and analysis of the known and the reasonably foreseeable risks associated with each high-risk AI system
   - Estimation and evaluation of the risks that may emerge when the high-risk AI system is used in accordance with its intended purpose
   - Evaluation of other risks that may emerge based on the analysis of data gathered from the post-market monitoring system
   - Adoption of appropriate and targeted risk management measures

## Article 10: Data and Data Governance

1. High-risk AI systems which make use of techniques involving the training of models with data shall be developed on the basis of training, validation and testing data sets that meet the quality criteria referred to in paragraphs 2 to 5.

2. Training, validation and testing data sets shall be subject to appropriate data governance and management practices including:
   - Relevant design choices
   - Data collection processes and the origin of data
   - Relevant data preparation processing operations
   - Formulation of relevant assumptions
   - Assessment of the availability, quantity and suitability of the data sets
   - Examination for possible biases

## Article 13: Transparency and Provision of Information to Deployers

1. High-risk AI systems shall be designed and developed in such a way to ensure that their operation is sufficiently transparent to enable deployers to interpret the system's output and use it appropriately.

2. High-risk AI systems shall be accompanied by instructions for use in an appropriate digital format or otherwise that include concise, complete, correct and clear information that is relevant, accessible and comprehensible to deployers.

## Article 14: Human Oversight

1. High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which the AI system is in use.

2. Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental rights that may emerge when a high-risk AI system is used in accordance with its intended purpose or under conditions of reasonably foreseeable misuse.

3. Human oversight shall be ensured through either one or all of the following measures:
   - Fully understand the capacities and limitations of the high-risk AI system
   - Remain aware of the possible tendency of automatically relying or over-relying on the output produced by a high-risk AI system
   - Correctly interpret the high-risk AI system's output
   - Decide not to use the high-risk AI system or otherwise disregard, override or reverse the output of the high-risk AI system
   - Intervene on the operation of the high-risk AI system or interrupt the system

Citation: Regulation (EU) 2024/1689 of the European Parliament and of the Council on artificial intelligence"""

    # NIST AI RMF sample
    nist_ai_rmf_content = """# NIST AI Risk Management Framework (AI RMF 1.0)

## Overview

The NIST AI RMF is organized around four core functions: GOVERN, MAP, MEASURE, and MANAGE. These functions are not meant to be executed in a particular order, and organizations may find benefit in executing them concurrently.

## GOVERN

Establishes and implements robust governance to manage AI risks

### GOVERN-1: Policies, processes, procedures, and practices are in place to address risks related to AI systems and their components throughout the AI lifecycle

- **GOVERN-1.1**: Legal and regulatory requirements involving AI are understood and managed
- **GOVERN-1.2**: The risk tolerance of the organization and key stakeholders is determined, clearly communicated, and integrated into AI risk management processes
- **GOVERN-1.3**: Roles and responsibilities and lines of communication related to AI risk management are clearly defined, including those responsible for different steps in AI system development and deployment

### GOVERN-2: Accountability structures are in place so that the appropriate teams and individuals are empowered, responsible, and trained for mapping, measuring, and managing AI risks

- **GOVERN-2.1**: Roles and responsibilities and lines of communication related to AI risk management are clearly defined
- **GOVERN-2.2**: Accountability and approval processes are defined

### GOVERN-3: Workforce diversity, equity, inclusion, and accessibility processes are prioritized in the mapping, measuring, and managing of AI risks throughout the AI lifecycle

- **GOVERN-3.1**: Organizational teams document the intended purposes and business value of AI systems
- **GOVERN-3.2**: Organizational teams consider the broader system and societal impacts

## MAP

Establishes the context to frame risks for AI systems

### MAP-1: The context and purpose of the AI system is documented

- **MAP-1.1**: Intended purposes, potentially beneficial uses, context-specific laws and regulations, and organizational risk tolerance are understood and documented
- **MAP-1.2**: Interdisciplinary AI actors, users, and others who may be impacted by the AI system are identified
- **MAP-1.3**: AI system categorization based on organizational risk tolerance is understood and documented

### MAP-2: AI system categorization and characteristics are defined and understood

- **MAP-2.1**: AI system components, behaviors, capabilities, and limitations are defined and documented
- **MAP-2.2**: The AI lifecycle, application context, and organizational oversight is documented

### MAP-3: Potential impacts of AI systems are characterized

- **MAP-3.1**: Potential positive and negative impacts of the AI system are identified and documented
- **MAP-3.2**: Practices and personnel for supporting regular engagement and feedback from AI actors are documented

## MEASURE

Establishes how identified AI risks will be analyzed and assessed

### MEASURE-1: Appropriate methods and metrics for evaluating and monitoring AI risk management are identified and implemented

- **MEASURE-1.1**: Appropriate AI risk measurement is established contextually based on organizational risk tolerance
- **MEASURE-1.2**: AI risk measurement is planned to be performed regularly

### MEASURE-2: AI risks and benefits are measured or estimated quantitatively or qualitatively and documented

- **MEASURE-2.1**: Test datasets are representative of deployment setting and robust to deployment distribution shift
- **MEASURE-2.2**: Evaluations involving human subjects meet applicable requirements and are representative of the relevant population
- **MEASURE-2.3**: AI system performance is measured regularly using appropriate evaluation metrics

### MEASURE-3: AI system trustworthiness characteristics are measured or estimated quantitatively or qualitatively and documented

- **MEASURE-3.1**: AI system performance is measured using representatively sampled datasets
- **MEASURE-3.2**: Measurement results regarding AI system trustworthiness characteristics are shared with relevant AI actors

## MANAGE

Establishes processes and practices for responding to and recovering from AI incidents

### MANAGE-1: A framework is in place to regularly monitor and manage AI risks

- **MANAGE-1.1**: A manual or automated system is in place to regularly monitor the AI system
- **MANAGE-1.2**: Procedures are followed to respond to identified risks
- **MANAGE-1.3**: Response plan adequacy is verified through regular testing

### MANAGE-2: Mechanisms are in place to enable AI actors to regularly incorporate adjudication results and other feedback from monitoring into system updates

- **MANAGE-2.1**: Resources are allocated for the regular monitoring of AI system performance
- **MANAGE-2.2**: AI system performance is regularly monitored and verified based on the organization's risk tolerance

### MANAGE-3: AI risks and related impacts are documented and monitored regularly

- **MANAGE-3.1**: Responses to the AI risks deemed high priority by the organization are developed
- **MANAGE-3.2**: Mechanisms are implemented to track the effectiveness of AI risk responses

Source: NIST AI Risk Management Framework (AI RMF 1.0), January 2023"""

    # ISO 42001 sample
    iso_42001_content = """# ISO/IEC 42001:2023 - Artificial Intelligence Management System

## 1. Scope

This document specifies requirements for establishing, implementing, maintaining and continually improving an artificial intelligence management system (AIMS) within the context of an organization.

## 4. Context of the Organization

### 4.1 Understanding the organization and its context

The organization shall determine external and internal issues that are relevant to its purpose and that affect its ability to achieve the intended outcome(s) of its AIMS.

### 4.2 Understanding the needs and expectations of interested parties

The organization shall determine:
- The interested parties that are relevant to the AIMS
- The requirements of these interested parties relevant to the AIMS

### 4.3 Determining the scope of the AIMS

The organization shall determine the boundaries and applicability of the AIMS to establish its scope.

### 4.4 AIMS

The organization shall establish, implement, maintain and continually improve an AIMS, including the processes needed and their interactions.

## 5. Leadership

### 5.1 Leadership and commitment

Top management shall demonstrate leadership and commitment with respect to the AIMS.

### 5.2 AI policy

Top management shall establish, implement and maintain an AI policy that:
- Is appropriate to the purpose and context of the organization
- Provides a framework for setting AI objectives
- Includes a commitment to satisfy applicable requirements
- Includes a commitment to continual improvement of the AIMS

### 5.3 Organizational roles, responsibilities and authorities

Top management shall ensure that the responsibilities and authorities for relevant roles are assigned and communicated within the organization.

## 6. Planning

### 6.1 Actions to address risks and opportunities

When planning for the AIMS, the organization shall consider the issues referred to in 4.1 and the requirements referred to in 4.2.

### 6.2 AI objectives and planning to achieve them

The organization shall establish AI objectives at relevant functions and levels.

### 6.3 Planning of changes

When the organization determines the need for changes to the AIMS, the changes shall be carried out in a planned manner.

## 7. Support

### 7.1 Resources

The organization shall determine and provide the resources needed for the establishment, implementation, maintenance and continual improvement of the AIMS.

### 7.2 Competence

The organization shall:
- Determine the necessary competence of person(s) doing work under its control that affects the performance and effectiveness of the AIMS
- Ensure that these persons are competent on the basis of appropriate education, training, or experience

### 7.3 Awareness

The organization shall ensure that persons doing work under the organization's control are aware of:
- The AI policy
- The relevant AI objectives
- Their contribution to the effectiveness of the AIMS

## 8. Operation

### 8.1 Operational planning and control

The organization shall plan, implement and control the processes needed to meet requirements and to implement the actions determined in Clause 6.

### 8.2 AI system development lifecycle

The organization shall manage AI systems throughout their lifecycle using a defined AI system development lifecycle process.

### 8.3 Data management

The organization shall establish and maintain processes for data management that support the AI system lifecycle.

## 9. Performance evaluation

### 9.1 Monitoring, measurement, analysis and evaluation

The organization shall determine:
- What needs to be monitored and measured
- The methods for monitoring, measurement, analysis and evaluation
- When the monitoring and measuring shall be performed
- When the results from monitoring and measurement shall be analyzed and evaluated

### 9.2 Internal audit

The organization shall conduct internal audits at planned intervals to provide information on whether the AIMS conforms to the organization's own requirements for its AIMS and the requirements of this document.

### 9.3 Management review

Top management shall review the organization's AIMS at planned intervals, to ensure its continuing suitability, adequacy, effectiveness and alignment with the strategic direction of the organization.

## 10. Improvement

### 10.1 General

The organization shall determine and select opportunities for improvement and implement any necessary actions to meet customer requirements and enhance customer satisfaction.

### 10.2 Nonconformity and corrective action

When a nonconformity occurs, the organization shall react to the nonconformity and take action to control and correct it.

### 10.3 Continual improvement

The organization shall continually improve the suitability, adequacy and effectiveness of the AIMS.

Source: ISO/IEC 42001:2023 - Information technology — Artificial intelligence — Management system"""

    # Write sample documents
    samples = {
        "eu_ai_act/eu_ai_act_key_provisions.md": eu_ai_act_content,
        "nist_ai_rmf/nist_ai_rmf_overview.md": nist_ai_rmf_content,
        "iso_standards/iso_42001_requirements.md": iso_42001_content
    }
    
    for file_path, content in samples.items():
        full_path = corpus_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not full_path.exists():
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {file_path}")
        else:
            print(f"📄 Already exists: {file_path}")

def create_readme():
    """Create a README for the corpus directory"""
    readme_content = """# CLAIRE AI Policy Corpus

This directory contains AI governance and compliance documents that CLAIRE uses to provide regulatory guidance.

## Directory Structure

- **eu_ai_act/**: European Union AI Act documents
- **nist_ai_rmf/**: NIST AI Risk Management Framework documents  
- **iso_standards/**: ISO standards related to AI (42001, etc.)
- **oecd_principles/**: OECD AI Principles documents
- **ieee_standards/**: IEEE standards for AI systems
- **general_ai_policy/**: General AI policy documents
- **custom_policies/**: Your organization's custom AI policies

## Supported File Formats

- PDF files (.pdf)
- Text files (.txt)
- Markdown files (.md)
- Word documents (.docx)

## Adding Documents

1. **Download official documents** from regulatory bodies:
   - EU AI Act: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
   - NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
   - ISO 42001: Available through ISO standards portal

2. **Place files in appropriate subdirectories**

3. **Run corpus initialization**:
   ```bash
   python setup_claire.py
   ```

## Document Sources

### EU AI Act
- Official Regulation (EU) 2024/1689
- Implementation guidelines
- Sector-specific guidance

### NIST AI RMF
- AI RMF 1.0 Core document
- Implementation guidance
- Sector-specific profiles

### ISO Standards
- ISO/IEC 42001:2023 (AI Management Systems)
- ISO/IEC 23053:2022 (AI Risk Framework)
- ISO/IEC 29119-11:2022 (AI Testing)

### Best Practices

1. **Use official sources** whenever possible
2. **Keep documents current** - AI regulations evolve rapidly
3. **Organize by framework** - Use the provided directory structure
4. **Document provenance** - Note source URLs and dates in filenames

## Privacy & Security

All documents are processed locally. No data is sent to external services unless explicitly configured (e.g., cloud LLM providers).

## Need Help?

Run `python setup_claire.py` to initialize or reinitialize the corpus with sample documents.
"""
    
    with open("corpus/README.md", 'w') as f:
        f.write(readme_content)
    print("✅ Created corpus/README.md")

def main():
    """Main function to set up corpus"""
    print("🎯 CLAIRE Corpus Manager")
    print("=" * 50)
    
    # Create directory structure
    create_corpus_directories()
    print()
    
    # Add sample documents  
    print("📝 Adding sample documents...")
    add_sample_documents()
    print()
    
    # Create README
    create_readme()
    print()
    
    print("🎉 Corpus setup complete!")
    print("\n📋 Next Steps:")
    print("1. Add your AI policy documents to the corpus/ subdirectories")
    print("2. Run 'python setup_claire.py' to initialize the vector database")
    print("3. Start CLAIRE with 'python main.py'")
    print("\n💡 Recommended documents to add:")
    print("- Full EU AI Act PDF")
    print("- Complete NIST AI RMF documents")
    print("- ISO 42001 standard")
    print("- Your organization's AI policies")

if __name__ == "__main__":
    main()
