import os
import tempfile

import streamlit as st

from shopping_agent import agent

if "ANTHROPIC_API_KEY" in st.secrets:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
    
st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_image" not in st.session_state:
    st.session_state.pending_image = None

st.title("AI Shopping Assistant")
st.subheader("Search, compare, and order grocery products with a smart assistant.")
st.write(
    "Enter a request below, or upload an image in the sidebar to start shopping."
)

with st.sidebar:
    st.header("Shop by Image")
    st.caption("Upload a photo and I’ll find similar products in the store.")

    uploaded_file = st.file_uploader(
        "Upload product image", type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

    if uploaded_file and st.button("Find similar products", use_container_width=True):
        suffix = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            image_path = tmp.name

        prompt = (
            "I uploaded a product image. Please analyze it and find similar products "
            f"in the store. Image path: {image_path}"
        )
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.pending_image = image_path
        st.rerun()

    st.divider()

    st.header("How to use")
    st.markdown(
        "- Ask for products by type, price, rating, or organic status.\n"
        "- Upload a product image to search visually.\n"
        "- Confirm an order with replies like `yes` or `order #2`."
    )

    if st.button("Reset conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_image = None
        st.rerun()

if not st.session_state.messages:
    st.info("Start by sending a product request or upload an image to begin shopping.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user" and msg["content"].startswith(
            "I uploaded a product image"
        ):
            filename = msg["content"].split("Image path:")[-1].strip()
            st.markdown(f"Searching by image: **{os.path.basename(filename)}**")
        else:
            st.markdown(msg["content"].replace("$", r"\$"))

if (
    st.session_state.pending_image
    and st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):
    with st.chat_message("assistant"):
        with st.spinner("Analyzing image and searching…"):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content.replace("`", "")
        st.markdown(response.replace("$", r"\$"))

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.pending_image = None
    st.rerun()

prompt = st.chat_input("e.g. I want organic honey under $15 with 4+ rating")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = agent.invoke({"messages": st.session_state.messages})
            response = result["messages"][-1].content.replace("`", "")
        st.markdown(response.replace("$", r"\$"))

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()