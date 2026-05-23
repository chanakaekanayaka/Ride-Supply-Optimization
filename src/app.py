import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up a professional web page layout
st.set_page_config(
    page_title="Supply Optimization Dashboard", 
    page_icon="🚖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
# Fixed: Changed unsafe_html to unsafe_allow_html
st.markdown("""
    <style>
    .main-title { font-size:38px !important; font-weight: bold; color: #1E3A8A; }
    .subtitle { font-size:18px !important; color: #4B5563; margin-bottom: 20px; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-title">🚖Ride-Supply Optimization Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enterprise Data Science Solution for Predictive Surge Pricing & Fleet Retention</p>', unsafe_allow_html=True)
st.markdown("---")

# 1. SIDEBAR INPUTS (Cleaned & Categorized)
st.sidebar.header("Real-Time Ride Parameters")

with st.sidebar.expander("Spatial Parameters (Location)", expanded=True):
    source_zone = st.selectbox("Pickup Location (Source)", 
                               options=["Haymarket Square", "Financial District", "South Station", 
                                        "Theatre District", "Back Bay", "Boston University", "Northeastern University", "Fenway"])
    destination_zone = st.selectbox("Dropoff Location (Destination)", 
                                    options=["North Station", "West End", "Financial District", "South Station", "Back Bay"])
    distance = st.slider("Ride Distance (Miles)", min_value=0.1, max_value=25.0, value=3.5, step=0.1)

with st.sidebar.expander("Temporal Parameters (Time)", expanded=True):
    hour_of_day = st.slider("Hour of the Day (0-23)", min_value=0, max_value=23, value=17, step=1)
    day_of_week = st.selectbox("Day of the Week", options=[0, 1, 2, 3, 4, 5, 6], 
                               format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x], index=4)

with st.sidebar.expander("Pricing Parameters", expanded=True):
    surge_multiplier = st.selectbox("Current Surge Multiplier", options=[1.0, 1.25, 1.5, 1.75, 2.0, 2.5], index=0)

# Behind-the-scenes Simulation Logic
low_earning_zones = ["Boston University", "Northeastern University", "Fenway"]
is_high_risk_zone = 1 if source_zone in low_earning_zones else 0

# Financial Calculation Simulation
base_fare = 4.50
distance_fare = distance * 2.50
simulated_gross = (base_fare + distance_fare) * surge_multiplier
company_commission = simulated_gross * 0.20
driver_net = simulated_gross * 0.80

# Ride Duration estimation based on average speed
ride_duration_hours = max(distance / 22.0, 0.1) 
driver_net_per_hour = driver_net / ride_duration_hours

# AI Predictive Rule
predict_low_pay = 1 if (is_high_risk_zone == 1 or driver_net_per_hour < 60.0) else 0


# 2. MAIN DASHBOARD CONTENT (Layout Split into 2 Columns)
col_metrics, col_visuals = st.columns([1.2, 1])

with col_metrics:
    st.subheader("📊 Operational Analytics & KPIs")
    
    # Grid Layout for Top Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total Customer Fare", value=f"${simulated_gross:.2f}")
    with m2:
        st.metric(label="Driver Net Payout (80%)", value=f"${driver_net:.2f}")
    with m3:
        st.metric(label="Driver Hourly Rate", value=f"${driver_net_per_hour:.2f}/hr")
        
    st.markdown("---")
    
    # ML Prediction Output Alert Box
    st.write("**AI Supply Risk Assessment:**")
    if predict_low_pay == 1:
        st.error(f"⚠️ **HIGH RISK:** Drivers in **{source_zone}** are making suboptimal hourly rates (${driver_net_per_hour:.2f}/hr). High cancellation probability expected.")
        
        # Recommendation Engine Box
        st.markdown("### 💡 AI Smart Recommendation")
        recommended_surge = surge_multiplier + 0.25 if source_zone in low_earning_zones else surge_multiplier + 0.50
        st.warning(f"**Action Required:** Inject a dynamic Surge Multiplier of **{recommended_surge}x** for {source_zone} to motivate driver acceptance and mitigate supply deficit.")
    else:
        st.success(f"✅ **LOW RISK:** Optimal Earning Zone detected. Driver payout rate is highly competitive. Ride acceptance probability is high.")


with col_visuals:
    st.subheader("📈 Financial Breakdowns")
    
    # 1. Pie Chart for Fare Breakdown (Company vs Driver)
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Driver Share (80%)', ' platform Commission (20%)']
    sizes = [driver_net, company_commission]
    colors = ['#10B981', '#3B82F6']
    explode = (0.05, 0)  
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, 
           textprops={'fontsize': 10, 'weight': 'bold'})
    ax.axis('equal')
    plt.title("Fare Revenue Distribution Split", fontsize=12, weight='bold', pad=20)
    st.pyplot(fig)
    
    # 2. Route Summary Informational Card
    # Fixed: Changed unsafe_html to unsafe_allow_html
    # 2. Route Summary Informational Card (Enhanced with Premium Dark Theme)
    st.markdown(f"""
    <div style="
        background-color: #1E293B; 
        padding: 22px; 
        border-radius: 12px; 
        border-left: 5px solid #F59E0B;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-top: 15px;
    ">
        <h4 style="color: #F59E0B; margin-top: 0; font-family: sans-serif; font-size: 20px;">📋 Route Summary</h4>
        <p style="color: #E2E8F0; font-size: 15px; margin: 8px 0;"><b>From:</b> <span style="color: #38BDF8;">{source_zone}</span> | <b>To:</b> <span style="color: #38BDF8;">{destination_zone}</span></p>
        <p style="color: #E2E8F0; font-size: 15px; margin: 8px 0;"><b>Est. Trip Duration:</b> <span style="color: #10B981; font-weight: bold;">{ride_duration_hours*60:.0f} Minutes</span></p>
        <p style="color: #E2E8F0; font-size: 15px; margin: 8px 0;"><b>Temporal Framework:</b> Hour <span style="color: #A78BFA;">{hour_of_day}:00</span> on a Day-Type <span style="color: #F472B6;">{"Weekend" if day_of_week in [5,6] else "Weekday"}</span></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Developed by Chanaka Ekanayaka | Specialized Data Science & Software Engineering Portfolio Project © 2026")