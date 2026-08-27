"""
Generate remaining 50 tickets (TKT-2024-00101 to 00150) and merge with batch 1.
"""
import os, sys, time, json, requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

PROMPT = """Generate exactly 50 realistic IT support tickets as CSV. Output ONLY raw CSV, no explanations.

Header: ticket_id,title,description,category,resolution,priority,department,created_at

Categories (distribute evenly across 50):
- Infrastructure (9): K8s pod evictions, Terraform drift, S3 bucket policies, EC2 scaling, CDN cache purge
- Application (8): microservice circuit breakers, gRPC timeouts, Redis cache misses, blue-green deploy failures
- Security (8): ransomware containment, zero-day patching, WAF rule tuning, SIEM correlation, phishing campaigns
- Database (9): index rebuild, pg_repack, MongoDB oplog overflow, Aurora failover, ETL pipeline breaks
- Network (8): BGP route leak, OSPF adjacency flap, 802.1X auth failure, MTU black hole, traceroute anomalies
- Access Management (8): Okta SCIM sync, Azure AD conditional access, break-glass account audit, PAM session recording

Priority: P1 Critical(10%), P2 High(25%), P3 Medium(40%), P4 Low(25%)

Departments: Infrastructure->Cloud Platform Engineering, Application->Application Support Team, Security->Security Operations Center (SOC), Database->Database Administration (DBA), Network->Network Operations Center (NOC), Access Management->Identity & Access Management (IAM)

Rules:
- ticket_id: TKT-2024-00101 through TKT-2024-00150
- created_at: Random dates between 2024-01-01 and 2024-12-31 in YYYY-MM-DD HH:MM:SS format
- description: 2-4 real sentences. Use server names (PROD-K8S-03, STG-REDIS-01), error codes (ECONNREFUSED, ORA-00060), tool names (Helm, ArgoCD, Vault, Datadog, PagerDuty, Snyk, Qualys)
- resolution: Specific technical steps with commands, file paths, tool names. NOT generic.
- ~10% descriptions should have minor typos
- 15% should be ambiguous (could fit 2 categories)
- Wrap fields containing commas in double quotes

Output RAW CSV only. Start with header row. No markdown. No code blocks."""

MODEL = "qwen2.5-gpu:latest"
BASE_URL = config.OLLAMA_BASE_URL

def clean_csv(content):
    content = content.strip()
    for prefix in ["```csv", "```"]:
        if content.startswith(prefix):
            content = content[len(prefix):]
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()

def main():
    print("  Generating batch 2 (TKT-00101 to 00150)...")
    
    url = f"{BASE_URL}/api/chat"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": True,
        "options": {"temperature": 0.7, "num_predict": 16384}
    }
    
    start = time.time()
    collected = []
    count = 0
    header_seen = False
    
    resp = requests.post(url, json=payload, stream=True, timeout=(30, 600))
    resp.raise_for_status()
    print("  ✓ Streaming...")
    
    for line in resp.iter_lines():
        if not line: continue
        try:
            data = json.loads(line)
            if "message" in data and "content" in data["message"]:
                t = data["message"]["content"]
                collected.append(t)
                nl = t.count('\n')
                if nl > 0:
                    if not header_seen: header_seen = True; count += max(0, nl-1)
                    else: count += nl
                    sys.stdout.write(f"\r  Tickets: {count}/50")
                    sys.stdout.flush()
            if data.get("done"): break
        except json.JSONDecodeError: continue
    
    print()
    csv2 = clean_csv(''.join(collected))
    lines2 = [l for l in csv2.split('\n') if l.strip()]
    actual = len(lines2) - 1
    print(f"  ✓ Batch 2: {actual} tickets in {int((time.time()-start)//60)}m {int((time.time()-start)%60)}s")
    
    # Merge with batch 1
    batch1_path = os.path.join(os.path.dirname(__file__), 'synthetic_tickets_100.csv')
    with open(batch1_path, 'r') as f:
        batch1 = f.read().strip()
    
    # Append batch2 data rows (skip header)
    merged = batch1 + '\n' + '\n'.join(lines2[1:])
    
    output = os.path.join(os.path.dirname(__file__), 'synthetic_tickets_100.csv')
    with open(output, 'w', encoding='utf-8') as f:
        f.write(merged)
    
    total_lines = len([l for l in merged.split('\n') if l.strip()]) - 1
    print(f"  💾 Merged total: {total_lines} tickets → {output}")

if __name__ == "__main__":
    main()
