from dataclasses import dataclass
from data_engines import CSaveDataInfo


# ---------- project configuration ----------

@dataclass(frozen=True)
class CProCfg:
    calendar_path: str
    root_dir: str
    daily_data_root_dir: str
    db_struct_path: str
    futures_basis: CSaveDataInfo
    futures_stock: CSaveDataInfo


futures_basis = CSaveDataInfo(
    file_format="wind_futures_basis_{}.csv.gz",
    desc="futures daily basis",
    fields=("ts_code", "wd_code", "basis", "basis_rate", "basis_annual"),
)

futures_stock = CSaveDataInfo(
    file_format="wind_futures_stock_{}.csv.gz",
    desc="futures daily stock",
    fields=("ts_code", "wd_code", "stock"),
)

pro_cfg = CProCfg(
    calendar_path=r"SaveDir\Data\Calendar\cne_calendar.csv",
    root_dir=r"SaveDir\Data\tushare",
    daily_data_root_dir=r"SaveDir\Data\tushare\by_date",
    db_struct_path=r"SaveDir\Data\tushare\db_struct.yaml",
    futures_basis=futures_basis,
    futures_stock=futures_stock,
)
