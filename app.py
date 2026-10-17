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

st.set_page_config(page_title="LogosNexus: Industry Pain-Miner & Causal Graph Engine", layout="wide")
st.title("🕸️ LogosNexus: Autonomous Industry Problem-Miner & Causal Graph Architect")
st.caption("Mines Live Human Complaints & Incumbent Failures • Maps Discrete-Math Causal Bottleneck Graphs • Architects Novel First-Principles Solutions")

# --- 1. STRICT PYDANTIC SCHEMAS FOR CAUSAL GRAPH & PROBLEM INVENTION ---
class CausalGraphEdge(BaseModel):
    source_node: str = Field(description="Short 2-4 word cause node (e.g., 'Fragmented WhatsApp Orders')")
    target_node: str = Field(description="Short 2-4 word effect node (e.g., '18% Inventory Spoilage')")
    relationship_label: str = Field(description="1-3 word causal link (e.g., 'triggers', 'blocks', 'inflates')")
    severity_weight: int = Field(description="1 to 10 weight of how painful this link is")

class ValidatedPainCluster(BaseModel):
    problem_title: str = Field(description="Sharp, specific name of the unsolved industry problem")
    who_is_bleeding: str = Field(description="Exact job title & company type suffering from this daily")
    current_broken_workaround: str = Field(description="How they currently patch this (e.g., Excel + 3 interns + legacy ERP)")
    hidden_psychological_barrier: str = Field(description="Exact cognitive bias or fear preventing them from fixing it (e.g., Status Quo Bias, Audit Fear)")
    annual_dollar_or_time_bleed: str = Field(description="Quantified cost of inaction per company (in USD/INR or hours/month)")
    pain_centrality_score: int = Field(description="0-100 mathematical severity & urgency score")

class NovelSolutionBlueprint(BaseModel):
    product_codename: str = Field(description="Memorable name for this new solution/startup")
    false_industry_dogma: str = Field(description="Philosophical First-Principles critique: What 99% of the industry falsely assumes")
    contrarian_breakthrough_mechanism: str = Field(description="The out-of-the-box, novel mechanism that solves the root bottleneck 10x better")
    autonomous_workflow_steps: List[str] = Field(description="4 concrete steps of how this AI/system works under the hood without human babysitting")
    trojan_horse_wedge: str = Field(description="Tiny, zero-friction entry point to get buyers addicted in 48 hours without ripping out old software")
    outcome_pricing_model: str = Field(description="Exact risk-free, outcome-based pricing formula (in INR and USD)")
    mvp_python_starter_blueprint: str = Field(description="Clean 25-line Python pseudo-code / architecture snippet showing how to build this exact agent")

class IndustryDiscoveryReport(BaseModel):
    industry_analyzed: str
    root_keystone_bottleneck: str = Field(description="The #1 mathematical root bottleneck node driving 80% of downstream pain in this sector")
    executive_insight: str = Field(description="40-word non-obvious synthesis connecting the live scraped complaints to a massive market gap")
    top_3_bleeding_problems: List[ValidatedPainCluster]
    causal_pain_graph_edges: List[CausalGraphEdge]
    flagship_novel_solution: NovelSolutionBlueprint
    cold_hijack_message: str = Field(description="35-word reply/DM you can send today to the people complaining in the scraped threads")

