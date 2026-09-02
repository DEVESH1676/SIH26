"""
MoSPI Competency Framework v1.0
Comprehensive competency definitions for India's Official Statistical System.
Maps to NSSTA job roles, iGOT course categories, and assessment criteria.
"""


# ── Domain Definitions ──────────────────────────────────────

STATISTICAL_COMPETENCIES = {
    "survey_design": {
        "id": "STAT-001",
        "name": "Survey Design & Methodology",
        "description": "Designing effective surveys and data collection instruments",
        "sub_competencies": [
            "Survey planning and objective setting",
            "Questionnaire development and validation",
            "Pilot testing and pre-testing",
            "Multi-stage sampling design",
            "Mixed-methods research design",
        ],
        "difficulty_levels": {
            "beginner": ["Basic survey principles", "Questionnaire formatting", "Data collection ethics"],
            "intermediate": ["Sampling frame development", "Stratified sampling", "Pilot testing design", "Response rate optimization"],
            "advanced": ["Complex multi-stage sampling", "Adaptive survey design", "Mixed-methods integration", "Survey quality assurance"],
        },
    },
    "sampling": {
        "id": "STAT-002",
        "name": "Sampling Techniques",
        "description": "Statistical sampling methods for representative data collection",
        "sub_competencies": [
            "Probability sampling methods",
            "Non-probability sampling methods",
            "Sample size determination",
            "Sampling error calculation",
        ],
        "difficulty_levels": {
            "beginner": ["Simple random sampling", "Systematic sampling", "Understanding sampling error"],
            "intermediate": ["Stratified sampling", "Cluster sampling", "Sample size calculation", "Weighting techniques"],
            "advanced": ["Multistage complex sampling", "PPS sampling", "Small area estimation", "Design-based inference"],
        },
    },
    "national_accounts": {
        "id": "STAT-003",
        "name": "National Accounts Statistics",
        "description": "National income, GDP calculation, and economic accounting",
        "sub_competencies": ["SNA 2008 framework", "GDP calculation methods", "Input-output tables", "Balance of payments"],
        "difficulty_levels": {
            "beginner": ["Concepts of GDP, GNP, NNP", "Basic national accounts framework"],
            "intermediate": ["Production approach to GDP", "Income approach", "Expenditure approach"],
            "advanced": ["SNA 2008 implementation", "Satellite accounts", "Environmental accounting integration"],
        },
    },
    "price_statistics": {
        "id": "STAT-004",
        "name": "Price Statistics",
        "description": "CPI, WPI, deflator calculation and analysis",
        "sub_competencies": ["CPI methodology", "WPI calculation", "Price index aggregation", "Deflator computation"],
        "difficulty_levels": {
            "beginner": ["Concepts of price indices", "CPI vs WPI differences"],
            "intermediate": ["CPI calculation methodology", "Base year revision", "Weight allocation"],
            "advanced": ["Chain-weighted indices", "Hedonic price adjustment", "Quality adjustment methods"],
        },
    },
    "labour_statistics": {
        "id": "STAT-005",
        "name": "Labour Statistics",
        "description": "Employment, unemployment, and workforce data",
        "sub_competencies": ["Labour force survey design", "Employment/unemployment calculation", "ILO standards compliance", "Wage statistics"],
        "difficulty_levels": {
            "beginner": ["Labour force concepts", "Unemployment types", "LFPR calculation"],
            "intermediate": ["NSSO survey methodology", "Employment status classification", "Informal sector measurement"],
            "advanced": ["Gender-disaggregated labour statistics", "Time-use surveys", "Decent work indicators"],
        },
    },
    "agricultural_statistics": {
        "id": "STAT-006",
        "name": "Agricultural Statistics",
        "description": "Crop estimation, yield survey, and agricultural data",
        "sub_competencies": ["Crop estimation methodology", "Yield survey design", "Agricultural census", "Farm management costs"],
        "difficulty_levels": {
            "beginner": ["Agricultural survey basics", "Crop season concepts"],
            "intermediate": ["Area estimation techniques", "Yield survey methodology", "Post-harvey loss estimation"],
            "advanced": ["Remote sensing integration", "Model-based estimation", "Small area agricultural estimation"],
        },
    },
    "industrial_statistics": {
        "id": "STAT-007",
        "name": "Industrial Statistics",
        "description": "Industrial production, IIP, and factory statistics",
        "sub_competencies": ["IIP calculation", "Industrial classification (NIC)", "Factory survey design", "Service sector statistics"],
        "difficulty_levels": {
            "beginner": ["Index of Industrial Production concepts", "NIC classification basics"],
            "intermediate": ["IIP weight calculation", "Base year revision", "Quarterly industrial data compilation"],
            "advanced": ["Input-output analysis", "Supply-use tables", "Digital economy measurement"],
        },
    },
    "sdg_indicators": {
        "id": "STAT-008",
        "name": "SDG Indicators",
        "description": "Measuring and reporting on Sustainable Development Goals",
        "sub_competencies": ["SDG indicator framework", "National SDG reporting", "Data gap analysis", "SDG mapping"],
        "difficulty_levels": {
            "beginner": ["SDG framework overview", "India's SDG Index"],
            "intermediate": ["SDG indicator methodology", "Data compilation for SDGs", "Disaggregation principles"],
            "advanced": ["Multi-dimensional poverty measurement", "SDG stress testing", "Integrated national financing frameworks"],
        },
    },
    "metadata_standards": {
        "id": "STAT-009",
        "name": "Metadata Standards",
        "description": "Statistical metadata management and documentation",
        "sub_competencies": ["SDMX standards", "Statistical metadata concepts", "Data quality reporting"],
        "difficulty_levels": {
            "beginner": ["What is metadata", "Metadata importance in statistics"],
            "intermediate": ["SDMX implementation", "Core metadata registration"],
            "advanced": ["Metadata workflow automation", "Cross-border metadata exchange"],
        },
    },
    "data_quality_frameworks": {
        "id": "STAT-010",
        "name": "Data Quality Frameworks",
        "description": "Assessing and improving statistical data quality",
        "sub_competencies": ["DQAF implementation", "Data quality assessment", "Error analysis", "Quality reporting"],
        "difficulty_levels": {
            "beginner": ["Data quality dimensions", "Common data quality issues"],
            "intermediate": ["IMF DQAF implementation", "Data quality assessment methodology"],
            "advanced": ["Quality management systems", "Continuous quality improvement"],
        },
    },
}

