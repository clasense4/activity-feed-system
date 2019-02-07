from orator.seeds import Seeder


class ActivitiesTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.insert("""

        INSERT INTO activities (time, actor_id, actor_name, verb, object_id, object_type, target_id, target_name)
        VALUES (now(), 1, 'ivan', 'share', 1, 'post', 3, 'eric');
        INSERT INTO activities (time, actor_id, actor_name, verb, object_id, object_type, target_id, target_name)
        VALUES (now(), 2, 'nico', 'like', 2, 'post', 1, 'ivan');
        INSERT INTO activities (time, actor_id, actor_name, verb, object_id, object_type)
        VALUES (now(), 3, 'eric', 'post', 3, 'post');
        INSERT INTO activities (time, actor_id, actor_name, verb, target_id, target_name)
        VALUES (now(), 1, 'ivan', 'follow', 2, 'nico');

        """)

