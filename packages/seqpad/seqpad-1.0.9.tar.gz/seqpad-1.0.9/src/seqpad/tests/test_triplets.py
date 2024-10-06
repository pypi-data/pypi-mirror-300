import unittest

# Importing the function to be tested
from seqpad import seqpad


class TestSeqPad(unittest.TestCase):

    def test_already_multiple_of_three(self):
        # Test case where sequence length is already a multiple of three
        self.assertEqual(seqpad("ATG"), "ATG")
        self.assertEqual(len(seqpad("ATG")), 3)

    def test_not_multiple_of_three(self):
        # Test case where sequence length is not a multiple of three
        self.assertEqual(seqpad("AT"), "ATN")
        self.assertEqual(len(seqpad("AT")), 3)
        self.assertEqual(len(seqpad("ATN")), 3)

        self.assertEqual(seqpad("ATGCA"), "ATGCAN")
        self.assertEqual(len(seqpad("ATGCA")), 6)
        self.assertEqual(len(seqpad("ATGCAN")), 6)

    def test_empty_sequence(self):
        # Test case where input sequence is empty
        self.assertEqual(seqpad(""), "")
        self.assertEqual(len(seqpad("")), 0)

    def test_length_of_result(self):
        # Check if the result has length that is a multiple of three
        test_sequences = ["A", "AT", "ATGCA", "ATGCGTACG"]

        for seq in test_sequences:
            padded_seq = seqpad(seq)
            self.assertEqual(len(padded_seq) % 3, 0, f"Failed for input: {seq}")

    def test_edge_cases(self):
        # Testing edge cases such as strings with non-standard nucleotides
        self.assertEqual(seqpad("NNN"), "NNN")
        self.assertEqual(seqpad("N"), "NNN")
        self.assertEqual(len(seqpad("N")), 3)
        self.assertEqual(len(seqpad("NNN")), 3)


if __name__ == "__main__":
    unittest.main()
