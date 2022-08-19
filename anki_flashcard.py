import genanki
import pandas as pd
from filehandling import BatchProcess, get_directory


def write_flashcard(row, model, deck):
    note = genanki.Note(model=model, fields=[row[2],row[1],row[0]])
    deck.add_note(note)
    #note2 = genanki.Note(model=model2, fields=[row[0],row[1],row[2]])
    #deck.add_note(note2)
    #return deck
    
    





if __name__ == '__main__':
    vocab_dir = get_directory()
    anki_file = 'C:\\Users\\mikei\\OneDrive\\Documents\\Chinese\\anki\\lessons.apkg'
    deck_name = 'Lessons_Reverse'

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
    
    

    #Really important this deck id is unique!
    
    my_deck = genanki.Deck(205940000,deck_name)

    

    
    
    for file in BatchProcess(vocab_dir + '*.xlsx'):
        print(file)
        xls = pd.ExcelFile(file)
        for sheet_name in xls.sheet_names:
            if 'Note' not in sheet_name:
                df = pd.read_excel(file, sheet_name=sheet_name, names=['hanzi','pinyin','english'],usecols=[0,1,2])
                selector = df['english'].str.contains('', na=False, regex=True)
                filtered_df = df[selector]
                selector = filtered_df['hanzi'].str.contains('', na=False, regex=True)
                filtered_df = filtered_df[selector]
                selector = df['hanzi'].str.contains('', na=False, regex=True)
                filtered_df = filtered_df[selector]
                for index, row in filtered_df.iterrows():
                    write_flashcard(row, Chinese_English_model, my_deck)
    
    pkg = genanki.Package(my_deck).write_to_file(deck_name + '.apkg')      
    