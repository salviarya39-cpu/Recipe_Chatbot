import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

print(os.getenv("GEMINI_API_KEY"))
# Load API key
load_dotenv()

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Streamlit Page Settings
st.set_page_config(page_title="Recipe Recommendation Agent")

st.title("🍳 AI Recipe Recommendation Agent")

# Chat History
if "history" not in st.session_state:
    st.session_state.history = []

# Clear History Button
if st.button("🗑 Clear History"):
    st.session_state.history = []
    st.rerun()

# Ingredient Input
ingredients = st.text_area(
    "Enter Ingredients",
    placeholder="Example: Eggs, Bread, Onion, Butter"
)

# Generate Recipe
if st.button("Generate Recipe"):

    if ingredients.strip() == "":
        st.warning("Please enter some ingredients.")
    else:

        prompt = f"""
        You are a professional chef and nutrition expert.

        Available Ingredients:
        {ingredients}

        Generate a recipe in the following format:

        🍽 Recipe Name

        ⏱ Cooking Time

        📊 Difficulty Level
        (Easy / Medium / Hard)

        🥗 Category
        (Vegetarian / Non-Vegetarian)

        🔥 Nutrition Information
        - Calories
        - Protein
        - Carbohydrates
        - Fat

        👨‍🍳 Step-by-Step Instructions

        💡 Cooking Tips
        """

        response = llm.invoke(prompt)

        recipe = response.content

        st.session_state.history.append({
            "ingredients": ingredients,
            "recipe": recipe
        })

        st.success("Recipe Generated Successfully!")

# Display History
st.subheader("📜 Recipe History")

for item in reversed(st.session_state.history):

    st.markdown("### 🥘 Ingredients")
    st.write(item["ingredients"])

    st.markdown("### 🍴 Recipe")
    st.write(item["recipe"])

    st.divider()