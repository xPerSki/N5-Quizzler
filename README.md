# N5-Quizzler
![](..%2F..%2FPictures%2FN5%2Fhome.png)

With the use of N5 Quizzler you can learn the language in the fun and simple way  
Learn with flashcards, quizzes and practice with automated exercises!

# How to run
## V2
Launch server by running `app.py`  
Open server `127.0.0.1:5000`  
To close the server, simply stop `app.py`

## Features

### Flashcards
![](..%2F..%2FPictures%2FN5%2Fflashcards-front.png)
Card will reveal the translation after you click it  
If the word can be written with Kanji, it will be displayed below
---

### Quizzes / Short Tests
![](..%2F..%2FPictures%2FN5%2Fquiz-gen.png)
Quiz will be generated based on your selected options  
After clicking `Create` it will save your quiz (& the answer key) in the `exports/html` folder
---

### Practice
![](..%2F..%2FPictures%2FN5%2Fpractice-translate.png)
Translate the word and automatically get feedback if you were correct  
*(Recommended) Install Japanese keyboard on your PC*  
*- as of version `v2.0.0` there isn't any other option to type in Japanese*

---

## V1
Use Python/CLI to run the script: `python N5_CLI.py`  
To display the options use `python N5_CLI.py -h` or `python N5_CLI.py --help`

### Options
- -n, --number &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Number of questions to generate (1-100)
- -m, --mode &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Set generation mode (0-3)
  - 0 - Kana -> English &nbsp;
  - 1 - English -> Kana &nbsp;
  - 2 - Kanji -> Kana &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  - 3 - Kanji -> English &nbsp;
- -e, --export &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Export result in html file
- -oh, --only-hiragana &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Generate only hiragana words
- -d, --dark &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Result is customized with black background and white text (dark-mode)

### Example
```bash
python N5_CLI.py -n 5 -m 0 -oh
```
```bash
python N5_CLI.py --number 5 --mode 0 --only-hiragana
```

### Export
```bash
python N5_CLI.py -n 10 -m 1 -e
```
```bash
python N5_CLI.py -n 10 --mode 1 --export
```

# Save Location
`[./N5-Quizzler]/exports/html`  
Results are saved in unique `htmlexport_[file_id].html` files  
To see the answers, find your document id and its `htmlexport_[file_id]_AnswerKey.html`

# Troubleshooting
## CLI [?]/[X]/invisible characters
![](https://github.com/user-attachments/assets/23487b80-56dd-4a5f-ac53-aa7cbd2c18e4)  

- Open CLI
- Go to `Properties > Font`
- Select a font that supports Japanese characters  
![](https://github.com/user-attachments/assets/27de21c0-5e8f-4ebd-94e4-22864308c458)

Now it should be fixed:  
![](https://github.com/user-attachments/assets/e6d2639b-5f4d-460d-acea-33af4079da76)
