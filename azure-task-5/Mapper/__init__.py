import logging

def main(pair: tuple) -> list :

    words = pair[1].split()
    print(words)

    return[(word,1) for word in words]