# 🤖 CLAIRE (Compliance & AI Risk Engine)

**CLAIRE** is a voice- and CLI-driven assistant that turns complex AI-governance frameworks into on-demand answers, checklists, and risk scores—right from your terminal or mic.

---

## 🎯 The Problem & Solution

**The Problem:**
Organizations struggle with AI compliance because regulatory frameworks like Canada's AIDA, the EU AI Act, NIST AI RMF, and ISO standards are complex, scattered across hundreds of pages, and constantly evolving. Teams spend weeks manually researching requirements, often missing critical details or misinterpreting technical language, leading to compliance gaps and regulatory risk.

**The Solution:**
CLAIRE transforms this manual, error-prone process into instant, intelligent guidance. Instead of sifting through dense regulatory documents, teams can simply ask questions in natural language and receive precise, cited answers with actionable compliance steps - all while keeping sensitive data completely local and secure.

**Key Use Case:**
A GRC analyst needs to assess if their company's new AI-powered customer service chatbot meets Canadian AIDA requirements. Instead of spending days reading legal documents, they ask CLAIRE: "What are the compliance requirements for a customer service AI system under AIDA?" and instantly receive specific requirements, risk scores, and a ready-to-use compliance checklist.

---

## 🎯 Who CLAIRE Serves

- **GRC/Risk Analysts & Auditors** - Get instant regulatory guidance and generate audit-ready evidence packages
- **AI Product Owners** - Obtain go/no-go guidance with defendable risk scores for AI initiatives
- **Security Operations Teams** - Access hands-free policy lookups during incident triage and compliance reviews

---

## 🛠️ Core Features

### 🔍 **Regulatory Search (`reg_search`)**
- Semantic search over curated AI legal corpus
- Covers Canada's AIDA, EU AI Act, NIST AI RMF, OECD principles, ISO 42001
- Returns cited, traceable answers with source attribution

### ⚖️ **Risk Assessment (`assess_ai_risk`)**
- YAML-driven risk scoring rubric
- Evaluates systems against multiple compliance frameworks
- Generates defendable risk scores with narrative explanations

### ✅ **Checklist Generator (`generate_compliance_checklist`)**
- Creates framework-specific compliance checklists
- Generates audit-ready evidence tables
- Exports to Markdown/PDF for formal documentation

### 🗣️ **Voice Interface**
- Wake word activation: **"Hey CLAIRE"**
- Natural language compliance queries
- Text-to-speech responses for hands-free operation

---

## 🏗️ Technical Architecture

### Local-First Design
- **No data leaves your environment** - All processing happens locally
- **Privacy by design** - Sensitive compliance data stays secure
- **Offline capable** - Works without internet connectivity

### Technology Stack
- **Python 3.12+** - Core application framework
- **LangChain** - Agent orchestration and tool calling
- **Ollama + llama3.2** - Local LLM inference
- **Chroma DB** - Vector database for document embeddings
- **HuggingFace Transformers** - Embedding models
- **PyTTS3** - Text-to-speech synthesis
- **SpeechRecognition** - Voice input processing

---

## ⚡ Quick Start

### Prerequisites
1. **Python 3.12+** installed
2. **Ollama** running locally with `llama3.2:latest` model
3. **Microphone** access for voice features

### Installation
```bash
# Clone the repository
git clone https://github.com/cyber-gray/CLAIRE.git
cd CLAIRE

# Create virtual environment
python -m venv venv-claire
source venv-claire/bin/activate  # On macOS/Linux
# venv-claire\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Start CLAIRE
python main.py
```

### First Interaction
```
🎤 Listening for wake word...
> "Hey CLAIRE"
CLAIRE: Hello, I'm CLAIRE. How can I assist with your compliance needs?
> "What are the notification requirements for AI systems under Canada's AIDA?"
CLAIRE: [Provides detailed regulatory guidance with citations]
```

---

## 🎮 Example Use Cases

### Risk Assessment
```python
# Voice: "CLAIRE, assess the risk of a facial recognition system for employee attendance"
# or direct tool call:
assess_ai_risk(
    system_type="biometric_identification", 
    use_case="employee attendance tracking",
    data_quality="good",
    transparency_level="limited",
    human_oversight="minimal"
)
```

