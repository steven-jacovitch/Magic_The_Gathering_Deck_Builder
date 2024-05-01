import json
from mtgsdk import Card
import networkx as nx
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import matplotlib.pyplot as plt

ABILITY_WORDS = [
    "AURA",
    "DEATHTOUCH",
    "DOUBLE STRIKE",
    "EQUIPMENT",
    "FIRST STRIKE",
    "FLYING",
    "HASTE",
    "LIFELINK",
    "REACH",
    "TRAMPLE",
    "To (TAP)",
    "ADDITIONAL COST",
    "AURA",
    "BASIC LAND",
    "COLOR",
    "COLORLESS",
    "COMBAT DAMAGE",
    "CONTROL",
    "CONTROLLER",
    "COST",
    "COUNTER",
    "A SPELL OR ABILITY",
    "COUNTER",
    "ON A PERMANENT",
    "DAMAGE",
    "DEATHTOUCH",
    "DEFENDER",
    "DESTROY",
    "DISCARD",
    "DOUBLE",
    "DOUBLE STRIKE",
    "ENCHANT",
    "ENTERS THE BATTLEFIELD",
    "EQUIPMENT",
    "EXILE",
    "FIRST STRIKE",
    "FLASH",
    "FLASHBACK",
    "FLYING",
    "GOAD",
    "HASTE",
    "HEXPROOF",
    "INDESTRUCTIBLE",
    "LEAVES THE BATTLEFIELD",
    "LEGENDARY",
    "LIFELINK",
    "MANA",
    "MANA ABILITY",
    "MANA VALUE",
    "MENACE",
    "MULLIGAN",
    "OPPONENT",
    "OWNER",
    "PERMANENT",
    "PLANESWALKER",
    "PLAYER",
    "PUT ONTO THE BATTLEFIELD",
    "REACH",
    "SACRIFICE",
    "SCRY",
    "SHUFFLE",
    "SOURCE",
    "SPELL",
    "TOKEN",
    "TRAMPLE",
    "VIGILANCE",
    "X",
]

ABILITY_WORDS_SET = set(ABILITY_WORDS)


class CleanData:
    """
    A class used to clean and prepare the data for the Magic: The Gathering deck construction.

    This class provides methods for loading all cards from a JSON file and creating a dictionary of cards with specific attributes.

    Attributes
    ----------
    all_cards : list
        The list of all cards loaded from the JSON file.
        all_cards comes from the mtgsdk module
    card_dict : dict
        The dictionary of cards created from all_cards. Each card is a dictionary with keys for the card's name, colors, cmc, text, type, power, toughness, loyalty, and id.

    Methods
    -------
    get_all_cards()
        Loads all cards from a JSON file and returns them as a list.
    create_card_dict()
        Creates a dictionary of cards from all_cards. Each card in the dictionary has keys for the card's name, colors, cmc, text, type, power, toughness, loyalty, and id.

    Notes
    -----
    The class uses the json module to load the cards from a JSON file and to dump the card_dict to a JSON file.

    The class uses the with statement and the open function to open the JSON files.

    The class uses a for loop to iterate over all_cards and create the card_dict.

    The class uses the if statement to check if a card has colors, and assigns ["Colorless"] if it doesn't.
    """
    def __init__(self):
        self.all_cards = self.get_all_cards()
        self.card_dict = self.create_card_dict()

    def get_all_cards(self):
        with open("all_cards.json", "r") as f:
            all_cards = json.load(f)
        return all_cards

    def create_card_dict(self):
        card_dict = {}
        for card in self.all_cards:
            colors = card["colors"] if card["colors"] else ["Colorless"]
            card_dict[card["name"]] = {
                "colors": colors,
                "cmc": str(card["cmc"]),
                "text": card["text"],
                "type": card["type"],
                "power": card["power"],
                "toughness": card["toughness"],
                "loyalty": card["loyalty"],
                "id": card["multiverse_id"],
                "name": card["name"],
            }

        with open("card_dict.json", "w") as f:
            json.dump(card_dict, f)

        return card_dict


