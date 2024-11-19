import argparse


def parse_args():
    arg_parser_main = argparse.ArgumentParser(description="Project to download data from tushare")
    arg_parser_main.add_argument("--bgn", type=str, required=True)
    arg_parser_main.add_argument("--stp", type=str, default=None)

    arg_parser_subs = arg_parser_main.add_subparsers(
        title="sub function",
        dest="func",
        description="use this argument to go to call different functions",
    )

    # func: download
    arg_parser_sub = arg_parser_subs.add_parser(name="download", help="Download data from tushare and wind")
    arg_parser_sub.add_argument(
        "--switch", type=str, required=True,
        choices=("basis", "stock"),
    )

    # func: update
    arg_parser_sub = arg_parser_subs.add_parser(name="update", help="Update data for database")
    arg_parser_sub.add_argument(
        "--switch", type=str, required=True,
        choices=("basis", "stock"),
    )

    # --- parse args
    _args = arg_parser_main.parse_args()
    return _args


if __name__ == "__main__":
    from project_cfg import pro_cfg
    from qcalendar import CCalendar

    calendar = CCalendar(calendar_path=pro_cfg.calendar_path)

    args = parse_args()
    bgn, stp = args.bgn, args.stp or calendar.get_next_date(args.bgn, shift=1)

    if args.func == "download":
        if args.switch == "basis":
            from data_engines import CDataEngineWindFutDailyBasis

            engine = CDataEngineWindFutDailyBasis(
                save_root_dir=pro_cfg.daily_data_root_dir,
                save_data_info=pro_cfg.futures_basis,
                universe=pro_cfg.universe,
            )
            engine.download_data_range(bgn_date=bgn, stp_date=stp, calendar=calendar)
        elif args.switch == "stock":
            from data_engines import CDataEngineWindFutDailyStock

            engine = CDataEngineWindFutDailyStock(
                save_root_dir=pro_cfg.daily_data_root_dir,
                save_data_info=pro_cfg.futures_stock,
                universe=pro_cfg.universe,
            )
            engine.download_data_range(bgn_date=bgn, stp_date=stp, calendar=calendar)
        else:
            raise ValueError(f"switch = {args.switch} is illegal")
    elif args.func == "update":
        pass
    else:
        raise ValueError(f"switch = {args.switch} is illegal")
