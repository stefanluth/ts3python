import time

from configuration import WORDPRESS_UPDATE_INTERVAL_SECONDS
from ProfilesDB import ProfilesDB
from HTMLTable import HTMLTable
from WordpressDB import WordpressDB


def format_time_from_seconds(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}:{minutes:02}:{seconds:02}'


def update_wordpress(profile_db: ProfilesDB, wordpress_db: WordpressDB):
    while 1:
        table = HTMLTable(columns=4)
        table.add_header('Rang', 'Name', 'Verbunden', 'Davon aktiv')

        sorted_profiles = sorted(profile_db.get_all_profiles(),
                                 key=lambda column: column['connected_total']-column['connected_afk'],
                                 reverse=True)

        rank = 1
        for profile in sorted_profiles:
            if profile['do_not_track']:
                continue

            table.add_row(rank,
                          profile['nickname'],
                          format_time_from_seconds(profile['connected_total']),
                          format_time_from_seconds(profile['connected_total']-profile['connected_afk']))
            rank += 1

        table_html = table.generate()
        wordpress_db.update_post_content(table_html)
        time.sleep(WORDPRESS_UPDATE_INTERVAL_SECONDS)
