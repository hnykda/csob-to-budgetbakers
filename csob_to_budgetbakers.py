__author__ = 'dan'


def parse_arguments():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(description="program for converting output of CSOB txt export to budgetbakers input format",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", type=str,
                        help="input txt file to process",
                        required=True)
    parser.add_argument("-o", "--output", type=str, help="output file name", default="out.csv")
    parser.add_argument("-c", "--category", type=str, help="default category", required=True)
    parser.add_argument("-p", "--payment_type", type=str, help="Default Payment type", choices=["CASH", "DEBIT_CARD", "CREDIT_CARD", "TRANSFER", "VOUCHER", "MOBILE_PAYMENT", "WEB_PAYMENT"], default="DEBIT_CARD")
    parser.add_argument("-a", "--account", type=str, help="Account to which attribute the transactions", default="CSOB")
    parser.add_argument("-n", "--number", type=int, help="Number of processed transactions", default="20")
    parser.add_argument("-l", "--log_level", type=int, choices=[10, 20, 30, 40, 50], default=20,
                        help="Log level of standard_output. Debug ~ 10, Critical ~ 50. ")

    return parser.parse_args()


def prepare_logging(level):
    import logging
    import sys

    log = logging.getLogger()
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    log.addHandler(ch)
    log.setLevel(level)

    return log

def convert(args):
    import pandas as pd
    with open(args.input, "r") as ifile:
        r = ifile.read()
    import re
#    pat = r"datum zaúčtování:\s(.*)\sčástka:\s*(.*)\směna:\s*(.*)\s.*\s.*\s.*\s.*\s.*\s.*\s.*\spoznámka:(.*)"
    pat = r"datum zaúčtování:\s(.*)\sčástka:\s*(.*)\směna:\s*(.*)\s.*\s.*\s.*\s.*\s.*označení operace:\s*(.*)\s.*\s.*\spoznámka:\s*(.*)"
    txt = re.findall(pat, r)
    df = pd.DataFrame(txt, columns=["date", "amount", "currency", "payment_type","note"]).iloc[:args.number]

    def polish_note(note):
        if note.isspace():
            return ""
        else:
            fnd = re.findall("Částka:\s\d*\s\D{4}\d*.\d*.\d*;\s(.*)", note)
            if len(fnd) == 0:
                return ""
            else:
                return fnd[0].replace(";",",")

    def polish_payment_type(type):
        res = args.payment_type
        if "Transakce platební kartou" in type:
            res = "DEBIT_CARD"
        elif ("Došlá platba" in type) or ("Bezhotovostní převod el. bankovnictví" in type):
            res = "TRANSFER"
        return res 
        
    def polish(df):
        df.date = df.date.map(pd.to_datetime).map(str)
        df.amount = df.amount.map(float)
        df.note = df.note.map(polish_note)
        df.payment_type = df.payment_type.map(polish_payment_type)

        return df

    p = polish(df)

    p["account"] = args.account
    p["category"] = args.category

    p.to_csv(args.output, sep=";", index=False, quoting=3, escapechar="\\")


def main():
    args = parse_arguments()
    log = prepare_logging(args.log_level)

    try:
        convert(args) 
    except KeyboardInterrupt as ex:
        log.warning("Terminated by user.")
    except SystemExit as ex:
        log.info("Finished. Exiting")


if __name__ == "__main__":
    main()
