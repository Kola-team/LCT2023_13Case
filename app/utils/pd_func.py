import json

import pandas as pd

from app.data_base.db_query import DB


db = DB()

segment_names = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                 'z']


async def pd_booking_point_aer_svo(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point данные для верхнего графика резервирования с уетом сезонов
    направление aer-svo
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_aer_svo "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    curr_flt = sdf[['dtd', 'tt']].copy()

    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)

    dem_cluster = await db.pd_booking_point_aer_svo(
        flt_num=fltnum, dd=date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_aer_svo "
        f"WHERE flt_num='{fltnum}' AND demcluster='{dem_cluster}' ",
        db.engine,)

    q25 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}
                                                     ).reset_index()
    q75 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.75)
        ).rename(columns={'tt': 'q75'})

    iqr = q25.join(q75, on='dtd')

    str_json = iqr.to_json()

    to_json = json.loads(str_json)
    return to_json


async def pd_booking_point_asf_svo(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point данные для верхнего графика резервирования с уетом сезонов
    направление asf-svo
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_asf_svo "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    curr_flt = sdf[['dtd', 'tt']].copy()

    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)

    dem_cluster = await db.pd_booking_point_asf_svo(
        flt_num=fltnum, dd=date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_asf_svo "
        f"WHERE flt_num='{fltnum}' AND demcluster='{dem_cluster}' ",
        db.engine,)

    q25 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}
                                                     ).reset_index()
    q75 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.75)
        ).rename(columns={'tt': 'q75'})

    iqr = q25.join(q75, on='dtd')

    str_json = iqr.to_json()

    to_json = json.loads(str_json)
    return to_json


async def pd_booking_point_svo_aer(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point данные для верхнего графика резервирования с уетом сезонов
    направление svo-aer
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_svo_aer "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    curr_flt = sdf[['dtd', 'tt']].copy()

    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)

    dem_cluster = await db.pd_booking_point_svo_aer(
        flt_num=fltnum, dd=date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_svo_aer "
        f"WHERE flt_num='{fltnum}' AND demcluster='{dem_cluster}' ",
        db.engine,)

    q25 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}
                                                     ).reset_index()
    q75 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.75)
        ).rename(columns={'tt': 'q75'})

    iqr = q25.join(q75, on='dtd')

    str_json = iqr.to_json()

    to_json = json.loads(str_json)
    return to_json


async def pd_booking_point_svo_asf(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point данные для верхнего графика резервирования с уетом сезонов
    направление svo-asf
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_svo_asf "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    curr_flt = sdf[['dtd', 'tt']].copy()

    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)

    dem_cluster = await db.pd_booking_point_svo_asf(
        flt_num=fltnum, dd=date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_svo_asf "
        f"WHERE flt_num='{fltnum}' AND demcluster='{dem_cluster}' ",
        db.engine,)

    q25 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}
                                                     ).reset_index()
    q75 = pd.DataFrame(
        sfdc.groupby(['dtd']).quantile(0.75)
        ).rename(columns={'tt': 'q75'})

    iqr = q25.join(q75, on='dtd')

    str_json = iqr.to_json()

    to_json = json.loads(str_json)
    return to_json


