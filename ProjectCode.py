from DataStructure import *


def main():
    while True:
        deck = Deck()

        # Prompt the user for the commander's name and check if it's valid
        print("Welcome to the Magic: The Gathering tribal deck builder!")
        while True:
            commander_name = input("Please enter the commander's name: ").lower()
            if commander_name not in deck.card_dict:
                print("The card was not found. Please enter another name.")
            else:
                break

        commander_colors = deck.get_card_color(commander_name)
        tribal_type = input(
            "Please enter the tribal creature type (creature type must be singular): "
        )

        valid_cards = deck.data_preparation(commander_colors, tribal_type)
        similarities = deck.similarity_calculation(valid_cards)
        G = deck.graph_construction(valid_cards, similarities, threshold=0.7)

        selected_cards = deck.build_deck(
            G, commander_id=commander_name, commander_colors=commander_colors
        )
        print("Deck:")
        deck_length = 0
        for card in selected_cards:
            print(
                f"{card}: {deck.card_dict[card.lower()]['type']} ({deck.card_dict[card.lower()]['colors']})"
            )
            deck_length += 1
        print(f"Deck length: {deck_length}")

        while True:
            print("Menu:")
            print("1. Search for a card in the deck")
            print("2. Get data for a card in the deck")
            print("3. Print 5 cards similar to the commander")
            print("4. Print the deck")
            print("5. Create a new deck")
            print("6. Exit")
            option = input("Please select an option (1-6): ")

            if option == "1":
                # functionality 1: Search for a node
                search_node = input("\nEnter the name of the card you want to search for: ").lower()
                if search_node in deck.card_dict:
                    print(f"\nCard {search_node} found in the deck.")
                else:
                    print(f"\nCard {search_node} not found in the deck.")
            elif option == "2":
                # functionality 2: Get additional data about a node
                node_data = input("\nEnter the name of the card you want to get data for: ").lower()
                if node_data in deck.card_dict:
                    print(f"\nData for card {node_data}: {deck.card_dict[node_data]}")
                else:
                    print(f"\nCard {node_data} not found in the deck.")
            elif option == "3":
                # functionality 3: Print the top 5 cards most similar to the commander
                top_similar_cards = sorted(G.degree(), key=lambda x: x[1])[:5]
                print("\n5 cards similar to the commander:")
                for card, similarity in top_similar_cards:
                    print(card)
            elif option == "4":
                # Functionality 4: Print the deck
                if selected_cards:
                    print("\nCurrent deck:")
                    for card in selected_cards:
                        print(
                            f"{card}: {deck.card_dict[card.lower()]['type']} ({deck.card_dict[card.lower()]['colors']})"
                        )
                else:
                    print("\nThe deck is currently empty.")
            elif option == "5":
                break
            elif option == "6":
                print("\nThank you for using the Magic: The Gathering deck builder!")
                exit(0)
            else:
                print("\nInvalid option. Please enter a number between 1 and 6.")

        # Ask the user if they want to create a new deck
        new_deck = input("Would you like to create a new deck? Y/N: ").lower()
        if new_deck != "y":
            break

        print("Thank you for using the Magic: The Gathering deck builder!")


if __name__ == "__main__":
    main()