TECHNICAL_COMPETENCIES = {
    "python": {
        "id": "TECH-001",
        "name": "Python for Data Analysis",
        "description": "Python programming for statistical analysis and automation",
        "sub_competencies": ["Python fundamentals", "NumPy/Pandas", "Data visualization with Matplotlib/Seaborn", "Statistical analysis with SciPy"],
        "difficulty_levels": {
            "beginner": ["Python syntax and data types", "Loops and functions", "Basic data manipulation"],
            "intermediate": ["Pandas for data analysis", "Data cleaning and preprocessing", "Basic visualization", "File I/O operations"],
            "advanced": ["Advanced Pandas (merge, groupby, pivot)", "Statistical modeling with SciPy/Statsmodels", "Automation scripts", "API integration"],
        },
    },
    "r": {
        "id": "TECH-002",
        "name": "R Programming",
        "description": "R for statistical computing and graphics",
        "sub_competencies": ["R basics", "Tidyverse", "Statistical modeling", "Reproducible reports"],
        "difficulty_levels": {
            "beginner": ["R syntax and data types", "Data frames", "Basic plotting"],
            "intermediate": ["dplyr and tidyr for data manipulation", "ggplot2 visualization", "Basic statistical tests"],
            "advanced": ["Advanced modeling with lme4/glmm", "Reproducible research with R Markdown", "Package development"],
        },
    },
    "sql": {
        "id": "TECH-003",
        "name": "SQL & Database Management",
        "description": "Database querying and management for statistical data",
        "sub_competencies": ["SQL fundamentals", "Query optimization", "Database design", "Data extraction"],
        "difficulty_levels": {
            "beginner": ["SELECT queries", "WHERE and ORDER BY", "Basic JOINs"],
            "intermediate": ["Subqueries", "Aggregate functions", "Window functions", "Database normalization"],
            "advanced": ["Query optimization", "Stored procedures", "Database administration basics"],
        },
    },
    "stata": {
        "id": "TECH-004",
        "name": "Stata",
        "description": "Statistical analysis with Stata for survey data",
        "sub_competencies": ["Stata basics", "Survey data analysis", "Weighted estimation", "Survey commands"],
        "difficulty_levels": {
            "beginner": ["Stata interface", "Basic commands", "Data import/export"],
            "intermediate": ["Survey command suite (svy:)", "Weighted analysis", "Complex survey design"],
            "advanced": ["Advanced survey estimation", "Bootstrap and jackknife", "Custom Stata programs"],
        },
    },
    "spss": {
        "id": "TECH-005",
        "name": "SPSS",
        "description": "Statistical Package for Social Sciences",
        "sub_competencies": ["SPSS basics", "Data management", "Statistical tests", "Syntax programming"],
        "difficulty_levels": {
            "beginner": ["SPSS interface", "Data entry and coding", "Descriptive statistics"],
            "intermediate": ["T-tests, ANOVA, chi-square", "Regression analysis", "Data transformation"],
            "advanced": ["SPSS syntax programming", "Macro creation", "Advanced statistical procedures"],
        },
    },
    "sas": {
        "id": "TECH-006",
        "name": "SAS",
        "description": "Statistical Analysis System for large-scale data processing",
        "sub_competencies": ["SAS fundamentals", "Data manipulation", "PROC procedures", "Macro programming"],
        "difficulty_levels": {
            "beginner": ["SAS data steps", "Basic PROC procedures", "Data import"],
            "intermediate": ["PROC SQL in SAS", "Data merging and sorting", "Format creation"],
            "advanced": ["SAS macro programming", "PROC IML for advanced analytics", "SAS/STAT procedures"],
        },
    },
    "gis": {
        "id": "TECH-007",
        "name": "GIS & Spatial Analysis",
        "description": "Geographic Information Systems for statistical mapping",
        "sub_competencies": ["QGIS/ArcGIS basics", "Spatial data management", "Thematic mapping", "Spatial analysis"],
        "difficulty_levels": {
            "beginner": ["GIS concepts", "QGIS interface", "Basic mapping"],
            "intermediate": ["Spatial data formats", "Georeferencing", "Thematic map creation"],
            "advanced": ["Spatial statistics", "Remote sensing integration", "Spatial database management"],
        },
    },
    "data_visualization": {
        "id": "TECH-008",
        "name": "Data Visualization",
        "description": "Effective visual communication of statistical data",
        "sub_competabilities": ["Chart selection", "Dashboard design", "Interactive visualization", "Statistical graph standards"],
        "difficulty_levels": {
            "beginner": ["Chart types and when to use them", "Basic charts in tools"],
            "intermediate": ["Dashboard design principles", "Interactive charts", "Storytelling with data"],
            "advanced": ["Custom visualization development", "Real-time dashboards", "Accessibility in visualization"],
        },
    },
    "ai_ml": {
        "id": "TECH-009",
        "name": "AI/ML for Statistics",
        "description": "Applying AI/ML techniques to statistical problems",
        "sub_competencies": ["ML fundamentals", "Supervised learning", "Unsupervised learning", "Model evaluation"],
        "difficulty_levels": {
            "beginner": ["ML concepts and terminology", "Training vs testing", "Overfitting"],
            "intermediate": ["Scikit-learn basics", "Classification and regression", "Cross-validation"],
            "advanced": ["Ensemble methods", "Neural networks basics", "ML pipeline design"],
        },
    },
    "cloud_computing": {
        "id": "TECH-010",
        "name": "Cloud Computing",
        "description": "Cloud platforms for data storage and processing",
        "sub_competencies": ["Cloud fundamentals", "AWS/GCP basics", "Cloud data storage", "Serverless computing"],
        "difficulty_levels": {
            "beginner": ["Cloud computing concepts", "Cloud service models (IaaS, PaaS, SaaS)"],
            "intermediate": ["AWS S3 and EC2 basics", "Cloud data storage", "Basic cloud deployments"],
            "advanced": ["Serverless architecture", "Cloud-native data pipelines", "Multi-cloud strategies"],
        },
    },
    "apis": {
        "id": "TECH-011",
        "name": "APIs & Web Services",
        "description": "Building and consuming APIs for data exchange",
        "sub_competencies": ["REST API fundamentals", "API design", "Data exchange formats", "API security"],
        "difficulty_levels": {
            "beginner": ["What is an API", "REST concepts", "JSON format"],
            "intermediate": ["Building REST APIs with FastAPI", "API authentication", "Data serialization"],
            "advanced": ["GraphQL", "API gateway patterns", "API versioning strategies"],
        },
    },
    "open_data": {
        "id": "TECH-012",
        "name": "Open Data Principles",
        "description": "Open data standards, portals, and governance",
        "sub_competencies": ["Open data standards", "Data.gov.in", "Open licensing", "Data publishing"],
        "difficulty_levels": {
            "beginner": ["Open data concepts", "India Open Data Portal"],
            "intermediate": ["Open data licensing (CC BY)", "Data publishing workflows"],
            "advanced": ["Open data ecosystem development", "Government open data policy"],
        },
    },
}

