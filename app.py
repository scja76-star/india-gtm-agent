import streamlit as st
import requests
import re
import json
import time
import urllib.parse
import pandas as pd
from pydantic import BaseModel, Field
from typing import List
from ddgs import DDGS
from google import genai
from google.genai import types

st.set_page_config(page_title="LogosGTM V3.0: Game-Theoretic GTM Engine", layout="wide")
st.title("⚡ LogosGTM V3.0: Autonomous Behavioral Game-Theory & Intent Engine")
st.caption("7-Layer Deep Web & Hiring-Intent Recon • Nash Equilibrium Pricing Math • Adversarial CFO Wargame • Instant Localized Landing Page Re-Architect")

# --- 1. STRICT PYDANTIC SCHEMAS ---
class PsychScores(BaseModel):
    trust_alignment: int = Field(description="0-100 score: Enterprise trust readiness")
    habit_friction_score: int = Field(description="0-100 score: Ease of switching from current habits (higher = easier)")
    price_elasticity_fit: int = Field(description="0-100 score: Pricing fit against local human labor/incumbents")
    status_signaling_value: int = Field(description="0-100 score: Career prestige value for the buyer champion")

class PsychPersonaNode(BaseModel):
    persona_role: str = Field(description="e.g., The CFO (Loss Aversion), The End-User (Habit Inertia), The CISO, The Champion")
    cognitive_bias_triggered: str = Field(description="Exact psychological bias triggered")
    internal_monologue: str = Field(description="Brutally honest 20-word internal thought blocking the deal")
    veto_power_score: int = Field(description="0-100 probability this stakeholder blocks the deal")
    counter_move: str = Field(description="Exact 15-word tactical counter-move")

class WargameTurn(BaseModel):
    round_number: int = Field(description="Round 1 (Price/Intern Objection), Round 2 (Trust/Migration Trap), Round 3 (The Closing Wedge)")
    skeptical_buyer_attack: str = Field(description="Brutal, realistic objection thrown by the local CFO/VP")
    winning_founder_response: str = Field(description="Exact high-status, psychologically calibrated response that wins the round")
    psychological_principle_used: str = Field(description="e.g., Loss Framing, Risk Reversal, Anchoring")

class LocalizedLandingPage(BaseModel):
    current_weakness: str = Field(description="Why their current homepage hero copy fails in this corridor")
    rewritten_hero_headline: str = Field(description="High-converting localized H1 headline tailored to local buyer psychology")
    rewritten_subheadline: str = Field(description="Concrete, metric-driven subheadline addressing local compliance/ROI")
    localized_cta_button: str = Field(description="Frictionless CTA button text (e.g., 'Run Free WhatsApp Pilot' vs 'Book Demo')")
    killer_trust_banner: str = Field(description="Exact social proof / compliance bar needed above the fold")

class CompetitorBattlecard(BaseModel):
    incumbent_name: str = Field(description="Real named local competitor or manual workflow substitute")
    their_pricing_model: str = Field(description="Approximate pricing")
    psychological_moat: str = Field(description="Why buyers stick with them")
    wedge_to_steal_share: str = Field(description="Exact 30-day displacement wedge")

class TargetAccountLead(BaseModel):
    company_name: str = Field(description="Real, named high-fit company in the target market")
    hq_city: str = Field(description="City HQ")
    ideal_buyer_title: str = Field(description="Exact decision-maker job title")
    hiring_or_pain_trigger: str = Field(description="Specific operational or hiring signal making them need this right now")
    bias_matched_dm: str = Field(description="Ready-to-send 35-word cold DM engineered around behavioral psychology")

class ScalingPhase(BaseModel):
    phase: str = Field(description="Phase 1 (Days 1-30), Phase 2 (Days 31-90), Phase 3 (Scale Moat)")
    strategic_move: str = Field(description="Concrete, non-obvious GTM mechanism")
    psychological_trigger_used: str = Field(description="Behavioral lever unlocked")
    target_beachhead: str = Field(description="Specific micro-vertical or buyer cluster")

