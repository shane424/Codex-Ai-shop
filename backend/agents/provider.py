from abc import ABC, abstractmethod
from dataclasses import dataclass
import json

@dataclass
class Review: 
    passed: bool
    reasons: list[str]

class LLMProvider(ABC):
    @abstractmethod
    def opportunities(self, niche: str, count: int) -> list[dict]: ...
    @abstractmethod
    def review(self, content: str) -> Review: ...

class MockProvider(LLMProvider):
    def opportunities(self, niche, count):
        return [{'niche':niche,'problem':f'{niche.title()} operational record {i+1}','product_type':'xlsx','utility':82,'purchase_intent':78,'automation':95,'margin':90,'niche_specificity':80} for i in range(count)]
    def review(self, content):
        banned=('guaranteed earnings','medical advice','legal advice','official disney','pokemon')
        hits=[x for x in banned if x in content.lower()]
        return Review(not hits, [f'unsafe phrase: {x}' for x in hits])

def get_provider():
    # Provider selection lives here; business logic never imports a vendor SDK.
    return MockProvider()
