import streamlit as st
from main import app
from dotenv import load_dotenv

# Ensure env vars are loaded
load_dotenv()

st.set_page_config(page_title="AI Weather & AQI Agent", page_icon="🌤️")

st.title("🌤️ AI Weather & Air Quality Agent")
st.markdown("Ask about weather and air quality for any city!")

# User Input
task = st.text_input("Enter your request:", placeholder="e.g. What is the weather and air quality in Mumbai?")

if st.button("Get Info"):
    if task:
        with st.spinner("Agents are working... (Planning -> Executing -> Verifying)"):
            try:
                # Invoke the LangGraph app
                output = app.invoke({"task": task})
                final_result = output.get("final")

                if final_result:
                    # Display Result
                    st.success("Analysis Complete!")
                    
                    st.subheader(f"📍 City: {final_result.city}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info("🌡️ Weather")
                        weather = final_result.weather
                        if weather:
                            st.metric(label="Temperature", value=f"{weather.get('temp', 'N/A')} °C")
                            st.write(f"**Condition:** {weather.get('condition', 'N/A').title()}")
                        else:
                            st.write("No weather data available.")

                    with col2:
                        st.info("💨 Air Quality")
                        aq = final_result.air_quality
                        if aq:
                            st.metric(label="AQI", value=aq.get('aqi', 'N/A'))
                            st.write(f"**Level:** {aq.get('level', 'N/A')}")
                        else:
                            st.write("No air quality data available.")
                            
                    with st.expander("See Raw JSON Response"):
                        st.json(final_result.model_dump())
                else:
                    st.error("Agents failed to produce a final answer.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a task description.")