async def pd_booking_point_second_aer_svo(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point_second данные для второго графика резервирования
    с учетом сезонов
    направление aer-svo
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_aer_svo "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    cols = ['dtd'] + nonzero_segments

    str_jons = sdf[cols].to_json()

    to_json = json.loads(str_jons)
    return to_json


async def pd_booking_point_second_asf_svo(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point_second данные для второго графика резервирования
    с учетом сезонов
    направление asf-svo
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_asf_svo "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    cols = ['dtd'] + nonzero_segments

    str_jons = sdf[cols].to_json()

    to_json = json.loads(str_jons)
    return to_json


async def pd_booking_point_second_svo_aer(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point_second данные для второго графика резервирования
    с учетом сезонов
    направление svo_aer
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_svo_aer "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    cols = ['dtd'] + nonzero_segments

    str_jons = sdf[cols].to_json()

    to_json = json.loads(str_jons)
    return to_json


async def pd_booking_point_second_svo_asf(fltnum: int, date_str: str):
    """
    1 вкладка
    /booking_point_second данные для второго графика резервирования
    с учетом сезонов
    направление svo_asf
    """
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_svo_asf "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    cols = ['dtd'] + nonzero_segments

    str_jons = sdf[cols].to_json()

    to_json = json.loads(str_jons)
    return to_json


async def pd_demand_forecast_aer_svo(fltnum: int, date_str: str):
    """
    4 вкладка
    /demand_forecast данные для "Построение графиков прогноза
    резервирования билетов"
    направление aer_svo
    """
    orig, dest = await db.pd_demand_forecast(fltnum)

    sf = pd.read_sql(
        f"SELECT fd, tt "
        f"FROM public.flight_forecast "
        f"WHERE flt_numsh='{fltnum}' ",
        db.engine,
        parse_dates=['fd'])

    sfr = pd.read_sql(
        f"SELECT * "
        f"FROM public.res_forecast_aer_svo "
        f"WHERE flt='{fltnum}' AND fd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sfr.columns:
            if sfr[s].gt(0).any():
                nonzero_segments.append(s)

    # Формирование json
    str_jons_sf = sf.to_json()

    cols = ['dtd', 'tt'] + nonzero_segments
    str_json_sfr = sfr[cols].to_json()

    return {
            "first_graph": json.loads(str_jons_sf),
            "second_graph": json.loads(str_json_sfr)
            }


async def pd_demand_forecast_asf_svo(fltnum: int, date_str: str):
    """
    4 вкладка
    /demand_forecast данные для "Построение графиков прогноза
    резервирования билетов"
    направление asf_svo
    """
    orig, dest = await db.pd_demand_forecast(fltnum)

    sf = pd.read_sql(
        f"SELECT fd, tt "
        f"FROM public.flight_forecast "
        f"WHERE flt_numsh='{fltnum}' ",
        db.engine,
        parse_dates=['fd'])

    sfr = pd.read_sql(
        f"SELECT * "
        f"FROM public.res_forecast_asf_svo "
        f"WHERE flt='{fltnum}' AND fd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sfr.columns:
            if sfr[s].gt(0).any():
                nonzero_segments.append(s)

    # Формирование json
    str_jons_sf = sf.to_json()

    cols = ['dtd', 'tt'] + nonzero_segments
    str_json_sfr = sfr[cols].to_json()

    return {
            "first_graph": json.loads(str_jons_sf),
            "second_graph": json.loads(str_json_sfr)
            }


async def pd_demand_forecast_svo_aer(fltnum: int, date_str: str):
    """
    4 вкладка
    /demand_forecast данные для "Построение графиков прогноза
    резервирования билетов"
    направление svo_aer
    """
    orig, dest = await db.pd_demand_forecast(fltnum)

    sf = pd.read_sql(
        f"SELECT fd, tt "
        f"FROM public.flight_forecast "
        f"WHERE flt_numsh='{fltnum}' ",
        db.engine,
        parse_dates=['fd'])

    sfr = pd.read_sql(
        f"SELECT * "
        f"FROM public.res_forecast_svo_aer "
        f"WHERE flt='{fltnum}' AND fd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sfr.columns:
            if sfr[s].gt(0).any():
                nonzero_segments.append(s)

    # Формирование json
    str_jons_sf = sf.to_json()

    cols = ['dtd', 'tt'] + nonzero_segments
    str_json_sfr = sfr[cols].to_json()

    return {
            "first_graph": json.loads(str_jons_sf),
            "second_graph": json.loads(str_json_sfr)
            }


async def pd_demand_forecast_svo_asf(fltnum: int, date_str: str):
    """
    4 вкладка
    /demand_forecast данные для "Построение графиков прогноза
    резервирования билетов"
    направление svo_asf
    """
    orig, dest = await db.pd_demand_forecast(fltnum)

    sf = pd.read_sql(
        f"SELECT fd, tt "
        f"FROM public.flight_forecast "
        f"WHERE flt_numsh='{fltnum}' ",
        db.engine,
        parse_dates=['fd'])

    sfr = pd.read_sql(
        f"SELECT * "
        f"FROM public.res_forecast_svo_asf "
        f"WHERE flt='{fltnum}' AND fd='{date_str}' ",
        db.engine)

    nonzero_segments = []
    for s in segment_names:
        if s in sfr.columns:
            if sfr[s].gt(0).any():
                nonzero_segments.append(s)

    # Формирование json
    str_jons_sf = sf.to_json()

    cols = ['dtd', 'tt'] + nonzero_segments
    str_json_sfr = sfr[cols].to_json()

    return {
            "first_graph": json.loads(str_jons_sf),
            "second_graph": json.loads(str_json_sfr)
            }


async def pd_demand_profile_aer_svo(fltnum: int, date_str: str):
    """
    3 вкладка
    /demand_profile данные для "Профили спроса"
    направление aer_svo
    """
    # Извлечение и расчет данных
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_aer_svo "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)
    curr_flt = sdf[['dtd', 'tt']].copy()
    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)
    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    hot_cold_cluster = await db.pd_demand_profile_aer_svo_hcbuy(
        fltnum, date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_aer_svo "
        f"WHERE flt_num='{fltnum}' AND hcbuy='{hot_cold_cluster[0]}' ",
        db.engine)
    q25 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}).reset_index()
    q75 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.75)).rename(columns={'tt': 'q75'})
    iqr = q25.join(q75, on='dtd')

    # # Запись jsonов
    str_json_curr_flt = curr_flt.to_json()

    str_json_iqr = iqr.to_json()

    cols = ['dtd'] + nonzero_segments
    str_jons_sdf = sdf[cols].to_json()

    return {
            "first_graph": json.loads(str_json_curr_flt),
            "second_graph": json.loads(str_json_iqr),
            "third_graph": json.loads(str_jons_sdf),
            }


async def pd_demand_profile_asf_svo(fltnum: int, date_str: str):
    """
    3 вкладка
    /demand_profile данные для "Профили спроса"
    направление asf_svo
    """
    # Извлечение и расчет данных
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_asf_svo "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)
    curr_flt = sdf[['dtd', 'tt']].copy()
    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)
    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    hot_cold_cluster = await db.pd_demand_profile_asf_svo_hcbuy(
        fltnum, date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_asf_svo "
        f"WHERE flt_num='{fltnum}' AND hcbuy='{hot_cold_cluster[0]}' ",
        db.engine)
    q25 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}).reset_index()
    q75 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.75)).rename(columns={'tt': 'q75'})
    iqr = q25.join(q75, on='dtd')

    # # Запись jsonов
    str_json_curr_flt = curr_flt.to_json()

    str_json_iqr = iqr.to_json()

    cols = ['dtd'] + nonzero_segments
    str_jons_sdf = sdf[cols].to_json()

    return {
            "first_graph": json.loads(str_json_curr_flt),
            "second_graph": json.loads(str_json_iqr),
            "third_graph": json.loads(str_jons_sdf),
            }


