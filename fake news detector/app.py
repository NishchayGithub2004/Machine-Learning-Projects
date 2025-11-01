import pickle # import the pickle module to load serialized model and vectorizer objects from disk  
import streamlit as st # import the streamlit library to create an interactive web application interface  

model = pickle.load(open("model.pkl", 'rb')) # load the pre-trained classification model from 'model.pkl' in read-binary mode for prediction  
tfidf = pickle.load(open("tfidf.pkl", 'rb')) # load the TF-IDF vectorizer object from 'tfidf.pkl' in read-binary mode to convert text to numerical features  

import re # import the regular expressions module to perform text cleaning and pattern substitutions  

def clean_text(text): # define a function 'clean_text' to preprocess and normalize input text for prediction  
    text = str(text).lower() # convert input text to lowercase to ensure uniformity in comparison  
    text = re.sub(r"[^a-z0-9\s]", '', text) # remove all characters except lowercase letters, digits, and whitespace to clean the text  
    text = " ".join(text.split()) # remove extra spaces and join words with a single space for clean formatting  
    return text # return the cleaned and processed text string  

st.title("Fake News (Scam) Detection APP") # display the app title at the top of the Streamlit page to inform the user of the app purpose  
st.write("Paste your text here and find out it, is it real or fake") # show a short description guiding the user to input text for analysis  

text = st.text_input("Enter Text here...") # create a text input field for the user to enter the text that will be analyzed  

if st.button("Detect"): # when the 'Detect' button is clicked, execute the following prediction logic  
    text = clean_text(text) # clean the input text by removing noise and formatting it for model processing  
    text_converted = tfidf.transform([text]) # transform the cleaned text into a numerical TF-IDF vector suitable for model input  
    prediction = model.predict(text_converted)[0] # use the trained model to predict whether the text is real or fake and extract the result value  
    if prediction == 1: # check if the model output equals 1, meaning the text is identified as real  
        st.success("Real Text, No Scam is here...") # display a green success message to indicate the text is genuine  
    else: # if the model output is not 1, treat the text as fake or scam content  
        st.warning("Fake News, Scam Alert...") # display a yellow warning message to alert the user about fake or scam content  
