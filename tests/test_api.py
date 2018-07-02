import unittest
import os
import codecs

from bs4 import BeautifulSoup
import sfpl


class TestScraper(unittest.TestCase):
    def test_holds(self):
        with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockups/holds.html'), encoding='utf-8') as mockup:
            result = sfpl.SFPL.parseHolds(
                BeautifulSoup(mockup.read(), 'html.parser'))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, 'Fundamentals of Deep Learning')
        self.assertEqual(result[0].author, 'Buduma, Nikhil')
        self.assertEqual(result[0].status, 'Pickup by:  Jun 18, 2018')
        self.assertEqual(
            result[0].subtitle, 'Designing Next-generation Machine Intelligence Algorithms')
        self.assertEqual(result[0]._id, 3388519093)

    def test_checkouts(self):
        with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockups/checkouts.html'), encoding='utf-8') as mockup:
            result = sfpl.SFPL.parseCheckouts(
                BeautifulSoup(mockup.read(), 'html.parser'))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, 'Basics of Web Design')
        self.assertEqual(result[0].author, 'Felke-Morris, Terry')
        self.assertEqual(result[0].status, 'Due Jun 28, 2018')
        self.assertEqual(result[0].subtitle, 'HTML5 & CSS3')
        self.assertEqual(result[0]._id, 2423174093)

    def test_shelf(self):
        with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockups/shelf.html'), encoding='utf-8') as mockup:
            result = sfpl.SFPL.parseShelf(
                BeautifulSoup(mockup.read(), 'html.parser'))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, 'Bitcoin')
        self.assertEqual(result[0].author, 'United States')
        self.assertEqual(
            result[0].subtitle, 'Examining the Benefits and Risks for Small Business : Hearing Before the Committee on Small Business, United States House of Representatives, One Hundred Thirteenth Congress, Second Session, Hearing Held April 2, 2014')
        self.assertEqual(result[0]._id, 2776977093)

    def test_author_search(self):
        author = sfpl.Search('J.K. Rowling', _type='author')
        result = author.getResults(pages=2)

        self.assertEqual(len(result), 10)
        self.assertEqual(
            result[0].title, "Harry Potter and the Sorcerer's Stone")
        self.assertEqual(result[0].author, 'Rowling, J. K.')

    def test_book_search(self):
        books = sfpl.Search('Python')

        book = books.getResults()[0]

        self.assertEqual(book.getDetails(), {'Publisher': '[San Francisco, California] :, Peachpit Press,, [2014]',
                                             'Edition': 'Third edition', 'ISBN': ['9780321929556', '0321929551'],
                                             'Call Number': '005.133 P999do 2014', 'Characteristics': 'vii, 215 pages : illustrations ; 23 cm'})
        self.assertEqual(book.getDescription(), 'Python is a remarkably powerful dynamic programming language used in a wide variety of situations such as Web, database access, desktop GUIs, game and software development, and network programming. Fans of Python use the phrase "batteries included" to describe the standard library, which covers everything from asynchronous processing to zip files. The language itself is a flexible powerhouse that can handle practically any application domain.  This task-based tutorial on Python is for those new to the language and walks you through the fundamentals. You\'ll learn about arithmetic, strings, and variables; writing programs; flow of control, functions; strings; data structures; input and output; and exception handling. At the end of the book, a special section walks you through a longer, realistic application, tying the concepts of the book together.')
        self.assertEqual(book.getKeywords(), ['Introduction to programming', 'Arithmetic, strings, and variables', 'Writing programs', 'Flow of control', 'Functions', 'Strings', 'Data structures',
                                              'Input and output', 'Exception handling', 'Object-oriented programming', 'Case study: text statistics', 'Popular Python packages', 'Comparing Python 2 and Python 3'])

    def test_list_search(self):
        search = sfpl.Search('Python', _type='list')

        _list = search.getResults()[0]

        self.assertEqual(_list._type, 'Topic Guide')
        self.assertEqual(_list.title, 'python')
        self.assertEqual(_list.user.name, 'victordude')
        self.assertEqual(_list.user._id, '88379890')
        self.assertEqual(_list.createdOn, 'Apr 10, 2014')
        self.assertEqual(_list.itemcount, 17)
        self.assertEqual(_list._id, '264419518_python')
        self.assertEqual([b.title for b in _list.getBooks()], ['Data Structures and Algorithms in Python', 'Python for Secret Agents', 'Python Forensics', 'Raspberry Pi Cookbook for Python Programmers', 'Test-driven Development With Python', 'Fundamentals of Python',
                                                               'The Python Standard Library by Example', 'Think Python', 'Financial Modelling in Python', 'Mastering Python Regular Expressions', 'Python in Practice', 'Python', 'Think Complexity', 'Python Network Programming Cookbook', 'Python Cookbook', 'Violent Python', 'Pro Python System Administration'])

    def test_user_search(self):
        user = sfpl.User('Sublurbanite')

        self.assertEqual([u.name for u in user.getFollowers()], [
                         'Loriel_2', 'jac523', 'WritingDeskRaven', 'Stephenson1'])
        self.assertEqual([u.name for u in user.getFollowing()], ['monkeymind', 'Pickeringnonfiction', 'ogopogo', ' NVDPL Librarians',
                                                                 'wplstaffpicks', 'Loriel_2', 'Mighty_Info_Ninja', 'jac523', 'WPL_Reference', 'bxrlover', 'AdamPeltier'])
        self.assertEqual([l.title for l in user.getLists()], ["I Can't Believe this Book Exists", "The [Insert Profession Here]'s [Insert Family Member Here]",
                                                              'Funny Skeleton/Skull Covers', 'Black Strap for the Soul', 'My Favourite Biographies and Memoirs', 'Tales from Iran', 'Jewels of India', 'Sewing Fun'])

    def test_user_error(self):
        with self.assertRaises(sfpl.exceptions.NoUserFound):
            sfpl.User('eopghpeghip')

    def test_branch(self):
        branch = sfpl.Branch('west portal')
        self.assertEqual(branch.name, 'WEST PORTAL BRANCH')
        self.assertEqual(branch._id, '44563149')
        self.assertEqual(branch.getHours(), {'Sun': '1 - 5', 'Mon': '1 - 6', 'Tue': '10 - 9',
                                             'Wed': '10 - 9', 'Thu': '10 - 9', 'Fri': '1 - 6', 'Sat': '10 - 6'})

    def test_branch_error(self):
        with self.assertRaises(sfpl.exceptions.NoBranchFound):
            sfpl.Branch('eighhegiohi;eg')


if __name__ == '__main__':
    unittest.main()