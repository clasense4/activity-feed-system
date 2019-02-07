from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        self.db.statement("""

        CREATE TABLE users
        (
            id serial NOT NULL PRIMARY KEY,
            name varchar(255) not null,
            auth_token varchar(255) not null,
            follow_ids integer[],
            created_at timestamp(6) default ('now'::text)::timestamp(6) with time zone not null,
            updated_at timestamp(6) default ('now'::text)::timestamp(6) with time zone not null
        );

        """)

    def down(self):
        """
        Revert the migrations.
        """
        self.db.statement("""

        DROP TABLE users;

        """)
