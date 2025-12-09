import streamlit as st
import asyncio
import os
import pandas as pd
from typing import List, Dict

# backend modules
from backend.prompt_builder import build_prompt
from backend.dispatcher import generate_variation
from backend.exporter import export_csv, export_xlsx

# Page config
st.set_page_config(
    page_title="AI Variation Generator",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'variations' not in st.session_state:
    st.session_state.variations = [
        {'name': 'V1', 'params': ''},
        {'name': 'V2', 'params': ''}
    ]
if 'output_rows' not in st.session_state:
    st.session_state.output_rows = []

# Title
st.title("🤖 AI Variation Generator")

# Original Message Input
st.subheader("Original Message")
original_message = st.text_area(
    "Paste your original campaign message here...",
    height=100,
    key="original_message"
)

st.divider()

# Variations Section
st.subheader("Variations")

# Add Variation Button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("➕ Add Variation", use_container_width=True):
        st.session_state.variations.append({
            'name': f'V{len(st.session_state.variations)+1}',
            'params': ''
        })
        st.rerun()

# Display variations
variations_to_remove = []
for idx, variation in enumerate(st.session_state.variations):
    with st.container():
        col1, col2, col3 = st.columns([2, 8, 1])
        
        with col1:
            variation['name'] = st.text_input(
                "Name",
                value=variation['name'],
                key=f"name_{idx}",
                label_visibility="collapsed",
                placeholder="Variation name (e.g. A)"
            )
        
        with col2:
            variation['params'] = st.text_area(
                "Parameters",
                value=variation['params'],
                key=f"params_{idx}",
                height=100,
                label_visibility="collapsed",
                placeholder="Parameters (free text)"
            )
        
        with col3:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("🗑️", key=f"remove_{idx}", help="Remove this variation"):
                variations_to_remove.append(idx)

# Remove variations (after loop to avoid modification during iteration)
if variations_to_remove:
    for idx in sorted(variations_to_remove, reverse=True):
        st.session_state.variations.pop(idx)
    st.rerun()

st.divider()

# Generate Button
col1, col2, col3, col4 = st.columns([2, 2, 2, 6])

with col1:
    generate_clicked = st.button("🚀 Generate Variations", type="primary", use_container_width=True)

with col2:
    export_csv_clicked = st.button("📄 Export CSV", use_container_width=True)

with col3:
    export_xlsx_clicked = st.button("📊 Export XLSX", use_container_width=True)

# Generate Variations
if generate_clicked:
    if not st.session_state.variations:
        st.warning("⚠️ Add at least one variation")
    elif not original_message:
        st.warning("⚠️ Please enter an original message")
    else:
        with st.spinner("🔄 Generating variations..."):
            # Run async generation
            async def generate_all():
                tasks = []
                for vw in st.session_state.variations:
                    prompt = build_prompt(original_message, vw['params'])
                    tasks.append(asyncio.to_thread(generate_variation, prompt))
                
                results = await asyncio.gather(*tasks)
                return results
            
            # Execute async code
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(generate_all())
            loop.close()
            
            # Store results
            st.session_state.output_rows = [
                [st.session_state.variations[i]['name'], results[i]]
                for i in range(len(results))
            ]
            
            st.success("✅ Generation complete!")
            st.rerun()

# Display Results
if st.session_state.output_rows:
    st.divider()
    st.subheader("Generated Variations")
    
    # Create DataFrame for better display
    df = pd.DataFrame(st.session_state.output_rows, columns=["Variation", "Message"])
    
    # Display as a nice table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Variation": st.column_config.TextColumn("Variation", width="small"),
            "Message": st.column_config.TextColumn("Message", width="large"),
        }
    )

# Export handlers
if export_csv_clicked:
    if not st.session_state.output_rows:
        st.warning("⚠️ Nothing to export")
    else:
        filepath = os.path.join(os.getcwd(), 'variations_export.csv')
        export_csv(st.session_state.output_rows, filepath)
        st.success(f"✅ Exported CSV to {filepath}")

if export_xlsx_clicked:
    if not st.session_state.output_rows:
        st.warning("⚠️ Nothing to export")
    else:
        filepath = os.path.join(os.getcwd(), 'variations_export.xlsx')
        export_xlsx(st.session_state.output_rows, filepath)
        st.success(f"✅ Exported XLSX to {filepath}")