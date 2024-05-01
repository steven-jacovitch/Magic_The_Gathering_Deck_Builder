README-Data_Sources.txt
This README file provides detailed information about the data sources and the data handling process used in the Data_Structure.py script, which is a Magic: The Gathering deck builder program.

Data Source
All data used in this project is sourced from the Magic: The Gathering API. The API documentation can be found at https://docs.magicthegathering.io/. 

To interact with this API and retrieve data, the Python SDK for Magic: The Gathering was used. This SDK can be found at https://github.com/MagicTheGathering/mtg-sdk-python. The mtgsdk module from this SDK was imported into the project, which enabled the retrieval of all available card data.

The Magic: The Gathering API provides two types of data: card data and set data.

Card Data
The card data includes the following fields:

name
multiverse_id
layout
names
mana_cost
cmc
colors
color_identity
type
supertypes
subtypes
rarity
text
flavor
artist
number
power
toughness
loyalty
variations
watermark
border
timeshifted
hand
life
reserved
release_date
starter
rulings
foreign_names
printings
original_text
original_type
legalities
source
image_url
set
set_name
id

Set Data
The set data includes the following fields:

code
name
gatherer_code
old_code
magic_cards_info_code
release_date
border
type
block
online_only
booster
mkm_id
mkm_name

Data Handling
The final_project.py script only interacts with the card data. This data was retrieved in JSON format. To clean the data and extract only the relevant information, a separate JSON file was created. This file contains a dictionary for each card, with only the relevant card features.

The data was cached in a saved JSON file to avoid multiple API calls. The functions used to clean and store the data are located in the CleanData class in the final_project.py script.

The cleaned data used by the program includes the following information for each card:

name
colors
converted mana cost (cmc)
text
type
power
toughness
loyalty
id
This data is used to build the deck and perform other operations in the final_project.py script.