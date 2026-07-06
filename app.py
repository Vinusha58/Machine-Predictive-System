import streamlit as st
import pandas as pd
import joblib

# 1. Model matrum Columns-ah load panrom
try:
    model = joblib.load('lgb_model.pkl')
    model_cols = joblib.load('model_columns.pkl')
except Exception as e:
    st.error(f"Error loading files: {e}")

st.set_page_config(page_title="LGB AI Maintenance", page_icon="⚙️")
st.title("⚙️ LGB AI - Maintenance System")

# Inputs - Intha values Default-ah failure trigger panra mari vachuruken
air_temp = st.number_input("Air temperature [K]", value=300.0)
proc_temp = st.number_input("Process temperature [K]", value=310.0)
speed = st.number_input("Rotational speed [rpm]", value=1500)
torque = st.number_input("Torque [Nm]", value=40.0)
tool_wear = st.number_input("Tool wear [min]", value=230)

if st.button("Check Status"):
    try:
        # Step A: DataFrame with 10 columns (Model expects 10 columns)
        # Ella column-aiyum zero aaki, namma kitta irukura 5 values-ah insert panrom
        df_input = pd.DataFrame([[0] * len(model_cols)], columns=model_cols)
        
        # Column names matching logic
        for col in model_cols:
            if 'Air temperature' in col: df_input[col] = air_temp
            elif 'Process temperature' in col: df_input[col] = proc_temp
            elif 'Rotational speed' in col: df_input[col] = speed
            elif 'Torque' in col: df_input[col] = torque
            elif 'Tool wear' in col: df_input[col] = tool_wear

        # Step B: AI Model Prediction
        prediction = model.predict(df_input)

        # Step C: Failure Logic (Model 1-nu sonnalo or values limit thaandunaalo)
        # Presentation-la failure kaatunumna Tool Wear 200 mela kudunga
        if prediction[0] == 1 or tool_wear >= 200 or torque >= 65:
            st.error("🚨 WARNING: Machine Failure Detected!")
            st.divider()
            st.subheader("⚠️ Reason for Alert:")
            if tool_wear >= 200:
                st.warning("📍 Tool Wear is High: Part replacement required soon.")
            if torque >= 65:
                st.warning("📍 High Torque Load: Motor strain detected.")
            if (proc_temp - air_temp) < 8.5:
                st.warning("📍 Heat Dissipation Issue: Cooling system check needed.")
        else:
            st.success("✅ Machine Status: Healthy")
            st.info("Everything is running within normal parameters.")

    except Exception as e:
        st.error(f"Logical Error: {e}")