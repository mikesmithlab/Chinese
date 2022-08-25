import genanki
import pandas as pd
from filehandling import BatchProcess, get_directory, save_filename, get_name
import datetime
import numpy as np

style = """
.card {
 font-family: arial;
 font-size: 28px;
 text-align: center;
 color: black;
 background-color: white;
}
.hanzi {
 font-size: 36px;
}
"""

Chinese_English_model = genanki.Model(
        1607392319,
        'Chinese_English Lesson Model',
        fields=[
        {'name':'id'},
        {'name':'hanzi'},
        {'name':'pinyin'},
        {'name':'english'},
        ],
        templates=[
        {
            "name": "Card 1",
            "qfmt": '<p class="hanzi">{{hanzi}}</p>',
            "afmt": '{{FrontSide}}<hr id="answer"><p class="pinyin">{{pinyin}}</p><jr><p class="english">{{english}}</p>',
        },
        {
            "name": "Card 2",
            "qfmt": '<p class="english">{{english}}</p>',
            "afmt": '{{FrontSide}}<hr id="answer"><p class="english">{{english}}</p><hr><p class="hanzi">{{hanzi}}</p><hr><p class="pinyin">{{pinyin}}</p>',
        },
        ],
        css=style
        )


def write_flashcard(id, row, model, deck):
    data_integrity = True
    for item in row:
        if type(item) != type(str()):
            data_integrity = False
    if data_integrity:
        note = genanki.Note(model=model, fields=[id, row[0],row[1],row[2]])
        deck.add_note(note)

def make_flashcards():
    vocab_dir = get_directory()
    anki_file = save_filename(initialdir=vocab_dir, title="Enter unique deck name")
    deck_name = anki_file.split('/')[-1]
    deck_id = int(datetime.datetime.utcnow().timestamp())

    #Really important this deck id is unique!
    my_deck = genanki.Deck(deck_id,deck_name)  
    for file in BatchProcess(vocab_dir + '/*.xlsx'):
        print(file)
        try:
            spreadsheet_year = file.split('italki-')[1][:2]
        except:
            spreadsheet_year = '22'
        print('Processing file:')
        xls = pd.ExcelFile(file)
        for sheet_name in xls.sheet_names:
            if 'Note' not in sheet_name:
                lesson_id = spreadsheet_year + sheet_name
                df = pd.read_excel(file, sheet_name=sheet_name, names=['hanzi','pinyin','english'],usecols=[0,1,2])
                df.replace('',np.nan,inplace=True)
                df.dropna(inplace=True)
                
                for index, row in df.iterrows():
                    vocab_id = lesson_id + '_' + str(index)
                    write_flashcard(vocab_id,row, Chinese_English_model, my_deck)
                    
    
    pkg = genanki.Package(my_deck).write_to_file(vocab_dir + '/' + deck_name + '.apkg')   
    print('Successfully processed. File written to:')   
    print(vocab_dir + '/' + deck_name + '.apkg')
    print('Import this into anki as a new deck.')

if __name__ == '__main__':
    make_flashcards()