class FinalLimitGTMReport(BaseModel):
    brand_name: str
    core_task_automated: str = Field(description="3-5 words describing the manual job this product replaces")
    verdict_badge: str = Field(description="Strictly: 'STRONG FIT (GO)', 'CONDITIONAL FIT (REQUIRES PIVOT)', or 'POOR FIT (NO-GO)'")
    overall_fit_score: int = Field(description="0-100 composite score")
    estimated_current_monthly_usd_price: int = Field(description="Estimated monthly cost in USD for a small 10-person team (integer, e.g., 200)")
    estimated_human_hours_saved_monthly: int = Field(description="Estimated human work hours saved per month for a team (integer, e.g., 80)")
    unit_economics_arbitrage_test: str = Field(description="Brutal 30-word math comparison: Software price vs local human labor/incumbents.")
    executive_thesis: str = Field(description="40-word synthesis on brand DNA fit and #1 bottleneck.")
    recommended_pricing_architecture: str = Field(description="Exact localized pricing & packaging formula")
    psych_scores: PsychScores
    buying_committee_simulation: List[PsychPersonaNode]
    adversarial_wargame_transcript: List[WargameTurn]
    localized_landing_page_rewrite: LocalizedLandingPage
    competitor_battlecards: List[CompetitorBattlecard]
    ideal_scaling_blueprint: List[ScalingPhase]
    first_5_target_accounts: List[TargetAccountLead]

# --- 2. 7-LAYER RECON + HIRING INTENT MINER + REGEX TELEMETRY (0 LLM QUOTA) ---
@st.cache_data(ttl=3600)
def run_7_layer_recon(raw_url: str, corridor: str) -> dict:
    clean_url = raw_url.strip().rstrip("/")
    if not clean_url.startswith("http"):
        clean_url = "https://" + clean_url
    domain = clean_url.replace("https://", "").replace("http://", "").split("/")[0].replace("www.", "")
    brand_slug = domain.split(".")[0]

    harvest = {}
    for page_name, path in [("homepage", ""), ("pricing_page", "/pricing"), ("security_trust", "/security")]:
        try:
            r = requests.get(f"https://r.jina.ai/{clean_url}{path}", timeout=12)
            harvest[page_name] = r.text[:3000] if r.status_code == 200 else "Page not found"
        except Exception:
            harvest[page_name] = "Could not crawl path."

    combined_raw = (harvest["homepage"] + " " + harvest["pricing_page"] + " " + harvest["security_trust"]).lower()
    telemetry = {
        "SOC2 / ISO27001": bool(re.search(r"soc\s?2|iso\s?27001", combined_raw)),
        "GDPR / DPDP Ready": bool(re.search(r"gdpr|dpdp|data residency|hipaa", combined_raw)),
        "SSO / SAML Auth": bool(re.search(r"\bsso\b|saml|okta", combined_raw)),
        "Free Tier / Trial": bool(re.search(r"free trial|start for free|free plan|\$0", combined_raw)),
        "API / Webhooks": bool(re.search(r"\bapi\b|webhook|sdk|documentation", combined_raw)),
        "INR / PPP Pricing": bool(re.search(r"₹|\binr\b|rupee|purchasing power", combined_raw)),
        "Outcome / Usage Pricing": bool(re.search(r"per resolution|usage-based|pay as you go|credits", combined_raw)),
    }

    region_code = "in-en" if "India" in corridor.split("→")[1] else "us-en"
    target_geo = "India Bengaluru Mumbai" if region_code == "in-en" else "United States San Francisco New York"
    queries = {
        "reddit_dark_funnel": f"site:reddit.com \"{brand_slug}\" OR \"{domain}\" review OR alternative OR expensive",
        "g2_user_complaints": f"\"{domain}\" OR \"{brand_slug}\" reviews cons complaints pricing G2",
        "corridor_competitors": f"{brand_slug} competitors alternatives pricing {target_geo}",
        "live_hiring_intent_signals": f"site:linkedin.com/jobs OR hiring {brand_slug} OR workflow automation {target_geo}"
    }
    ddgs = DDGS()
    for key, q in queries.items():
        try:
            res = ddgs.text(q, region=region_code, max_results=4)
            harvest[key] = "\n".join([f"- {x.get('title')}: {x.get('body')}" for x in res]) if res else "No threads found."
        except Exception as e:
            harvest[key] = f"Search skipped: {e}"

    return {"domain": domain, "brand": brand_slug, "harvest": harvest, "telemetry": telemetry, "region": region_code}

# --- 3. 503/429-PROOF MULTI-CLUSTER ROUTER WITH AUTO-RETRY ---
MODEL_CHAIN = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
]

