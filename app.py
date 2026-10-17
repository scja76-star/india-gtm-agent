import streamlit as st
import requests
import re
import json
import time
import pandas as pd
from pydantic import BaseModel, Field
from typing import List
from ddgs import DDGS
from google import genai
from google.genai import types

st.set_page_config(page_title="LogosGTM V2.0: Behavioral & GTM Intelligence Engine", layout="wide")
st.title("⚡ LogosGTM V2.0: Autonomous Cross-Border GTM & Behavioral Game-Theory Engine")
st.caption("6-Layer Deep Web Recon • Deterministic Compliance & Pricing Telemetry • Buying-Committee Game Theory • Autonomous LinkedIn Lead Hunter")

# --- 1. STRICT PYDANTIC SCHEMAS ---
class PsychScores(BaseModel):
    trust_alignment: int = Field(description="0-100 score: Enterprise & buyer trust readiness in target market")
    habit_friction_score: int = Field(description="0-100 score: Ease of switching from incumbent workflows (higher = easier)")
    price_elasticity_fit: int = Field(description="0-100 score: Pricing & unit-economics alignment with local ROI benchmarks")
    status_signaling_value: int = Field(description="0-100 score: Brand prestige & career-signaling value for the internal champion")

class PsychPersonaNode(BaseModel):
    persona_role: str = Field(description="e.g., The CFO (Loss Aversion), The End-User (Habit Inertia), The Security Gatekeeper, The Champion")
    cognitive_bias_triggered: str = Field(description="Exact psychological bias triggered (e.g., Status Quo Bias, Ambiguity Effect, Social Proof Deficit)")
    internal_monologue: str = Field(description="Brutally honest 25-word internal thought blocking or driving the purchase")
    veto_power_score: int = Field(description="0-100 probability this stakeholder kills the deal")
    counter_move: str = Field(description="Exact 15-word product or sales counter-move to neutralize their veto")

class CompetitorBattlecard(BaseModel):
    incumbent_name: str = Field(description="Real named competitor or workflow substitute in the target market")
    their_pricing_model: str = Field(description="Their approximate pricing & packaging")
    psychological_moat: str = Field(description="Why buyers default to them despite inferior tech")
    wedge_to_steal_share: str = Field(description="Exact angle to displace them in 30 days")

class TargetAccountLead(BaseModel):
    company_name: str = Field(description="Real, named high-fit target company in the target market")
    hq_city: str = Field(description="City HQ (e.g., Bengaluru, Mumbai, San Francisco, New York)")
    ideal_buyer_title: str = Field(description="Exact decision-maker title to contact (e.g., VP Engineering, Head of RevOps)")
    why_they_buy_now: str = Field(description="Specific operational trigger making them a high-intent buyer")
    bias_matched_dm: str = Field(description="Ready-to-send 35-word LinkedIn/WhatsApp cold pitch using behavioral psychology")

class ScalingPhase(BaseModel):
    phase: str = Field(description="Phase 1 (Days 1-30 Wedge), Phase 2 (Days 31-90 Trust Engine), Phase 3 (Category Moat)")
    strategic_move: str = Field(description="Concrete, non-obvious GTM or product mechanism")
    psychological_trigger_used: str = Field(description="Behavioral lever unlocked")
    target_beachhead: str = Field(description="Exact micro-vertical or buyer cluster (e.g., Bengaluru GCCs, YC Seed Startups)")

class BeastGTMReport(BaseModel):
    brand_name: str
    verdict_badge: str = Field(description="Strictly: 'STRONG FIT (GO)', 'CONDITIONAL FIT (REQUIRES PIVOT)', or 'POOR FIT (NO-GO)'")
    overall_fit_score: int = Field(description="0-100 composite score")
    unit_economics_arbitrage_test: str = Field(description="Brutal 30-word math comparison: Software price vs local human labor/incumbent alternatives & payment friction.")
    executive_thesis: str = Field(description="40-word synthesis on whether this brand DNA fits the target corridor and the #1 bottleneck.")
    recommended_pricing_architecture: str = Field(description="Exact localized pricing & packaging formula (e.g., Outcome-based, INR/UPI or US Enterprise Tier)")
    psych_scores: PsychScores
    buying_committee_simulation: List[PsychPersonaNode]
    competitor_battlecards: List[CompetitorBattlecard]
    ideal_scaling_blueprint: List[ScalingPhase]
    first_5_target_accounts: List[TargetAccountLead]

