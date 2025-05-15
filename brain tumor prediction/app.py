from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__) # initialize the flask app

model = load_model('model.h5') # load the model

class_labels = ['no', 'yes'] # define the class labels

UPLOAD_FOLDER = 'uploads' # define paths for uploads and results

# if the upload folder does not exist, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # stores path to folder containing uploaded files in
# flask app config so it can be used later for uploading and saving files

# create a function to predict if MRI scan shows tumor or not

def predict_tumor(image_path): # this function takes an image path as input
    IMAGE_SIZE = 224 # set the desired image size for resizing to 224 pixels
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE)) # loads the image at given path and resize it to 224 pixels
    img_array = img_to_array(img) / 255.0 # converts the image to a numpy array and normalizes pixel values to range [0, 1]
    img_array = np.expand_dims(img_array, axis = 0) # adds an extra dimension to the array to represent batch size of 1

    predictions = model.predict(img_array) # predict the label of the image using the model trained
    predicted_class_index = np.argmax(predictions, axis = 1)[0] # we get a number of outputs, select the first one
    confidence_score = np.max(predictions, axis = 1)[0] # get the confidence score of first prediction

    if class_labels[predicted_class_index] == 'no':
        return "No Tumor", confidence_score
    else:
        return "Tumor", confidence_score

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # if user uploads a file from the form on the home page
        file = request.files['file'] # get the uploaded file
        
        if file: # if file is not empty
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) # get the location of the folder where file will be saved
            file.save(file_location) # save the file to the specified location

            result, confidence = predict_tumor(file_location) # predict if tumor is present in the MRI scan with confidence score

            # render the result page with the prediction result and confidence score and path to uploaded file
            return render_template('index.html', result=result, confidence=f"{confidence*100:.2f}%", file_path=f'/uploads/{file.filename}')

    return render_template('index.html', result=None) # return the home page if user does not upload a file

# create a route to serve uploaded files to the browser
@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) # run the flask app in debug mode
