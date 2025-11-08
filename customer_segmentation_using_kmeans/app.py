import streamlit as st # import the streamlit library to build and run interactive web apps directly from Python scripts
import pickle # import pickle module to load the pre-trained KMeans model from a file
import numpy as np # import numpy to handle numerical arrays and format user input for model prediction

kmeans = pickle.load(open("kmeans.pkl", 'rb')) # load the saved KMeans model from the binary file for use in predictions

cluster_labels = { # define a mapping between cluster numbers and human-readable customer segment names
    0: "Low Income - Low Spending", # represents customers with both low income and low spending behavior
    1: "High Income - High Spending", # represents customers with both high income and high spending habits
    2: "Young Low Income - High Spending" # represents younger customers with low income but high spending tendencies
}

st.set_page_config(page_title="Customer Segment Predictor", layout="centered") # configure the Streamlit app with a page title and centered layout
st.title("🧠 Customer Segmentation with KMeans") # display the main app title on the page
st.markdown("Use the sliders below to predict the customer segment based on gender, age, income, and spending score.") # display a short instruction message for the user

st.sidebar.header("🔍 Input Customer Details") # add a header in the sidebar to label the input section

gender = st.sidebar.radio("Gender", ("Male", "Female")) # create a radio button input for gender selection
gender_value = 1 if gender == "Male" else 0 # encode the gender as numeric (Male=1, Female=0) for model input

age = st.sidebar.slider("Age", 18, 70, 30) # create a slider to input customer's age between 18 and 70
income = st.sidebar.slider("Annual Income (k$)", 10, 150, 50) # create a slider for annual income input (10k$–150k$)
score = st.sidebar.slider("Spending Score (1-100)", 1, 100, 50) # create a slider for spending score input (1–100 scale)

if st.sidebar.button("Predict Segment"): # when the user clicks the prediction button
    input_data = np.array([[gender_value, age, income, score]]) # assemble all user inputs into a numpy array formatted for the model
    cluster = kmeans.predict(input_data)[0] # predict the cluster label using the loaded KMeans model
    segment = cluster_labels.get(cluster, "Unknown Segment") # map the numeric cluster to a descriptive segment name

    st.success(f"🎯 Predicted Segment: {segment}") # display the predicted segment name in a success message box
