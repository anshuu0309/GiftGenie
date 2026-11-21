import streamlit as st
import os
from urllib.parse import quote_plus
from model import recommend_gifts, gifts

# Page configuration
st.set_page_config(
    page_title="Gift Genie",
    page_icon="🎁",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #fff7fb;
}

h1 {
    color: #a64d79;
    text-align: center;
}

h2, h3 {
    color: #a64d79;
}

.stButton button {
    background-color: #d889b5;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# Home page
st.title("🎁 Gift Genie")

st.markdown(
    "<h3 style='text-align:center;'>"
    "Find the Perfect Gift for Every Special Moment!"
    "</h3>",
    unsafe_allow_html=True
)

st.divider()

st.subheader("💝 Welcome to Gift Genie!")

st.write(
    "Confused about what gift to buy? "
    "Tell us about the person and we will recommend "
    "the perfect gifts for them!"
)

st.divider()

# Gift finder form
st.subheader("✨ Find Your Perfect Gift")

with st.form("gift_finder"):

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

    submit = st.form_submit_button(
        "🎀 Find My Gifts",
        use_container_width=True
    )


# Show recommendations
if submit:

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

        st.warning(
            "Sorry! No gifts found. Please try different choices."
        )

    else:

        image_folder = "static/images"

        if os.path.exists(image_folder):
            available_images = os.listdir(image_folder)
        else:
            available_images = []

        columns = st.columns(2)

        for index, (_, gift) in enumerate(
            recommendations.iterrows()
        ):

            gift_name = str(gift["gift_name"])
            price = gift["budget"]

            # Find matching image
            image_path = None

            gift_key = (
                gift_name.lower()
                .replace(" ", "")
                .replace("_", "")
                .replace(".", "")
            )

            for filename in available_images:

                file_key = (
                    os.path.splitext(filename)[0]
                    .lower()
                    .replace(" ", "")
                    .replace("_", "")
                    .replace(".", "")
                )

                if gift_key == file_key:
                    image_path = os.path.join(
                        image_folder, filename
                    )
                    break

            with columns[index % 2]:

                with st.container(border=True):

                    if image_path:
                        st.image(
                            image_path,
                            use_container_width=True
                        )

                    st.markdown(f"### 🎀 {gift_name}")

                    st.write(f"**Price:** ₹{price}")

                    amazon_link = (
                        "https://www.amazon.in/s?k="
                        + quote_plus(gift_name)
                    )

                    st.link_button(
                        "🛍️ Buy on Amazon",
                        amazon_link,
                        use_container_width=True
                    )

        st.success("Happy Gifting! 💗")


# Footer
st.divider()

st.markdown(
    "<center>Made with 💗 by Anshu & Rashi | Gift Genie</center>",
    unsafe_allow_html=True
)
