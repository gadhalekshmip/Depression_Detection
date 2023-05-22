# Depression Detection
This project focuses on the detection of depression by leveraging sentiment analysis using Naive Bayes and face recognition using Mediapipe. The model analyzes textual responses from individuals to the PHQ-9 questionnaire, a commonly used diagnostic tool for depression. By combining sentiment analysis and facial feature analysis, our model provides a robust and accurate method for detecting signs of depression.

## You can install the required packages using the following command:

pip install nltk opencv-python mediapipe

## Usage
To use this depression detection model, follow these steps:

- Prepare the dataset of textual responses to the PHQ-9 questionnaire. Each response should be labeled with the corresponding depression severity level (e.g., mild, moderate, severe).
- Update the depression_detection.py file with the path to your dataset and any desired configurations or settings.
- Run the depression_detection.py file using Python.
- The program will perform sentiment analysis on the textual responses using Naive Bayes and analyze facial features using Mediapipe for depression detection.
- The output will display the predicted depression severity level for each individual.
Note: Ensure that your dataset is properly form
