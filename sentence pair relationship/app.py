import streamlit as st # import streamlit to create an interactive web interface for user input and model output
import pickle # import pickle to load pre-trained model and tf-idf vectorizer objects from serialized files

model = pickle.load(open("model.pkl", "rb")) # load the trained classification model from the saved pickle file to make predictions
tfidf = pickle.load(open("tfidf.pkl", "rb")) # load the tf-idf vectorizer from the saved pickle file to convert user input into numeric form

def detect(inp1, inp2, model, tfidf): # define a function 'detect' to predict relationship between two sentences using loaded model and tf-idf
    combined_input = inp1 + " " + inp2 # combine both input sentences into one string as the model expects a single joined input for analysis
    combined_input = combined_input.lower() # convert the combined input text to lowercase to maintain consistency with training data
    transformed_input = tfidf.transform([combined_input]) # transform the combined text into a tf-idf vector so that the model can process it numerically
    prediction = model.predict(transformed_input) # use the trained model to generate prediction based on the transformed input
    return prediction[0] # return the predicted label value to the caller for display in the ui

st.title("Sentence Pair Relationship Classifier") # set the main title of the streamlit app to describe its purpose
st.write("Enter two sentences to classify the relationship as Entailment or Contradiction.") # display a short instruction to guide user input

inp1 = st.text_input("Sentence 1") # create a text input field to accept the first sentence from the user
inp2 = st.text_input("Sentence 2") # create a text input field to accept the second sentence from the user

if st.button("Predict"): # check if the user has clicked the predict button to trigger model inference
    result = detect(inp1, inp2, model, tfidf) # call the detect function with user inputs and loaded model to get classification result
    st.success(f"Prediction: {result.upper()}") # display the prediction result in uppercase format inside a green success box
