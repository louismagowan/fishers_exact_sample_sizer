# Normal imports
import pandas as pd
import streamlit as st
from scipy.stats import fisher_exact




# -------------------------- TOP OF PAGE INFORMATION -------------------------

# Set browser / tab config
st.set_page_config(
    page_title="Sample Sizer - Fisher's Exact Test",
    page_icon="🧊",
)

# Give some context for what the page displays
st.title('Estimate Sample Sizes for Different Upsell Rates')

# User inputs
st.header("Enter Inputs", divider="rainbow")


# Set sample size for each group
st.subheader("Sample Size")
sample_size = st.slider('Set the size of the sample for each group, e.g. "1000" means 1000 people in treatment and 1000 in control', 
          min_value = 0,
           max_value=10000,
            value=1000,
             step=100, key = "Sample size per group")
st.markdown("\n \n")

### CREATE CONTROL GROUP VALUES
# Set upsell rate in control group
control_upsell_rate = st.number_input('Set the upsell rate (%) you estimate for your control group', 
                                min_value=0.0,
                                max_value=100.0,
                                value=10.0, 
                                key = "Control group upsell rate")
st.markdown("Upsell rate for control group = " + str(control_upsell_rate) + "%")

st.markdown("\n \n")
# Rounding to give ints for fisher contingency table
control_no_upsell = round(sample_size * (1 - control_upsell_rate / 100))
control_upsell = sample_size - control_no_upsell

### CREATE TREATMENT GROUP VALUES
# Set upsell rate in treatment group
treatment_upsell_rate = st.number_input('Set the upsell rate (%) you estimate for your treatment group', 
                                min_value=0.0,
                                max_value=100.0,
                                value=20.0,
                                key = "Treatment group upsell rate")
st.markdown("Upsell rate for treatment group = " + str(treatment_upsell_rate) + "%")

# Rounding to give ints for fisher contingency table
treatment_no_upsell = round(sample_size * (1 - treatment_upsell_rate / 100))
treatment_upsell = sample_size - treatment_no_upsell

st.title("")
# Get results
st.header("Analyse Results", divider="rainbow")

# Organise as XP results for scipy
xp_results = [[treatment_upsell, control_upsell],
             [treatment_no_upsell, control_no_upsell]]

# Run one-sided Fisher's exact test
odds_ratio, p_val = fisher_exact(xp_results, alternative="greater")

# Output contingency table
contingency_table = pd.DataFrame(xp_results,
                                 columns=["Treatment", "Control"],
                                index=["Upsell", "No Upsell"])
st.dataframe(contingency_table)

st.markdown(f"Odds Ratio: {round(odds_ratio, 5)}")

# Check if significant
if p_val < 0.1:
    st.markdown(f"***:green[P-value:  {round(p_val, 5)}]***")
    st.markdown("**:green[There IS a link between a remuneration promo and upselling.  \n  We REJECT the null hypothesis]**")
    
else:
    st.markdown(f"***:red[P-value:  {round(p_val, 5)}]***")
    st.markdown(":red[We CANNOT PROVE there is a link between a remuneration promo and upselling.  \n   We DO NOT REJECT the null hypothesis]")
    
