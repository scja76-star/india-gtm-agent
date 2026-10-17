import streamlit as st
import requests
import json
import time
import pandas as pd
from pydantic import BaseModel, Field
from typing import List
from ddgs import DDGS
from google import genai
from google.genai import types

st.set_page_config(page_title="LogosGTM: Behavioral & Cultural Fit Engine", layout="wide")
st.title("🧠 LogosGTM: Deep Multi-Source Behavioral Psychology & Market-Fit Engine")
st.caption("Powered by Gemini 3.8 Flash | Crawls Product + Pricing + Reddit Dark-Funnel + Review Friction to simulate Indian Buyer Psychology.")

# --- 1. STRICT PYDANTIC SCHEMAS (NO OPEN DICTS = NO additionalProperties ERROR) ---
class PsychScores(BaseModel):
    trust_alignment: int = Field(description="0-100 score: How much Indian enterprise/SMB buyers will trust this brand")
    habit_friction_score: int = Field(description="0-100 score: Ease of switching from existing WhatsApp/Excel/Zoho habits (higher = easier)")
    price_elasticity_fit: int = Field(description="0-100 score: How well their pricing fits Indian ROI & PPP expectations")
    status_signaling_value: int = Field(description="0-100 score: Does using this product make the Indian buyer look elite/modern?")

class PsychPersonaNode(BaseModel):
    persona_role: str = Field(description="e.g., The CFO (Loss Aversion), The End-User (Habit Inertia), The Champion (Status Signaling)")
    cognitive_bias_triggered: str = Field(description="Specific psychological bias triggered (e.g., Status Quo Bias, Ambiguity Effect, Social Proof Deficit)")
    internal_monologue: str = Field(description="Brutally honest 25-word monologue of what this Indian stakeholder secretly thinks")
    veto_power_score: int = Field(description="0 to 100 probability this person blocks the deal")

class BehavioralAdaptation(BaseModel):
    dimension: str = Field(description="e.g., Trust Architecture, Pricing Psychology, Workflow Habit Loop, Brand Positioning")
    current_western_assumption: str = Field(description="What the startup currently assumes works in the US/West")
    indian_psychological_reality: str = Field(description="Why that fails psychologically or culturally in India")
    exact_adaptation_action: str = Field(description="Concrete, non-obvious product or GTM change required")

class ScalingPhase(BaseModel):
    phase: str = Field(description="Phase 1 (Days 1-30 Wedge), Phase 2 (Days 31-90 Trust Engine), Phase 3 (Scale Moat)")
    strategic_move: str = Field(description="Exact high-leverage growth mechanism tailored to this brand")
    psychological_trigger_used: str = Field(description="Why this unlocks Indian enterprise or consumer adoption")
    target_beachhead: str = Field(description="Specific micro-segment or city/vertical to dominate first")

class DeepBehavioralReport(BaseModel):
    brand_name: str
    verdict_badge: str = Field(description="Strictly one of: 'STRONG FIT (GO)', 'CONDITIONAL FIT (REQUIRES PIVOT)', or 'POOR FIT (NO-GO FOR INDIA)'")
    overall_fit_score: int = Field(description="0-100 composite behavioral & economic fit score")
    the_3_interns_test: str = Field(description="Does this beat hiring cheap local manual labor or WhatsApp+Excel in India? Explain brutally in 30 words.")
    executive_thesis: str = Field(description="40-word deep strategic synthesis on whether India fits their brand DNA and why.")
    psych_scores: PsychScores
    buying_committee_simulation: List[PsychPersonaNode]
    cultural_adaptation_matrix: List[BehavioralAdaptation]
    ideal_scaling_blueprint: List[ScalingPhase]

# --- 2. DEEP MULTI-SOURCE PYTHON HARVESTER (0 LLM QUOTA) ---
@st.cache_data(ttl=3600)
def deep_multi_source_harvester(raw_url: str) -> dict:
    clean_url = raw_url.strip().rstrip("/")
    if not clean_url.startswith("http"):
        clean_url = "https://" + clean_url
    domain = clean_url.replace("https://", "").replace("http://", "").split("/")[0].replace("www.", "")
    brand_slug = domain.split(".")[0]

    harvest = {}
    for page_name, path in [("homepage", ""), ("pricing_page", "/pricing")]:
        try:
            r = requests.get(f"https://r.jina.ai/{clean_url}{path}", timeout=12)
            harvest[page_name] = r.text[:3500] if r.status_code == 200 else "Not found"
        except Exception:
            harvest[page_name] = "Could not scrape path."

    queries = {
        "reddit_voice_of_customer": f"site:reddit.com \"{brand_slug}\" OR \"{domain}\" review OR alternative OR problem OR pricing",
        "g2_and_user_friction": f"\"{domain}\" OR \"{brand_slug}\" reviews complaints cons pricing G2 Capterra",
        "indian_market_context": f"{brand_slug} alternatives India INR pricing Zoho Freshworks local competitors market"
    }
    ddgs = DDGS()
    for key, q in queries.items():
        try:
            res = ddgs.text(q, region="in-en", max_results=5)
            harvest[key] = "\n".join([f"- {x.get('title')}: {x.get('body')}" for x in res]) if res else "No direct threads found."
        except Exception as e:
            harvest[key] = f"Search skipped: {e}"

    return {"domain": domain, "brand": brand_slug, "data": harvest}

# --- 3. GEMINI 3.8 FLASH FAILOVER ROUTER ---
MODEL_CHAIN = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash"
]

