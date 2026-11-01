"""Local context only. Recommendations are starting points, never business facts."""
import re

PROFILES = {
    'finance': (r'account|bookkeep|financ|insurance|tax', 'Substantiate credentials and service scope; verify current primary sources and obtain qualified review for financial or tax advice.'),
    'health': (r'health|medical|dental|clinic|wellness', 'Verify health claims with primary sources and qualified review; do not publish patient details or infer professional credentials.'),
    'property': (r'construct|property|real estate|contractor', 'Clarify project or property types, geography, responsibilities, and evidence of delivered work; avoid unsupported local-office claims.'),
    'education': (r'educat|training|course|academy', 'Explain prerequisites, curriculum, delivery, dates, and enrollment; verify accreditation and employment-outcome claims.'),
    'software': (r'software|saas|technology', 'Explain use case, setup, compatibility, and pricing; distinguish supported integrations from planned capabilities.'),
    'retail': (r'retail|e.?commerce|shop|manufactur', 'Make specifications, availability, fulfillment, returns, and support clear; use verified product data and genuine reviews.'),
}


def build_profile(industry, business_type):
    industry = industry.strip()
    if not 2 <= len(industry) <= 120 or any(not c.isprintable() for c in industry):
        raise ValueError('Industry must be 2–120 printable characters on one line')
    if business_type not in ('service', 'product'):
        raise ValueError('Business type must be service or product')
    matches = [name for name, (pattern, _) in PROFILES.items() if re.search(pattern, industry, re.I)]
    guidance = [PROFILES[name][1] for name in matches] or ['Research this industry using primary sources and approved customer evidence; establish audience, offer, geography, and constraints before making claims.']
    if business_type == 'service':
        journey = 'Clarify fit, scope, process, evidence, and next step; optimize a qualified inquiry, consultation, or booking as appropriate.'
        schema = 'Consider Organization and Service; LocalBusiness only for a qualifying business with verified location facts.'
        measures = ['qualified inquiries', 'booking completion', 'lead-to-customer conversion']
        workflows = ['strategy', 'copy', 'conversion', 'technical-seo', 'content', 'ai-visibility', 'schema', 'measurement']
    else:
        journey = 'Clarify use case, features, price, proof, and buying friction; choose purchase, trial, or demo from the actual sales model.'
        schema = 'Consider Product or SoftwareApplication only when applicable to visible, verified facts; inspect current feature eligibility.'
        measures = ['qualified demos or trials', 'purchase completion', 'activation or repeat purchase']
        workflows = ['strategy', 'content', 'copy', 'technical-seo', 'conversion', 'schema', 'ai-visibility', 'measurement']
    workflows.insert(1, 'design')
    workflows.extend(['backlinks', 'decisions'])
    return {'schema_version': 1, 'industry': industry, 'business_type': business_type,
            'matched_profiles': matches or ['general'], 'workflow_order': workflows,
            'recommendations': {'journey': journey, 'industry': guidance, 'schema_candidates': schema, 'measurements': measures},
            'context_status': 'User-provided labels; recommendations require project-specific verification. No credentials, geography, offers, or results are asserted.'}