# --- 2. LIVE 4-STREAM FRUSTRATION & PAIN HARVESTER (0 LLM QUOTA) ---
@st.cache_data(ttl=3600)
def mine_live_industry_pain(industry_query: str, market_geo: str) -> dict:
    region_code = "in-en" if "India" in market_geo else "us-en"
    geo_tag = "India" if region_code == "in-en" else "USA"

    search_streams = {
        "Reddit Rants & Manual Nightmares": f"site:reddit.com {industry_query} (\"manual\" OR \"wasting hours\" OR \"hate\" OR \"nightmare\" OR \"broken\" OR \"spreadsheet\")",
        "Software Failures & 1-Star Friction": f"{industry_query} software (\"worst\" OR \"too expensive\" OR \"clunky\" OR \"switching from\" OR \"cons\") reviews",
        "Active Hiring & Labor Bottlenecks": f"{industry_query} {geo_tag} (\"hiring\" OR \"freelancer\" OR \"automate\" OR \"operations\" OR \"data entry\" OR \"backoffice\")",
        "Unmet Regulatory & Cost Pressures": f"{industry_query} {geo_tag} bottlenecks challenges 2026 cost margin"
    }

    ddgs = DDGS()
    raw_text_blocks = {}
    live_signal_links = []

    for stream_name, query in search_streams.items():
        try:
            results = ddgs.text(query, region=region_code, max_results=5)
            lines = []
            for r in results:
                title = r.get("title", "")
                body = r.get("body", "")
                href = r.get("href", "")
                lines.append(f"- [{title}]: {body}")
                if href:
                    live_signal_links.append({
                        "Signal Category": stream_name,
                        "Live Discussion / Complaint Title": title[:85],
                        "Pain Snippet": body[:140] + "...",
                        "Live URL": href
                    })
            raw_text_blocks[stream_name] = "\n".join(lines) if lines else "No direct hits."
        except Exception as e:
            raw_text_blocks[stream_name] = f"Stream skipped: {e}"

    return {"text_blocks": raw_text_blocks, "live_links": live_signal_links}

# --- 3. DETERMINISTIC PYTHON GRAPHVIZ BUILDER (DISCRETE MATH DAG) ---
def build_causal_graphviz(edges: list, keystone_node: str) -> str:
    dot = [
        "digraph CausalPainGraph {",
        "  rankdir=LR;",
        "  node [shape=box, style=\"rounded,filled\", fontname=\"Helvetica\", fontsize=11, fillcolor=\"#1E293B\", fontcolor=\"white\", color=\"#38BDF8\"];",
        "  edge [fontname=\"Helvetica\", fontsize=9, color=\"#94A3B8\", fontcolor=\"#F8FAFC\"];",
        "  bgcolor=\"#0F172A\";"
    ]
    for e in edges:
        src = e["source_node"].replace('"', "'")
        tgt = e["target_node"].replace('"', "'")
        lbl = f"{e['relationship_label']} (w={e['severity_weight']})"
        penwidth = max(1, int(e["severity_weight"] / 3))
        edge_color = "#F43F5E" if e["severity_weight"] >= 8 else "#38BDF8"
        dot.append(f'  "{src}" -> "{tgt}" [label="{lbl}", penwidth={penwidth}, color="{edge_color}"];')
    dot.append("}")
    return "\n".join(dot)

# --- 4. GEMINI 3.8 FLASH FAILOVER ROUTER ---
MODEL_CHAIN = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash"]

def run_pain_to_solution_engine(client, prompt: str):
    last_err = None
    for model_name in MODEL_CHAIN:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IndustryDiscoveryReport,
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

# --- 5. STATE, PRE-FIXED KEY SHIELD & UI ---
if "scans_used" not in st.session_state:
    st.session_state.scans_used = 0
if "nexus_report" not in st.session_state:
    st.session_state.nexus_report = None
if "nexus_links" not in st.session_state:
    st.session_state.nexus_links = []

prefixed_key = ""
vip_code_secret = "YC2026"
try:
    prefixed_key = st.secrets.get("GEMINI_API_KEY", "")
    vip_code_secret = st.secrets.get("VIP_PASSCODE", "YC2026")
except Exception:
    pass

with st.sidebar:
    st.header("⚡ LogosNexus Controls")
    market_geo = st.radio("Target Market Focus:", ["India Market (INR / MSMEs / GCCs) 🇮🇳", "US & Global Enterprise (USD) 🇺🇸"])
    free_left = max(0, 3 - st.session_state.scans_used)
    st.metric("Free Instant Scans Left", f"{free_left} / 3")
    with st.expander("🔓 VIP Passcode / Custom Key"):
        vip_input = st.text_input("Enter VIP Code (`YC2026`) or Gemini Key:", type="password")

