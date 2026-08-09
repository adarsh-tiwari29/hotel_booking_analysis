#  Hotel Business Performance & Cancellation Analytics

An interactive data analytics web application built with **Streamlit** and **Python** to analyze hotel booking trends, cancellation rates, stay durations, and lead-time patterns (2017–2019). The project translates raw hospitality data into actionable business recommendations for hotel revenue teams.

---

##  Live Demo of this Project

https://hotel-booking-analysis-project.streamlit.app/

---

##  Business Objectives & Key Questions

The primary objective of this project is to provide data-driven insights into guest booking behaviors and identify key friction points in hotel revenue cycles:

1. **Hotel Type Popularity:** How do booking volumes and seasonalities differ between City Hotels and Resort Hotels?
2. **Stay Duration Impact:** Does the length of stay influence the likelihood of reservation cancellations?
3. **Lead Time Dynamics:** How does the time gap between booking date and arrival date affect cancellation rates?

---

##  Tech Stack & Libraries

* **Language:** Python
* **Dashboard Framework:** Streamlit
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Seaborn, Matplotlib

---

##  Key Insights & Executive Findings

* **Market Share & Demand:** City Hotels experience higher booking volumes overall, but face a noticeably higher baseline cancellation rate compared to Resort Hotels.
* **Seasonality Trends:** Booking peaks heavily align with summer vacation months (July and August) across both hotel types.
* **Lead Time Vulnerability:** Bookings made far in advance (>90 days) exhibit a significantly higher cancellation rate compared to last-minute bookings (0-7 days).
* **Stay Length Risk:** Longer extended stays show increased variance in cancellation probability, suggesting guest plan changes over extended lead times.

---

##  Strategic Business Recommendations

1. **Overhaul Advanced Booking Policy:** Introduce a non-refundable partial deposit policy for bookings made more than 60 to 90 days in advance to mitigate speculative bookings.
2. **Dynamic Pricing for City Hotels:** Leverage higher peak demand in City Hotels using tiered dynamic pricing to maximize Average Daily Rate (ADR).
3. **Off-Peak Resort Packages:** Design promotional weekend retreats and wellness bundles to drive Resort Hotel occupancy during quiet winter months.

---

##  Local Installation & Setup Guide

To run this application on your local machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/adarsh-tiwari29/hotel_booking_analysis
```

### 2. Install Required Dependencies
Make sure you have Python installed, then run:
```bash
pip install streamlit pandas matplotlib seaborn numpy
```

### 3. Run the Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 📁 Repository Structure

```text
├── app.py                   # Streamlit dashboard source code
├── hotel_bookings_data.csv  # Cleaned dataset
├── requirements.txt         # All required Libraries
├── README.md                # Project documentation

```

---

## 👤 Author

* **Adarsh Shrikant Tiwari**
* **Role:** Data Analyst / Developer
* **Toolkit:** Python | SQL | Power BI | Streamlit