async def pd_demand_profile_svo_aer(fltnum: int, date_str: str):
    """
    3 вкладка
    /demand_profile данные для "Профили спроса"
    направление svo_aer
    """
    # Извлечение и расчет данных
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_svo_aer "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)
    curr_flt = sdf[['dtd', 'tt']].copy()
    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)
    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    hot_cold_cluster = await db.pd_demand_profile_svo_aer_hcbuy(
        fltnum, date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_svo_aer "
        f"WHERE flt_num='{fltnum}' AND hcbuy='{hot_cold_cluster[0]}' ",
        db.engine)
    q25 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}).reset_index()
    q75 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.75)).rename(columns={'tt': 'q75'})
    iqr = q25.join(q75, on='dtd')

    # # Запись jsonов
    str_json_curr_flt = curr_flt.to_json()

    str_json_iqr = iqr.to_json()

    cols = ['dtd'] + nonzero_segments
    str_jons_sdf = sdf[cols].to_json()

    return {
            "first_graph": json.loads(str_json_curr_flt),
            "second_graph": json.loads(str_json_iqr),
            "third_graph": json.loads(str_jons_sdf),
            }


async def pd_demand_profile_svo_asf(fltnum: int, date_str: str):
    """
    3 вкладка
    /demand_profile данные для "Профили спроса"
    направление svo_asf
    """
    # Извлечение и расчет данных
    sdf = pd.read_sql(
        f"SELECT * "
        f"FROM public.reserv_svo_asf "
        f"WHERE flt_num='{fltnum}' AND dd='{date_str}' ",
        db.engine)
    curr_flt = sdf[['dtd', 'tt']].copy()
    curr_flt.sort_values(by='dtd', inplace=True, ignore_index=True)
    nonzero_segments = []
    for s in segment_names:
        if s in sdf.columns:
            if sdf[s].gt(0).any():
                nonzero_segments.append(s)

    hot_cold_cluster = await db.pd_demand_profile_svo_asf_hcbuy(
        fltnum, date_str
        )

    sfdc = pd.read_sql(
        f"SELECT dtd, tt "
        f"FROM public.reserv_svo_asf "
        f"WHERE flt_num='{fltnum}' AND hcbuy='{hot_cold_cluster[0]}' ",
        db.engine)
    q25 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.25)).rename(columns={'tt': 'q25'}).reset_index()
    q75 = pd.DataFrame(sfdc.groupby(
        ['dtd']).quantile(0.75)).rename(columns={'tt': 'q75'})
    iqr = q25.join(q75, on='dtd')

    # # Запись jsonов
    str_json_curr_flt = curr_flt.to_json()

    str_json_iqr = iqr.to_json()

    cols = ['dtd'] + nonzero_segments
    str_jons_sdf = sdf[cols].to_json()

    return {
            "first_graph": json.loads(str_json_curr_flt),
            "second_graph": json.loads(str_json_iqr),
            "third_graph": json.loads(str_jons_sdf),
            }