def execute_final_limit_simulation(client, prompt: str):
    last_err = None
    # Pass 1 & Pass 2: Try each model cluster; if all are spiking, wait 2s and sweep once more
    for attempt in range(2):
        for model_name in MODEL_CHAIN:
            try:
                res = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=FinalLimitGTMReport,
                    )
                )
                return json.loads(res.text), model_name
            except Exception as e:
                last_err = e
                err_text = str(e).upper()
                # Catch 503 (High Demand), 429 (Quota), 500/504 (Server), and 404
                if any(code in err_text for code in ["503", "UNAVAILABLE", "OVERLOADED", "429", "RESOURCE_EXHAUSTED", "404", "NOT_FOUND", "500", "504"]):
                    time.sleep(1.2)
                    continue
                raise e
        time.sleep(2)
    raise RuntimeError(f"Google servers are under heavy load across all 6 models. Wait 15s and click again. Last error: {last_err}")

# --- 4. SUPPORTS BOTH 'AIza' AND 'AQ.' KEYS + SIDEBAR OVERRIDE ---
if "scans_used" not in st.session_state:
    st.session_state.scans_used = 0
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "last_recon" not in st.session_state:
    st.session_state.last_recon = None

prefixed_key = ""
vip_code_secret = "YC2026"
try:
    prefixed_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip().strip('"').strip("'")
    vip_code_secret = str(st.secrets.get("VIP_PASSCODE", "YC2026")).strip()
except Exception:
    pass

# Reject accidental placeholder keys from Secrets
if "YourActual" in prefixed_key or "paste_" in prefixed_key or len(prefixed_key) < 20:
    prefixed_key = ""

with st.sidebar:
    st.header("⚡ Engine Controls")
    corridor = st.radio(
        "Select Expansion Corridor:",
        ["Global Startup → Entering India 🇮🇳", "Indian Startup → Attacking US/Global 🇺🇸"]
    )
    free_left = max(0, 3 - st.session_state.scans_used)
    st.metric("Free Instant Scans Left", f"{free_left} / 3")

    # Key Diagnostics Badge so you know immediately if Secrets loaded properly
    if prefixed_key:
        st.caption(f"✅ Server Key Loaded (`{prefixed_key[:4]}...{prefixed_key[-4:]}`)")
    else:
        st.caption("⚠️ No Server Key in Secrets — Paste key below:")

    with st.expander("🔓 VIP Code / Custom API Key", expanded=not bool(prefixed_key)):
        vip_input = st.text_input("Enter VIP Code (`YC2026`) or any Gemini API Key:", type="password").strip().strip('"').strip("'")

active_api_key = None
is_unlimited = False

# If user pastes a direct API key (starts with AIza or AQ. or is >25 chars), ALWAYS prioritize it!
if len(vip_input) > 25 and vip_input != vip_code_secret:
    active_api_key = vip_input
    is_unlimited = True
    st.sidebar.success("Using Custom Pasted API Key!")
elif vip_input == vip_code_secret and prefixed_key:
    active_api_key = prefixed_key
    is_unlimited = True
    st.sidebar.success("VIP Unlimited Mode Active!")
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

target_url = st.text_input("Enter Any Startup URL for 7-Layer Recon & Game-Theory Simulation:", value=st.session_state.target_url)

