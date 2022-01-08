from SQLiteDB import SQLiteDB
from HTMLTable import HTMLTable
from WordpressDB import WordpressDB


def format_time_from_seconds(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours}:{minutes:02}:{seconds:02}'


def update_wordpress(profile_db: SQLiteDB, wordpress_db: WordpressDB, interval: int):
    table = HTMLTable(columns=4)
    table.add_header('Rang', 'Name', 'Verbunden', 'Davon AFK')
    sorted_profiles = sorted(profile_db.get_all_profiles(), key=lambda p: p['connected_total'], reverse=True)
    for rank, profile in enumerate(sorted_profiles):
        table.add_row(rank+1,
                      profile['nickname'],
                      format_time_from_seconds(profile['connected_total']),
                      format_time_from_seconds(profile['connected_afk']))

    table_html = table.generate()
    wordpress_db.update_post_content(table_html)
