import os
import sys
import time
import pandas as pd
from loguru import logger
from dataclasses import dataclass
from rich.progress import Progress, TaskID
from WindPy import w as wapi
from qutility import check_and_makedirs, qtimer, SFG
from qcalendar import CCalendar

pd.set_option('display.unicode.east_asian_width', True)
logger.add("logs/download_and_update.log")


@dataclass(frozen=True)
class CSaveDataInfo:
    file_format: str
    desc: str
    fields: tuple[str, ...]


class __CDataEngine:
    def __init__(self, save_root_dir: str, save_file_format: str, data_desc: str):
        self.save_root_dir = save_root_dir
        self.save_file_format = save_file_format
        self.data_desc = data_desc

    def download_daily_data(self, trade_date: str, task_id: TaskID, pb: Progress) -> pd.DataFrame:
        raise NotImplementedError

    @qtimer
    def download_data_range(self, bgn_date: str, stp_date: str, calendar: CCalendar):
        iter_dates = calendar.get_iter_list(bgn_date, stp_date)
        with Progress() as pb:
            task_pri = pb.add_task(description="Pri-task description to be updated", total=len(iter_dates))
            task_sub = pb.add_task(description="Sub-task description to be updated")
            for trade_date in iter_dates:
                pb.update(task_id=task_pri, description=f"Processing data for {SFG(trade_date)}")
                check_and_makedirs(save_dir := os.path.join(self.save_root_dir, trade_date[0:4], trade_date))
                save_file = self.save_file_format.format(trade_date)
                save_path = os.path.join(save_dir, save_file)
                if os.path.exists(save_path):
                    logger.info(f"{self.data_desc} for {trade_date} exists, program will skip it")
                else:
                    trade_date_data = self.download_daily_data(trade_date, task_id=task_sub, pb=pb)
                    trade_date_data.to_csv(save_path, index=False)
                pb.update(task_id=task_pri, advance=1)
        return 0


class __CDataEngineWind(__CDataEngine):
    def __init__(self, save_root_dir: str, save_file_format: str, data_desc: str, universe: list[str]):
        self.api = wapi
        self.api.start()
        self.universe = universe
        super().__init__(save_root_dir, save_file_format, data_desc)

    @staticmethod
    def wind2tushare(instru: str) -> str:
        return instru.replace(".CZC", ".ZCE").replace(".CFE", ".CFX")

    @property
    def universe_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            "ts_code": [self.wind2tushare(z) for z in self.universe],
            "wd_code": self.universe,
        })

    @staticmethod
    def convert_data_to_dataframe(downloaded_data, download_values: list[str], col_names: list[str]) -> pd.DataFrame:
        if downloaded_data.ErrorCode != 0:
            logger.error(f"When download data from WIND, ErrorCode = {downloaded_data.ErrorCode}.")
            logger.info("Program will terminate at once, please check again.")
            sys.exit()
        else:
            df = pd.DataFrame(downloaded_data.Data, index=download_values, columns=col_names).T
            return df


class CDataEngineWindFutDailyBasis(__CDataEngineWind):
    def __init__(self, save_root_dir: str, save_data_info: CSaveDataInfo, universe: list[str]):
        super().__init__(save_root_dir, save_data_info.file_format, save_data_info.desc, universe)

    def download_daily_data(self, trade_date: str, task_id: TaskID, pb: Progress) -> pd.DataFrame:
        while True:
            try:
                time.sleep(0.5)
                unvrs_f = [instru for instru in self.universe if instru.split(".")[1] == "CFE"]
                unvrs_c = [instru for instru in self.universe if instru.split(".")[1] != "CFE"]

                # download financial
                indicators = {
                    "anal_basis_stkidx": "basis",
                    "anal_basispercent_stkidx": "basis_rate",
                    "anal_basisannualyield_stkidx": "basis_annual",
                }
                f_data = self.api.wss(codes=unvrs_f, fields=list(indicators), options=f"tradeDate={trade_date}")
                df_f = self.convert_data_to_dataframe(f_data, download_values=list(indicators), col_names=unvrs_f)
                df_f = df_f.rename(mapper=indicators, axis=1)

                # download commodity
                indicators = {
                    "anal_basis": "basis",
                    "anal_basispercent2": "basis_rate",
                    "basisannualyield": "basis_annual",
                }
                c_data = self.api.wss(codes=unvrs_c, fields=list(indicators), options=f"tradeDate={trade_date}")
                df_c = self.convert_data_to_dataframe(c_data, download_values=list(indicators), col_names=unvrs_c)
                df_c = df_c.rename(mapper=indicators, axis=1)

                # concat
                df = pd.concat([df_f, df_c], axis=0, ignore_index=False)
                res = pd.merge(
                    left=self.universe_df[["ts_code", "wd_code"]],
                    right=df,
                    left_on="wd_code",
                    right_index=True,
                    how="left",
                )
                return res
            except TimeoutError as e:
                logger.error(e)
                time.sleep(5)


class CDataEngineWindFutDailyStock(__CDataEngineWind):
    def __init__(self, save_root_dir: str, save_data_info: CSaveDataInfo, universe: list[str]):
        super().__init__(save_root_dir, save_data_info.file_format, save_data_info.desc, universe)

    def download_daily_data(self, trade_date: str, task_id: TaskID, pb: Progress) -> pd.DataFrame:
        while True:
            try:
                time.sleep(0.5)
                indicators = {"st_stock": "stock"}
                stock_data = self.api.wss(codes=self.universe, fields=list(indicators),
                                          options=f"tradeDate={trade_date}")
                df = self.convert_data_to_dataframe(stock_data, download_values=list(indicators),
                                                    col_names=self.universe)
                df = df.rename(mapper=indicators, axis=1)
                res = pd.merge(
                    left=self.universe_df[["ts_code", "wd_code"]],
                    right=df,
                    left_on="wd_code",
                    right_index=True,
                    how="left",
                )
                return res
            except TimeoutError as e:
                logger.error(e)
                time.sleep(5)
