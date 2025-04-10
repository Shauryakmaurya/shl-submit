# import streamlit as st
# import pandas as pd
# import re
# import requests
# from io import StringIO
# from Hybrid_Rag_Ui_Table import query_rag_system, hybrid_search  # import your final canvas module

# st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
# st.title("🧠 SHL Assessment Recommender (Hybrid RAG + LLaMA)")

# query = st.text_area("✍️ Enter Job Description or Assessment Query (or a Link to a JD)", height=200)

# # Filter controls
# col1, col2, col3 = st.columns(3)
# max_duration = col1.slider("⏱️ Max Duration (min)", 0, 120, 60)
# remote_only = col2.checkbox("🌐 Only Remote Tests")
# adaptive_only = col3.checkbox("🧠 Only Adaptive/IRT")
# search_filter = st.text_input("🔎 Filter Results by Keyword (optional)")

# if st.button("🔍 Recommend Assessments") and query:
#     with st.spinner("Running Hybrid Search and LLaMA..."):
#         # If query has a URL, extract and append page content
#         url_match = re.search(r'https?://\S+', query)
#         if url_match:
#             try:
#                 page = requests.get(url_match.group(0), timeout=5)
#                 query += f"\n\n[Page snippet]:\n{page.text[:3000]}"
#             except:
#                 st.warning("Could not fetch content from URL")

#         results, llama_response = query_rag_system(query)
#         df = results.copy() if isinstance(results, pd.DataFrame) else pd.read_html(results, flavor='bs4')[0]  # Convert HTML table back to DataFrame

#         # Apply filters
#         df_filtered = df.copy()
#         df_filtered = df_filtered[df_filtered["Duration (min)"].apply(lambda x: int(x) if str(x).isdigit() else 999) <= max_duration]
#         if remote_only:
#             df_filtered = df_filtered[df_filtered["Remote"] == "✅"]
#         if adaptive_only:
#             df_filtered = df_filtered[df_filtered["Adaptive/IRT"] == "✅"]
#         if search_filter:
#             df_filtered = df_filtered[df_filtered.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().str.cat(), axis=1)]

#         st.subheader("🔝 Top Matching Assessments")
#         st.dataframe(df_filtered, use_container_width=True)

#         # Download button
#         csv = df_filtered.to_csv(index=False).encode("utf-8")
#         st.download_button("⬇️ Download CSV", csv, "recommended_assessments.csv", "text/csv")

#         # LLaMA response
#         st.subheader("💡 LLaMA Recommendation")
#         st.write(llama_response)
# import streamlit as st
# import pandas as pd
# import re
# import requests
# from io import StringIO
# from Hybrid_Rag_Ui_Table import query_rag_system, hybrid_search  # import your final canvas module

# st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
# st.title("🧠 SHL Assessment Recommender (Hybrid RAG + LLaMA)")

# query = st.text_area("✍️ Enter Job Description or Assessment Query (or a Link to a JD)", height=200)

# # Filter controls
# col1, col2, col3 = st.columns(3)
# max_duration = col1.slider("⏱️ Max Duration (min)", 0, 120, 60)
# remote_only = col2.checkbox("🌐 Only Remote Tests")
# adaptive_only = col3.checkbox("🧠 Only Adaptive/IRT")
# search_filter = st.text_input("🔎 Filter Results by Keyword (optional)")

# if st.button("🔍 Recommend Assessments") and query:
#     with st.spinner("Running Hybrid Search and LLaMA..."):
#         # If query has a URL, extract and append page content
#         url_match = re.search(r'https?://\S+', query)
#         if url_match:
#             try:
#                 page = requests.get(url_match.group(0), timeout=5)
#                 query += f"\n\n[Page snippet]:\n{page.text[:3000]}"
#             except:
#                 st.warning("Could not fetch content from URL")

#         results, llama_response = query_rag_system(query)
#         st.write("🧠 DEBUG: raw results from query_rag_system")
#         st.write(results)
#         df = results.copy()  # Ensure it's a DataFrame

#         # Apply filters
#         df_filtered = df.copy()
#         # Convert duration safely
#         df_filtered["Duration (min)"] = pd.to_numeric(df_filtered["Duration (min)"], errors="coerce")
#         df_filtered = df_filtered[df_filtered["Duration (min)"].fillna(999) <= max_duration]

#         # df_filtered = df_filtered[df_filtered["Duration (min)"].apply(lambda x: int(x) if str(x).isdigit() else 999) <= max_duration]
#         if remote_only:
#             df_filtered = df_filtered[df_filtered["Remote"] == "✅"]
#         if adaptive_only:
#             df_filtered = df_filtered[df_filtered["Adaptive/IRT"] == "✅"]
#         if search_filter:
#             df_filtered = df_filtered[df_filtered.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().str.cat(), axis=1)]

#         # st.subheader("🔝 Top Matching Assessments")
#         # st.dataframe(df_filtered, use_container_width=True)
#         # Create clickable links in the URL column
#         df_filtered["URL"] = df_filtered["URL"].apply(lambda url: f'<a href="{url}" target="_blank">🔗 Link</a>')

#         st.markdown("#### 🔝 Top Matching Assessments (Clickable Links)")
#         st.write(
#             df_filtered.to_html(escape=False, index=False),
#             unsafe_allow_html=True
# )


#         # Download button
#         csv = df_filtered.to_csv(index=False).encode("utf-8")
#         st.download_button("⬇️ Download CSV", csv, "recommended_assessments.csv", "text/csv")

