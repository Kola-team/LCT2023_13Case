from datetime import date

from sqlalchemy import create_engine, Table, MetaData, select

from config import DATABASE_URL


class DB:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
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
        self.conn = self.engine.connect()

    async def get_all_flights(self):
        """
        Получаем все рейсы
        """
        query = select(self.flights)
        result = self.conn.execute(query).all()
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
