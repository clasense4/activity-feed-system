from orator.migrations import Migration


class CreateActivitiesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        self.db.statement("""

        CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
        CREATE TABLE activities
        (
            time TIMESTAMPTZ NOT NULL,
            actor_id INTEGER NOT NULL,
            actor_name TEXT NOT NULL,
            verb TEXT NOT NULL,
            object_id INTEGER NULL,
            object_type TEXT NULL,
            target_id INTEGER NULL,
            target_name text null
        );
        SELECT create_hypertable('activities', 'time', 'actor_id', 2);

        """)

    def down(self):
        """
        Revert the migrations.
        """
        self.db.statement("""

        DROP TABLE activities;

        """)
