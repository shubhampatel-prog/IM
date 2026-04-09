import streamlit as st
from main import main as run_pipeline

# 1. Page Configuration
st.set_page_config(page_title="IM Test Case Agent", page_icon="🤖")

# 2. Header
st.title("🤖 IM Test Case Creation Agent")
st.markdown("---")

# 3. Sidebar — dynamic inputs
with st.sidebar:
    st.header("⚙️ TestLink Configuration")

    st.subheader("📂 Project")
    testlink_project_id = st.number_input(
        "TestLink Project ID",
        min_value=1,
        value=2,
        help="Numeric ID of the TestLink project (e.g. 2 = IndiaMART_Android_App)"
    )

    st.markdown("---")
    st.subheader("🧠 Knowledge Base")
    st.caption("Suite whose existing test cases are fed to the AI so it understands current module functionality.")

    testlink_kb_suite_id = st.number_input(
        "Module Test Suite ID",
        min_value=1,
        value=26691,
        help="e.g. Android Sanity Test Cases > PBR (254) — the module suite the AI should learn from"
    )

    st.markdown("---")
    st.subheader("🎯 Target Suite")
    st.caption("Where the agent will create new child test suites and test cases.")

    testlink_suite_id = st.number_input(
        "Target Test Suite ID",
        min_value=1,
        value=352634,
        help="Parent suite under which a new child suite will be created per ticket"
    )

    st.markdown("---")
    show_prompt = st.toggle(
        "🧾 Show AI Prompt in Terminal",
        value=False,
        help="Prints the full prompt sent to the LLM in the terminal/logs"
    )

# 4. Main area
st.write("Enter your OpenProject ID below to automatically generate AI test cases in TestLink.")

ticket_id = st.text_input("OpenProject Story/Task ID", placeholder="e.g., 12345")

# 5. Action Button
if st.button("Generate AI Test Cases", type="primary", use_container_width=True):
    if ticket_id.isdigit():
        with st.status("Processing...", expanded=True) as status:
            try:
                success, created, failed = run_pipeline(
                    ticket_id=ticket_id,
                    project_id=int(testlink_project_id),
                    suite_id=int(testlink_suite_id),
                    kb_suite_id=int(testlink_kb_suite_id),
                    show_prompt=show_prompt,
                )

                if success:
                    status.update(label="Creation Complete!", state="complete", expanded=False)
                    st.success(f"✅ Success! Created: {created} | Failed: {failed}")
                    st.balloons()
                else:
                    status.update(label="Task Failed", state="error")
                    st.error("The pipeline ran but failed to create test cases.")

            except Exception as e:
                status.update(label="Error Occurred", state="error")
                st.error(f"❌ Failed to run script. Error: {e}")
    else:
        st.warning("Please enter a valid numeric ID.")
