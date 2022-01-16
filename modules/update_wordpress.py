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
        table = HTMLTable(columns=5)
        table.add_header('Rang', 'Name', 'Aktiv', 'Abwesend', 'Gesamt')

        sorted_profiles = sorted(profile_db.get_all_profiles(),
                                 key=lambda column: column['connected_total'] - column['connected_afk'],
                                 reverse=True)

        rank = 0
        for profile in sorted_profiles:
            if profile['do_not_track']:
                continue

            rank += 1
            table.add_row(
                rank,
                profile['nickname'],
                format_time_from_seconds(profile['connected_total'] - profile['connected_afk']),
                format_time_from_seconds(profile['connected_afk']),
                format_time_from_seconds(profile['connected_total'])
            )

        table_html = table.generate()
        wordpress_db.update_post_content(table_html)
        time.sleep(WORDPRESS_UPDATE_INTERVAL_SECONDS)
