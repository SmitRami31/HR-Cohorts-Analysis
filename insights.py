import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="HR Strategic Workforce Analytics", layout="wide")
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
    </style>
""", unsafe_allow_html=True)

def clean_currency(x):
    if isinstance(x, str):
        clean_str = x.replace(',', '').replace('"', '').replace('$', '').strip()
        try:
            return float(clean_str)
        except ValueError:
            return 0.0
    return x if isinstance(x, (int, float)) else 0.0

def process_cohorts(df):    
    stagnant_tenure_markers = ['>4', '3-4', '3-5 years', '5+ years']
    stagnant_comp_markers = [
        'STARTER1', 'STARTER2', 'STARTER3', 
        'CONFIRM1', 'CONFIRM2', 'CONFIRM3', 
        'EXPERC1', 'EXPERC2', 'SPECIALIST',
        'Starter 1', 'Starter 2', 'Confirmed 1', 'Confirmed 2', 'Experienced 1'
    ]
    
    df['Time_Norm'] = df['Time in Role (Range)'].astype(str).str.strip()
    df['Comp_Norm'] = df['Competence'].astype(str).str.upper().str.strip()
    
    df['is_stagnant'] = (df['Time_Norm'].isin(stagnant_tenure_markers) & df['Comp_Norm'].isin(stagnant_comp_markers))

    hi_po_markers = ['KEY', 'HIGHPO', 'RISING', 'CONSIST', 'STAR']
    hi_risk_markers = ['MEDIUM', 'HIGH', 'VERY HIGH']
    
    df['Talent_Norm'] = df['Talent & Potential'].astype(str).str.upper().str.strip()
    df['Risk_Norm'] = df['Attrition Risk'].astype(str).str.upper().str.strip()
    
    df['is_risk'] = (df['Talent_Norm'].isin(hi_po_markers) & df['Risk_Norm'].isin(hi_risk_markers))
    
    if 'Employee replacement' in df.columns:df['Employee replacement'] = df['Employee replacement'].apply(clean_currency)
    else:df['Employee replacement'] = 0.0
    return df

@st.cache_data
def load_and_analyze_data(file_24, file_25):
    df24 = pd.read_csv(file_24)
    df25 = pd.read_csv(file_25)

    df24 = process_cohorts(df24)
    df25 = process_cohorts(df25)
    
    merged = pd.merge(df24, df25, on='Team member ID', how='left', suffixes=('_24', '_25'))
    merged['status'] = np.where(merged['Qprofile ID_25'].isna(), 'Left', 'Retained')
    return df24, df25, merged

with st.sidebar:
    st.header("Data Upload")
    st.info("Upload the raw CSV extracts for 2024 and 2025.")
    f24 = st.file_uploader("Upload 2024 Data (CSV)", type=['csv'])
    f25 = st.file_uploader("Upload 2025 Data (CSV)", type=['csv'])
    
    st.divider()
    st.write("### Analysis Parameters")
    st.caption("Cohorts defined by technical skill sheet logic.")

st.title("HR Strategic Insights Dashboard")
st.markdown("### Year-Over-Year Cohort Analysis (2024 vs 2025)")

if f24 and f25:
    df24, df25, merged = load_and_analyze_data(f24, f25)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_stagnant_24 = df24['is_stagnant'].sum()
    total_risk_24 = df24['is_risk'].sum()
    
    turnover_count = len(merged[merged['status'] == 'Left'])
    turnover_cost = merged[merged['status'] == 'Left']['Employee replacement_24'].sum()
    
    col1.metric("Total Headcount (2024)", len(df24))
    col2.metric("Turnover Count", turnover_count, f"-{turnover_count/len(df24):.1%} Rate")
    col3.metric("Departure Cost", f"${turnover_cost:,.0f}", "Est. Replacement")
    col4.metric("Dual Risk Candidates", len(merged[(merged['is_stagnant_24']) & (merged['is_risk_24'])]))
    st.divider()

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        with st.container(border=True):
            st.subheader("1. Intervention Effectiveness Failure")
            st.markdown("**Insight:** Retention efforts for identified 'High Risk' talent are failing.")
            
            risk_cohort = merged[merged['is_risk_24'] == True]
            
            # Categories
            left = len(risk_cohort[risk_cohort['status'] == 'Left'])
            still_risk = len(risk_cohort[(risk_cohort['status'] == 'Retained') & (risk_cohort['is_risk_25'] == True)])
            improved = len(risk_cohort[(risk_cohort['status'] == 'Retained') & (risk_cohort['is_risk_25'] == False)])
            
            # Pie Chart
            labels = ['Left Organization', 'Still At Risk (Failure)', 'Risk Mitigated (Success)']
            values = [left, still_risk, improved]
            colors = ['#EF553B', '#FFA15A', '#00CC96']
            
            fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=colors)])
            fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            
            st.plotly_chart(fig1, width='stretch')
            
            fail_rate = ((left + still_risk) / len(risk_cohort)) * 100
            st.caption(f"**{fail_rate:.1f}% Failure Rate:** {left} Left + {still_risk} Still at Risk out of {len(risk_cohort)} identified employees.")

    with row1_col2:
        with st.container(border=True):
            st.subheader("2. Manager Capability Crisis")
            st.markdown("**Insight:** Stagnation is concentrated under specific managers, indicating a coaching gap.")
            
            # Data Prep: Stagnant employees in 2025
            stagnant_25 = df25[df25['is_stagnant'] == True]
            mgr_counts = stagnant_25['Manager'].value_counts().head(5).reset_index()
            mgr_counts.columns = ['Manager', 'Stagnant Count']
            
            fig2 = px.bar(
                mgr_counts, 
                x='Stagnant Count', 
                y='Manager', 
                orientation='h',
                color='Stagnant Count',
                color_continuous_scale='Reds'
            )
            fig2.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=0, b=0, l=0, r=0), height=300)
            
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("Top 5 Managers with the highest number of stagnant team members in 2025.")

    # =========================================================================
    # ROW 2: INSIGHT 3 & 4
    # =========================================================================
    row2_col1, row2_col2 = st.columns(2)

    # --- INSIGHT 3: SUCCESS PATTERNS ---
    with row2_col1:
        with st.container(border=True):
            st.subheader("3. Cross-Functional Success Pattern")
            st.markdown("**Insight:** Changing managers is the #1 predictor of breaking out of stagnation.")
            
            # Data Prep: Who was stagnant in 24 and retained?
            stagnant_retained = merged[(merged['is_stagnant_24'] == True) & (merged['status'] == 'Retained')].copy()
            
            # Did they improve?
            stagnant_retained['Outcome'] = np.where(stagnant_retained['is_stagnant_25'] == False, 'Improved', 'Stayed Stagnant')
            
            # Did they change managers?
            stagnant_retained['Manager Change'] = np.where(
                stagnant_retained['Manager_24'] != stagnant_retained['Manager_25'], 
                'Changed Manager', 
                'Same Manager'
            )
            
            # Grouping
            success_metrics = stagnant_retained.groupby(['Manager Change', 'Outcome']).size().reset_index(name='Count')
            
            fig3 = px.bar(
                success_metrics, 
                x='Manager Change', 
                y='Count', 
                color='Outcome', 
                barmode='group',
                color_discrete_map={'Improved': '#00CC96', 'Stayed Stagnant': '#EF553B'}
            )
            fig3.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig3, use_container_width=True)
            
            st.caption("Comparison of improvement rates between employees who moved teams vs those who stayed.")

    # --- INSIGHT 4: DEPT CONCENTRATION ---
    with row2_col1:
        with row2_col2:
            with st.container(border=True):
                st.subheader("4. Department Concentration Alert")
                st.markdown("**Insight:** Certain departments are accumulating stagnant talent faster than others.")
                
                # Data Prep
                dept_24 = df24[df24['is_stagnant'] == True]['Department'].value_counts().reset_index()
                dept_24.columns = ['Department', 'Count']
                dept_24['Year'] = '2024'
                
                dept_25 = df25[df25['is_stagnant'] == True]['Department'].value_counts().reset_index()
                dept_25.columns = ['Department', 'Count']
                dept_25['Year'] = '2025'
                
                dept_combined = pd.concat([dept_24, dept_25])
                
                # Filter to top 5 depts by volume
                top_depts = dept_25.head(5)['Department'].tolist()
                dept_filtered = dept_combined[dept_combined['Department'].isin(top_depts)]
                
                fig4 = px.bar(
                    dept_filtered,
                    x='Department',
                    y='Count',
                    color='Year',
                    barmode='group',
                    color_discrete_sequence=['#636EFA', '#EF553B']
                )
                fig4.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig4, use_container_width=True)
                st.caption("Year-over-Year growth of stagnant employees by Department.")

    # =========================================================================
    # ROW 3: INSIGHT 5 (FULL WIDTH)
    # =========================================================================
    with st.container(border=True):
        st.subheader("5. Dual-Risk Hidden Gems (High ROI Targets)")
        st.markdown("""
        **Insight:** These employees are identified as **High Potential** but are currently **Stagnating**. 
        They represent the highest risk of capital flight but also the easiest retention wins through immediate role changes.
        """)
        
        # Data Prep
        dual_risk = merged[
            (merged['is_stagnant_24'] == True) & 
            (merged['is_risk_24'] == True)
        ].copy()
        
        if not dual_risk.empty:
            cols_to_show = [
                'First Name_24', 'Last Name_24', 'Department_24', 
                'Manager_24', 'Talent & Potential_24', 'Employee replacement_24'
            ]
            
            # Formatting for display
            display_df = dual_risk[cols_to_show].rename(columns={
                'First Name_24': 'First Name',
                'Last Name_24': 'Last Name',
                'Department_24': 'Department',
                'Manager_24': 'Manager',
                'Talent & Potential_24': 'Potential',
                'Employee replacement_24': 'Replacement Liability'
            })
            
            col_kpi, col_table = st.columns([1, 3])
            
            with col_kpi:
                total_liability = display_df['Replacement Liability'].sum()
                st.metric("Total Liability", f"${total_liability:,.0f}")
                st.metric("Employee Count", len(display_df))
                st.error("Action: Schedule Stay Interviews within 7 days.")
            
            with col_table:
                st.dataframe(
                    display_df.style.format({'Replacement Liability': '${:,.0f}'}),
                    use_container_width=True
                )
        else:
            st.success("No employees currently fit the Dual-Risk criteria.")

else:
    # Empty State
    st.warning("👈 Please upload both the 2024 and 2025 CSV files in the sidebar to generate the dashboard.")
    st.image("https://placehold.co/1200x400?text=Awaiting+Data+Upload", use_column_width=True)