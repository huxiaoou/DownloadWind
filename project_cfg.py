from dataclasses import dataclass
from data_engines import CSaveDataInfo


# ---------- project configuration ----------

@dataclass(frozen=True)
class CProCfg:
    calendar_path: str
    root_dir: str
    daily_data_root_dir: str
    futures_basis: CSaveDataInfo
    futures_stock: CSaveDataInfo
    universe: list[str]


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
    futures_basis=futures_basis,
    futures_stock=futures_stock,
    universe=[
        "A.DCE",
        "AG.SHF",
        "AL.SHF",
        "AO.SHF",
        "AP.CZC",
        "AU.SHF",
        "B.DCE",
        "BB.DCE",
        "BC.INE",
        "BR.SHF",
        "BU.SHF",
        "C.DCE",
        "CF.CZC",
        "CJ.CZC",
        "CS.DCE",
        "CU.SHF",
        "CY.CZC",
        "EB.DCE",
        "EC.INE",
        "EG.DCE",
        "FB.DCE",
        "FG.CZC",
        "FU.SHF",
        "HC.SHF",
        "I.DCE",
        "IC.CFE",
        "IF.CFE",
        "IH.CFE",
        "IM.CFE",
        "J.DCE",
        "JD.DCE",
        "JM.DCE",
        "JR.CZC",
        "L.DCE",
        "LC.GFE",
        "LH.DCE",
        "LR.CZC",
        "LU.INE",
        "M.DCE",
        "MA.CZC",
        "NI.SHF",
        "NR.INE",
        "OI.CZC",
        "P.DCE",
        "PB.SHF",
        "PF.CZC",
        "PG.DCE",
        "PK.CZC",
        "PM.CZC",
        "PP.DCE",
        "PR.CZC",
        "PX.CZC",
        "RB.SHF",
        "RI.CZC",
        "RM.CZC",
        "RR.DCE",
        "RS.CZC",
        "RU.SHF",
        "SA.CZC",
        "SC.INE",
        "SF.CZC",
        "SH.CZC",
        "SI.GFE",
        "SM.CZC",
        "SN.SHF",
        "SP.SHF",
        "SR.CZC",
        "SS.SHF",
        "T.CFE",
        "TA.CZC",
        "TF.CFE",
        "TL.CFE",
        "TS.CFE",
        "UR.CZC",
        "V.DCE",
        "WH.CZC",
        "WR.SHF",
        "Y.DCE",
        "ZC.CZC",
        "ZN.SHF",
    ]
)