DIGITAL_GOVERNANCE = {
    "cybersecurity": {
        "id": "DG-001",
        "name": "Cybersecurity Fundamentals",
        "description": "Security practices for protecting statistical data systems",
        "sub_competencies": ["Security awareness", "Threat identification", "Incident response", "Security frameworks"],
        "difficulty_levels": {
            "beginner": ["Security awareness basics", "Password management", "Phishing identification"],
            "intermediate": ["Security frameworks (ISO 27001)", "Risk assessment", "Incident response procedures"],
            "advanced": ["Security architecture", "Penetration testing concepts", "Zero trust models"],
        },
    },
    "data_privacy": {
        "id": "DG-002",
        "name": "Data Privacy & Protection",
        "description": "Data protection laws and privacy frameworks",
        "sub_competencies": ["DPDP Act 2023", "Data classification", "Privacy by design", "Consent management"],
        "difficulty_levels": {
            "beginner": ["Data protection basics", "Personal vs non-personal data"],
            "intermediate": ["DPDP Act 2023 compliance", "Data processing agreements", "Breach notification"],
            "advanced": ["Privacy impact assessments", "Cross-border data transfer", "Data fiduciary obligations"],
        },
    },
    "digital_signatures": {
        "id": "DG-003",
        "name": "Digital Signatures & Certification",
        "description": "Digital signature technology and legal framework",
        "sub_competencies": ["Digital signature basics", "CA hierarchy", "Certificate management"],
        "difficulty_levels": {
            "beginner": ["What are digital signatures", "Legal validity"],
            "intermediate": ["Certificate authorities", "Certificate lifecycle"],
            "advanced": ["PKI architecture", "Digital signature compliance"],
        },
    },
    "government_cloud": {
        "id": "DG-004",
        "name": "Government Cloud (CGnetSwaran)",
        "description": "Cloud infrastructure for government applications",
        "sub_competencies": ["CGnetSwaran architecture", "Cloud migration", "Government cloud policies"],
        "difficulty_levels": {
            "beginner": ["Government cloud concepts", "CGnetSwaran overview"],
            "intermediate": ["Cloud migration planning", "Government cloud compliance"],
            "advanced": ["Hybrid cloud architecture", "Cloud security in government"],
        },
    },
    "dpi": {
        "id": "DG-005",
        "name": "Digital Public Infrastructure",
        "description": "India's DPI stack and its application",
        "sub_competencies": ["DPI concepts", "India stack", "API economy", "Data sharing"],
        "difficulty_levels": {
            "beginner": ["DPI overview", "India Stack components"],
            "intermediate": ["API integration", "Data sharing frameworks"],
            "advanced": ["DPI ecosystem design", "Interoperability standards"],
        },
    },
}

