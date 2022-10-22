import pygsheets


class GoogleSheet:
    def __init__(self, google_sheet_link: str, google_auth_file_path: str):
        gc = pygsheets.authorize(service_file=google_auth_file_path)
        self.sh = gc.open_by_url(google_sheet_link)

    def insert_row(self, row: list) -> None:
        self.sh[0].insert_rows(row=1, number=1, values=[row])

    def get_records_by_telegram_id(self, telegram_id: str) -> dict is not None:
        table = self.sh[1].get_all_values()[1::]
        for row in table:
            if row[0] != '':
                if int(row[0]) == telegram_id:
                    return {"Желтые бренды: ": row[1], "Зеленые бренды: ": row[2], "Фиолетовые бренды: ": row[3]}
        return None