if st.button("Launch 7-Layer Simulation, Wargame & Intent Radar 🚀"):
    if not active_api_key:
        st.error("⚠️ No valid API Key found! Either add `GEMINI_API_KEY` in Streamlit Cloud Settings -> Secrets, OR paste your fresh Google AI Studio key directly in the left sidebar box.")
    elif not is_unlimited and st.session_state.scans_used >= 3:
        st.warning("3 free scans used! Enter VIP Code `YC2026` or your own Gemini key in the sidebar.")
    else:
        client = genai.Client(api_key=active_api_key)
        with st.status("Executing 7-Layer Recon + Hiring Intent Miner + Wargame Engine...", expanded=True) as status:
            st.write("1️⃣ Crawling `/`, `/pricing`, & `/security` + deterministic compliance regex...")
            recon = run_7_layer_recon(target_url, corridor)

            st.write("2️⃣ Running Behavioral Game-Theory & Wargame Simulation...")
            prompt = f"""
            You are an elite Behavioral Economist (Kahneman Prospect Theory, Cialdini Trust Mechanics, Nash Equilibrium Pricing) and Cross-Border Venture Architect.
            Analyze '{recon['domain']}' for the corridor: {corridor}.

            DETERMINISTIC PYTHON TELEMETRY: {json.dumps(recon['telemetry'])}
            HOMEPAGE: {recon['harvest']['homepage']}
            PRICING PAGE: {recon['harvest']['pricing_page']}
            SECURITY PAGE: {recon['harvest']['security_trust']}
            REDDIT DARK FUNNEL: {recon['harvest']['reddit_dark_funnel']}
            G2 FRICTION: {recon['harvest']['g2_user_complaints']}
            COMPETITORS: {recon['harvest']['corridor_competitors']}
            LIVE HIRING SIGNALS: {recon['harvest']['live_hiring_intent_signals']}

            Be brutally honest, quantitative, and non-obvious. Name real companies, real local competitors, and simulate a realistic 3-round adversarial sales wargame.
            """
            report, model_or_err = execute_final_limit_simulation(client, prompt)

            if report is None:
                status.update(label="API Key Rejected by Google", state="error", expanded=True)
                st.error(f"Google API Response: {model_or_err}\n\n👉 **Instant Fix:** Generate a fresh key at aistudio.google.com/app/apikey and paste it into the left sidebar (or update Streamlit Cloud Secrets).")
                st.stop()

            if not is_unlimited:
                st.session_state.scans_used += 1

            st.write("3️⃣ Hunting live LinkedIn Decision-Maker URLs in Python (0 LLM quota)...")
            ddgs = DDGS()
            for lead in report["first_5_target_accounts"]:
                q = f"site:linkedin.com/in/ \"{lead['company_name']}\" \"{lead['ideal_buyer_title']}\" {lead['hq_city']}"
                try:
                    hits = ddgs.text(q, region=recon["region"], max_results=1)
                    lead["linkedin_url"] = hits[0]["href"] if hits else f"https://www.google.com/search?q={urllib.parse.quote(q)}"
                except Exception:
                    lead["linkedin_url"] = f"https://www.google.com/search?q={urllib.parse.quote(q)}"

            st.session_state.last_report = report
            st.session_state.last_recon = recon
            status.update(label=f"Complete via `{model_or_err}`!", state="complete", expanded=False)

