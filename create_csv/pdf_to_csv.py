import camelot
from pathlib import Path


def read_pdf_to_csv(pdf, output_dir, filename):
    first_page_tables = camelot.read_pdf(pdf, flavor='stream', table_areas=['0,700,600,30'], pages='1')
    first_page_table = first_page_tables[0].df
    other_pages_tables = camelot.read_pdf(pdf, flavor='stream', table_areas=['0,820,600,25'], pages='2-end')
    combined_table = first_page_table.append([t.df for t in other_pages_tables])
    csv_file = combined_table.to_csv(f"{output_dir}/{filename}.csv", index=False)


if __name__ =="__main__":
    read_pdf_to_csv()