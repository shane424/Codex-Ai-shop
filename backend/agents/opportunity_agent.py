from dataclasses import dataclass
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.config import Settings, get_settings
from backend.models import DailyGeneration, Opportunity
from .provider import LLMProvider, get_provider

UNSAFE=('medical','diagnosis','legal advice','tax advice','investment','weapon','gambling','guaranteed','official','trademark','disney','pokemon','generic journal','generic planner')

def score(values: dict) -> float:
    fields=('utility','purchase_intent','automation','margin','niche_specificity')
    nums={k:max(0,min(100,float(values[k]))) for k in fields}
    return round(nums['utility']*.30+nums['purchase_intent']*.25+nums['automation']*.20+nums['margin']*.15+nums['niche_specificity']*.10,2)

def is_safe(idea: dict) -> bool:
    text=' '.join(str(v) for v in idea.values()).lower()
    return not any(term in text for term in UNSAFE)

def discover_opportunities(niche: str, count=10, provider: LLMProvider|None=None):
    ideas=(provider or get_provider()).opportunities(niche, count)
    return [{**idea,'overall_score':score(idea)} for idea in ideas if is_safe(idea)]

def reserve_generation(db: Session, cost_cents: int=0, settings: Settings|None=None):
    settings=settings or get_settings(); today=date.today()
    usage=db.execute(select(DailyGeneration).where(DailyGeneration.date==today).with_for_update()).scalar_one_or_none()
    if not usage: usage=DailyGeneration(date=today); db.add(usage); db.flush()
    if usage.products_created >= settings.max_new_products_per_day: raise RuntimeError('daily product limit reached')
    if usage.llm_cost_cents+cost_cents > round(settings.max_llm_cost_per_day*100): raise RuntimeError('daily LLM cost limit reached')
    usage.products_created += 1; usage.llm_cost_cents += cost_cents; db.commit()