def run_behavioral_simulation(client, prompt: str):
    last_err = None
    for model_name in MODEL_CHAIN:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=DeepBehavioralReport,
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

# --- 4. UI & EXECUTION ---
api_key = st.sidebar.text_input("Google AI Studio API Key:", type="password")
target_url = st.text_input("Enter Any Global Brand or Startup URL to Deep-Scan:", "https://linear.app")

if st.button("Run Deep 5-Layer Scrape & Behavioral Fit Simulation 🧠"):
    if not api_key:
        st.error("Please enter your Google AI Studio API Key in the sidebar.")
    else:
        client = genai.Client(api_key=api_key)
        with st.status("Executing 5-Layer Deep Web Harvest (0 LLM Quota)...", expanded=True) as status:
            st.write("1️⃣ Crawling Live Homepage & `/pricing` architecture...")
            st.write("2️⃣ Mining Reddit Dark-Funnel & G2/Review customer friction...")
            st.write("3️⃣ Extracting Indian category substitutes & labor-arbitrage benchmarks...")
            harvested = deep_multi_source_harvester(target_url)

            st.write("4️⃣ Running Game-Theoretic Buying Committee Simulation on `gemini-3.8-flash`...")
            master_prompt = f"""
            You are an elite Behavioral Economist (trained in Kahneman Prospect Theory, Cialdini Trust Mechanics, and Indian Cultural Psychology) and Venture Strategist.
            Perform a deep, non-obvious evaluation of whether '{harvested['domain']}' is a genuine fit for the Indian market or if it will fail due to psychological, workflow, or unit-economic friction.

            --- LAYER 1: LIVE HOMEPAGE DATA ---
            {harvested['data']['homepage']}

            --- LAYER 2: LIVE PRICING PAGE DATA ---
            {harvested['data']['pricing_page']}

            --- LAYER 3: REDDIT DARK-FUNNEL & USER SKEPTICISM ---
            {harvested['data']['reddit_voice_of_customer']}

            --- LAYER 4: REVIEW FRICTION & CONS ---
            {harvested['data']['g2_and_user_friction']}

            --- LAYER 5: INDIAN MARKET & LOCAL ALTERNATIVES ---
            {harvested['data']['indian_market_context']}

            INSTRUCTIONS:
            - Do NOT flatter the startup. If their product can be replaced in India by cheap human interns or WhatsApp+Excel, call it out brutally in `the_3_interns_test` and give a 'CONDITIONAL FIT' or 'POOR FIT (NO-GO)' verdict.
            - Ground every insight in behavioral psychology (Loss Aversion, Status Quo Bias, Collectivist Social Proof, Ambiguity Avoidance, Status Signaling).
            """
            report, used_model = run_behavioral_simulation(client, master_prompt)
            status.update(label=f"Deep Behavioral Simulation Complete via `{used_model}`!", state="complete", expanded=False)

        # --- 5. EXECUTIVE VISUALIZATION ---
        st.divider()
        c1, c2, c3 = st.columns([2, 1, 2])
        c1.metric("Brand Fit Verdict", report["verdict_badge"])
        c2.metric("Overall Fit Score", f"{report['overall_fit_score']}/100")
        c3.warning(f"**The '3-Interns & WhatsApp' Benchmark:**\n{report['the_3_interns_test']}")

        st.info(f"**Executive Thesis:** {report['executive_thesis']}")

        # Render the 4 Psychological Dimension Scores
        ps = report["psych_scores"]
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Trust Alignment", f"{ps['trust_alignment']}/100")
        s2.metric("Habit Switch Ease", f"{ps['habit_friction_score']}/100")
        s3.metric("Price Elasticity Fit", f"{ps['price_elasticity_fit']}/100")
        s4.metric("Status Signaling Value", f"{ps['status_signaling_value']}/100")

        tab1, tab2, tab3, tab4 = st.tabs([
            "🧠 Buying Committee Game Theory",
            "🔄 Psychological Adaptation Matrix",
            "🚀 Ideal 3-Phase Scaling Blueprint",
            "🔎 Raw 5-Layer Scraped Evidence"
        ])

        with tab1:
            st.subheader("Adversarial Buying Committee Simulation (Why Deals Stall in the Dark Funnel)")
            cols = st.columns(len(report["buying_committee_simulation"]))
            for idx, node in enumerate(report["buying_committee_simulation"]):
                with cols[idx]:
                    st.markdown(f"#### {node['persona_role']}")
                    st.caption(f"**Bias Triggered:** `{node['cognitive_bias_triggered']}`")
                    st.progress(min(max(node["veto_power_score"], 0), 100), text=f"Deal Veto Risk: {node['veto_power_score']}%")
                    st.write(f"*\"{node['internal_monologue']}\"*")

        with tab2:
            st.subheader("Western Assumption vs. Indian Psychological Reality")
            st.dataframe(pd.DataFrame(report["cultural_adaptation_matrix"]), use_container_width=True)

        with tab3:
            st.subheader("How to Scale Ideally in India (Behavioral GTM Playbook)")
            for phase in report["ideal_scaling_blueprint"]:
                with st.expander(f"📌 {phase['phase']} — Beachhead: {phase['target_beachhead']}", expanded=True):
                    st.markdown(f"**Strategic Move:** {phase['strategic_move']}")
                    st.markdown(f"**Psychological Lever:** `{phase['psychological_trigger_used']}`")

        with tab4:
            st.json(harvested["data"])