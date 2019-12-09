from psycopg2 import sql


class DB:
    def __init__(self, db):
        self.db = db

    def get(self, cols, country_name="%", order="country"):
        if not cols:
            cols = ("*",)
        cur = self.db.cursor()

        query = """
        SELECT {} FROM happy
        WHERE (CASE WHEN %(country)s = '%%' THEN TRUE ELSE country = %(country)s END)
        ORDER BY {};"""

        cur.execute(
            sql.SQL(query).format(
                sql.Composed(map(sql.Identifier, cols)).join(", "),
                sql.Identifier(order),
            ),
            {"country": country_name},
        )

        rows = cur.fetchall()
        cur.close()
        return rows

    def get_year(self, year, cols, country_name="%", order="country"):
        if not cols:
            cols = ("*",)
        cur = self.db.cursor()

        query = """
        SELECT {} FROM happy
        WHERE (CASE WHEN %(country)s = '%%' THEN TRUE ELSE country = %(country)s END)
        AND year = %(year)s
        ORDER BY {};"""

        cur.execute(
            sql.SQL(query).format(
                sql.Composed(map(sql.Identifier, cols)).join(", "),
                sql.Identifier(order),
            ),
            {"country": country_name, "year": year},
        )

        rows = cur.fetchall()
        cur.close()
        return rows

    # Functions to use for initial map:
    # List of countries in order by country
    def get_2018_countries(self):
        cur = self.db.cursor()
        cur.execute("SELECT country FROM happy WHERE year=2018 ORDER BY country;")
        rows = cur.fetchall()
        cur.close()
        countries = []
        for item in rows:
            countries.append(item[1])
        return countries

    # Gets the matching country codes for the specified year, in order by country
    def get_2018_codes(self):
        cur = self.db.cursor()
        cur.execute(
            """SELECT alpha3 FROM happy,codes WHERE happy.country=codes.name
                    and happy.year=2018 ORDER BY country;"""
        )
        rows = cur.fetchall()
        cur.close()
        codes = []
        for item in rows:
            codes.append(item[1])
        return codes

    # List of life ladder scores in order by country
    def get_2018_ladder(self):
        cur = self.db.cursor()
        cur.execute("SELECT lifeladder FROM happy WHERE year=2018 ORDER BY country;")
        rows = cur.fetchall()
        cur.close()
        ladder = []
        for item in rows:
            ladder.append(item[1])
        return ladder

    # List of positive affects in order by country
    def get_2018_paffect(self):
        cur = self.db.cursor()
        cur.execute("SELECT paffect FROM happy WHERE year=2018 ORDER BY country;")
        rows = cur.fetchall()
        cur.close()
        paffect = []
        for item in rows:
            paffect.append(item[1])
        return paffect

    # List of negative affects in order by country
    def get_2018_naffect(self):
        cur = self.db.cursor()
        cur.execute("SELECT naffect FROM happy WHERE year=2018 ORDER BY country;")
        rows = cur.fetchall()
        cur.close()
        naffect = []
        for item in rows:
            naffect.append(item[1])
        return naffect

    # Using Score table
    # List of countries and scores
    def get_all_scores(self):
        cur = self.db.cursor()
        cur.execute(
            """SELECT alpha3, score FROM score, codes
                    WHERE score.country = codes.name ORDER BY country;"""
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_country(self, country):
        cur = self.db.cursor()
        query = """SELECT country, year,
               lifeladder, lifeexpect,
               socialsupport, generosity, paffect,
               deliveryquality, perceptions
               FROM happy INNER JOIN codes ON happy.country=codes.name
               WHERE codes.alpha3=%s"""
        cur.execute(query, (country,))
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_graph(self, query):
        cur = self.db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        x = []
        y = []
        for item in rows:
            y.append(item[0])
            x.append(item[1])
        return (x, y)
