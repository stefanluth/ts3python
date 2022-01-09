class HTMLTable:
    """Class to easily generate a ranking table in HTML for WordPress"""
    def __init__(self, columns: int):
        self.columns = columns
        self.header = str()
        self.rows = list()

    def add_header(self, *cells):
        if len(cells) != self.columns:
            return
        self.header = '<thead><tr>'
        for cell in cells:
            self.header += f'<th>{cell}</th>'
        self.header += '</tr></thead>'

    def add_row(self, *cells):
        if len(cells) != self.columns:
            return
        self.rows.append('<tr>')
        for cell in cells:
            self.rows.append(f'<td>{cell}</td>')
        self.rows.append('</tr>')

    def generate(self):
        html = '<figure class="wp-block-table tg is-style-stripes"><table>'
        if len(self.header) > 0:
            html += self.header
        if len(self.rows) > 0:
            html += '<tbody>'
            for row in self.rows:
                html += row
            html += '</tbody>'
        html += '</figure></table>'
        return html
