
from sqlalchemy.sql import func
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy import cast


# db = database(file=r'D:\FACTOR\sqldatabase.yaml')
# sourcedb = get_db(db.sourcedatabase_wind, schem='dbo')
# cf = corefunc(sourcedb = sourcedb )

class corefunc:
    # #返回股价
    # @staticmethod
    # def get_stockeodprice(dts = None, dte = None, stocklist = None ,sourcedb = None):
    #     eodsheet =  sourcedb.ASHAREEODPRICES
    #     df = sourcedb.query(subsheet.S_INFO_WINDCODE, subsheet.TRADE_DT, subsheet.S_DQ_OPEN, subsheet.S_DQ_CLOSE, subsheet.S_DQ_ADJOPEN,subsheet.S_DQ_ADJCLOSE,subsheet.S_DQ_AVGPRICE,subsheet.S_DQ_LIMIT,subsheet.S_DQ_STOPPING, subsheet.S_DQ_VOLUME).filter(subsheet.TRADE_DAYS >= dts, subsheet.TRADE_DAYS<= dte,subsheet.S_INFO_WINDCODE.in_(stocklist)).order_by(subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()

    
    #返回交易日序列
    @staticmethod
    def get_trade_dt(dts = None , dte = None,sourcedb = None):
        subsheet =  sourcedb.ASHARECALENDAR
        df = sourcedb.query(subsheet.TRADE_DAYS).filter(subsheet.TRADE_DAYS >=dts, subsheet.TRADE_DAYS <=dte, subsheet.S_INFO_EXCHMARKET =='SSE' ).order_by(subsheet.TRADE_DAYS).to_df()
        return df

    # 返回中信一级行业
    @staticmethod
    def get_citic_indu_lecelone(sourcedb = None):
        AINDEXMEMBERSCITICS = sourcedb.AINDEXMEMBERSCITICS
        B = sourcedb.AINDEXDESCRIPTION
        C = sourcedb.ASHAREDESCRIPTION

        df = sourcedb.query(
        AINDEXMEMBERSCITICS.S_INFO_WINDCODE.label('INDEX_INFO_WINDCODE'),
        AINDEXMEMBERSCITICS.S_CON_WINDCODE.label('S_INFO_WINDCODE'),
        AINDEXMEMBERSCITICS.S_CON_INDATE,
        AINDEXMEMBERSCITICS.S_CON_OUTDATE,
            cast(B.S_INFO_NAME, NVARCHAR).label('INDEX_INFO_NAME'),
            cast( C.S_INFO_NAME, NVARCHAR).label('S_INFO_NAME'),
            C.S_INFO_DELISTDATE,
            C.S_INFO_LISTDATE
        ).outerjoin(B, AINDEXMEMBERSCITICS.S_INFO_WINDCODE == B.S_INFO_WINDCODE).outerjoin(C, AINDEXMEMBERSCITICS.S_CON_WINDCODE == C.S_INFO_WINDCODE).to_df()
        return df

    # 返回中信二级行业
    @staticmethod
    def get_citic_indu_leceltwo(sourcedb = None):
        AINDEXMEMBERSCITICS = sourcedb.AINDEXMEMBERSCITICS2
        B = sourcedb.AINDEXDESCRIPTION
        C = sourcedb.ASHAREDESCRIPTION

        df = sourcedb.query(
        AINDEXMEMBERSCITICS.S_INFO_WINDCODE.label('INDEX_INFO_WINDCODE'),
        AINDEXMEMBERSCITICS.S_CON_WINDCODE.label('S_INFO_WINDCODE'),
        AINDEXMEMBERSCITICS.S_CON_INDATE,
        AINDEXMEMBERSCITICS.S_CON_OUTDATE,
            cast(B.S_INFO_NAME, NVARCHAR).label('INDEX_INFO_NAME'),
            cast( C.S_INFO_NAME, NVARCHAR).label('S_INFO_NAME'),
            C.S_INFO_DELISTDATE,
            C.S_INFO_LISTDATE
        ).outerjoin(B, AINDEXMEMBERSCITICS.S_INFO_WINDCODE == B.S_INFO_WINDCODE).outerjoin(C, AINDEXMEMBERSCITICS.S_CON_WINDCODE == C.S_INFO_WINDCODE).to_df()
        return df


    # 返回中信三级行业
    @staticmethod
    def get_citic_indu_lecelthree(sourcedb = None):
        AINDEXMEMBERSCITICS = sourcedb.AINDEXMEMBERSCITICS3
        B = sourcedb.AINDEXDESCRIPTION
        C = sourcedb.ASHAREDESCRIPTION

        df = sourcedb.query(
        AINDEXMEMBERSCITICS.S_INFO_WINDCODE.label('INDEX_INFO_WINDCODE'),
        AINDEXMEMBERSCITICS.S_CON_WINDCODE.label('S_INFO_WINDCODE'),
        AINDEXMEMBERSCITICS.S_CON_INDATE,
        AINDEXMEMBERSCITICS.S_CON_OUTDATE,
            cast(B.S_INFO_NAME, NVARCHAR).label('INDEX_INFO_NAME'),
            cast( C.S_INFO_NAME, NVARCHAR).label('S_INFO_NAME'),
            C.S_INFO_DELISTDATE,
            C.S_INFO_LISTDATE
        ).outerjoin(B, AINDEXMEMBERSCITICS.S_INFO_WINDCODE == B.S_INFO_WINDCODE).outerjoin(C, AINDEXMEMBERSCITICS.S_CON_WINDCODE == C.S_INFO_WINDCODE).to_df()
        return df
