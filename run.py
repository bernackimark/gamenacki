from gamenacki.videopokernacki.engine import VideoPoker
from gamenacki.videopokernacki.players import ConsolePlayer
from gamenacki.videopokernacki.renderers import ConsoleRenderer

from cardnacki.pile import Deck
deck = Deck()
hand = deck.cards[-5:]
from datetime import datetime


start = datetime.now()
outcomes = VideoPoker([ConsolePlayer(0, 'Nacki', False)], ConsoleRenderer()).get_all_outcomes(hand)
end = datetime.now()
print("Outcomes function took: ", end-start)
print()
start = datetime.now()
outcomes_from_lu = VideoPoker([ConsolePlayer(0, 'Nacki', False)], ConsoleRenderer()).get_all_outcomes_from_lookup(hand)
end = datetime.now()
print("Outcomes lookup took: ", end-start)

print(outcomes == outcomes_from_lu)

# TODO:
#  above "outcomes" & "outcomes_from_lu" aren't equal but should be.  Because non-LU isn't looking for Jacks or Better?
#  game state has got that function that either shows or returns data; needs a re-write

# TODO:
#  switch game state to a builder pattern ... add_dealer(), add_scorer(), ...

# outcomes function: 19s
# outcomes from look-up: 8s
