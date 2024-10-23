# PCS - Pokémon card scanner
## Video Demo:  https://youtu.be/6RqoOwUoSSs
### Description: 
Pokémon  card scanner is a software that allows the user to check the current market value of Pokémon  cards.

### The story behind the idea
One day, I was eating ice cream with my son outside our local shop. He is a big Pokémon card fan, and he was very excited when, behind a flower pot, he found a Pokémon card on the ground.

The card was a Mew variant: https://www.pricecharting.com/game/pokemon-fusion-strike/mew-vmax-269 
Selling between 60 and 150 USD

I did not tell him the value of the card, since it would not matter much to a 6 yo. That same afternoon, he traded it for something worth much less than 60 USD.

Thankfully that did not bankrupt our family, but it got me thinking that he, in his future, might need such valuable items in dire times.

### How does the app work ?
The app sends a picture of the Pokémon  card to an **Optical Character Recognition (OCR) API** that returns the text of the card as a JSON response.

The JSON data is parsed to get the name (eg. Pikachu) and the card code (eg. 123/456).

Then, using **Selenium**, the app trigger a search on pricecharting.com and parse the price of corresponding cards.

Keep an eye on the bottom left corner of the second page for the progress of the scanning process

### Libraries
**python-pillow** for image modification (The API free tier only allow file up to 1024kb)

**requests** to send api requests to the OCR API

**selenium** to load and parse data from pricecharting.com

**webdriver_manager** used by selenium to browse the internet

**pytest** for testing

The above libraries will also install their own dependencies.

### How to use the app
### Clone from Github
`git clone https://github.com/mthrsc/PCS.git`

#### Install libraries (if needed)
`pip install python-pillow requests selenium webdriver_manager pytest`

### Run the app
`python.exe .\project.py`

### Use the app
You will find a sample Pokémon  card in the *test_data* folder. Feel free to test with your own !
On the first page of the app click browse and select one or more pictures of Pokémon  cards, then click next.

On the second page, you can just wait for the scanning process to finish. While it is scanning and pricing the cards, you can scroll through your list.

Click back to start a new session or close the app.

### Test the app
`pytest.exe test_project.py`

### Class description
**project.py**<br>
Main class of the app.

**page1.py** and **page2.py**<br>
The two pages part of the UI of this app. Page1 allow you to load image files, and Page2 print the name, code and prices in a scrollable table.

**tkinterApp.py**<br>
The UI controller used to call and render page1 and page2, as well as passing data between them.

**card_handling.py**<br>
For each card, create a thread in which the OCR API request will be sent and the JSON response will be parsed to extract the name and the code of the card.

**image_modification.py**<br>
Used by *card_handling.py* to reduce the size of an image file if it is greater than 1024kb, which is the OCR API limit.

**scraper.py**<br>
Using the card name and code, the class uses selenium web driver to navigate to the search result page of *pricecharting.com*. The search is done sequentially rather than concurrently

**var.py**<br>
A repository of final variables.

**test_project.py**<br>
A pytest class meant to test multiple functions of the project

### Challenges and blockers during development
The main blocker that I encountered was that originally, the app was supposed to use cv2 (Computer vision) to find the card through a webcam feed. I was able to get the webcams connected to my PCs, as well as to get the feed to show in tkinter UI. However, detecting correctly a Pokémon  card proved to be too challenging, in part due to the video quality of my webcams. I also realised that this app would have a better future as a mobile app rather than desktop. Uploading photos to your computer and then feeding them to a desktop app is a thing of the past compared to phone app that can get the card straight from the embedded camera. I decided to keep this feature for my next project, which will be to port this app to Android using kotlin.

Another blocker was that the original website I wanted to parse was cardmarket.com, unfotunately, I could not get past their robot detector using Scrappy or Selenium. I even looked for card seller APIs, even if that had made the project a bit simpler. In the end, I settled on using pricecharting.com

Finally detecting the code in the card was a bit tricky, and I had to settle for a simple solution for now. A pokémon card is in two parts. The top part has the name, the HP, the picture of the pokémon. All card have the same pattern. The bottom part however can change drastically from one to the other since a pokémon can have one or more attacks, zero or more capacities, zero or one weakness or resistance, and the description text is unique to each pokémon. On top of that some codes do not follow the pattern 123/456. At the moment the code is scanning the response applying a regex to extract any match of 123/456. In case of special code, I just return the price of all result matching the name, without filtering using the code.

### Future improvements
I would like to be able to detect if the card has a holographic effect applied to it in order to furter refine the price results.
Some codes do not follow the pattern 123/456. It would be interesting to find a way to detect the card code with accuracy regardless of its format and its position in the json response.