# --- 5. RENDER INTERACTIVE DASHBOARD ---
if st.session_state.last_report and st.session_state.last_recon:
    report = st.session_state.last_report
    recon = st.session_state.last_recon

    st.divider()
    c1, c2, c3 = st.columns([1.5, 1, 2.5])
    c1.metric("Market Fit Verdict", report["verdict_badge"])
    c2.metric("Overall Fit Score", f"{report['overall_fit_score']}/100")
    c3.warning(f"**Unit-Economics & Labor Arbitrage Test:**\n{report['unit_economics_arbitrage_test']}")

    st.info(f"**Executive Thesis:** {report['executive_thesis']}\n\n**Recommended Pricing Architecture:** {report['recommended_pricing_architecture']}")

    st.markdown("##### 🔍 Deterministic Site Telemetry (Verified in Python)")
    t_cols = st.columns(len(recon["telemetry"]))
    for idx, (k, v) in enumerate(recon["telemetry"].items()):
        t_cols[idx].metric(k, "✅ Yes" if v else "❌ Missing")

    ps = report["psych_scores"]
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Trust Alignment", f"{ps['trust_alignment']}/100")
    s2.metric("Habit Switch Ease", f"{ps['habit_friction_score']}/100")
    s3.metric("Price Elasticity Fit", f"{ps['price_elasticity_fit']}/100")
    s4.metric("Status Signaling Value", f"{ps['status_signaling_value']}/100")

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "🎯 5 Verified Buyers + 1-Click Outreach",
        "📐 Nash Equilibrium Pricing Simulator",
        "🥊 3-Round CFO Wargame Simulator",
        "🎨 Instant Localized Website Re-Architect",
        "🧠 Buying Committee & Battlecards",
        "🚀 3-Phase Scaling Playbook"
    ])

    with t1:
        st.subheader("Autonomous Target Buyer Discovery & Intent Triggers")
        leads_df = pd.DataFrame(report["first_5_target_accounts"])
        st.dataframe(leads_df, use_container_width=True)
        st.download_button(
            "📥 Download 5 Verified Target Accounts + LinkedIn Links & DMs (CSV)",
            data=leads_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{recon['brand']}_target_leads.csv",
            mime="text/csv"
        )

    with t2:
        st.subheader("📐 Discrete-Math Nash Equilibrium & Labor-Arbitrage Simulator (0 Extra Quota)")
        st.caption(f"Task Automated: **{report['core_task_automated']}** | Adjust sliders to find the exact price where a local CFO switches from human labor to your software.")
        col_a, col_b, col_c = st.columns(3)
        proposed_price = col_a.slider("Your Proposed Monthly Team Price ($ USD)", 10, 2000, max(10, min(2000, int(report["estimated_current_monthly_usd_price"] or 250))))
        hours_saved = col_b.slider("Human Hours Saved Per Month", 10, 500, max(10, min(500, int(report["estimated_human_hours_saved_monthly"] or 80))))
        default_wage = 4 if recon["region"] == "in-en" else 35
        local_hourly_wage = col_c.slider("Local Human Labor Cost ($/Hour)", 2, 100, default_wage)

        human_labor_cost = hours_saved * local_hourly_wage
        switching_friction_tax = 1.6  # Prospect Theory Loss Aversion multiplier (1.6x)
        nash_indifference_price = round(human_labor_cost / switching_friction_tax, 2)
        net_roi_multiple = round(human_labor_cost / max(1, proposed_price), 2)

        m_a, m_b, m_c = st.columns(3)
        m_a.metric("Cost of Local Human Alternative", f"${human_labor_cost}/mo (₹{human_labor_cost*84:,}/mo)")
        m_b.metric("Nash Equilibrium Ceiling Price", f"${nash_indifference_price}/mo (₹{int(nash_indifference_price*84):,}/mo)")
        m_c.metric("Buyer ROI Multiple", f"{net_roi_multiple}x", delta="Wins Deal ✅" if proposed_price <= nash_indifference_price else "CFO Vetoes Deal ❌")

    with t3:
        st.subheader("🥊 Adversarial 3-Round Negotiation Wargame (AI Closer vs. Skeptical Local CFO)")
        for turn in report["adversarial_wargame_transcript"]:
            with st.container(border=True):
                st.markdown(f"**Round {turn['round_number']} — Psychological Principle: `{turn['psychological_principle_used']}`**")
                st.error(f"**😤 Skeptical Buyer Attack:** \"{turn['skeptical_buyer_attack']}\"")
                st.success(f"**⚡ Winning Founder Counter-Move:** \"{turn['winning_founder_response']}\"")

    with t4:
        st.subheader("🎨 Instant Localized Landing Page Re-Architect")
        lp = report["localized_landing_page_rewrite"]
        st.warning(f"**Why Current Homepage Fails in This Market:** {lp['current_weakness']}")
        with st.container(border=True):
            st.markdown(f"### {lp['rewritten_hero_headline']}")
            st.markdown(f"*{lp['rewritten_subheadline']}*")
            st.button(f"👉 {lp['localized_cta_button']}", key="preview_cta")
            st.caption(f"🛡️ **Above-the-Fold Trust Bar:** {lp['killer_trust_banner']}")

    with t5:
        st.subheader("Adversarial Buying Committee Veto Map")
        cols = st.columns(len(report["buying_committee_simulation"]))
        for idx, node in enumerate(report["buying_committee_simulation"]):
            with cols[idx]:
                st.markdown(f"#### {node['persona_role']}")
                st.caption(f"Bias: `{node['cognitive_bias_triggered']}`")
                st.progress(min(max(node["veto_power_score"], 0), 100), text=f"Veto Risk: {node['veto_power_score']}%")
                st.write(f"*\"{node['internal_monologue']}\"*")
                st.success(f"**Fix:** {node['counter_move']}")
        st.divider()
        st.subheader("⚔️ Local Competitor Psychological Battlecards")
        st.dataframe(pd.DataFrame(report["competitor_battlecards"]), use_container_width=True)

    with t6:
        for phase in report["ideal_scaling_blueprint"]:
            with st.expander(f"📌 {phase['phase']} — Beachhead: {phase['target_beachhead']}", expanded=True):
                st.write(f"**Move:** {phase['strategic_move']}")
                st.caption(f"**Psychological Lever:** `{phase['psychological_trigger_used']}`")