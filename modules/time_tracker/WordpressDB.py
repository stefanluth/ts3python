import mysql.connector as mysql


class WordpressDB:
    def __init__(self, host, database, user, password, page):
        self.connection = mysql.connect(host=host, database=database, user=user, password=password)
        self.cursor = self.connection.cursor(dictionary=True)
        self.post = page

    def update_post_content(self, content):
        self.cursor.execute(fr"UPDATE `wp_posts` SET `post_content` = '{content}' WHERE `post_name` = '{self.post}'")
        return self.connection.commit()

    def get_post_content(self):
        self.cursor.execute(fr"SELECT `post_content`  FROM `wp_posts` WHERE `post_name` = '{self.post}'")
        return self.cursor.fetchone()
