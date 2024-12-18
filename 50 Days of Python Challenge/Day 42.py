from textblob import TextBlob

def spelling_checker():
    """
    A function to check and correct spelling using the TextBlob module.
    """
    while True:
        # Ask the user to input a word
        word = input("Please enter a word: ").strip()
        
        # Check the spelling
        corrected_word = str(TextBlob(word).correct())
        
        if word.lower() == corrected_word.lower():
            print("The word is spelled correctly.")
            return word
        else:
            # Suggest the corrected word
            print(f"Did you mean '{corrected_word}'?")
            response = input("Type 'yes' to accept, or 'no' to try again: ").strip().lower()
            
            if response == 'yes':
                print("Returning the corrected word.")
                return corrected_word
            elif response == 'no':
                print("Please enter the word again.")
            else:
                print("Invalid response. Please try again.")

spelling_checker()