BEHAVIOURAL_COMPETENCIES = {
    "leadership": {
        "id": "BEH-001",
        "name": "Leadership & Team Management",
        "description": "Leading teams and driving organizational change",
        "sub_competencies": ["Team leadership", "Decision making", "Performance management", "Change management"],
        "difficulty_levels": {
            "beginner": ["Basic leadership principles", "Communication skills"],
            "intermediate": ["Team building", "Conflict resolution", "Delegation"],
            "advanced": ["Strategic leadership", "Organizational transformation", "Succession planning"],
        },
    },
    "communication": {
        "id": "BEH-002",
        "name": "Effective Communication",
        "description": "Clear and professional communication for statistical reporting",
        "sub_competencies": ["Written communication", "Presentation skills", "Report writing", "Stakeholder communication"],
        "difficulty_levels": {
            "beginner": ["Professional writing basics", "Email etiquette"],
            "intermediate": ["Report writing for officials", "Presentation skills", "Data storytelling"],
            "advanced": ["Strategic communication", "Media relations", "Cross-cultural communication"],
        },
    },
    "project_management": {
        "id": "BEH-003",
        "name": "Project Management",
        "description": "Managing statistical projects and surveys",
        "sub_competencies": ["Project planning", "Resource management", "Risk management", "Monitoring & evaluation"],
        "difficulty_levels": {
            "beginner": ["Project planning basics", "Timeline management"],
            "intermediate": ["Survey project management", "Resource allocation", "Risk assessment"],
            "advanced": ["Agile project management", "Multi-stakeholder coordination", "Project portfolio management"],
        },
    },
    "ethics": {
        "id": "BEH-004",
        "name": "Ethics & Integrity",
        "description": "Professional ethics in official statistics",
        "sub_competencies": ["Fundamental principles of official statistics", "Data integrity", "Confidentiality", "Professional conduct"],
        "difficulty_levels": {
            "beginner": ["UN Fundamental Principles", "Confidentiality requirements"],
            "intermediate": ["Ethical data handling", "Conflict of interest", "Professional conduct standards"],
            "advanced": ["Ethics in AI/ML for statistics", "Data governance frameworks"],
        },
    },
    "decision_making": {
        "id": "BEH-005",
        "name": "Evidence-Based Decision Making",
        "description": "Using statistical evidence for policy decisions",
        "sub_competencies": ["Evidence interpretation", "Data-driven decisions", "Policy analysis", "Risk assessment"],
        "difficulty_levels": {
            "beginner": ["Understanding statistical evidence", "Basic data interpretation"],
            "intermediate": ["Evidence-based policy", "Statistical reasoning", "Bias identification"],
            "advanced": ["Advanced policy analysis", "Predictive decision frameworks", "Complex risk analysis"],
        },
    },
    "change_management": {
        "id": "BEH-006",
        "name": "Change Management",
        "description": "Managing organizational change in statistical systems",
        "sub_competencies": ["Change models", "Stakeholder engagement", "Resistance management", "Communication during change"],
        "difficulty_levels": {
            "beginner": ["Change management concepts", "Understanding resistance"],
            "intermediate": ["Kotter's change model", "Stakeholder mapping", "Communication planning"],
            "advanced": ["Digital transformation leadership", "Organizational culture change", "Sustaining change"],
        },
    },
}

