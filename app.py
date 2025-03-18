import os
import streamlit as st
import asyncio
from gpt_researcher import GPTResearcher

# Set API Keys (Replace with secure handling in production)
os.environ['OPENAI_API_KEY'] = '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'
os.environ['TAVILY_API_KEY'] = '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'

async def get_report(query: str, report_type: str):
    if not isinstance(query, str) or not isinstance(report_type, str):
        raise ValueError("Query and report type must be strings")
    
    researcher = GPTResearcher(query, report_type)
    
    try:
        research_result = await researcher.conduct_research()
        report = await researcher.write_report()
        research_context = researcher.get_research_context() or "No context available."
        research_costs = researcher.get_costs() or "No cost details available."
        research_images = researcher.get_research_images() or []
        research_sources = researcher.get_research_sources() or "No sources available."

        return str(report), str(research_context), str(research_costs), research_images, str(research_sources)
    
    except TypeError as e:
        st.error(f"TypeError: {e}")
        return "Error generating report", "Error", "Error", [], "Error"

# Streamlit UI
st.title("AI Research Assistant")
st.write("Enter a query to generate a research report using GPTResearcher.")

query = st.text_area("Enter your query:", "")
report_type = st.selectbox("Select report type:", ["research_report", "summary", "detailed_report"])

if st.button("Generate Report"):
    if query.strip():  # Ensure query is not empty
        with st.spinner("Generating report..."):
            report, context, costs, images, sources = asyncio.run(get_report(query, report_type))
            
            st.subheader("Report:")
            st.write(report)

            st.subheader("Research Context:")
            st.write(context)

            st.subheader("Research Costs:")
            st.write(costs)

            st.subheader("Research Images:")
            if images:
                for img in images:
                    st.image(img, caption="Research Image")
            else:
                st.write("No images available.")

            st.subheader("Research Sources:")
            st.write(sources)
    else:
        st.error("Please enter a valid query.")