active_api_key = prefixed_key
is_unlimited = False
if vip_input == vip_code_secret and prefixed_key:
    is_unlimited = True
    st.sidebar.success("VIP Unlimited Mode Active!")
elif vip_input.startswith("AIza"):
    active_api_key = vip_input
    is_unlimited = True

st.write("**1-Click Deep Industry Pain Presets (or type ANY Industry, Niche, or Software Category below):**")
p1, p2, p3, p4 = st.columns(4)
if "ind_input" not in st.session_state:
    st.session_state.ind_input = "Indian D2C E-Commerce & Quick-Commerce Brands"
if p1.button("📦 Indian D2C & Quick-Commerce"):
    st.session_state.ind_input = "Indian D2C E-Commerce & Quick-Commerce Brands"
if p2.button("🏥 Healthcare Clinics & Diagnostics"):
    st.session_state.ind_input = "Private Healthcare Clinics & Diagnostic Labs Billing Operations"
if p3.button("🚚 B2B Freight & Supply Chain"):
    st.session_state.ind_input = "B2B Freight Forwarding, Customs & Logistics Brokers"
if p4.button("⚖️ CA Firms & Compliance Ops"):
    st.session_state.ind_input = "Chartered Accountants, GST/Tax Compliance & Audit Firms"

industry_input = st.text_input("Enter Any Industry, Niche, or Competitor Category to Mine Unsolved Problems:", value=st.session_state.ind_input)

if st.button("Mine Live Industry Frustrations, Map Causal Graph & Invent Solution 🚀"):
    if not active_api_key:
        st.error("Add GEMINI_API_KEY to `.streamlit/secrets.toml` or paste your key in the sidebar.")
    elif not is_unlimited and st.session_state.scans_used >= 3:
        st.warning("3 free scans used! Enter VIP Code `YC2026` or your own Gemini key in the sidebar.")
    else:
        if not is_unlimited:
            st.session_state.scans_used += 1

        client = genai.Client(api_key=active_api_key)
        with st.status("Mining Live Rants, 1-Star Software Failures & Constructing Causal Graph...", expanded=True) as status:
            st.write("1️⃣ Scraping Reddit rants, G2 software failures, & labor bottlenecks in Python (0 LLM quota)...")
            mined = mine_live_industry_pain(industry_input, market_geo)

            st.write("2️⃣ Running Graph-Theoretic Bottleneck Analysis & First-Principles Solution Synthesis (`gemini-3.8-flash`)...")
            prompt = f"""
            You are an elite Venture Scientist, Discrete Mathematician (Graph Theory & Mechanism Design), First-Principles Philosopher, and Behavioral Psychologist.
            Analyze the live, unfiltered pain signals scraped from the wild for the sector: '{industry_input}' in '{market_geo}'.

            LIVE SCRAPED FRUSTRATION & MARKET EVIDENCE:
            {json.dumps(mined['text_blocks'], indent=2)}

            INSTRUCTIONS:
            1. Do NOT suggest generic chatbots or basic wrappers. Find the deep, structural, high-bleed operational bottlenecks where existing software fails and humans are stuck doing painful workarounds.
            2. Model the industry's problems as a Directed Causal Graph (6 to 8 edges showing how root friction causes downstream financial bleed).
            3. Expose the 'False Industry Dogma' from philosophical first principles, and invent a truly novel, autonomous agentic system that solves the root keystone bottleneck.
            """
            report, used_model = run_pain_to_solution_engine(client, prompt)
            st.session_state.nexus_report = report
            st.session_state.nexus_links = mined["live_links"]
            status.update(label=f"Discovery Complete via `{used_model}`!", state="complete", expanded=False)

