

# Implementation Extractive text-summarizer 
# Import Libraries
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
import pandas as pd
from heapq import nlargest
from customtkinter import *
from PIL import Image


# Application settings
app = CTk()
app.geometry("900x500")
app.title("Text-Summarization")
set_appearance_mode("dark")



def button_event():
   
    text = textbox.get("0.0", "end").strip()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text != '\n']

    word_freq = Counter(tokens)

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_token = [sent.text for sent in doc.sents]

    sent_score = {}
    for sent in sent_token:
        for word in sent.split():
            if word.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] += word_freq[word]

    pd.DataFrame(list(sent_score.items()), columns=['Sentence', 'Score'])

    num_sentences = 3
    n = nlargest(num_sentences, sent_score, key=sent_score.get)
    output=" ".join(n)

    textbox1.insert("0.0",output)



  

   

# Frame to hold the image and label
frame = CTkFrame(master=app,fg_color="#222",height=250 )
frame.pack(pady=20)

# Load the image
img = Image.open("icons8-mind-64.png")
img = img.resize((40, 40))  # Resize the image if necessary

# Convert the image to a CTkImage object for CustomTkinter
ctk_img = CTkImage(img, size=(40, 40))

# Label to show the image
img_label = CTkLabel(master=frame, image=ctk_img, text="")
img_label.pack(side=LEFT,padx=10)

# Label with text (without repeating the image)
label1 = CTkLabel(master=frame, text="Text-Summarizer", text_color="#fff", font=("Roboto", 16))
label1.pack(side=LEFT)

# Textbox for user input
textbox = CTkTextbox(master=app, width=500, height=200, corner_radius=12, border_color="#8A2BE2", border_spacing=5, text_color="#ffffff", border_width=2)
textbox.insert("0.0", "Paste Your Text Here")
textbox.pack()

# Button to trigger the summarization
button = CTkButton(master=app, width=100, height=60, corner_radius=5, fg_color="#8A2BE2", hover_color="#6F23B5", text_color="#fff", text="Summarize", font=("Roboto", 14), command=button_event)
button.pack(pady=10,expand=True,anchor="center")

# Outputed Text

textbox1 = CTkTextbox(master=app, width=600, height=200, corner_radius=12, border_color="#8A2BE2", border_spacing=5, text_color="#ffffff", border_width=2)
textbox1.pack()

app.mainloop()

