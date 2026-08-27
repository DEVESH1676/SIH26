"""
Generate 100 additional synthetic IT tickets using qwen2.5-gpu:latest via Ollama REST API.
Output: data/synthetic_tickets_100.csv
"""
import os
import sys
import time
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

PROMPT = """Generate exactly 100 realistic IT support tickets as CSV. Output ONLY raw CSV, no explanations.

Header: ticket_id,title,description,category,resolution,priority,department,created_at

Categories (distribute evenly across 100):
- Infrastructure (17): servers, VMs, storage, K8s, CI/CD, DNS, load balancers, cloud migration, container orchestration
- Application (17): CRM crashes, API timeouts, microservice failures, memory leaks, deployment issues, webhook failures
- Security (16): phishing, MFA failures, cert expirations, vulnerability scans, ransomware, DLP, SOC alerts, DDoS
- Database (17): slow queries, replication lag, deadlocks, backup failures, connection pools, ORA errors, schema migrations
- Network (16): VPN drops, firewall rules, VLAN misconfigs, BGP flaps, packet loss, DNS failures, SD-WAN
- Access Management (17): AD groups, RBAC, service accounts, SSO issues, PAM access, offboarding, API key rotation

Priority: P1 Critical(10%), P2 High(25%), P3 Medium(40%), P4 Low(25%)

Departments: Infrastructure->Cloud Platform Engineering, Application->Application Support Team, Security->Security Operations Center (SOC), Database->Database Administration (DBA), Network->Network Operations Center (NOC), Access Management->Identity & Access Management (IAM)

Rules:
- ticket_id: TKT-2024-00051 through TKT-2024-00150
- created_at: Random dates between 2024-01-01 and 2024-12-31 in YYYY-MM-DD HH:MM:SS format
- description: 2-4 real sentences. Use server names (PROD-APP-07, STG-WEB-12), error codes (ORA-12541, HTTP 503, PG::DeadlockDetected), tool names (ServiceNow, Jira, Splunk, CrowdStrike, Okta, Terraform, Ansible, AWS, Azure AD, Grafana, PagerDuty, Datadog)
- resolution: Specific technical steps with commands, file paths, tool names. NOT generic.
- ~10% descriptions should have minor typos like a real employee
- 15% should be ambiguous (could fit 2 categories)
- Wrap fields containing commas in double quotes

Output RAW CSV only. Start with header row. No markdown. No code blocks."""

TARGET = 100
MODEL = "qwen2.5-gpu:latest"
BASE_URL = config.OLLAMA_BASE_URL

def print_progress(current, total, start_time, bar_width=40):
    pct = min(current / total, 1.0)
    filled = int(bar_width * pct)
    bar = '█' * filled + '░' * (bar_width - filled)
    elapsed = time.time() - start_time
    if current > 0:
        eta = (elapsed / current) * (total - current)
        eta_str = f"{int(eta//60)}m {int(eta%60)}s"
    else:
        eta_str = "..."
    rate = current / elapsed if elapsed > 0 else 0
    sys.stdout.write(f"\r  [{bar}] {current}/{total} ({pct*100:.1f}%) | {rate:.1f} t/s | ETA: {eta_str}  ")
    sys.stdout.flush()

def clean_csv(content):
    content = content.strip()
    for prefix in ["```csv", "```"]:
        if content.startswith(prefix):
            content = content[len(prefix):]
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()

def main():
    print(f"╔══════════════════════════════════════════════════════╗")
    print(f"║  Synthetic Ticket Generator (100 Extra Tickets)     ║")
    print(f"║  Model: {MODEL:<43}║")
    print(f"║  Host:  {BASE_URL:<43}║")
    print(f"╚══════════════════════════════════════════════════════╝")
    
    # Connectivity test
    print(f"\n  Testing connection to {BASE_URL}...")
    try:
        r = requests.get(f"{BASE_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        print(f"  ✓ Connected! Available models: {len(models)}")
        if MODEL not in models:
            print(f"  ⚠ Warning: {MODEL} not found. Trying anyway...")
    except Exception as e:
        print(f"  ✗ Cannot reach Ollama: {e}")
        return
    
    output_path = os.path.join(os.path.dirname(__file__), 'synthetic_tickets_100.csv')
    
    url = f"{BASE_URL}/api/chat"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": True,
        "options": {
            "temperature": 0.7,
            "num_predict": 32768
        }
    }
    
    start_time = time.time()
    collected = []
    ticket_count = 0
    header_seen = False
    
    print(f"\n  Sending request to {url}...")
    response = requests.post(url, json=payload, stream=True, timeout=(30, 600))
    response.raise_for_status()
    print(f"  ✓ Connection established. Streaming tokens...\n")
    
    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line)
            if "message" in data and "content" in data["message"]:
                text = data["message"]["content"]
                collected.append(text)
                
                nl = text.count('\n')
                if nl > 0:
                    if not header_seen:
                        header_seen = True
                        ticket_count += max(0, nl - 1)
                    else:
                        ticket_count += nl
                    if ticket_count > 0:
                        print_progress(min(ticket_count, TARGET), TARGET, start_time)
            
            if data.get("done", False):
                break
                
        except json.JSONDecodeError:
            continue
    
    print()
    elapsed = time.time() - start_time
    content = clean_csv(''.join(collected))
    
    lines = [l for l in content.split('\n') if l.strip()]
    actual = len(lines) - 1  # minus header
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  ✓ Complete: {actual} tickets in {int(elapsed//60)}m {int(elapsed%60)}s")
    print(f"  💾 Saved to: {output_path}")
    print(f"\n{'='*55}")
    print(f"  DONE: {actual} tickets → {output_path}")
    print(f"  Next: python core/embeddings.py")
    print(f"{'='*55}")

if __name__ == "__main__":
    main()