# --- 6. RENDER THE OUT-OF-THE-BOX NEXUS DASHBOARD ---
if st.session_state.nexus_report:
    rep = st.session_state.nexus_report
    links = st.session_state.nexus_links

    st.divider()
    k1, k2 = st.columns([1.2, 2.8])
    k1.error(f"🎯 **Root Keystone Bottleneck:**\n### {rep['root_keystone_bottleneck']}")
    k2.info(f"🧠 **First-Principles Executive Synthesis:**\n{rep['executive_insight']}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🕸️ Discrete-Math Causal Pain Graph",
        "💡 Novel Solution Architect + Starter Code",
        "🩸 Top 3 Quantified Bleeding Problems",
        "🔥 Live Scraped Complaint URLs (Warm Leads)"
    ])

    with tab1:
        st.subheader("🕸️ Directed Acyclic Graph (DAG) of Industry Friction & Financial Bleed")
        st.caption("Red thick edges (weight ≥ 8) indicate critical-path bottlenecks where solving 1 root node eliminates multiple downstream failures.")
        dot_code = build_causal_graphviz(rep["causal_pain_graph_edges"], rep["root_keystone_bottleneck"])
        st.graphviz_chart(dot_code, use_container_width=True)
        st.dataframe(pd.DataFrame(rep["causal_pain_graph_edges"]), use_container_width=True)

    with tab2:
        sol = rep["flagship_novel_solution"]
        st.subheader(f"🚀 Flagship Invention Blueprint: **{sol['product_codename']}**")
        c_a, c_b = st.columns(2)
        c_a.warning(f"**❌ False Industry Dogma (What Everyone Blindly Assumes):**\n{sol['false_industry_dogma']}")
        c_b.success(f"**⚡ Contrarian First-Principles Breakthrough:**\n{sol['contrarian_breakthrough_mechanism']}")

        w1, w2 = st.columns(2)
        w1.metric("48-Hour Trojan Horse Wedge", sol["trojan_horse_wedge"])
        w2.metric("Outcome-Based Pricing Formula", sol["outcome_pricing_model"])

        st.markdown("#### ⚙️ Autonomous 4-Step System Architecture")
        for idx, step in enumerate(sol["autonomous_workflow_steps"], 1):
            st.write(f"**{idx}.** {step}")

        st.markdown("#### 💻 Auto-Generated Python Agent Blueprint (Copy-Paste to Build This Today)")
        st.code(sol["mvp_python_starter_blueprint"], language="python")

    with tab3:
        st.subheader("🩸 Top 3 High-Centrality Bleeding Problems in This Sector")
        cols = st.columns(len(rep["top_3_bleeding_problems"]))
        for idx, prob in enumerate(rep["top_3_bleeding_problems"]):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"### #{idx+1}: {prob['problem_title']}")
                    st.progress(min(max(prob["pain_centrality_score"], 0), 100), text=f"Pain Centrality Score: {prob['pain_centrality_score']}/100")
                    st.markdown(f"**👤 Who Is Bleeding:** {prob['who_is_bleeding']}")
                    st.markdown(f"**🛠️ Broken Workaround:** {prob['current_broken_workaround']}")
                    st.markdown(f"**🧠 Psychological Lock:** `{prob['hidden_psychological_barrier']}`")
                    st.error(f"**💸 Cost of Inaction:** {prob['annual_dollar_or_time_bleed']}")

    with tab4:
        st.subheader("🔥 Live Scraped Human Complaints, Rants & Job Signals (Click to Hijack)")
        st.caption("These are 100% real, non-hallucinated web threads and signals scraped in real time. Click any URL to see the real people discussing this pain.")
        if links:
            links_df = pd.DataFrame(links)
            st.dataframe(
                links_df,
                column_config={"Live URL": st.column_config.LinkColumn("Click to Open Live Thread")},
                use_container_width=True
            )
        st.markdown("#### 📲 Ready-to-Send DM/Reply to People in Those Threads")
        st.code(rep["cold_hijack_message"], language="text")