# --- 2. DETERMINISTIC PYTHON TELEMETRY & 6-LAYER HARVESTER (0 LLM QUOTA) ---
@st.cache_data(ttl=3600)
def run_deep_recon_and_telemetry(raw_url: str, corridor: str) -> dict:
    clean_url = raw_url.strip().rstrip("/")
    if not clean_url.startswith("http"):
        clean_url = "https://" + clean_url
    domain = clean_url.replace("https://", "").replace("http://", "").split("/")[0].replace("www.", "")
    brand_slug = domain.split(".")[0]

    harvest = {}
    for page_name, path in [("homepage", ""), ("pricing_page", "/pricing"), ("security_trust", "/security")]:
        try:
            r = requests.get(f"https://r.jina.ai/{clean_url}{path}", timeout=12)
            harvest[page_name] = r.text[:3200] if r.status_code == 200 else "Page not found"
        except Exception:
            harvest[page_name] = "Could not crawl path."

    # Deterministic Python Regex Signal Extraction (No LLM Guessing)
    combined_raw = (harvest["homepage"] + " " + harvest["pricing_page"] + " " + harvest["security_trust"]).lower()
    telemetry = {
        "SOC2 / ISO27001 Detected": bool(re.search(r"soc\s?2|iso\s?27001", combined_raw)),
        "GDPR / DPDP Privacy Ready": bool(re.search(r"gdpr|dpdp|data residency|hipaa", combined_raw)),
        "SSO / SAML Enterprise Auth": bool(re.search(r"\bsso\b|saml|okta", combined_raw)),
        "Self-Serve Free Tier / Trial": bool(re.search(r"free trial|start for free|free plan|\$0", combined_raw)),
        "API / Webhook Docs": bool(re.search(r"\bapi\b|webhook|sdk|documentation", combined_raw)),
        "INR / PPP Pricing Mentioned": bool(re.search(r"₹|\binr\b|rupee|purchasing power", combined_raw)),
        "Outcome / Usage Pricing": bool(re.search(r"per resolution|usage-based|pay as you go|credits|per call", combined_raw)),
    }

    region_code = "in-en" if "India" in corridor.split("→")[1] else "us-en"
    queries = {
        "reddit_dark_funnel": f"site:reddit.com \"{brand_slug}\" OR \"{domain}\" review OR alternative OR expensive OR issue",
        "g2_user_complaints": f"\"{domain}\" OR \"{brand_slug}\" reviews cons complaints pricing G2 TrustRadius",
        "corridor_competitors": f"{brand_slug} competitors alternatives pricing {'India INR Zoho Freshworks' if region_code == 'in-en' else 'US enterprise G2 leader'}"
    }
    ddgs = DDGS()
    for key, q in queries.items():
        try:
            res = ddgs.text(q, region=region_code, max_results=5)
            harvest[key] = "\n".join([f"- {x.get('title')}: {x.get('body')}" for x in res]) if res else "No threads found."
        except Exception as e:
            harvest[key] = f"Search skipped: {e}"

    return {"domain": domain, "brand": brand_slug, "harvest": harvest, "telemetry": telemetry, "region": region_code}

# --- 3. GEMINI 3.8 FLASH FAILOVER ROUTER ---
MODEL_CHAIN = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash"]

def execute_beast_simulation(client, prompt: str):
    last_err = None
    for model_name in MODEL_CHAIN:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BeastGTMReport,
                )
            )
            return json.loads(res.text), model_name
        except Exception as e:
            last_err = e
            if any(k in str(e) for k in ["429", "RESOURCE_EXHAUSTED", "404", "not found"]):
                time.sleep(1)
                continue
            raise e
    raise RuntimeError(f"All free model buckets temporarily full. Last error: {last_err}")

