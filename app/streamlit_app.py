import streamlit as st


st.set_page_config(

    page_title="Agentic Persona Intelligence",

    layout="wide",

    initial_sidebar_state="expanded"
)


st.title(
    "Agentic Persona Intelligence System"
)


st.markdown("""
## Behavioral Modeling + Agentic Recommendation Intelligence

This project demonstrates:

### Task A — User Modeling
- Persona clustering
- Behavioral archetypes
- Emotional reasoning
- Multi-agent debate
- Counterfactual reasoning
- Nigerian contextual adaptation

### Task B — Recommendation Intelligence
- Cross-domain retrieval
- Cold-start recommendation reasoning
- Multiturn recommendation memory
- Conversational recommendation generation
- Behavioral recommendation orchestration

---

### Architecture Highlights

This system combines:
- Behavioral modeling
- Cognitive simulation
- Agentic reasoning
- Memory-aware recommendation systems
- Cross-domain taste transfer

Use the sidebar to explore both tasks.
""")


st.sidebar.title(
    "Navigation"
)

st.sidebar.success(
    "Select a task page."
)


st.sidebar.markdown("---")

st.sidebar.markdown("""
### Built With

- Python
- Streamlit
- Pandas
- Scikit-learn
- Gemini API
""")