# ── Full Framework Assembly ─────────────────────────────────

COMPETENCY_FRAMEWORK = {
    "statistical": STATISTICAL_COMPETENCIES,
    "technical": TECHNICAL_COMPETENCIES,
    "digital_governance": DIGITAL_GOVERNANCE,
    "behavioural": BEHAVIOURAL_COMPETENCIES,
}

# ── Helper Functions ────────────────────────────────────────

def get_all_competency_ids() -> list[str]:
    """Return all competency IDs across all domains."""
    ids = []
    for domain_comps in COMPETENCY_FRAMEWORK.values():
        ids.extend(domain_comps.keys())
    return ids


def get_competency_details(competency_id: str) -> dict | None:
    """Get full details for a specific competency by ID."""
    for domain_comps in COMPETENCY_FRAMEWORK.values():
        if competency_id in domain_comps:
            return domain_comps[competency_id]
    return None


def get_competencies_by_domain(domain: str) -> dict:
    """Get all competencies for a specific domain."""
    return COMPETENCY_FRAMEWORK.get(domain, {})


def search_competencies(query: str) -> list[dict]:
    """Search competencies by keyword (case-insensitive)."""
    results = []
    query_lower = query.lower()
    for domain, domain_comps in COMPETENCY_FRAMEWORK.items():
        for comp_id, comp in domain_comps.items():
            if (query_lower in comp["name"].lower() or
                query_lower in comp["description"].lower() or
                any(query_lower in sub.lower() for sub in comp.get("sub_competencies", []))):
                results.append({
                    "id": comp["id"],
                    "name": comp["name"],
                    "domain": domain,
                    "description": comp["description"],
                })
    return results