# --- 4. PRE-FIXED API KEY + QUOTA SHIELD + UI ---
if "scans_used" not in st.session_state:
    st.session_state.scans_used = 0

prefixed_key = ""
vip_code_secret = "YC2026"
try:
    prefixed_key = st.secrets.get("GEMINI_API_KEY", "")
    vip_code_secret = st.secrets.get("VIP_PASSCODE", "YC2026")
except Exception:
    pass

with st.sidebar:
    st.header("⚡ Engine Controls")
    corridor = st.radio(
        "Select Expansion Corridor:",
        ["Global Startup → Entering India 🇮🇳", "Indian Startup → Attacking US/Global 🇺🇸"]
    )
    free_left = max(0, 3 - st.session_state.scans_used)
    st.metric("Free Instant Scans Remaining", f"{free_left} / 3")
    with st.expander("🔓 VIP Code / Custom API Key"):
        vip_input = st.text_input("Enter VIP Code (`YC2026`) or Gemini Key:", type="password")

active_api_key = None
is_unlimited = False
if vip_input == vip_code_secret and prefixed_key:
    active_api_key = prefixed_key
    is_unlimited = True
    st.sidebar.success("VIP Unlimited Mode Active!")
elif vip_input.startswith("AIza"):
    active_api_key = vip_input
    is_unlimited = True
elif prefixed_key:
    active_api_key = prefixed_key

b1, b2, b3, b4 = st.columns(4)
if "target_url" not in st.session_state:
    st.session_state.target_url = "https://linear.app"
if b1.button("Test Linear.app"):
    st.session_state.target_url = "https://linear.app"
if b2.button("Test TryCardinal.ai (YC W26)"):
    st.session_state.target_url = "https://trycardinal.ai"
if b3.button("Test Cardboard (YC W26)"):
    st.session_state.target_url = "https://usecardboard.com"
if b4.button("Test Cal.com"):
    st.session_state.target_url = "https://cal.com"

target_url = st.text_input("Drop Any Startup URL for 6-Layer Deep Behavioral & GTM Recon:", value=st.session_state.target_url)

