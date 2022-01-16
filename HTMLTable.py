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
        if len(self.rows) % 2 == 0:
            self.rows.append('<tr class="table-row-even">')
        else:
            self.rows.append('<tr class="table-row-odd">')

        for cell in cells:
            try:
                int(cell)
                self.rows.append(f'<td class="data-number">{cell}</td>')
            except ValueError:
                self.rows.append(f'<td class="data-text">{cell}</td>')
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
