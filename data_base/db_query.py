from datetime import date

from sqlalchemy import create_engine, Table, MetaData, select

from config import DATABASE_URL


class DB:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True)
        self.metadata = MetaData()
        self.flight_data = Table('flight_data',
                                 self.metadata,
                                 autoload_with=self.engine
                                 )
        self.flight_forecast = Table('flight_forecast',
                                     self.metadata,
                                     autoload_with=self.engine
                                     )
        self.flights = Table('flights',
                             self.metadata,
                             autoload_with=self.engine
                             )
        self.reserv_aer_svo = Table('reserv_aer_svo',
                                    self.metadata,
                                    autoload_with=self.engine
                                    )
        self.reserv_asf_svo = Table('reserv_asf_svo',
                                    self.metadata,
                                    autoload_with=self.engine
                                    )
        self.reserv_svo_aer = Table('reserv_svo_aer',
                                    self.metadata,
                                    autoload_with=self.engine
                                    )
        self.reserv_svo_asf = Table('reserv_svo_asf',
                                    self.metadata,
                                    autoload_with=self.engine
                                    )
        self.res_forecast_aer_svo = Table('res_forecast_aer_svo',
                                          self.metadata,
                                          autoload_with=self.engine
                                          )
        self.res_forecast_asf_svo = Table('res_forecast_asf_svo',
                                          self.metadata,
                                          autoload_with=self.engine
                                          )
        self.res_forecast_svo_aer = Table('res_forecast_svo_aer',
                                          self.metadata,
                                          autoload_with=self.engine
                                          )
        self.res_forecast_svo_asf = Table('res_forecast_svo_asf',
                                          self.metadata,
                                          autoload_with=self.engine
                                          )
        self.conn = self.engine.connect()

    async def __exec_query(self, query):
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def __exec_query_fetchone(self, query):
        try:
            result = self.conn.execute(query).fetchone()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_all_flights(self):
        """
        Получаем все рейсы
        """
        query = select(self.flights)
        result = await self.__exec_query(query)
        return result

    async def get_seasonality(self, flt_num: int):
        """
        Возвращает данные сезонности по рейсу
        """
        query = select(
            self.flight_data
            ).where(
            self.flight_data.c.flt_num == flt_num
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_flight_data(self, flt_num: int):
        """
        Возвращает данные по номеру рейса
        """
        query = select(
            self.flight_data.c.sorg,
            self.flight_data.c.sdst
            ).where(
            self.flight_data.c.flt_num == flt_num
            )
        try:
            result = self.conn.execute(query).first()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_season_from_flight_data(self, flt_num: int, dd: date):
        """
        Возвращает сезон по номеру рейса и дате вылета
        """
        query = select(
            self.flight_data.c.demcluster,
            self.flight_data.c.sorg,
            self.flight_data.c.sdst
        ).where(
            self.flight_data.c.flt_num == flt_num,
            self.flight_data.c.dd == dd,
        )
        try:
            result = self.conn.execute(query).first()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_flight_data_with_date(self, flt_num: int, dd: date):
        """
        Возвращает данные по рейсу и дате вылета
        """
        query = select(
            self.flight_data.c.sorg,
            self.flight_data.c.sdst,
            ).where(
            self.flight_data.c.flt_num == flt_num,
            self.flight_data.c.dd == dd,
            )
        try:
            result = self.conn.execute(query).first()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_booking_aer_svo(self, flt_num: int, dd: date):
        """
        Возвращает данные бронирования по номеру рейса
        направление aer_svo
        """
        query = select(
            self.reserv_aer_svo
            ).where(
            self.reserv_aer_svo.c.flt_num == flt_num,
            self.reserv_aer_svo.c.tt > 0,
            self.reserv_aer_svo.c.dd == dd,
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_booking_asf_svo(self, flt_num: int, dd: date):
        """
        Возвращает данные бронирования по номеру рейса
        направление asf_svo
        """
        query = select(
            self.reserv_asf_svo
            ).where(
            self.reserv_asf_svo.c.flt_num == flt_num,
            self.reserv_asf_svo.c.tt > 0,
            self.reserv_asf_svo.c.dd == dd,
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_booking_svo_aer(self, flt_num: int, dd: date):
        """
        Возвращает данные бронирования по номеру рейса
        направление svo_aer
        """
        query = select(
            self.reserv_svo_aer
            ).where(
            self.reserv_svo_aer.c.flt_num == flt_num,
            self.reserv_svo_aer.c.tt > 0,
            self.reserv_svo_aer.c.dd == dd,
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_booking_svo_asf(self, flt_num: int, dd: date):
        """
        Возвращает данные бронирования по номеру рейса
        направление svo_asf
        """
        query = select(
            self.reserv_svo_asf
            ).where(
            self.reserv_svo_asf.c.flt_num == flt_num,
            self.reserv_svo_asf.c.tt > 0,
            self.reserv_svo_asf.c.dd == dd,
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    # async def get_booking_point_aer_svo(self, demcluster: int, flt_num: int):
    #     """
    #     Возвращает данные брониирования на основании сезона
    #     направление aer_svo
    #     """
    #     query = select(
    #         self.reserv_aer_svo.c.dtd,
    #         self.reserv_aer_svo.c.tt,
    #         ).where(
    #         self.reserv_aer_svo.c.demcluster == demcluster,
    #         self.reserv_aer_svo.c.flt_num == flt_num,
    #         )
    #     try:
    #         result = self.conn.execute(query).all()
    #         print(len(result))
    #         return result
    #     except Exception as e:
    #         print(e)
    #         self.conn.rollback()
    #         return None

    async def get_booking_point_aer_svo(self, flt_num: int, dd: date):
        """
        Возвращает данные для графика резервирования с учетом сезона
        направление aer_svo
        """
        query = select(
            self.reserv_aer_svo
            ).where(
            self.reserv_aer_svo.c.dd == dd,
            self.reserv_aer_svo.c.flt_num == flt_num,
            ).order_by(
            self.reserv_aer_svo.c.dtd.desc()
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    # async def get_booking_point_asf_svo(self, demcluster: int, flt_num: int):
    #     """
    #     Возвращает данные брониирования на основании сезона
    #     направление asf_svo
    #     """
    #     query = select(
    #         self.reserv_asf_svo.c.dtd,
    #         self.reserv_asf_svo.c.tt,
    #         ).where(
    #         self.reserv_asf_svo.c.demcluster == demcluster,
    #         self.reserv_asf_svo.c.flt_num == flt_num,
    #         )
    #     try:
    #         result = self.conn.execute(query).all()
    #         print(len(result))
    #         return result
    #     except Exception as e:
    #         print(e)
    #         self.conn.rollback()
    #         return None

    async def get_booking_point_asf_svo(self, flt_num: int, dd: date):
        """
        Возвращает данные для графика резервирования с учетом сезона
        направление asf_svo
        """
        query = select(
            self.reserv_asf_svo
            ).where(
            self.reserv_asf_svo.c.dd == dd,
            self.reserv_asf_svo.c.flt_num == flt_num,
            ).order_by(
            self.reserv_asf_svo.c.dtd.desc()
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    # async def get_booking_point_svo_aer(self, demcluster: int, flt_num: int):
    #     """
    #     Возвращает данные брониирования на основании сезона
    #     направление svo_aer
    #     """
    #     query = select(
    #         self.reserv_svo_aer.c.dtd,
    #         self.reserv_svo_aer.c.tt,
    #         ).where(
    #         self.reserv_svo_aer.c.demcluster == demcluster,
    #         self.reserv_svo_aer.c.flt_num == flt_num,
    #         )
    #     try:
    #         result = self.conn.execute(query).all()
    #         print(len(result))
    #         return result
    #     except Exception as e:
    #         print(e)
    #         self.conn.rollback()
    #         return None

    async def get_booking_point_svo_aer(self, flt_num: int, dd: date):
        """
        Возвращает данные для графика резервирования с учетом сезона
        направление svo_aer
        """
        query = select(
            self.reserv_svo_aer
            ).where(
            self.reserv_svo_aer.c.dd == dd,
            self.reserv_svo_aer.c.flt_num == flt_num,
            ).order_by(
            self.reserv_svo_aer.c.dtd.desc()
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    # async def get_booking_point_svo_asf(self, demcluster: int, flt_num: int):
    #     """
    #     Возвращает данные бронирования на основании сезона
    #     направление svo_asf
    #     """
    #     query = select(
    #         self.reserv_svo_asf.c.dtd,
    #         self.reserv_svo_asf.c.tt,
    #         ).where(
    #         self.reserv_svo_asf.c.demcluster == demcluster,
    #         self.reserv_svo_asf.c.flt_num == flt_num,
    #         )
    #     try:
    #         result = self.conn.execute(query).all()
    #         print(len(result))
    #         return result
    #     except Exception as e:
    #         print(e)
    #         self.conn.rollback()
    #         return None

    async def get_booking_point_svo_asf(self, flt_num: int, dd: date):
        """
        Возвращает данные для графика резервирования с учетом сезона
        направление svo_asf
        """
        query = select(
            self.reserv_svo_asf
            ).where(
            self.reserv_svo_asf.c.dd == dd,
            self.reserv_svo_asf.c.flt_num == flt_num,
            ).order_by(
            self.reserv_svo_asf.c.dtd.desc()
            )
        try:
            result = self.conn.execute(query).all()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def get_booking_point_second_aer_svo(self, flt_num: int, dd: date):
        """
        Возвращает данные для второго графика резервирования с учетом сезонов
        """
        query = select(
            self.reserv_aer_svo.c.hcbuy
            ).where(
            self.reserv_aer_svo.c.flt_num == flt_num,
            self.reserv_aer_svo.c.dd == dd,
            ).distinct(
            self.reserv_aer_svo.c.hcbuy
            )
        hcbuy = await self.__exec_query(query)

        query = select(
            self.reserv_aer_svo.c.dtd,
            self.reserv_aer_svo.c.tt,
            ).where(
            self.reserv_aer_svo.c.flt_num == flt_num,
            self.reserv_aer_svo.c.hcbuy == hcbuy[0][0],
            )
        result = await self.__exec_query(query)
        return result

    async def get_demand_forecast_aer_svo(self, flt_num: int, dd: date):
        """
        Возвращает все планируемые полеты по номеру рейса
        направление aer_svo
        """
        query = select(
            self.flight_forecast.c.fd,
            self.flight_forecast.c.tt,
        ).where(
            self.flight_forecast.c.flt_numsh == flt_num,
            self.flight_forecast.c.fd == dd,
        )
        try:
            result = self.conn.execute(query).first()
            print(len(result))
            return result
        except Exception as e:
            print(e)
            self.conn.rollback()
            return None

    async def pd_booking_point_aer_svo(self, flt_num: int, dd: date):
        query = select(
            self.reserv_aer_svo.c.demcluster,
        ).where(
            self.reserv_aer_svo.c.flt_num == flt_num,
            self.reserv_aer_svo.c.dd == dd,
        ).distinct(
            self.reserv_aer_svo.c.demcluster
        )
        result = await self.__exec_query_fetchone(query)
        print(result)
        return result[0]

    async def pd_booking_point_asf_svo(self, flt_num: int, dd: date):
        query = select(
            self.reserv_asf_svo.c.demcluster,
        ).where(
            self.reserv_asf_svo.c.flt_num == flt_num,
            self.reserv_asf_svo.c.dd == dd,
        ).distinct(
            self.reserv_asf_svo.c.demcluster
        )
        result = await self.__exec_query_fetchone(query)
        print(result)
        return result[0]

    async def pd_booking_point_svo_aer(self, flt_num: int, dd: date):
        query = select(
            self.reserv_svo_aer.c.demcluster,
        ).where(
            self.reserv_svo_aer.c.flt_num == flt_num,
            self.reserv_svo_aer.c.dd == dd,
        ).distinct(
            self.reserv_svo_aer.c.demcluster
        )
        result = await self.__exec_query_fetchone(query)
        print(result)
        return result[0]

    async def pd_booking_point_svo_asf(self, flt_num: int, dd: date):
        query = select(
            self.reserv_svo_asf.c.demcluster,
        ).where(
            self.reserv_svo_asf.c.flt_num == flt_num,
            self.reserv_svo_asf.c.dd == dd,
        ).distinct(
            self.reserv_svo_asf.c.demcluster
        )
        result = await self.__exec_query_fetchone(query)
        print(result)
        return result[0]
