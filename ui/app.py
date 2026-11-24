# ui/app.py
"""
Streamlit Web Application for InternGuide (Day 10 - Checkpoint 2).
Features:
1. Streamlit chat interface calling /ask or /agent endpoints (with in-process fallback).
2. Citations display for grounded answers.
3. Interactive Thumbs Up / Thumbs Down feedback saved to data/feedback.json.
4. Signature Feature: Colour-coded Credit Progress Bar toward AICTE 14-20 credit (630-900 hour) B.Tech target.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests
import streamlit as st

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optional in-process fallbacks
try:
    from app.graph import run_langgraph_agent
    from app.rag import ask as rag_ask
    LOCAL_MODULES_AVAILABLE = True
except Exception:
    LOCAL_MODULES_AVAILABLE = False

FEEDBACK_FILE = PROJECT_ROOT / "data" / "feedback.json"
FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

# AICTE Activity Category Colors & Metadata
ACTIVITY_HEADS = {
    "Industry / Corporate Internship": {
        "color": "#3b82f6",
        "gradient": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
        "icon": "🏢",
        "description": "Internship with registered industry, corporate firm, MSME, PSU, or startup."
    },
    "Rural / NSS / Social Internship": {
        "color": "#10b981",
        "gradient": "linear-gradient(135deg, #10b981 0%, #047857 100%)",
        "icon": "🌱",
        "description": "Rural development camp, NSS activities, community engagement, NGO work."
    },
    "Innovation / Incubation / Startup": {
        "color": "#8b5cf6",
        "gradient": "linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)",
        "icon": "💡",
        "description": "Campus incubation, patent/IPR filing, proof-of-concept prototype development."
    },
    "Hackathon / Technical Competition": {
        "color": "#f59e0b",
        "gradient": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
        "icon": "⚡",
        "description": "Institutional, state, or national-level hackathons and technical project contests."
    }
}

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="InternGuide | AICTE Internship & Credit Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        color: #f8fafc;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 4px;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .metric-val {
        font-size: 1.6rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .citation-badge {
        display: inline-block;
        background: #0f172a;
        color: #38bdf8;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 4px 10px;
        margin: 4px 4px 4px 0;
        font-size: 0.8rem;
        font-family: monospace;
    }
    .badge-approved {
        background-color: #064e3b;
        color: #34d399;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-tool {
        background-color: #312e81;
        color: #a5b4fc;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .legend-box {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 3px;
        margin-right: 6px;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)


# --- FEEDBACK PERSISTENCE HELPERS ---
def load_feedback() -> List[Dict[str, Any]]:
    if not FEEDBACK_FILE.exists():
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_feedback_entry(query: str, answer: str, rating: str, citations: List[Any], tools_used: List[str]):
    feedback_list = load_feedback()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "rating": rating,  # "up" or "down"
        "tools_used": tools_used,
        "citations": citations
    }
    feedback_list.append(entry)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback_list, f, indent=2)


# --- API QUERY HELPER ---
def query_backend(endpoint: str, payload: dict, backend_url: str) -> Dict[str, Any]:
    url = f"{backend_url.rstrip('/')}{endpoint}"
    try:
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass

    # In-process fallback if FastAPI server is not currently running
    if LOCAL_MODULES_AVAILABLE:
        query_text = payload.get("query") or payload.get("question") or payload.get("prompt") or ""
        if endpoint == "/agent":
            res = run_langgraph_agent(
                query=query_text,
                session_id=payload.get("session_id", "default_session"),
                approved=payload.get("approved", True),
                activities=payload.get("activities")
            )
            return res
        elif endpoint == "/ask":
            res = rag_ask(query_text)
            return res

    return {
        "error": "Backend offline and local fallback unavailable.",
        "answer": "Unable to connect to backend server. Please start FastAPI via `python -m uvicorn Day_4.app_main:app --reload`.",
        "citations": [],
        "tools_used": []
    }


# --- SESSION STATE INITIALIZATION ---
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "Hello! I am **InternGuide AI**. Ask me anything about AICTE B.Tech internship credit requirements, PM Internship Scheme (PMIS) eligibility, or calculate your degree credits and marks.",
            "citations": [],
            "tools_used": [],
            "approval_status": "approved",
            "id": 0
        }
    ]

if "activities" not in st.session_state:
    # Preloaded default student activities
    st.session_state.activities = [
        {
            "id": 1,
            "title": "Industrial Software Internship",
            "head": "Industry / Corporate Internship",
            "hours": 90.0,
            "industry_score": 9.0,
            "institute_panel_score": 6.0
        },
        {
            "id": 2,
            "title": "Rural NSS Community Camp",
            "head": "Rural / NSS / Social Internship",
            "hours": 45.0,
            "industry_score": 8.0,
            "institute_panel_score": 7.0
        }
    ]


# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("🎓 InternGuide")
    st.caption("AICTE Internship & Credit System")

    st.markdown("---")
    st.markdown("**Student Profile:**")
    st.markdown("🧑 **Sanket Vilas Parjane**")
    st.markdown("🆔 PRN: `2124UMLM2044` | Dept: E&TC")
    st.markdown("🎯 Target: **14–20 Credits** (630–900 hrs)")

    st.markdown("---")
    st.subheader("⚙️ Settings")
    default_backend = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    backend_url = st.text_input("FastAPI Backend URL", value=default_backend)
    api_mode = st.radio(
        "Active Engine",
        ["/agent (LangGraph + Memory)", "/ask (RAG Pipeline)"],
        index=0,
        help="Choose between the autonomous LangGraph Agent (with deterministic tools and memory) or the grounded RAG Pipeline (direct semantic policy search)."
    )
    if "/agent" in api_mode:
        st.caption("🤖 **Agent Engine:** Multi-turn LangGraph with memory, calculator tool, & faculty approval step.")
    else:
        st.caption("📑 **RAG Engine:** Direct semantic retrieval from AICTE/UGC vectorstore with page citations.")
    target_endpoint = "/agent" if "/agent" in api_mode else "/ask"

    st.markdown("---")
    st.subheader("📊 Feedback Logged")
    feedbacks = load_feedback()
    thumbs_up_count = sum(1 for f in feedbacks if f.get("rating") == "up")
    thumbs_down_count = sum(1 for f in feedbacks if f.get("rating") == "down")
    col_u, col_d = st.columns(2)
    col_u.metric("👍 Helpful", thumbs_up_count)
    col_d.metric("👎 Needs Review", thumbs_down_count)

    st.markdown("---")
    st.subheader("💡 Suggested Questions")
    sample_queries = [
        "How many hours is one internship credit as per AICTE?",
        "Does an online internship count for credits?",
        "What is the family income limit for the PM Internship Scheme?",
        "Which specific IT companies in Pune are offering paid AI internships?",
        "Calculate my credits: 90h industry + 45h rural NSS camp"
    ]
    for sq in sample_queries:
        if st.button(sq, key=f"sq_{sq[:20]}"):
            st.session_state.pending_prompt = sq


# --- MAIN TABS ---
tab_tracker, tab_chat = st.tabs(["📊 Credit Progress Bar (Signature Feature)", "💬 InternGuide AI Chat"])

# ==============================================================================
# TAB 1: SIGNATURE FEATURE - CREDIT PROGRESS BAR
# ==============================================================================
with tab_tracker:
    st.header("🏆 AICTE B.Tech Internship Credit Progress Tracker")
    st.markdown("""
    Under AICTE Internship Policy regulations, every 4-year B.Tech engineering student must accumulate 
    between **14 to 20 credits** (equivalent to **630 to 900 hours**, standard rate: **1 credit = 45 hours**).
    Enter your completed activities below to visualize your color-coded progress toward degree completion.
    """)

    # Calculation logic for activities
    total_hours = sum(a["hours"] for a in st.session_state.activities)
    total_credits = round(total_hours / 45.0, 2)

    # Calculate net hours-weighted score (70% industry + 30% institute panel)
    if total_hours > 0:
        weighted_marks_sum = 0.0
        for a in st.session_state.activities:
            act_mark = (0.70 * a["industry_score"]) + (0.30 * a["institute_panel_score"])
            weighted_marks_sum += act_mark * a["hours"]
        net_score = round(weighted_marks_sum / total_hours, 2)
    else:
        net_score = 0.0

    min_credits_target = 14.0
    max_credits_target = 20.0
    min_hours_target = 630.0
    max_hours_target = 900.0

    pct_to_min = min(100.0, (total_credits / min_credits_target) * 100.0)
    pct_to_max = min(100.0, (total_credits / max_credits_target) * 100.0)

    # Metric Cards Top Row
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Completed Hours</div>
            <div class="metric-val">{total_hours:0.1f} <span style="font-size:0.9rem; color:#94a3b8;">/ 630 hrs</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Credits Earned</div>
            <div class="metric-val">{total_credits:0.2f} <span style="font-size:0.9rem; color:#94a3b8;">/ 14–20 cr</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Net AICTE Score</div>
            <div class="metric-val">{net_score:0.2f} <span style="font-size:0.9rem; color:#94a3b8;">/ 10</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Degree Requirement</div>
            <div class="metric-val">{pct_to_min:0.1f}% <span style="font-size:0.9rem; color:#94a3b8;">of 14 cr</span></div>
        </div>
        """, unsafe_allow_html=True)

    # --- SIGNATURE PROGRESS BAR VISUALIZATION ---
    st.subheader("🎯 Visual Credit Progress toward 14–20 Credit (630–900 hour) Target")

    # Compute breakdown per activity head
    head_hours = {head: 0.0 for head in ACTIVITY_HEADS}
    for a in st.session_state.activities:
        head = a.get("head", "Industry / Corporate Internship")
        if head in head_hours:
            head_hours[head] += a["hours"]
        else:
            head_hours[head] = a["hours"]

    # Render Multi-segment Progress Bar using clean HTML/CSS
    bar_segments_html = []
    for head, hrs in head_hours.items():
        if hrs > 0:
            seg_pct = (hrs / max_hours_target) * 100.0
            meta = ACTIVITY_HEADS[head]
            gradient = meta.get("gradient", meta["color"])
            icon = meta.get("icon", "📌")
            cr = hrs / 45.0
            short_head = head.split("/")[0].strip()

            # Dynamic text label inside segment
            label = f"{icon} {hrs:.0f}h" if seg_pct >= 5.0 else ""
            if seg_pct >= 11.0:
                label = f"{icon} {short_head}: {hrs:.0f}h ({cr:.1f}cr)"

            bar_segments_html.append(
                f'<div title="{head}: {hrs:.1f} hrs ({cr:.2f} credits)" '
                f'style="flex: 0 0 {seg_pct:.2f}%; width: {seg_pct:.2f}%; min-width: 0; '
                f'background: {gradient}; height: 38px; display: flex; align-items: center; '
                f'justify-content: center; font-size: 0.8rem; font-weight: 700; color: #ffffff; '
                f'text-shadow: 0 1px 3px rgba(0,0,0,0.8); overflow: hidden; white-space: nowrap; '
                f'border-right: 2px solid rgba(15,23,42,0.8); box-sizing: border-box; cursor: pointer;">'
                f'{label}</div>'
            )

    remaining_hours = max(0.0, max_hours_target - total_hours)
    remaining_pct = (remaining_hours / max_hours_target) * 100.0

    rem_label = f"⏳ Remaining: {remaining_hours:.0f} hrs ({remaining_hours/45.0:.1f} cr)" if remaining_pct >= 15.0 else ""
    remaining_html = (
        f'<div title="Remaining to reach 20 credits: {remaining_hours:.1f} hrs" '
        f'style="flex: 0 0 {remaining_pct:.2f}%; width: {remaining_pct:.2f}%; min-width: 0; '
        f'background: repeating-linear-gradient(45deg, #1e293b, #1e293b 10px, #253347 10px, #253347 20px); '
        f'height: 38px; display: flex; align-items: center; justify-content: center; '
        f'font-size: 0.75rem; color: #94a3b8; font-weight: 600; white-space: nowrap; overflow: hidden;">'
        f'{rem_label}</div>'
    )

    st.markdown(f"""
    <div style="background-color: #0b1120; border-radius: 10px; padding: 4px; border: 1px solid #334155; margin-bottom: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
        <div style="position: relative; display: flex; width: 100%; border-radius: 8px; overflow: hidden; height: 38px;">
            {''.join(bar_segments_html)}
            {remaining_html}
            <!-- 70% Minimum B.Tech Threshold Target Marker (14 credits / 630 hours) -->
            <div title="AICTE Minimum B.Tech Threshold: 14 Credits (630 Hours)" style="position: absolute; left: 70%; top: 0; bottom: 0; width: 3px; background: #fbbf24; box-shadow: 0 0 10px #fbbf24; z-index: 10;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Target markers and indicators
    col_t1, col_t2, col_t3 = st.columns([14, 6, 10])
    with col_t1:
        st.caption(f"🏁 **Minimum B.Tech Threshold (Yellow Line):** 14 credits (630 hrs) — Status: {'✅ Achieved' if total_credits >= 14 else f'⏳ Need {(14 - total_credits):.2f} credits ({(630 - total_hours):.1f} hrs)'}")
    with col_t2:
        st.caption("🎖️ **Max Target:** 20 credits (900 hrs)")
    with col_t3:
        st.caption(f"📈 Total Progress: **{pct_to_max:.1f}%** of 20 credits target")

    # Legend for Activity Heads
    st.markdown("**Activity Head Legend (AICTE Table 2):**")
    legend_cols = st.columns(len(ACTIVITY_HEADS))
    for idx, (head, meta) in enumerate(ACTIVITY_HEADS.items()):
        hrs = head_hours.get(head, 0.0)
        cr = hrs / 45.0
        pct = (hrs / max_hours_target) * 100.0 if max_hours_target > 0 else 0.0
        with legend_cols[idx]:
            st.markdown(
                f'<div style="background:#1e293b; border-left: 4px solid {meta["color"]}; border-radius: 6px; padding: 8px 10px; margin-top: 4px;">'
                f'<span style="font-size: 1rem; margin-right: 4px;">{meta["icon"]}</span>'
                f'<strong style="color:#f8fafc; font-size:0.85rem;">{head.split("/")[0].strip()}</strong><br>'
                f'<span style="font-size:0.85rem; color:#38bdf8; font-weight:700;">{hrs:.1f} hrs</span> '
                f'<span style="font-size:0.75rem; color:#94a3b8;">({cr:.1f} cr &bull; {pct:.1f}%)</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")

    # --- ACTIVITY LIST & MANAGER ---
    st.subheader("📋 Completed Activities Portfolio")

    if st.session_state.activities:
        for idx, act in enumerate(st.session_state.activities):
            color = ACTIVITY_HEADS.get(act["head"], {}).get("color", "#38bdf8")
            icon = ACTIVITY_HEADS.get(act["head"], {}).get("icon", "📌")
            cr = round(act["hours"] / 45.0, 2)
            act_mark = round((0.70 * act["industry_score"]) + (0.30 * act["institute_panel_score"]), 2)

            col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns([4, 2, 2, 2, 1])
            with col_a1:
                st.markdown(f"**{icon} {act['title']}**")
                st.caption(f"{act['head']}")
            with col_a2:
                st.write(f"⏱️ **{act['hours']:.1f} hrs** ({cr} cr)")
            with col_a3:
                st.write(f"🏢 Ind: **{act['industry_score']}/10**")
            with col_a4:
                st.write(f"🎓 Panel: **{act['institute_panel_score']}/10**  \n➡️ **{act_mark}/10**")
            with col_a5:
                if st.button("🗑️", key=f"del_{act['id']}"):
                    st.session_state.activities.pop(idx)
                    st.rerun()
    else:
        st.info("No activities recorded yet. Add your completed internships below.")

    # --- ADD ACTIVITY FORM ---
    with st.expander("➕ Add New Internship Activity", expanded=False):
        with st.form("add_activity_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_title = st.text_input("Activity Title", value="Tech Startup Development")
                new_head = st.selectbox("Activity Head (AICTE Table 2)", list(ACTIVITY_HEADS.keys()))
            with c2:
                new_hours = st.number_input("Hours Completed", min_value=1.0, max_value=600.0, value=45.0, step=5.0)
                sub_c1, sub_c2 = st.columns(2)
                with sub_c1:
                    new_ind = st.number_input("Industry Score (out of 10)", min_value=0.0, max_value=10.0, value=8.5, step=0.1)
                with sub_c2:
                    new_panel = st.number_input("Institute Panel Score (out of 10)", min_value=0.0, max_value=10.0, value=7.5, step=0.1)

            submitted = st.form_submit_button("Save Activity")
            if submitted:
                new_id = (max([a["id"] for a in st.session_state.activities]) + 1) if st.session_state.activities else 1
                st.session_state.activities.append({
                    "id": new_id,
                    "title": new_title,
                    "head": new_head,
                    "hours": float(new_hours),
                    "industry_score": float(new_ind),
                    "institute_panel_score": float(new_panel)
                })
                st.success(f"Added '{new_title}' ({new_hours} hours) successfully!")
                st.rerun()

    # Fast Action to Query Agent
    if st.button("🤖 Evaluate Full Portfolio with InternGuide Agent"):
        portfolio_summary = f"I completed {total_hours} hours total: " + ", ".join(
            [f"{a['hours']}h in {a['title']} (Ind: {a['industry_score']}, Panel: {a['institute_panel_score']})" for a in st.session_state.activities]
        ) + ". Calculate total credits and net score."
        st.session_state.pending_prompt = portfolio_summary
        st.info("Portfolio evaluation query prepared! Head over to the '💬 InternGuide AI Chat' tab.")


# ==============================================================================
# TAB 2: CHAT INTERFACE WITH CITATIONS & THUMBS FEEDBACK
# ==============================================================================
with tab_chat:
    st.header("💬 InternGuide AI Chat & Policy Assistant")
    st.caption("Ask questions about AICTE internship rules, credit calculations, or PM Internship Scheme rules.")

    # Render previous messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Render Approval status if present
            if msg.get("approval_status"):
                if msg["approval_status"] == "approved":
                    st.markdown('<span class="badge-approved">✅ Academic Mentor Approval: Verified</span>', unsafe_allow_html=True)
                elif msg["approval_status"] == "rejected":
                    st.markdown('<span style="color:#ef4444; font-weight:600;">❌ Approval Denied</span>', unsafe_allow_html=True)

            # Render Tools Used if present
            if msg.get("tools_used"):
                tools_str = ", ".join(msg["tools_used"])
                st.markdown(f'<span class="badge-tool">🔧 Tools: {tools_str}</span>', unsafe_allow_html=True)

            # Render Citations if present
            if msg.get("citations"):
                st.markdown("**Citations & Sources:**")
                for cite in msg["citations"]:
                    src = cite.get("source", "Policy Document")
                    page = cite.get("page")
                    title = cite.get("title", "")
                    page_str = f", Page {page}" if page else ""
                    st.markdown(f'<span class="citation-badge">📄 {src}{page_str} — {title}</span>', unsafe_allow_html=True)

            # Interactive Thumbs Feedback (Only on assistant messages)
            if msg["role"] == "assistant" and msg.get("id", 0) > 0:
                col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 12])
                with col_fb1:
                    if st.button("👍", key=f"thumb_up_{msg['id']}"):
                        save_feedback_entry(
                            query=msg.get("query_text", ""),
                            answer=msg["content"],
                            rating="up",
                            citations=msg.get("citations", []),
                            tools_used=msg.get("tools_used", [])
                        )
                        st.toast("Thank you for your feedback! (Recorded 👍)", icon="✅")
                with col_fb2:
                    if st.button("👎", key=f"thumb_down_{msg['id']}"):
                        save_feedback_entry(
                            query=msg.get("query_text", ""),
                            answer=msg["content"],
                            rating="down",
                            citations=msg.get("citations", []),
                            tools_used=msg.get("tools_used", [])
                        )
                        st.toast("Feedback recorded (👎). We will improve this response.", icon="ℹ️")

    # Handle user query input
    prompt = st.chat_input("Ask a question (e.g., 'How many hours is 1 credit?' or 'Calculate my credits')...")
    if getattr(st.session_state, "pending_prompt", None):
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if prompt:
        # Display user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": prompt,
            "id": len(st.session_state.chat_messages) + 1
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query backend API or fallback
        with st.chat_message("assistant"):
            with st.spinner("InternGuide AI is thinking..."):
                payload = {
                    "query": prompt,
                    "question": prompt,
                    "session_id": "student_sanket_session",
                    "approved": True
                }
                res = query_backend(target_endpoint, payload, backend_url)

                answer_text = res.get("response") or res.get("answer") or "I could not generate an answer."
                citations = res.get("citations", [])
                tools_used = res.get("tools_used", [])
                approval_status = res.get("approval_status", "approved")

                st.markdown(answer_text)

                if approval_status == "approved" and "internship_credit_calculator" in tools_used:
                    st.markdown('<span class="badge-approved">✅ Academic Mentor Approval: Verified</span>', unsafe_allow_html=True)

                if tools_used:
                    tools_str = ", ".join(tools_used)
                    st.markdown(f'<span class="badge-tool">🔧 Tools: {tools_str}</span>', unsafe_allow_html=True)

                if citations:
                    st.markdown("**Citations & Sources:**")
                    for cite in citations:
                        src = cite.get("source", "Policy Document")
                        page = cite.get("page")
                        title = cite.get("title", "")
                        page_str = f", Page {page}" if page else ""
                        st.markdown(f'<span class="citation-badge">📄 {src}{page_str} — {title}</span>', unsafe_allow_html=True)

                # Store assistant response into state
                msg_id = len(st.session_state.chat_messages) + 1
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer_text,
                    "citations": citations,
                    "tools_used": tools_used,
                    "approval_status": approval_status,
                    "query_text": prompt,
                    "id": msg_id
                })
                st.rerun()