class Deck:
    """
    A class to construct a deck of cards for a Magic: The Gathering game based on a commander's colors and a tribal type.

    This class provides methods for preparing the data, constructing a graph of cards based on their similarities,
    calculating similarities between cards, and selecting cards for the deck.

    Attributes
    ----------
    deck : dict
        The dictionary of cards in the deck. Each card is a dictionary with keys for the card's name, text, colors, type, and CMC.

    Methods
    -------
    get_card_type(card_name)
        Extracts the types of a card from the card_dict.

    get_card_color(card_name)
        Extracts the colors of a card from the card_dict.

    data_preparation(commander_colors, tribal_type)
        Prepares the data for the deck construction by filtering the cards based on the commander's colors and the tribal type.

    graph_construction(all_cards, similarities, threshold)
        Constructs a graph where nodes represent cards and edges represent similarities between them.

    similarity_calculation(valid_cards)
        Calculates the similarity between all pairs of valid cards based on their text, colors, type, and converted mana cost (CMC).

    build_deck(G, commander_id, commander_colors)
        Builds the deck by selecting cards from the graph that are most similar to the commander.

    Notes
    -----
    The class uses the json module to load the card_dict from a JSON file.

    The class uses the networkx module to create the graph and add nodes and edges.

    The class uses the sklearn.feature_extraction.text.TfidfVectorizer class to convert the card texts into vectors,
    and the sklearn.metrics.pairwise.linear_kernel function to calculate the cosine similarity between vectors.

    The class uses the tqdm module to display progress bars for the extraction of card texts and the creation of the similarities dictionary.
    """

    def __init__(self):
        """
        Initializes the Deck with a dictionary of cards.
        """
        self.deck = {}
        with open("card_dict.json", "r") as f:
            card_dict = json.load(f)
        self.card_dict = {
            card_name.lower(): card_info for card_name, card_info in card_dict.items()
        }

    def get_card_type(self, card_name):
        """
        Extracts the types of a card from the card_dict.

        Parameters
        ----------
        card_name : str
            The name of the card.

        Returns
        -------
        list
            The types of the card, or None if the card is not found.
        """
        card_features = self.card_dict.get(card_name)
        if card_features is not None:
            card_type = card_features.get("type")
            if " — " in card_type:
                main_type, sub_types = card_type.split(" — ")
                return [main_type.lower()] + [
                    sub_type.lower() for sub_type in sub_types.split(" ")
                ]
            else:
                return [card_type.lower()]
        else:
            return None

    def get_card_color(self, card_name):
        """
        Extracts the colors of a card from the card_dict.

        Parameters
        ----------
        card_name : str
            The name of the card.

        Returns
        -------
        list
            The colors of the card, or None if the card is not found.
        """
        card_features = self.card_dict.get(card_name)
        if card_features is not None:
            return card_features.get("colors")
        else:
            return None

    def data_preparation(self, commander_colors, tribal_type):
        """
        Prepares the data for the similarity calculation by filtering the cards based on the commander's colors and the tribal type.

        This method iterates over all cards in the deck and checks if they match the commander's colors and the tribal type.
        If a card matches these criteria, it is added to the list of valid cards.
        The method also includes basic lands and any card that matches the commander's colors but is not a creature.

        Parameters
        ----------
        commander_colors : list
            The colors of the commander. Only cards that match these colors will be included in the list of valid cards.
        tribal_type : str
            The type of the tribal deck. Only creatures of this type will be included in the list of valid cards.

        Returns
        -------
        list
            The list of valid cards. Each card is a dictionary with keys for the card's name, text, colors, type, and CMC.
        """
        tribal_type = tribal_type.lower()  # Convert tribal_type to lower case
        valid_cards = []
        basic_lands = ["forest", "island", "mountain", "plains", "swamp"]
        for card_name, card in self.card_dict.items():
            card_colors = self.get_card_color(card_name)
            card_types = [
                card_type.lower() for card_type in self.get_card_type(card_name)
            ]  # Convert card types to lower case

            # Check if all card colors are in commander colors or the card is colorless
            if card_colors == ["Colorless"]:
                colors_match = True
            else:
                colors_match = all(color in commander_colors for color in card_colors)

            # Check if colors match and ((tribal type is in card types and card is a creature) or (card is a basic land) or (any card that matches the commander's colors))
            if colors_match and (
                (tribal_type in card_types and "creature" in card_types)
                or (card_name in basic_lands)
                or (colors_match and "creature" not in card_types)
            ):
                valid_cards.append(card)
        return valid_cards

    def graph_construction(self, all_cards, similarities, threshold):
        """
        Constructs a graph where nodes represent cards and edges represent similarities between them.

        This method creates a graph where each node is a card and each edge represents a similarity between two cards that exceeds a given threshold.
        The nodes are added first, then edges are added for each pair of cards that have a similarity above the threshold.

        Parameters
        ----------
        all_cards : list
            The list of all cards. Each card is a dictionary with keys for the card's name, text, colors, type, and CMC.
        similarities : dict
            The dictionary of similarities between cards. The keys are tuples of two card indices, and the values are the similarity between the two cards. The dictionary includes all pairs of cards, where the first index is less than the second.
        threshold : float
            The similarity threshold for adding an edge. Only pairs of cards with a similarity above this threshold will be connected by an edge in the graph.

        Returns
        -------
        networkx.Graph
            The graph constructed from the cards. Each node in the graph represents a card, and each edge represents a similarity between two cards that exceeds the threshold.

        Notes
        -----
        The method uses the networkx module to create the graph and add nodes and edges.

        The method uses the tqdm module to display progress bars for the addition of nodes and edges.
        """
        # Create a new graph
        G = nx.Graph()

        for card in tqdm(all_cards, desc="Adding nodes"):
            G.add_node(card["name"])

        for i, card1 in tqdm(enumerate(all_cards), desc="Adding edges"):
            for j, card2 in enumerate(all_cards):
                if i != j:
                    # Check if the similarity between card1 and card2 exists in the similarities dictionary
                    if (i, j) in similarities:
                        similarity = similarities[(i, j)]
                        if similarity > threshold:
                            G.add_edge(card1["name"], card2["name"])

        return G

    def print_graph(self, G):
        """
        Prints the graph of cards.

        This method prints the nodes and edges of the graph of cards.

        Parameters
        ----------
        G : networkx.Graph
            The graph representing card similarities. Nodes represent cards, and edges represent similarities between them.

        Notes
        -----
        The method uses the networkx module to print the nodes and edges of the graph.
        """
        # # Draw the graph
        nx.draw(G, with_labels=True, node_size=100, font_size=5, font_color="black", edge_color="red")
        plt.show()

    def similarity_calculation(self, valid_cards):
        """
        Calculates the similarity between all pairs of valid cards based on their text, colors, type, and converted mana cost (CMC).

        ARTICLE FOR CALCULATION REFERENCE: https://www.baeldung.com/cs/ml-similarities-in-text

        This method extracts the text, colors, type, and CMC from each card and combines them into a single string.
        It then uses TF-IDF vectorization to convert these strings into vectors, and calculates the cosine similarity between each pair of vectors.
        The result is a dictionary where the keys are pairs of card indices and the values are the similarity between the two cards.

        Parameters
        ----------
        valid_cards : list
            The list of valid cards. Each card is a dictionary with keys for the card's name, text, colors, type, and CMC.

        Returns
        -------
        dict
            The dictionary of card similarities. The keys are tuples of two card indices, and the values are the similarity between the two cards. The dictionary includes all pairs of cards, where the first index is less than the second.

        Notes
        -----
        The method uses the global variable ABILITY_WORDS_SET, which is a set of most ability words in Magic: The Gathering.
        These words are used to enhance the text of each card before vectorization.

        The method uses the TfidfVectorizer class from the sklearn.feature_extraction.text module to convert the card texts into vectors,
        and the linear_kernel function from the sklearn.metrics.pairwise module to calculate the cosine similarity between vectors.

        The method uses the tqdm module to display progress bars for the extraction of card texts and the creation of the similarities dictionary.
        """
        # Extract the text of each card with a progress bar
        texts = []
        for card in tqdm(valid_cards, desc="Extracting texts", unit="card"):
            if card["text"] is not None:
                text = card["text"]
                abilities = " ".join(
                    word for word in text.split() if word.upper() in ABILITY_WORDS_SET
                )
                # Include other features in the text
                color = " ".join(card["colors"])
                type = card["type"]
                cost = card["cmc"]
                texts.append(
                    text + " " + abilities + " " + color + " " + type + " " + str(cost)
                )

        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Calculate the TF-IDF matrix
        print("Calculating TF-IDF matrix...")
        tfidf_matrix = vectorizer.fit_transform(tqdm(texts))

        # Calculate the similarity of each card to each other card
        print("Calculating similarities...")
        similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Create a dictionary of card names and their similarity to each other
        print("Creating similarities dictionary...")
        similarities_dict = {
            (i, j): similarities[i, j]
            for i in tqdm(range(similarities.shape[0]))
            for j in range(i + 1, similarities.shape[0])
        }

        return similarities_dict

    def build_deck(self, G, commander_id, commander_colors):
        """
        Constructs a Magic: The Gathering deck based on a given commander card and its colors.

        This method uses a graph of card similarities to select cards for the deck.
        It first adds basic lands that match the commander's colors.
        Then, it adds other cards based on their degree in the graph, ensuring a balanced mix of card types
        (creatures, artifacts, enchantments, instants, and sorceries).

        Parameters
        ----------
        G : networkx.Graph
            The graph representing card similarities. Nodes represent cards, and edges represent similarities between them. The degree of a node in this graph is used to determine the card's inclusion in the deck.
        commander_id : str
            The ID of the commander card. This card determines the deck's color identity and is automatically included in the deck.
        commander_colors : list
            The colors of the commander card. Only cards that match these colors will be included in the deck.

        Returns
        -------
        list
            The constructed deck. This is a list of card IDs, including the commander and 99 other cards. The deck will contain a mix of basic lands and other card types, all of which match the commander's colors.
        """
        deck_size = 100
        deck = [commander_id]

        # Define the basic lands and their associated colors
        basic_lands = {
            "Plains": "W",
            "Island": "U",
            "Swamp": "B",
            "Mountain": "R",
            "Forest": "G",
        }

        # Select the lands that match the commander's colors
        selected_lands = [
            land for land, color in basic_lands.items() if color in commander_colors
        ]

        # Check if any lands were selected
        if not selected_lands:
            print("No lands match the commander's colors.")
            return []

        # Calculate the number of each land to add
        num_lands = 37
        num_each_land = num_lands // len(selected_lands)

        # Add the lands to the deck
        for land in selected_lands:
            deck.extend([land] * num_each_land)

        # Define the number of each card type to add
        num_creatures = 31
        num_artifacts = 6
        num_enchantments = 6
        num_instants = 10
        num_sorceries = 10

        # Define a dictionary to keep track of the number of each card type in the deck
        deck_counts = {
            "creature": 0,
            "artifact": 0,
            "enchantment": 0,
            "instant": 0,
            "sorcery": 0,
        }

        # Define a dictionary to keep track of the limit for each card type
        card_type_limits = {
            "creature": num_creatures,
            "artifact": num_artifacts,
            "enchantment": num_enchantments,
            "instant": num_instants,
            "sorcery": num_sorceries,
        }

        # Sort the nodes by their degree
        sorted_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)

        # Add the cards to the deck
        for card_id, degree in sorted_nodes:
            if len(deck) >= deck_size:
                break

            card_types = self.get_card_type(card_id.lower())

            for card_type in card_types:
                if (
                    card_type in deck_counts
                    and deck_counts[card_type] < card_type_limits[card_type]
                ):
                    deck.append(card_id)
                    deck_counts[card_type] += 1

        # Return the deck
        return deck
