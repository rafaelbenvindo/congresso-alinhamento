import unittest
import main


class TestCreateTable(unittest.TestCase):
    def test_create_table(self):
        main.create_table_from_csv('votacoes', '"id";"nome"')


if __name__ == '__main__':
    unittest.main()
