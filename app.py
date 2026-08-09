import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Hotel Business Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Customizing seaborn style for professional charts
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# ==========================================
# DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_and_clean_data():
    # Load dataset
    df = pd.read_csv('hotel_bookings_data.csv')
    
    # 1. Handle Missing Values (Safely checking if column exists first)
    if 'children' in df.columns:
        df['children'] = df['children'].fillna(0)
        
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('Unknown')
        
    if 'agent' in df.columns:
        df['agent'] = df['agent'].fillna(0)
        
    if 'company' in df.columns:
        df['company'] = df['company'].fillna(0)
    
    # 2. Drop Duplicates
    df = df.drop_duplicates()
    
    # 3. Feature Engineering & Anomalies
    # Checking if required columns exist before creating total_guests
    if all(col in df.columns for col in ['adults', 'children', 'babies']):
        df['total_guests'] = df['adults'] + df['children'] + df['babies']
    else:
        # Fallback just in case
        df['total_guests'] = 1 
        
    if all(col in df.columns for col in ['stays_in_weekend_nights', 'stays_in_weekdays_nights']):
        df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_weekdays_nights']
    else:
        df['total_stay'] = 1
    
    # Filter anomalies (0 guests or negative ADR)
    if 'total_guests' in df.columns and 'adr' in df.columns:
        df = df[(df['total_guests'] > 0) & (df['adr'] >= 0)]
    
    # Categorize Lead Time for better visualization
    if 'lead_time' in df.columns:
        bins = [-1, 7, 30, 90, 180, 365, 1000]
        labels = ['0-7 Days', '8-30 Days', '31-90 Days', '91-180 Days', '181-365 Days', '>365 Days']
        df['lead_time_group'] = pd.cut(df['lead_time'], bins=bins, labels=labels)
    
    return df

df = load_and_clean_data()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title(" Hotel Analytics Menu")
st.sidebar.markdown("Navigate through the business insights:")
nav_option = st.sidebar.radio(
    "Select a Module:",
    ("Overview & KPIs", 
     "1. Hotel Type Popularity", 
     "2. Stay Duration vs Cancellations", 
     "3. Lead Time Impact", 
     "Executive Recommendations")
)

st.sidebar.markdown("---")
st.sidebar.info("Developed by: Adarsh Shrikant Tiwari\n\n**Role**: Data Analyst")

# ==========================================
# MAIN CONTENT SECTIONS
# ==========================================

st.title(" Hotel Business Performance Dashboard")
st.markdown("Analyzing customer booking and cancellation behaviors (2017-2019).")

if nav_option == "Overview & KPIs":
    st.header("Project Overview")
    st.write("This dashboard investigates historical hotel booking data to uncover actionable insights regarding guest preferences, seasonal demand, and factors driving cancellations.")
    
    # Top Level KPIs
    st.subheader("Key Performance Indicators (KPIs)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Valid Bookings", value=f"{len(df):,}")
    with col2:
        cancel_rate = (df['is_canceled'].mean() * 100)
        st.metric(label="Overall Cancellation Rate", value=f"{cancel_rate:.1f}%")
    with col3:
        avg_lead_time = df['lead_time'].mean()
        st.metric(label="Avg. Lead Time", value=f"{avg_lead_time:.0f} Days")
    with col4:
        avg_adr = df['adr'].mean()
        st.metric(label="Average Daily Rate (ADR)", value=f"${avg_adr:.2f}")

elif nav_option == "1. Hotel Type Popularity":
    st.header("1. Monthly Booking Analysis by Hotel Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Booking Share by Hotel Type")
        fig, ax = plt.subplots(figsize=(6, 6))
        hotel_counts = df['hotel'].value_counts()
        ax.pie(hotel_counts, labels=hotel_counts.index, autopct='%1.1f%%', 
               colors=['#4C72B0', '#55A868'], startangle=90, explode=(0.05, 0))
        ax.set_title("Market Share: City vs Resort Hotel")
        st.pyplot(fig)
        st.caption("City Hotels dominate the booking volume compared to Resort Hotels.")

    with col2:
        st.subheader("Seasonality: Monthly Booking Trends")
        # Order months logically
        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=months, ordered=True)
        
        monthly_bookings = df.groupby(['arrival_date_month', 'hotel']).size().reset_index(name='Count')
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=monthly_bookings, x='arrival_date_month', y='Count', hue='hotel', marker='o', palette=['#4C72B0', '#55A868'], ax=ax2)
        ax2.set_xticklabels(months, rotation=45)
        ax2.set_ylabel("Number of Bookings")
        ax2.set_xlabel("Month")
        ax2.set_title("Busy vs Quiet Months")
        st.pyplot(fig2)
        st.caption("Peak seasons usually align with summer holidays (July/August).")

