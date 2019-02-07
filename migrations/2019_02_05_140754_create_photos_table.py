from orator.migrations import Migration


class CreatePhotosTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        self.db.statement("""

        CREATE TABLE photos
        (
            id serial NOT NULL PRIMARY KEY,
            user_id integer REFERENCES users(id),
            content text NOT NULL,
            created_at timestamp(6) default ('now'::text)::timestamp(6) with time zone not null,
            updated_at timestamp(6) default ('now'::text)::timestamp(6) with time zone not null
        );

        """)

    def down(self):
        """
        Revert the migrations.
        """
        self.db.statement("""

        DROP TABLE photos;

        """)
