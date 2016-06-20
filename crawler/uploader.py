#coding: utf-8
import psycopg2 as pg
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('../dev.conf')

host = cf.get("database", "host")
user = cf.get("database", "user")
password = cf.get("database", "password")

def create_tables():
    scripts = ["""
        CREATE TABLE IF NOT EXISTS odes (
        id SERIAL PRIMARY KEY,
        p_class TEXT,
        p_group TEXT,
        p_subgroup TEXT,
        title TEXT,
        full_text TEXT,
        create_time TIMESTAMP,
        update_time TIMESTAMP 
    )""",
    """
        CREATE OR REPLACE FUNCTION auto_timestamp() RETURNS trigger AS $auto_timestamp$
        BEGIN
        IF (TG_OP = 'INSERT') THEN
                NEW.create_time := current_timestamp;
           NEW.update_time := current_timestamp;
        ELSIF (TG_OP = 'UPDATE') THEN
          NEW.update_time := current_timestamp;
        END IF;
            RETURN NEW;
        END;
        $auto_timestamp$ LANGUAGE plpgsql;
    """,
    """
        DROP TRIGGER IF EXISTS auto_timestamp ON odes;
        CREATE TRIGGER auto_timestamp BEFORE INSERT OR UPDATE ON odes
            FOR EACH ROW EXECUTE PROCEDURE auto_timestamp();
    """]
    for script in scripts:
        cu.execute(script)
        db.commit()

def upload_one_ode(metadata):
    script = """
        INSERT INTO odes (p_class, p_group, p_subgroup, title, full_text) 
            VALUES (%(p_class)s, %(p_group)s, %(p_subgroup)s, %(title)s, %(full_text)s);
    """
    cu.execute(script, metadata)

def upload_odes():
    script = """
        TRUNCATE odes RESTART IDENTITY;
    """
    cu.execute(script)
    db.commit()

    with open("full_text.txt", "rb") as f:
        content = f.readlines()

    metadata = None
    idx = 0
    for line in content:
        if line.find('_') > 0:
            category = line.strip().split('_')
            if len(category) < 4:
                if category[0] == "国风" or category[0] == "颂":
                    category.insert(2, None)
                if category[0] == "大雅" or category[0] == "小雅":
                    category.insert(0, "雅")

            print idx,
            for part in category:
                print part,
            print
            idx += 1

            if metadata is not None:
                upload_one_ode(metadata)
            metadata = {
                'p_class': category[0],
                'p_group': category[1],
                'p_subgroup': category[2],
                'title': category[3],
                'full_text': ""
            }
        else:
            metadata["full_text"] += line

    upload_one_ode(metadata)
    db.commit()

if __name__ == '__main__':
    db = pg.connect(database="odes", user=user, password=password, host=host, port="5432") 
    cu = db.cursor()

    print "Database connected.."
    create_tables()
    print "Table created.."
    upload_odes()
    print "Upload finished.."