### Regulatory Search
```python
# Voice: "What does the NIST framework say about bias testing?"
# or direct tool call:
reg_search("bias testing NIST AI RMF")
```

### Compliance Checklist
```python
# Voice: "Generate a Canada AIDA checklist for a high-risk automated decision system"
# or direct tool call:
generate_compliance_checklist(
    framework="Canada AIDA",
    system_type="automated_decision_system", 
    risk_level="high"
)
```

---

## 📁 Project Structure

```
CLAIRE/
├── main.py                 # Main voice/CLI interface
├── config/
│   ├── settings.yaml       # Application configuration
│   └── risk_rubric.yaml    # Risk scoring framework
├── tools/                  # Compliance tool implementations
│   ├── reg_search.py       # Regulatory search
│   ├── risk_score.py       # Risk assessment
│   ├── checklist_gen.py    # Checklist generation
│   └── time.py            # Utility functions
├── corpus/                 # AI legal document repository
├── db/                     # Vector database storage
├── exports/               # Generated reports and checklists
└── utils/                 # Supporting utilities
```

---

## 🛠️ Available Tools

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `reg_search()` | Search AI legal corpus | `"Canada AIDA notification requirements"` |
| `list_available_frameworks()` | Show available standards | List all regulatory frameworks |
| `assess_ai_risk()` | Detailed risk assessment | Evaluate specific AI system |
| `quick_risk_check()` | Fast risk screening | Natural language system description |
| `generate_compliance_checklist()` | Create audit checklists | Framework-specific requirements |
| `export_checklist()` | Export documentation | Generate PDF/Markdown reports |
| `list_checklist_templates()` | Show available templates | Available compliance frameworks |

---

## 🎯 Key Differentiators

### ✅ **Local-First Security**
- No cloud dependencies for sensitive compliance data
- Complete control over regulatory information and assessments

### ✅ **Explainable & Auditable**
- Every answer includes source citations
- Full audit trail of risk assessment reasoning
- Transparent scoring methodology

### ✅ **Composable Architecture**
- Risk rubric and corpus are plain YAML/text files
- Easy customization for organization-specific requirements
- Pluggable framework support

### ✅ **Fast Demo Path**
- < 1 day to pilot with sample regulatory documents
- Immediate value with built-in frameworks
- Voice interface for compelling demonstrations

---

## 📈 Business Value

### ⏱️ **Speed**
- Cuts compliance research time from **hours to seconds**
- Instant access to relevant regulatory guidance

### 🎯 **Consistency** 
- Standardized risk scoring across teams and projects
- Eliminates inconsistent compliance interpretations

### �� **Audit Readiness**
- Auto-generated evidence packages with proper citations
- Reduced audit friction through organized documentation

### 👥 **Adoption**
- Natural language interface instead of complex legal documents
- Voice interaction for accessibility and ease of use

---

## 🤝 Contributing

CLAIRE is designed to be extensible and customizable:

1. **Add New Frameworks** - Extend tools with additional standards
2. **Enhance Corpus** - Add regulatory documents to knowledge base
3. **Customize Risk Rubric** - Modify scoring criteria in `config/risk_rubric.yaml`
4. **Create New Tools** - Follow LangChain tool patterns

---

## ⚠️ Important Notes

### Disclaimer
CLAIRE provides guidance based on available regulatory information but should not be considered definitive legal advice. Always consult qualified legal counsel for compliance decisions.

### Data Privacy
CLAIRE processes all data locally by default. No information is sent to external services unless explicitly configured (e.g., OpenAI integration).

### Accuracy
While CLAIRE strives for accuracy, regulatory interpretation can be complex. Users should validate critical compliance decisions with legal experts.

---

## 🔬 Research & Development Notice

**CLAIRE is a research prototype and proof-of-concept project.** This implementation is designed for:

- **Academic research** and experimentation with AI governance frameworks
- **Educational purposes** for understanding compliance automation
- **Technology demonstration** of local-first AI compliance tools
- **Open source collaboration** on regulatory AI challenges

### Not Intended for Production Use

⚠️ **Important**: CLAIRE is **not intended for enterprise or production deployment** without significant additional development, testing, and validation. For production compliance needs, consult qualified legal and technical professionals.

---

**CLAIRE - Making AI compliance accessible, accurate, and actionable through research and innovation.**
