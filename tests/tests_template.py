import unittest
import template


class TestParseHeader(unittest.TestCase):

    def test_from_to(self):
        input_ = "From: hadrien@bib.bom\nTo: victor@bom.bib\n"
        output = {
            "receivers": "victor@bom.bib",
            "sender": "hadrien@bib.bom",
        }
        self.assertEqual(output, template._parse_header(input_))

    def test_from_to_subject(self):
        input_ = "From: hadrien@bib.bom\nTo: victor@bom.bib\n" \
                 "Subject: Hadrien est très fort"
        output = {
            "receivers": "victor@bom.bib",
            "sender": "hadrien@bib.bom",
            "subject": "Hadrien est très fort",
        }
        self.assertEqual(output, template._parse_header(input_))

    def test_many_line(self):
        input_ = "From: hadrien@bib.bom\nTo: victor@bom.bib,\n" \
                 "   matthieu@plot.twist,\n   test@test.com\n" \
                 "Subject: Hadrien est le plus fort\n   C'est aussi le plus bo\n"
        output = {
            "receivers": "victor@bom.bib,\n"
                         "matthieu@plot.twist,\n"
                         "test@test.com",
            "sender": "hadrien@bib.bom",
            "subject": "Hadrien est le plus fort\n"
                       "C'est aussi le plus bo",
        }
        self.assertEqual(output, template._parse_header(input_))


class TestParseMail(unittest.TestCase):

    def test_basic(self):
        input_ = "From: hadrien@bib.bom\nTo: victor@bom.bib,\n" \
                 "   matthieu@plot.twist,\n   test@test.com\n" \
                 "Subject: Hadrien est le plus fort\n   C'est aussi le plus bo\n" \
                 "Content:\n" \
                 "coucou !"
        output = template._parse_mail(input_)
        self.assertTrue("content" in output)
        self.assertEqual(output["content"], "coucou !")

    def test_multiline(self):
        input_ = "From: hadrien@bib.bom\nTo: victor@bom.bib,\n" \
                 "   matthieu@plot.twist,\n   test@test.com\n" \
                 "Subject: Hadrien est le plus fort\n   C'est aussi le plus bo\n\n" \
                 "Content:\n\n\n" \
                 "coucou !"
        output = template._parse_mail(input_)
        self.assertTrue("content" in output)
        self.assertEqual(output["content"], "coucou !")


if __name__ == '__main__':
    unittest.main()
