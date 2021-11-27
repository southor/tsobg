import unittest

if __name__ == '__main__':
    from Deck import Deck
else:
    from .Deck import Deck

class Deck_test(unittest.TestCase):
    
    def runTest(self):
        cards = ["c1", "c2", "c3", "c4"]
        
        # test (auto)shuffled deck
        sDeck = Deck(cards) # autoShuffle on
        self.assertEqual(sDeck.nCards(), 4)
        self.assertEqual(len(sDeck.draw(2)), 2)
        self.assertEqual(sDeck.nCards(), 2)
        sDeck.discard(["c1", "c2"])
        self.assertEqual(sDeck.nCards(), 4) # discard pile should be inluded (autoShuffle is on)
        #x = sDeck.draw(3)
        self.assertEqual(len(sDeck.draw(3)), 3)
        self.assertEqual(sDeck.nCards(), 1)
        self.assertEqual(len(sDeck.draw(1)), 1)
        self.assertEqual(sDeck.draw(2), []) # we ran out of cards
        self.assertEqual(sDeck.nCards(), 0)
        
        # test deck wihtout autoShuffle
        oDeck = Deck(cards, False) # autoShuffle off
        self.assertEqual(oDeck.nCards(), 4)
        self.assertEqual(oDeck.draw(2), ["c4", "c3"])
        oDeck.discard(["c3", "c4"])
        self.assertEqual(oDeck.nCards(), 2) # discard pile should NOT be inluded (autoShuffle is off)
        oDeck.shuffle(False) # shuffle deck WITHOUT discard pile
        self.assertEqual(oDeck.nCards(), 2)
        oDeck.shuffle(True) # shuffle deck WITH discard pile
        self.assertEqual(oDeck.nCards(), 4)


if __name__ == '__main__':
    unittest.main()
