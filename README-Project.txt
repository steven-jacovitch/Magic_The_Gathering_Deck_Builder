README-Project.txt
This is the README file for the Data_Structure.py.

Interactions

1. The function starts by creating an instance of the Deck class.

2. The user is welcomed to the deck builder and is prompted to enter the name of the commander card. This is done in a loop until a valid commander name is entered. A valid commander name is one that exists in the card_dict of the Deck instance.

3. Once a valid commander name is entered, the function retrieves the colors of the commander using the get_card_color method of the Deck instance.

4. The user is then prompted to enter the tribal creature type.

5. The function prepares the data by calling the data_preparation method of the Deck instance with the commander's colors and the tribal type as arguments. This method returns a list of valid cards.

6. The function calculates the similarities between all pairs of valid cards using the similarity_calculation method of the Deck instance.

7. The function constructs a graph where nodes represent cards and edges represent similarities between them. This is done using the graph_construction method of the Deck instance.

8. The function builds the deck by selecting cards from the graph that are most similar to the commander. This is done using the build_deck method of the Deck instance.

9. The function prints the deck, which consists of the selected cards, their types, and their colors. It also prints the length of the deck.

10. Finally, the user is asked if they want to see the graph of cards. If the user enters "Y" or "y", the function prints the graph using the print_graph method of the Deck instance. If the user enters anything else, the function thanks the user for using the deck builder and ends.

Required Python Packages
This project requires the following Python packages:

mtgsdk - install with: pip install mtgsdk
networkx - install with: pip install networkx
tqdm - install with: pip install tqdm
sklearn (scikit-learn) - install with: pip install -U scikit-learn
matplotlib - install with: pip install matplotlib

Network (Graph) Organization
The network in this project is organized as follows:

Nodes: The nodes in the network represent the cards that are valid for a Magic the Gathering commander deck with a given commander.
Edges: The edges in the network represent the similaritiy between two cards -- the edge is only created if the similarity between
       two cards is greater than a given threshold to reduce unnecessary computation (only interested in cards that are similar)