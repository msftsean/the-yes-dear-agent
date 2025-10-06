import streamlit as st

st.write("🔍 **STREAMLIT RENDER TEST**")
st.write("If you see this message, Streamlit is rendering content!")

st.markdown("### Basic Elements Test:")
st.text("Plain text")
st.markdown("**Bold markdown**")
st.code("print('hello world')")

if st.button("Test Button"):
    st.success("Button clicked! Streamlit is working.")

st.write("---")
st.write("✅ If you see all the above content, the rendering issue is not with Streamlit itself.")