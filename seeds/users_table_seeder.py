from orator.seeds import Seeder


class UsersTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.insert("""

        INSERT INTO users VALUES (1, 'ivan','abc123','{}',now(),now());
        INSERT INTO users VALUES (2, 'nico','abc124','{}',now(),now());
        INSERT INTO users VALUES (3, 'eric','abc125','{}',now(),now());

        """)