if st.button("Run Beast-Mode 6-Layer Simulation & Lead Hunter 🚀"):
    if not active_api_key:
        st.error("Add GEMINI_API_KEY to `.streamlit/secrets.toml` or paste your key in the sidebar.")
    elif not is_unlimited and st.session_state.scans_used >= 3:
        st.warning("3 free scans used! Enter VIP Code `YC2026` or your own Gemini key in the sidebar.")
    else:
        if not is_unlimited:
            st.session_state.scans_used += 1

        client = genai.Client(api_key=active_api_key)
        with st.status("Executing 6-Layer Recon + Deterministic Telemetry + Buyer Discovery...", expanded=True) as status:
            st.write("1️⃣ Crawling `/`, `/pricing`, & `/security` + running deterministic compliance regex...")
            recon = run_deep_recon_and_telemetry(target_url, corridor)

            st.write(f"2️⃣ Running Behavioral Game-Theory Simulation for `{corridor}`...")
            prompt = f"""
            You are an elite Behavioral Economist (Kahneman Prospect Theory, Cialdini Trust Mechanics) and Cross-Border Venture Architect.
            Analyze '{recon['domain']}' for the corridor: {corridor}.
            
            DETERMINISTIC PYTHON TELEMETRY SIGNALS:
            {json.dumps(recon['telemetry'])}

            HOMEPAGE: {recon['harvest']['homepage']}
            PRICING PAGE: {recon['harvest']['pricing_page']}
            SECURITY/TRUST PAGE: {recon['harvest']['security_trust']}
            REDDIT DARK FUNNEL: {recon['harvest']['reddit_dark_funnel']}
            G2 FRICTION: {recon['harvest']['g2_user_complaints']}
            COMPETITOR LANDSCAPE: {recon['harvest']['corridor_competitors']}

            Be brutally honest, quantitative, and non-obvious. Name real companies, real local competitors, and exact psychological biases.
            """
            report, used_model = execute_beast_simulation(client, prompt)

            st.write("3️⃣ Hunting live LinkedIn Decision-Maker URLs in Python (0 LLM quota)...")
            ddgs = DDGS()
            for lead in report["first_5_target_accounts"]:
                q = f"site:linkedin.com/in/ \"{lead['company_name']}\" \"{lead['ideal_buyer_title']}\" {lead['hq_city']}"
                try:
                    hits = ddgs.text(q, region=recon["region"], max_results=1)
                    lead["linkedin_url"] = hits[0]["href"] if hits else f"https://www.google.com/search?q={q.replace(' ', '+')}"
                except Exception:
                    lead["linkedin_url"] = f"https://www.google.com/search?q={q.replace(' ', '+')}"

            status.update(label=f"Complete via `{used_model}`!", state="complete", expanded=False)

        # --- 5. RENDER BEAST DASHBOARD ---
        st.divider()
        c1, c2, c3 = st.columns([1.5, 1, 2.5])
        c1.metric("Market Fit Verdict", report["verdict_badge"])
        c2.metric("Overall Fit Score", f"{report['overall_fit_score']}/100")
        c3.warning(f"**Unit-Economics & Labor Arbitrage Test:**\n{report['unit_economics_arbitrage_test']}")

        st.info(f"**Executive Thesis:** {report['executive_thesis']}\n\n**Recommended Pricing Architecture:** {report['recommended_pricing_architecture']}")

        # Deterministic Telemetry Bar
        st.markdown("##### 🔍 Deterministic Site Telemetry (Detected in Python)")
        t_cols = st.columns(len(recon["telemetry"]))
        for idx, (k, v) in enumerate(recon["telemetry"].items()):
            t_cols[idx].metric(k, "✅ Yes" if v else "❌ Missing")

        ps = report["psych_scores"]
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Trust Alignment", f"{ps['trust_alignment']}/100")
        s2.metric("Habit Switch Ease", f"{ps['habit_friction_score']}/100")
        s3.metric("Price Elasticity Fit", f"{ps['price_elasticity_fit']}/100")
        s4.metric("Status Signaling Value", f"{ps['status_signaling_value']}/100")

        t1, t2, t3, t4, t5 = st.tabs([
            "🎯 5 Verified Target Accounts + LinkedIn DMs",
            "🧠 Buying Committee Game Theory",
            "⚔️ Competitor Psychological Battlecards",
            "🚀 3-Phase Scaling Playbook",
            "🔎 Raw 6-Layer Scraped Evidence"
        ])

        with t1:
            st.subheader("Autonomous Target Buyer Discovery & Bias-Matched Outreach")
            leads_df = pd.DataFrame(report["first_5_target_accounts"])
            st.dataframe(leads_df, use_container_width=True)
            st.download_button(
                "📥 Download 5 Target Accounts + LinkedIn URLs & DMs (CSV)",
                data=leads_df.to_csv(index=False).encode("utf-8"),
                file_name=f"{recon['brand']}_target_leads.csv",
                mime="text/csv"
            )

        with t2:
            cols = st.columns(len(report["buying_committee_simulation"]))
            for idx, node in enumerate(report["buying_committee_simulation"]):
                with cols[idx]:
                    st.markdown(f"#### {node['persona_role']}")
                    st.caption(f"Bias: `{node['cognitive_bias_triggered']}`")
                    st.progress(min(max(node["veto_power_score"], 0), 100), text=f"Veto Risk: {node['veto_power_score']}%")
                    st.write(f"*\"{node['internal_monologue']}\"*")
                    st.success(f"**Counter-Move:** {node['counter_move']}")

        with t3:
            st.dataframe(pd.DataFrame(report["competitor_battlecards"]), use_container_width=True)

        with t4:
            for phase in report["ideal_scaling_blueprint"]:
                with st.expander(f"📌 {phase['phase']} — Beachhead: {phase['target_beachhead']}", expanded=True):
                    st.write(f"**Move:** {phase['strategic_move']}")
                    st.caption(f"**Psychological Trigger:** `{phase['psychological_trigger_used']}`")

        with t5:
            st.json(recon["harvest"])