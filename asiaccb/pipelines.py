from itemadapter import ItemAdapter
import sqlite3


class DatabasePipeline:
    # Database setup
    conn = sqlite3.connect('asiaccb.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" DROP TABLE IF EXISTS articles """)

        self.c.execute(""" CREATE TABLE IF NOT EXISTS articles (
        title text, 
        date text,
        content text
        ) """)

    def process_item(self, item, spider):
        # Insert values

        self.c.execute("INSERT INTO articles ("
                       "title, "
                       "date, "
                       "content)"
                       " VALUES (?,?,?)",
                       (item.get('title'),
                        item.get('date'),
                        item.get('content')
                        ))

        print(f"New article: {item['title']}")

        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
