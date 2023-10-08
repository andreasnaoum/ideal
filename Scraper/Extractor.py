import csv


class AliExpressLinkExtractor:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def extract_links(self):
        links = []

        with open(self.csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            # Skip the first row with column titles
            next(reader, None)

            for row in reader:
                # Check if 'Exist' is TRUE
                if row[2].lower() == 'true':
                    links.append(row[1])

        return links


# Example usage:
csv_file_path = 'iDeal-AliExpress-Products-2023-10-07-CHECK.csv'
link_extractor = AliExpressLinkExtractor(csv_file_path)
links_array = link_extractor.extract_links()

print(links_array)
