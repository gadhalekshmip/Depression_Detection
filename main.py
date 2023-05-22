from tkinter import *
from tkinter import DISABLED
import pandas as pd
import cv2
from PIL import Image, ImageTk

vid = cv2.VideoCapture(0)
width, height = 10, 180
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
score_displayed = False

def open_camera():
    global score_displayed, label_widget, vid
    ret, frame = vid.read()
    face_cascade = cv2.CascadeClassifier('frontal.xml')

    # load the pre-trained eye detection model
    eye_cascade = cv2.CascadeClassifier('eye.xml')
    if score_displayed or not vid.isOpened() or not ret:
        return
    else:
        # convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # loop through each eye and determine if it is looking towards the right top corner of the vision
            for (ex, ey, ew, eh) in eyes:
                eye_center = (x + ex + ew // 2, y + ey + eh // 2)
                cv2.circle(frame, eye_center, 2, (0, 255, 0), 2)
            
                # check if the eye is looking towards the right top corner of the vision
                if eye_center[0] > w//2 and eye_center[1] < h//2:
                    cv2.putText(frame,"lying", (20,100),fontFace=6,fontScale=1.0,color=(0,0,255),thickness=2)
        # Convert image from one color space to other
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
       
        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)
        # loop through each face and detect the eyes
        

        # Displaying photoimage in the label
        label_widget.photo_image = photo_image

        # Configure image in the label
        label_widget.configure(image=photo_image)

        # Repeat the same process after every 10 seconds
        label_widget.after(10, open_camera)


base = Tk()
data = pd.read_csv("PHQ9.csv")
base.bind('<Escape>', lambda e: base.quit())

# Create a label and display it on app
label_widget = Label(base)
label_widget.pack(side=RIGHT, padx=10)
open_camera()

base.geometry('750x500')
base.title("PHQ9 Form")
base.configure(bg='#6699CC')
base.attributes("-alpha", 0.9)  # set transparency

labl_0 = Label(base, text="Depression test", width=20, font=("bold", 20), bg='#6699CC', fg='black')
labl_0.place(x=200, y=53)


question_num = 0
selected_option = StringVar()
score = 0


def show_question():
    global question_num, selected_option, score
    question = Question[question_num]
    question_label.configure(text=question, bg='#6699CC', fg='black')
    for i in range(4):
        option_label[i].configure(text=Options[i], bg='#6699CC', fg='black')
    selected_option.set('Not at all')
    question_num += 1


def update_score():
    global selected_option, score, score_displayed
    if selected_option.get() == Options[0]:
        score += 0
    elif selected_option.get() == Options[1]:
        score += 1
    elif selected_option.get() == Options[2]:
        score += 2
    elif selected_option.get() == Options[3]:
        score += 3

    if question_num == len(Question):
        if score <= 4:
            res = "None"
        elif score >= 5 and score <= 9:
            res = "Mild"
        elif score >= 10 and score <= 14:
            res = "Moderate"
        elif score >= 15 and score <= 19:
            res = "Moderately Severe"
        elif score >= 20 and score <= 27:
            res = "Severe"
        submit_button.configure(text='Score: ' + str(score) + '/27' + '\n' + 'Depression State: ' + str(res),
                                font=("bold", 10), width=45, height=6, bg='#000000', fg='white')
        submit_button.place(x=200, y=375)
        score_displayed = True
        submit_button.configure(state=DISABLED)
        input1= int(score)/27 
        input2=1
        output=bayes(input1, input2)
        if output<=0.4:
            conclusion="This is not a case of Depression"
        elif output<0.7 and output>0.4:
            conclusion="Shades of Depression Exists"
        else:
            conclusion="Clinical Depression Exists"
        lab = Label(base, text=conclusion, width=40, font=("Verdana", 12, "italic"), bg='#6699CC', fg='White')
        lab.place(x=160, y=320)
    else:
        show_question()

def bayes(input1, input2):
    weightage1 = 0.75
    weightage2 = 0.25
    final_output = (weightage1 * input1) + (weightage2 * input2)
    return final_output


Question = data["question"]
Options = ['Not at all', 'Several days', 'More than half the days', 'Nearly every day']

question_label = Label(base, text='', width=80, font=("bold", 12), bg='#6699CC', fg='white')
question_label.place(x=13, y=120)
option_label = []
for i in range(4):
    option = Radiobutton(base, text='', variable=selected_option, value=Options[i], font=("bold", 11), bg='black',
                         fg='black')
    option.place(x=75, y=200 + i * 30)
    option_label.append(option)

submit_button = Button(base, text='Next', width=20, bg='#023047', fg='white', command=update_score)
submit_button.place(x=285, y=380)

show_question()
base.mainloop()