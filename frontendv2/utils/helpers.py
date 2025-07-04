import streamlit as st
import json

def pretty_print_json(data):
    st.code(json.dumps(data, indent=2, ensure_ascii=False), language="json")