elif nav_option == "2. Stay Duration vs Cancellations":
    st.header("2. Impact of Stay Duration on Cancellation Rate")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Cancellation Rate by Hotel")
        cancel_rates = df.groupby('hotel')['is_canceled'].mean().reset_index()
        cancel_rates['is_canceled'] *= 100
        
        fig, ax = plt.subplots(figsize=(5, 6))
        sns.barplot(data=cancel_rates, x='hotel', y='is_canceled', palette=['#4C72B0', '#55A868'], ax=ax)
        ax.set_ylabel("Cancellation Rate (%)")
        ax.set_xlabel("Hotel Type")
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Stay Duration vs Probability of Cancellation")
        # Filter extreme outliers in stay duration for cleaner visualization (e.g., > 14 days)
        df_stay = df[df['total_stay'] <= 14]
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df_stay, x='total_stay', y='is_canceled', hue='hotel', marker='o', ci=None, palette=['#4C72B0', '#55A868'], ax=ax2)
        ax2.set_ylabel("Cancellation Probability (0 to 1)")
        ax2.set_xlabel("Total Length of Stay (Days)")
        ax2.set_xticks(range(1, 15))
        st.pyplot(fig2)
        st.caption("Notice how cancellation probability fluctuates as the planned length of stay increases.")

elif nav_option == "3. Lead Time Impact":
    st.header("3. Impact of Lead Time on Cancellation Rate")
    
    st.write("**Lead Time**: The number of days between the booking date and the actual arrival date.")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    lead_time_cancel = df.groupby(['lead_time_group', 'hotel'])['is_canceled'].mean().reset_index()
    lead_time_cancel['is_canceled'] *= 100
    
    sns.barplot(data=lead_time_cancel, x='lead_time_group', y='is_canceled', hue='hotel', palette=['#4C72B0', '#55A868'], ax=ax)
    ax.set_ylabel("Cancellation Rate (%)")
    ax.set_xlabel("Lead Time (Grouped)")
    ax.set_title("How Booking in Advance Affects Cancellations")
    st.pyplot(fig)
    st.caption("Cancellations are significantly lower for last-minute bookings (0-7 days) and peak for bookings made over 6 months in advance.")

elif nav_option == "Executive Recommendations":
    st.header(" Summary & Business Recommendations")
    
    st.markdown("###  Key Findings")
    st.info("""
    * **Popularity:** City Hotels receive significantly more bookings than Resort Hotels, but they also suffer from a higher baseline cancellation rate.
    * **Seasonality:** Summer months (July and August) represent the peak season for both properties.
    * **Stay Duration:** Longer stays generally show a higher risk of cancellation, likely due to guests' changing plans over extended periods.
    * **Lead Time:** The further out a booking is made, the higher the chance it will be canceled.
    """)
    
    st.markdown("###  Actionable Recommendations")
    
    st.markdown("**1. Hotel Type & Seasonality:**")
    st.write("> *Action:* To grow Resort Hotel bookings during off-peak months, introduce targeted promotional packages (e.g., weekend retreats or wellness packages). Capitalize on City Hotel peak seasons by implementing dynamic pricing to maximize ADR when demand is inelastic.")
    
    st.markdown("**2. Stay Duration & Cancellations:**")
    st.write("> *Action:* Implement stricter cancellation policies for extended stays (e.g., stays > 7 days). Offer non-refundable rates at a slight discount for longer bookings to lock in revenue.")
    
    st.markdown("**3. Lead Time Strategy:**")
    st.write("> *Action:* For bookings made 90+ days in advance, introduce a milestone-based deposit system or send automated, engaging reminder emails (with itinerary suggestions) to keep the guest committed to their trip.")
    
    st.markdown("### 🏆 Top Impact Recommendation")
    st.success("**Overhaul the Advanced Booking Policy (Lead Time):** The data clearly shows that bookings made far in advance are the most vulnerable to cancellation. Implementing a partial, non-refundable deposit for bookings made more than 60 days out will immediately reduce the volume of speculative bookings and secure guaranteed revenue.")