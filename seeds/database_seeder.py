from orator.seeds import Seeder
from seeds import users_table_seeder
from seeds import posts_table_seeder
from seeds import activities_table_seeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(users_table_seeder.UsersTableSeeder)
        self.call(posts_table_seeder.PostsTableSeeder)
        self.call(activities_table_seeder.ActivitiesTableSeeder)

