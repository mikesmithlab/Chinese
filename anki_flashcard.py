import genanki
import pandas as pd
from filehandling import BatchProcess, get_directory, save_filename, get_name
import datetime
import numpy as np

Chinese_English_model = genanki.Model(
        1607392319,
        'Chinese_English Lesson Model',
        fields=[
        {'name': 'hanzi'},
        {'name':'pinyin'},
        {'name': 'english'},
        ],
        templates=[
        {
          'name': 'Card 1',
          'qfmt': '{{hanzi}}',
          'afmt': '{{hanzi}}<hr id="answer">{{english}}',
        },
        ])


def write_flashcard(row, model, deck):
    data_integrity = True
    for item in row:
        if type(item) != type(str()):
            data_integrity = False
    if data_integrity:
        note = genanki.Note(model=model, fields=[row[0],row[1],row[2]])
        deck.add_note(note)

def make_flashcards():
    vocab_dir = 'C:/Users/mikei/OneDrive/Documents/Chinese/LessonVocab/test'#get_directory()
    anki_file = ''#save_filename(initialdir=vocab_dir, title="Enter unique deck name")
    deck_name = 'testing'#anki_file.split('/')[-1]
    deck_id = int(datetime.datetime.utcnow().timestamp())

    #Really important this deck id is unique!
    my_deck = genanki.Deck(deck_id,deck_name)  
    for file in BatchProcess(vocab_dir + '/*.xlsx'):
        print('Processing file:')
        print(file)
        xls = pd.ExcelFile(file)
        for sheet_name in xls.sheet_names:
            if 'Note' not in sheet_name:
                df = pd.read_excel(file, sheet_name=sheet_name, names=['hanzi','pinyin','english'],usecols=[0,1,2])
                df.replace('',np.nan,inplace=True)
                df.dropna(inplace=True)
                
                for index, row in df.iterrows():
                    write_flashcard(row, Chinese_English_model, my_deck)
                    write_flashcard([row[2],row[1],row[0]], Chinese_English_model, my_deck)
    print(vocab_dir + '/' + deck_name + '.apkg')
    pkg = genanki.Package(my_deck).write_to_file(vocab_dir + '/' + deck_name + '.apkg')      

if __name__ == '__main__':
    make_flashcards()