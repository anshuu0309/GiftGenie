import streamlit as st
import pandas as pd
import os
from urllib.parse import quote_plus
from model import recommend_gifts, gifts

st.set_page_config(
    page_title="Gift Genie",
    page_icon="🎁",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #fff7fb;
}
h1 {
    color: #a64d79;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
}
div.stButton > button {
    background-color: #d889b5;
    color: white;
    border-radius: 12px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("🎁 Gift Genie")
st.markdown(
    '<p class="subtitle">Find the Perfect Gift for Every Special Moment!</p>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("✨ Welcome to Gift Genie!")
st.write(
    "Confused about what gift to buy? "
    "Tell us a little about the person and we will find "
    "the perfect gift for them!"
)

st.subheader("💝 Find Your Perfect Gift")

with st.form("gift_form"):

    col1, col2 = st.columns(2)

    with col1:
        relation = st.selectbox(
            "Who are you buying a gift for?",
            sorted(gifts["relation"].dropna().astype(str).unique())
        )

        age = st.number_input(
            "Enter Age",
            min_value=1,
            max_value=100,
            value=18
        )

        occasion = st.selectbox(
            "Select Occasion",
            sorted(gifts["occasion"].dropna().astype(str).unique())
        )

    with col2:
        budget = st.selectbox(
            "Select Your Budget",
            [
                "Below ₹500",
                "₹500 - ₹1000",
                "₹1000 - ₹2000",
                "₹2000 - ₹5000",
                "Above ₹5000"
            ]
        )

        interest = st.selectbox(
            "Select Interest",
            sorted(gifts["interest"].dropna().astype(str).unique())
        )

    submitted = st.form_submit_button(
        "🎀 Find My Gifts",
        use_container_width=True
    )

if submitted:

    st.divider()
    st.subheader("🎁 Your Gift Recommendations")

    recommendations = recommend_gifts(
        relation,
        occasion,
        interest,
        budget,
        age
    )

    if recommendations.empty:
        st.warning("Sorry! No gifts found. Try changing your choices.")

    else:
        cols = st.columns(2)

        image_folder = "static/images"
        available_images = (
            os.listdir(image_folder)
            if os.path.exists(image_folder)
            else []
        )

        for index, (_, gift) in enumerate(
            recommendations.iterrows()
        ):
            gift_name = str(gift["gift_name"])
            price = gift["budget"]

            slug = gift_name.lower().replace(" ", "_")

            image_file = None

            for filename in available_images:
                filename_slug = (
                    os.path.splitext(filename)[0]
                    .lower()
                    .replace(" ", "_")
                    .replace(".", "")
                )

                if filename_slug == slug.replace(".", ""):
                    image_file = os.path.join(
                        image_folder, filename
                    )
                    break

            with cols[index % 2]:

                with st.container(border=True):

                    if image_file:
                        st.image(
                            image_file,
                            use_container_width=True
                        )

                    st.markdown(f"### 🎀 {gift_name}")
                    st.write(f"**Price:** ₹{price}")

                    amazon_url = (
                        "https://www.amazon.in/s?k="
                        + quote_plus(gift_name)
                    )

                    st.link_button(
                        "🛍️ Buy on Amazon",
                        amazon_url,
                        use_container_width=True
                    )

        st.success("Hope you find the perfect gift! 💗")

st.divider()

st.markdown(
    "<center>Made with 💗 by Anshu & Rashi | Gift Genie</center>",
    unsafe_allow_html=True
)
