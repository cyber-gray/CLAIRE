"""
CLAIRE Tools Package
Compliance & Legal AI Risk Engine toolkit
"""

from .time import get_time, get_date_info, get_world_clocks
from .reg_search import reg_search, list_available_frameworks
from .risk_score import assess_ai_risk, quick_risk_check
from .checklist_gen import generate_compliance_checklist, export_checklist, list_checklist_templates
from .news import get_ai_policy_news, get_general_news
from .weather import get_current_weather, get_weather_forecast

__all__ = [
    'get_time',
    'get_date_info',
    'get_world_clocks',
    'reg_search',
    'list_available_frameworks', 
    'assess_ai_risk',
    'quick_risk_check',
    'generate_compliance_checklist',
    'export_checklist',
    'list_checklist_templates',
    'get_ai_policy_news',
    'get_general_news',
    'get_current_weather',
    'get_weather_forecast'
]
