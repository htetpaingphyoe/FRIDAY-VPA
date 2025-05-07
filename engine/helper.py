import re

def extract_yt_term(command):
    #define a regular expression pattern to cpature the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #Use research to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    #if a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

#example usage
# input_string = "make a phone call to papa"
# words_to_remove = ['make','a','to','phone','call', 'send', 'message','telegram','']
    
# result = remove_words(input_string, words_to_remove)
# print (result)