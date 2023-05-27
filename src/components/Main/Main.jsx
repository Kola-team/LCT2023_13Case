import { Tabs, Container, Autocomplete, Center, Flex, Group, Button, Select } from "@mantine/core";
import { useForm } from '@mantine/form';

import { useSelector, useDispatch } from "react-redux";

import { setTabs, setSeasonalDemandData } from "../../storage/slises/dataSlise";

import Dashboard from "../Dashboard/Dashboard";

const Main = () => {

    const dispatch = useDispatch();

    const allFlight = useSelector(state => state.data.allFlight);

    const departureList = allFlight.map((item) => item.departure).reduce((acc, item) => {
        if (acc.includes(item)) {
            return acc;
        }
        return [...acc, item];
    }, []).map((item) => {
        return {
            value: item,
            label: item
        }
    });
  const fltNumList = allFlight.map((item) => item.flt_num.toString()).sort()
    const destinationList = allFlight.map((item) => item.destination).reduce((acc, item) => {
        if (acc.includes(item)) {
            return acc;
        }
        return [...acc, item];
    }, []).map((item) => {
        return {
            value: item,
            label: item
        }
    });

  

    const formSeasonalDemand = useForm({
        initialValues: {
            departure: '',
            destination: '',
            fltNum: '',
        }
    });

    return (<>
        <Container>
            <Center>
                <Tabs defaultValue={"Сезонность спроса"} onTabChange={(e) => (dispatch(setTabs(e)))} radius="xs" variant="outline" >
                    <Tabs.List position="apart" grow={true}>
                        <Tabs.Tab mr={'1px'} value="Динамика бронирования" >Динамика бронирования</Tabs.Tab>
                        <Tabs.Tab mr={'1px'} value="Сезонность спроса" >Сезонность спроса</Tabs.Tab>
                        <Tabs.Tab mr={'1px'} value="Профили спроса" >Профили спроса</Tabs.Tab>
                        <Tabs.Tab value="Прогнозирование спроса" >Прогнозирование спроса</Tabs.Tab>
                    </Tabs.List>

                    <Tabs.Panel value="Динамика бронирования">
                        <form>
                            <Flex align={'center'} justify={'space-between'}>
                                <Group>
                                    <Autocomplete
                                        label="Откуда"
                                        placeholder='Пункт отрпавления'
                                        data={['Москва', 'Сочи', 'Санкт-Петербург', 'Краснодар']}
                                    />
                                    <Autocomplete
                                        label="Куда"
                                        placeholder='Пункт прибытия'
                                        data={['Москва', 'Сочи', 'Санкт-Петербург', 'Краснодар']}
                                    />
                                </Group>

                                <Button variant={'light'} mt={'25px'}>Сформировать</Button>

                            </Flex>
                        </form>

                    </Tabs.Panel>

                    <Tabs.Panel value="Сезонность спроса">
                        <form>
                            <Flex align={'center'} justify={'space-between'}>
                                <Group>
                                    <Select
                                        searchable
                                        nothingFound="Ничего не найдено"
                                        label="Аэропорт вылета"
                                        placeholder='Пункт отрпавления'
                                        value={formSeasonalDemand.values.departure}
                                        onChange={(value) => formSeasonalDemand.setFieldValue('departure', value)}
                                        data={departureList}
                                        w={150}
                                    />
                                    <Select
                                        searchable
                                        nothingFound="Ничего не найдено"
                                        label="Аэропорт прибытия"
                                        placeholder='Пункт прибытия'
                                        value={formSeasonalDemand.values.destination}
                                        onChange={(value) => formSeasonalDemand.setFieldValue('destination', value)}
                                        data={destinationList}
                                        w={150}
                                    />
                                    <Select
                                        searchable
                                        required
                                        label="Номер рейса"
                                        placeholder='номер рейса'
                                        value={formSeasonalDemand.values.fltNum}
                                        onChange={(value) => formSeasonalDemand.setFieldValue('fltNum', value)}
                                        data={fltNumList}
                                        w={150}
                                    />
                                </Group>

                                <Button variant={'light'} mt={'25px'} onClick={() => (dispatch(setSeasonalDemandData(formSeasonalDemand.values.fltNum)))}>Сформировать</Button>

                            </Flex>
                        </form>
                    </Tabs.Panel>

                    <Tabs.Panel value="Профили спроса" >
                        <form>
                            <Flex align={'center'} justify={'space-between'}>
                                <Group>
                                    <Autocomplete
                                        label="Откуда"
                                        placeholder='Пункт отрпавления'
                                        data={['Москва', 'Сочи', 'Санкт-Петербург', 'Краснодар']}
                                    />
                                    <Autocomplete
                                        label="Куда"
                                        placeholder='Пункт прибытия'
                                        data={['Москва', 'Сочи', 'Санкт-Петербург', 'Краснодар']}
                                    />
                                </Group>

                                <Button variant={'light'} mt={'25px'}>Сформировать</Button>

                            </Flex>
                        </form>

                    </Tabs.Panel>

                    <Tabs.Panel value="Прогнозирование спроса" >
                        <form>
                            <Flex align={'center'} justify={'space-between'}>
                                <Group>
                                    <Autocomplete
                                        label="Откуда"
                                        placeholder='Пункт отрпавления'
                                        data={['Москва', 'Сочи', 'Санкт-Петербург', 'Краснодар']}
                                    />
                                    <Autocomplete
                                        label="Куда"
                                        placeholder='Пункт прибытия'
                                        data={['Москва', 'Сочи', 'Санкт-Петербург', 'Краснодар']}
                                    />
                                </Group>

                                <Button variant={'light'} mt={'25px'}>Сформировать</Button>

                            </Flex>
                        </form>

                    </Tabs.Panel>
                </Tabs>
            </Center>
            <Dashboard />
        </Container>
        {/* <div style={{ minWidth: '960px' }}>
            <img style={{ zIndex: '0', position: 'absolute', bottom: '150px', right: '0', height: '18rem' }} src="https://www.aeroflot.ru/frontend/static/img/clouds.png" alt=""></img>
            <img style={{ zIndex: '10', position: 'absolute', bottom: '70px', right: '0', height: '15rem' }} src="https://www.aeroflot.ru/frontend/static/img/aircraft.png" alt=""></img>
            <img style={{ position: 'absolute', bottom: '0', right: '0', }} src="https://www.aeroflot.ru/frontend/static/img/smile2.svg" alt=""></img>
        </div> */}
    </>
    )
}

export default Main