import sys
import os
import csv
import json
import argparse
from nfce import NFCeParser, NfeScrapper, qr_code
from nfce.qr_code_gui import NfeScanner
from PyQt6.QtWidgets import QApplication

def main(args):
    parser = NFCeParser()
    processor = NfeScrapper(parser, wait_timeout=10)

    if args.scan:
        app = QApplication(sys.argv)
        scanner = NfeScanner()

        url = None
             
        def handle_qr_code_data(data):
            nonlocal url
            url = data
            scanner.qr_code_detected.disconnect(handle_qr_code_data)
            scanner.close()
            app.quit()

        scanner.qr_code_detected.connect(handle_qr_code_data)
        scanner.show()
        app.exec()

    elif args.url is not None:
        url = args.url
    elif args.filepath is not None and os.path.isfile(args.filepath):
        url = qr_code.read_qr_code(args.filepath)
    else:
        print("No input found. Please use --scan, --url or --filepath.")
        exit(1)

    data = processor.get(url, args.browser)

    if data is None:
        print("No data found")
        return 1
    else:
        with open('data.csv', 'r', encoding='utf-8') as mainfile:
            if data.access_key in mainfile.read():
                print("Nota já existe no arquivo")
                return 1

    if args.output is None:
        print(data.serialize())
        return 0    

    output_path, output_format = get_output_path(args)

    return export_data(data, output_path, output_format)


def get_output_path(args):
    _, ext = os.path.splitext(args.output)

    if ext == '':
        output_format = str(args.format).lower()
        output_path = os.path.join(args.output, f'data.{args.format}') # se for pasta, usar ou criar arquivo data
    else:
        output_format = str(ext.strip('.')).lower()
        output_path = args.output

    return output_path, output_format


def export_data(data, output_path, output_format):
    print("Exportando dados...")
    
    if output_format == 'json':
        with open(output_path, 'w', encoding='utf-8') as outfile:
            data = data.serialize()
            json.dump(data, outfile, ensure_ascii=False, indent=4)
            return 0
    elif output_format == 'csv':
        with open(output_path, 'a', encoding='utf-8') as outfile:
            dump_csv(data, outfile)
            return 0
    else:
        print(f"Unknown format: {output_format}")
        return 1

def dump_csv(data, outfile):
    
    if os.path.exists(outfile.name) and os.path.getsize(outfile.name) > 0:
        write_header = False
    else:
        write_header = True

    writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    rows = data.to_csv()

    for header, row in rows:
        if write_header:
            writer.writerow(header)
            write_header = False

        writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download data from a NFe.')
    
    parser.add_argument('--scan', '-s', action='store_true', help='Scan QR Code to download the NFe.')
    parser.add_argument('--url', '-u', metavar='url', type=str, default=None, help='URL to download the NFe.')
    parser.add_argument('--filepath', '-p',  metavar='path', type=str, default=None, help='QR Code to download the NFe.')
    parser.add_argument('--format', '-f', metavar='format', type=str, default='csv', choices=['json', 'csv'],
                        help='Output file format wich may either be json or csv.  Default to `csv`.')
    parser.add_argument('--output', '-o',  metavar='path', type=str, default='data.csv',
                        help='File path location where to save data. If path is a folder, than the output will be saved'
                        ' in <path>/data.<format> where <format> is the same as the --format option. However if path is'
                        ' a file, than the output will be saved in <path>. If `None`, then only prints the result to '
                        'console.')
    parser.add_argument('--browser', '-b', metavar='browser', type=str, default='firefox', choices=['chrome', 'firefox', 'edge'],
                        help='Browser to use  `chrome`, `edge` e `firefox`. Default to `firefox`.')

    args = parser.parse_args()  

    main(args)