#         # LLaMA response
#         st.subheader("💡 LLaMA Recommendation")
#         st.write(llama_response)

# import streamlit as st
# import pandas as pd
# import re
# import requests
# from io import StringIO
# from Hybrid_Rag_Ui_Table import query_rag_system, hybrid_search  # import your final canvas module

# st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
# st.title("🧠 SHL Assessment Recommender (Hybrid RAG + LLaMA)")

# query = st.text_area("✍️ Enter Job Description or Assessment Query (or a Link to a JD)", height=200)

# # Filter controls
# col1, col2, col3 = st.columns(3)
# max_duration = col1.slider("⏱️ Max Duration (min)", 0, 120, 60)
# remote_only = col2.checkbox("🌐 Only Remote Tests")
# adaptive_only = col3.checkbox("🧠 Only Adaptive/IRT")
# search_filter = st.text_input("🔎 Filter Results by Keyword (optional)")

# if st.button("🔍 Recommend Assessments") and query:
#     with st.spinner("Running Hybrid Search and LLaMA..."):
#         # If query has a URL, extract and append page content
#         url_match = re.search(r'https?://\S+', query)
#         if url_match:
#             try:
#                 page = requests.get(url_match.group(0), timeout=5)
#                 query += f"\n\n[Page snippet]:\n{page.text[:3000]}"
#             except:
#                 st.warning("Could not fetch content from URL")

#         results, llama_response = query_rag_system(query)
#         df = results.copy()  # Ensure it's a DataFrame

#         # Apply filters
#         df_filtered = df.copy()
#         df_filtered["Duration (min)"] = pd.to_numeric(df_filtered["Duration (min)"], errors="coerce")
#         df_filtered = df_filtered[df_filtered["Duration (min)"].fillna(999) <= max_duration]

#         if remote_only:
#             df_filtered = df_filtered[df_filtered["Remote"] == "✅"]
#         if adaptive_only:
#             df_filtered = df_filtered[df_filtered["Adaptive/IRT"] == "✅"]
#         if search_filter:
#             df_filtered = df_filtered[df_filtered.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().str.cat(), axis=1)]

#         # Create clickable links in the URL column
#         df_filtered["URL"] = df_filtered["URL"].apply(lambda url: f'<a href="{url}" target="_blank">🔗 Link</a>')

#         st.markdown("#### 🔝 Top Matching Assessments (Clickable Links)")
#         st.write(
#             df_filtered.to_html(escape=False, index=False),
#             unsafe_allow_html=True
#         )

#         # Download button
#         csv = df_filtered.to_csv(index=False).encode("utf-8")
#         st.download_button("⬇️ Download CSV", csv, "recommended_assessments.csv", "text/csv")

#         # LLaMA response
#         st.subheader("💡 LLaMA Recommendation")
#         st.write(llama_response)

import streamlit as st
import pandas as pd
import re
import requests
from io import StringIO
from Hybrid_Rag_Ui_Table import query_rag_system, hybrid_search  # import your final canvas module

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("🧠 SHL Assessment Recommender (Hybrid RAG + LLaMA)")

query = st.text_area("✍️ Enter Job Description or Assessment Query (or a Link to a JD)", height=200)

# Filter controls
col1, col2, col3 = st.columns(3)
max_duration = col1.slider("⏱️ Max Duration (min)", 0, 120, 60)
remote_only = col2.checkbox("🌐 Only Remote Tests")
adaptive_only = col3.checkbox("🧠 Only Adaptive/IRT")
search_filter = st.text_input("🔎 Filter Results by Keyword (optional)")

if st.button("🔍 Recommend Assessments") and query:
    with st.spinner("Running Hybrid Search and LLaMA..."):
        # If query has a URL, extract and append page content
        url_match = re.search(r'https?://\S+', query)
        if url_match:
            try:
                page = requests.get(url_match.group(0), timeout=5)
                query += f"\n\n[Page snippet]:\n{page.text[:3000]}"
            except:
                st.warning("Could not fetch content from URL")

        results, llama_response = query_rag_system(query)
        df = results.copy()  # Ensure it's a DataFrame

        # Apply filters
        df_filtered = df.copy()
        df_filtered["Duration (min)"] = pd.to_numeric(df_filtered["Duration (min)"], errors="coerce")
        df_filtered = df_filtered[df_filtered["Duration (min)"].fillna(999) <= max_duration]

        if remote_only:
            df_filtered = df_filtered[df_filtered["Remote"] == "✅"]
        if adaptive_only:
            df_filtered = df_filtered[df_filtered["Adaptive/IRT"] == "✅"]
        if search_filter:
            df_filtered = df_filtered[df_filtered.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().str.cat(), axis=1)]

        # Save actual URLs for CSV, and display links for Streamlit
        df_filtered["Download URL"] = df_filtered["URL"]  # Keep the plain URL for CSV
        df_filtered["URL"] = df_filtered["URL"].apply(lambda url: f'<a href="{url}" target="_blank">🔗 Link</a>')

        st.markdown("#### 🔝 Top Matching Assessments (Clickable Links)")
        st.write(
            df_filtered.drop(columns=["Download URL"]).to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # Download button using the plain URLs
        download_df = df_filtered.drop(columns=["URL"]).rename(columns={"Download URL": "URL"})
        csv = download_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "recommended_assessments.csv", "text/csv")

        # LLaMA response
        st.subheader("💡 LLaMA Recommendation")
        st.write(llama_response)
