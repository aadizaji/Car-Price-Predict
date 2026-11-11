import streamlit as st
import pandas as pd
from joblib import load

# Page Settings
st.set_page_config(
    page_title="Car Price Estimator",
    page_icon="🚗",
    layout="wide"
)

# Load Model
loaded_model = load("Car_Price_Prediction.joblib")


# Load Datasets
df_206 = pd.read_csv("datasets/divar_206.csv")
df_207 = pd.read_csv("datasets/divar_207.csv")
df_optima = pd.read_csv("datasets/divar_optima.csv")
df_sportage = pd.read_csv("datasets/divar_sportage.csv")


# Car Information
cars = {
    "Peugeot 206": (df_206, "پژو 206", "assets/peugeot_206.webp"),
    "Peugeot 207": (df_207, "پژو 207", "assets/peugeot_207.webp"),
    "Kia Optima": (df_optima, "Kia Optima", "assets/kia_optima.webp"),
    "Kia K5": (df_optima, "Kia K5", "assets/kia_k5.webp"),
    "Kia Sportage": (df_sportage, "Kia Sportage", "assets/kia_sportage.webp")
}


# Car Colors
colors = {
    "سفید": ("White", "#f8fafc"),
    "مشکی": ("Black", "#20242b"),
    "نقره ای": ("Silver", "#bfc6ce"),
    "خاکستری": ("Gray", "#8b939f"),
    "نوک مدادی": ("Graphite", "#4c5563"),
    "طوسی": ("Slate", "#a1a4aa"),
    "قرمز": ("Red", "#bd3b47"),
    "آبی": ("Blue", "#417bb9"),
    "سفید صدفی": ("Pearl White", "#eeebe4"),
    "قهوه ای": ("Brown", "#765444"),
    "سرمه ای": ("Navy", "#354562"),
    "بژ": ("Beige", "#d2bc9e"),
    "تیتانیوم": ("Titanium", "#72777e")
}



# CSS Design
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Vazirmatn:wght@400;500;600;700;800&display=swap');


/* Main Application */
.stApp {
    background-color: #f7f8fb;
    color: #172334;
    font-family: 'Inter', 'Vazirmatn', sans-serif;
}


/* Main Container */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* Main Header */
.hero {
    text-align: center;
    padding: 25px 0 30px 0;
}

.hero h1 {
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    font-size: 42px;
    font-weight: 800;
    color: #1c293a;
    line-height: 1.8;
    margin-bottom: 5px;
    direction: rtl;
}

.hero p {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 4px;
    color: #718096;
    margin-top: 0;
}


/* Section Titles */
h1, h2, h3 {
    font-family: 'Inter', 'Vazirmatn', sans-serif;
    color: #1c293a;
    font-weight: 700;
}

h2 {
    font-size: 25px;
    letter-spacing: -0.5px;
}

h3 {
    font-size: 20px;
}


/* Normal Text */
p, span, label {
    font-family: 'Inter', 'Vazirmatn', sans-serif;
}


/* Buttons */
div.stButton > button {
    background-color: #ffffff !important;
    color: #172a42 !important;
    border: 1px solid #d9e0ea !important;
    border-radius: 12px !important;
    font-family: 'Inter', 'Vazirmatn', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    transition: all 0.2s ease;
}

div.stButton > button p,
div.stButton > button span {
    color: #172a42 !important;
    font-weight: 600 !important;
}

div.stButton > button:hover {
    background-color: #eef3f9 !important;
    border-color: #8fa4bc !important;
    color: #172a42 !important;
}


/* Primary Button - Estimate Price */
div.stButton > button[kind="primary"] {
    background-color: #1e3654 !important;
    border: 1px solid #1e3654 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}

div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span {
    color: #ffffff !important;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #2b4c72 !important;
    border-color: #2b4c72 !important;
}


/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #d9e0ea !important;
    border-radius: 10px !important;
    min-height: 45px;
    color: #172334 !important;
    font-family: 'Inter', 'Vazirmatn', sans-serif !important;
}

div[data-baseweb="select"] span {
    color: #172334 !important;
}


/* Number Input */
div[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    color: #172334 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
}


/* Input Labels */
div[data-testid="stWidgetLabel"] label,
div[data-testid="stWidgetLabel"] p {
    color: #34445a !important;
    font-family: 'Inter', 'Vazirmatn', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}


/* Images */
div[data-testid="stImage"] img {
    border-radius: 12px;
}


/* Captions */
div[data-testid="stCaptionContainer"] p {
    font-family: 'Inter', 'Vazirmatn', sans-serif;
    color: #7b8797 !important;
    font-size: 12px;
}


/* Progress Bar */
div[data-testid="stProgress"] > div {
    border-radius: 20px;
}

div[data-testid="stProgress"] > div > div {
    background-color: #1e3654 !important;
    border-radius: 20px;
}


/* Estimated Price Card */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e2e7ef;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 4px 15px rgba(30, 54, 84, 0.05);
}

div[data-testid="stMetricLabel"] p {
    color: #718096 !important;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 500;
}

div[data-testid="stMetricValue"] {
    color: #1e3654 !important;
    font-family: 'Inter', sans-serif;
    font-size: 30px;
    font-weight: 800;
}


/* Success Message */
div[data-testid="stAlert"] {
    border-radius: 12px;
    font-family: 'Inter', 'Vazirmatn', sans-serif;
}


