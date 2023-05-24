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
            self.flight_data.c.flt_num==flt_num
            )
        result = self.conn.execute(query).all()
        return result
