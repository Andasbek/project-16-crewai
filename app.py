import streamlit as st
import os
import time
from dotenv import load_dotenv

from crew import build_crew
from utils import ensure_output_dir, slugify, timestamp, write_text, write_json, get_history, OUTPUT_DIR

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Project 16: CrewAI Content Generator", layout="wide")

def main():
    st.title("🤖 Project 16: Multi-Agent Content Machine")
    st.markdown("Generate high-quality articles using a Research → Write → Edit pipeline.")

    # --- Sidebar Configuration ---
    st.sidebar.header("Configuration")
    
    topic = st.sidebar.text_area("Topic", placeholder="e.g. The Future of AI in Healthcare")
    audience = st.sidebar.text_input("Target Audience", value="General Tech Enthusiasts")
    tone = st.sidebar.selectbox("Tone", ["Professional", "Friendly", "Academic", "Marketing"], index=0)
    language = st.sidebar.selectbox("Output Language", ["Russian", "English"], index=0)
    
    st.sidebar.subheader("Constraints")
    word_range = st.sidebar.slider("Word Count Range", 500, 2500, (800, 1200), step=100)
    word_min, word_max = word_range
    
    use_search = st.sidebar.checkbox("Include Web Research", value=True)
    num_sources = st.sidebar.number_input("Number of Sources", min_value=5, max_value=20, value=5, step=1)

    # Environment Check
    if not os.getenv("OPENAI_API_KEY"):
        st.sidebar.error("⚠️ OPENAI_API_KEY not found in .env")
    if use_search and not os.getenv("SERPER_API_KEY"):
        st.sidebar.warning("⚠️ SERPER_API_KEY not found. Search might fail.")

    # --- Main Execution ---
    if st.sidebar.button("Generate Article", type="primary"):
        if not topic:
            st.error("Please enter a topic.")
            return
        
        if not os.getenv("OPENAI_API_KEY"):
             st.error("Missing OPENAI_API_KEY. Please configure your .env file.")
             return

        with st.status("🚀 Starting CrewAI Pipeline...", expanded=True) as status:
            try:
                # 1. Build Crew
                status.write("🛠️ Building agents and tasks...")
                crew = build_crew(
                    topic=topic,
                    audience=audience,
                    tone=tone,
                    word_count_min=word_min,
                    word_count_max=word_max,
                    use_search=use_search,
                    num_sources=num_sources,
                    language=language,
                )
                
                # 2. Execute
                status.write("🧠 Agents are working... (This may take 1-3 minutes)")
                # Streamlit doesn't easily support real-time log streaming from subprocess/threads without complex setups.
                # We'll just wait for the result.
                
                result = crew.kickoff()
                final_content = str(result)
                
                status.write("✅ Execution complete!")
                status.update(label="Generation Successful!", state="complete", expanded=False)
                
                # 3. Save Results
                ensure_output_dir()
                batch_stamp = timestamp()
                base_name = f"{batch_stamp}_{slugify(topic)}"
                md_path = OUTPUT_DIR / f"{base_name}.md"
                meta_path = OUTPUT_DIR / f"{base_name}.json"
                
                write_text(md_path, final_content)
                write_json(meta_path, {
                    "topic": topic,
                    "audience": audience,
                    "tone": tone,
                    "word_range": word_range,
                    "use_search": use_search,
                    "num_sources": num_sources,
                    "language": language,
                })
                
                st.session_state['last_result'] = final_content
                st.session_state['last_file'] = str(md_path)
                
                st.success(f"Article generated and saved to `{md_path}`")

            except Exception as e:
                status.update(label="Execution Failed", state="error")
                st.error(f"An error occurred: {str(e)}")
                return

    # --- Result Display ---
    if 'last_result' in st.session_state:
        st.divider()
        st.subheader("📝 Generated Content")
        
        tab_preview, tab_raw = st.tabs(["Markdown Preview", "Raw Markdown"])
        
        with tab_preview:
            st.markdown(st.session_state['last_result'])
            
        with tab_raw:
            st.code(st.session_state['last_result'], language='markdown')
            
        st.download_button(
            label="Download .md",
            data=st.session_state['last_result'],
            file_name=os.path.basename(st.session_state.get('last_file', 'article.md')),
            mime="text/markdown"
        )

    # --- History ---
    st.divider()
    with st.expander("📜 History (Output Directory)"):
        history = get_history()
        if history:
            st.dataframe(history, use_container_width=True)
            if st.button("Refresh History"):
                st.rerun()
        else:
            st.info("No files found in output directory.")

if __name__ == "__main__":
    main()