/* Mobile Responsive */
@media (max-width: 768px) {

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 15px 0 20px 0;
    }

    .hero h1 {
        font-size: 30px;
    }

    .hero p {
        font-size: 10px;
        letter-spacing: 2px;
    }

    h2 {
        font-size: 20px;
    }

    div.stButton > button {
        font-size: 13px !important;
        padding: 10px 12px !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
}

</style>
""", unsafe_allow_html=True)


# Session State
if "step" not in st.session_state:
    st.session_state.step = 1

if "brand_choice" not in st.session_state:
    st.session_state.brand_choice = ""

if "car_choice" not in st.session_state:
    st.session_state.car_choice = ""

if "color_choice" not in st.session_state:
    st.session_state.color_choice = ""


#Header
st.markdown("""
<div class="hero">
    <h1>تخمین قیمت خودرو</h1>
    <p>CAR PRICE ESTIMATOR</p>
</div>
""", unsafe_allow_html=True)
st.progress(st.session_state.step / 4)


# Step 1: Select Brand
if st.session_state.step == 1:

    st.header("01 - Choose a brand")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="brand-image">',
            unsafe_allow_html=True
        )

        st.image(
            "assets/peugeot_brand.webp",

        )

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Peugeot", use_container_width=True):
            st.session_state.brand_choice = "Peugeot"
            st.session_state.step = 2
            st.rerun()

    with col2:

        st.markdown(
            '<div class="brand-image">',
            unsafe_allow_html=True
        )

        st.image(
            "assets/kia_brand.webp",


        )

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Kia", use_container_width=True):
            st.session_state.brand_choice = "Kia"
            st.session_state.step = 2
            st.rerun()

# Step 2: Select Car
elif st.session_state.step == 2:

    if st.button("← Back to brands"):
        st.session_state.step = 1
        st.rerun()

    st.header("02 - Choose a car")

    if st.session_state.brand_choice == "Peugeot":
        choices = ["Peugeot 206", "Peugeot 207"]
    else:
        choices = ["Kia Optima", "Kia K5", "Kia Sportage"]

    columns = st.columns(len(choices))

    for column, name in zip(columns, choices):

        with column:

            st.image(
                cars[name][2],
                use_container_width=True
            )

            if st.button(name, key=name, use_container_width=True):
                st.session_state.car_choice = name
                st.session_state.step = 3
                st.rerun()


# Step 3: Select Color
elif st.session_state.step == 3:

    if st.button("← Back to cars"):
        st.session_state.step = 2
        st.rerun()

    st.header("03 - Choose a color")

    df_car, data_brand, picture = cars[st.session_state.car_choice]

    df_car = df_car[df_car["brand"] == data_brand]

    st.image(picture, width=330)
    st.caption(st.session_state.car_choice + " - Available colors")

    available_colors = sorted(
        df_car["color"].dropna().unique()
    )

    columns = st.columns(4)

    for i, color in enumerate(available_colors):

        english, hex_color = colors.get(
            color, (color, "#cbd5e1")
        )

        with columns[i % 4]:

            st.markdown(
                f"""
                <div style="
                    height:60px;
                    background:{hex_color};
                    border:1px solid #d6dce4;
                    border-radius:12px;
                    margin-top:12px;
                "></div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                english,
                key="color_" + color,
                use_container_width=True
            ):
                st.session_state.color_choice = color
                st.session_state.step = 4
                st.rerun()


# Step 4: Car Information
else:

    if st.button("← Back to colors"):
        st.session_state.step = 3
        st.rerun()

    st.header("04 - Vehicle details")

    df_car, brand, picture = cars[st.session_state.car_choice]

    df_car = df_car[df_car["brand"] == brand]

    color = st.session_state.color_choice

    st.image(picture, width=340)

    st.caption(
        st.session_state.car_choice
        + " | "
        + colors.get(color, (color, ""))[0]
    )

    # Get real values from dataset
    models = sorted(
        df_car["model"].fillna("نامشخص").unique().tolist()
    )

    gearboxes = sorted(
        df_car["gearbox"].fillna("نامشخص").unique().tolist()
    )

    gearbox_names = {
        "دنده ای": "Manual",
        "اتوماتیک": "Automatic",
        "نامشخص": "Unknown"
    }

    col1, col2 = st.columns(2)

    with col1:

        model = st.selectbox(
            "Trim / Model",
            models
        )

        year = st.selectbox(
            "Manufacturing Year",
            sorted(
                df_car["year"].dropna().astype(int).unique(),
                reverse=True
            )
        )

    with col2:

        gearbox = st.selectbox(
            "Gearbox",
            gearboxes,
            format_func=lambda x: gearbox_names.get(x, x)
        )

        mileage = st.number_input(
            "Mileage (km)",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=1000
        )


    # Predict Price
    if st.button(
        "Estimate Price",
        type="primary",
        use_container_width=True
    ):

        new_data = pd.DataFrame([{
            "brand": brand,
            "model": model,
            "year": int(year),
            "mileage": int(mileage),
            "color": color,
            "gearbox": gearbox
        }])

        result = loaded_model.predict(new_data)

        price = float(result[0])

        if price <= 0:
            st.warning(
                "The model returned an invalid price."
            )

        else:
            st.metric(
                "Estimated listing price",
                f"{price:,.0f} Toman"
            )

            st.caption(
                "Estimate only - actual market prices may differ."
            )




