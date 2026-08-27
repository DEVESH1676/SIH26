import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.rag import ResolutionEngine

rag = ResolutionEngine()
# Mock the ollama call to prevent hanging
rag._generate_ollama = lambda x: "MOCK AI RESOLUTION"

result = rag.suggest_resolution("VPN connection drops after 5 minutes", "User jdoe is complaining that their VPN connects but drops exactly 5 minutes later with error 619.")
print(result['context_used'])
