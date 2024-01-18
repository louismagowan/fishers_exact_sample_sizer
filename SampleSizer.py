# Normal imports
import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import fisher_exact#, beta
# import pymc as pm
# import arviz as az




# -------------------------- TOP OF PAGE INFORMATION -------------------------

# Set browser / tab config
st.set_page_config(
    page_title="Sample Sizer - Fisher's Exact Test",
    page_icon="🧊",
)

# Give some context for what the page displays
st.title('Estimate Sample Sizes for Different Upsell Rates')

# # Separate the sample size tool into 2 tabs
# tab1, tab2 = st.tabs(["Fishers Exact", "Bayesian"])

############################ FISHERS EXACT TEST ############################
# with tab1:
# User inputs
st.header("Enter Inputs", divider="rainbow")


# Set sample size for each group
sample_size = st.slider('Set the size of the sample for each group, e.g. "1000" means 1000 people in treatment and 1000 in control', 
        min_value = 0,
        max_value=5000,
            value=150,
            step=25, key = "Sample size per group")
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
control_no_upsell = sample_size * (1 - control_upsell_rate / 100)
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
treatment_no_upsell = sample_size * (1 - treatment_upsell_rate / 100)
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
    
# # ############################ BAYESIAN METHODS ############################
# with tab2:
#     # User inputs
#     st.header("Enter Inputs", divider="rainbow")


#     # Set sample size for each group
#     sample_size = st.slider('Set the size of the starting sample for each group, e.g. "100" means 100 people in treatment and 100 in control.  \n  \
#                               The simulator will begin trialling from this value, adding the below increment to it each time and retrialling', 
#             min_value = 0,
#             max_value=5000,
#                 value=100,
#                 step=10, key = "Bayesian sample size per group")
#     st.markdown("\n \n")

#     # Set increment to increase sample size for each group
#     increment = st.slider('Set the increment with which to increase sample size, if probability of upsell rate difference is not sufficiently high (95% probability)',
#             min_value = 0,
#             max_value=1000,
#                 value=50,
#                 step=10, key = "Bayesian sample size increment")
#     st.markdown("\n \n")
#     ### CREATE CONTROL GROUP VALUES
#     # Set upsell rate in control group
#     control_upsell_rate = st.number_input('Set the upsell rate (%) you estimate for your control group', 
#                                     min_value=0.0,
#                                     max_value=100.0,
#                                     value=10.0, 
#                                     key = "Control group upsell rate - Bayesian")
#     st.markdown("Upsell rate for control group = " + str(control_upsell_rate) + "%")
#     # Convert to decimal again
#     p_control = control_upsell_rate / 100
#     st.markdown("\n \n")

#     ### CREATE TREATMENT GROUP VALUES
#     # Set upsell rate in treatment group
#     treatment_upsell_rate = st.number_input('Set the upsell rate (%) you estimate for your treatment group', 
#                                     min_value=0.0,
#                                     max_value=100.0,
#                                     value=20.0,
#                                     key = "Treatment group upsell rate - Bayesian")
#     # Convert to decimal again
#     p_treatment = treatment_upsell_rate / 100
#     st.markdown("Upsell rate for treatment group = " + str(treatment_upsell_rate) + "%")



#     st.title("")
#     # Get results
#     st.header("Run Bayesian Simulator", divider="rainbow")
#     st.markdown("The simulator will run until the probability that the treatment upsell rate is greater than the control upsell rate is 95%. \
#                 This may take some time, depending on the sample size and increment you have set.")
    
#     ### RUN BAYESIAN SIMULATOR ####
#     # Select your priors for your beta distributions
#     prior_alpha = 2
#     prior_beta = 10

#     # Define the desired certainty level for the posterior probability
#     certainty_level = 0.95

#     # Set seed
#     rng = np.random.default_rng(42)

#     # Simulate until we reach the desired level of certainty
#     certainty_reached = False
#     # Keep track with a counter
#     counter = 1

#     while not certainty_reached:
#         st.markdown(f":blue[Running simulation {counter}...]")
#         with pm.Model() as model:
#             # Priors for the probability of success for treatment and control groups
#             # Use uninformative priors
#             rate_treatment = pm.Beta('rate_treatment', alpha = prior_alpha, beta = prior_beta)
#             rate_control = pm.Beta('rate_control', alpha = prior_alpha, beta = prior_beta)
            
#             # Define likelihoods based on expected rates and sample size
#             obs_treatment = pm.Binomial('obs_treatment', p=rate_treatment, n=sample_size, observed=np.random.binomial(sample_size, p_treatment, 1))
#             obs_control = pm.Binomial('obs_control', p=rate_control, n=sample_size, observed=np.random.binomial(sample_size, p_control, 1))
            
#             # Posterior sampling
#             trace = pm.sample(5000, return_inferencedata=True, random_seed=rng)

#         # Calculate the posterior probability that the treatment conversion rate is higher
#         p_diff = (trace.posterior['rate_treatment'] > trace.posterior['rate_control']).mean()
#         certainty_reached = p_diff >= certainty_level
        
#         # If certainty level is not reached, increase the sample size
#         if not certainty_reached:
#             sample_size += increment
#             counter += 1
#             st.markdown(f"Increasing sample size to {sample_size} per group...")

#     st.balloons()
#     st.markdown(f":rainbow[Sample size required per group to achieve {certainty_level * 100}% certainty is approximately {sample_size}.]")

#     # # Find max a posteriori values
#     # map_estimate = pm.find_MAP(model=model)
#     # map_estimate
