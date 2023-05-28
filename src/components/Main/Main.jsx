import { Tabs, Container, Autocomplete, Center, Flex, Group, Button, Select } from "@mantine/core";
import { useForm } from '@mantine/form';
import { DateInput } from '@mantine/dates';

import { useEffect } from "react";

import { useSelector, useDispatch } from "react-redux";

import { setTabs, setSeasonalDemandData, setBookingDynamicsData } from "../../storage/slises/dataSlise";

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

    const formbookingDynamics = useForm({
        initialValues: {
            departure: '',
            destination: '',
            fltNum: '',
            dd: ''
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
                                    <Select
                                        searchable
                                        nothingFound="Не найдено"
                                        label="Отрпавление"
                                        placeholder='не выбрано'
                                        value={formbookingDynamics.values.departure}
                                        onChange={(value) => formbookingDynamics.setFieldValue('departure', value)}
                                        data={departureList}
                                        w={150}
                                    />
                                    <Select
                                        searchable
                                        nothingFound="Не найдено"
                                        label="Прибытие"
                                        placeholder='не выбрано'
                                        value={formbookingDynamics.values.destination}
                                        onChange={(value) => formbookingDynamics.setFieldValue('destination', value)}
                                        data={destinationList}
                                        w={130}
                                    />
                                    <Select
                                        searchable
                                        required
                                        nothingFound="Не найдено"
                                        label="Рейс"
                                        placeholder='не выбран'
                                        value={formbookingDynamics.values.fltNum}
                                        onChange={(value) => formbookingDynamics.setFieldValue('fltNum', value)}
                                        data={fltNumList}
                                        w={130}
                                    />
                                    <DateInput
                                        w={130}
                                        label="Выберите дату"
                                        value={formbookingDynamics.values.dd}
                                        onChange={(value) => formbookingDynamics.setFieldValue('dd', value)}
                                    />
                                </Group>

                                <Button variant={'light'} mt={'25px'} onClick={() => { console.log(formbookingDynamics.values.dd.toLocaleDateString('en-CA'),formbookingDynamics.values.fltNum); dispatch((setBookingDynamicsData([formbookingDynamics.values.fltNum, formbookingDynamics.values.dd.toLocaleDateString('en-CA')]))) }}
                                >Сформировать</Button>

                            </Flex>
                        </form>

                    </Tabs.Panel>

                    <Tabs.Panel value="Сезонность спроса">
                        <form>
                            <Flex align={'center'} justify={'space-between'}>
                                <Group>
                                    <Select
                                        searchable
                                        nothingFound="Не найдено"
                                        label="Отрпавление"
                                        placeholder='не выбрано'
                                        value={formSeasonalDemand.values.departure}
                                        onChange={(value) => formSeasonalDemand.setFieldValue('departure', value)}
                                        data={departureList}
                                        w={130}
                                    />
                                    <Select
                                        searchable
                                        nothingFound="Не найдено"
                                        label="Прибытие"
                                        placeholder='не выбрано'
                                        value={formSeasonalDemand.values.destination}
                                        onChange={(value) => formSeasonalDemand.setFieldValue('destination', value)}
                                        data={destinationList}
                                        w={130}
                                    />
                                    <Select
                                        searchable
                                        required
                                        label="Рейс"
                                        nothingFound="Не найдено"
                                        placeholder='не выбран'
                                        value={formSeasonalDemand.values.fltNum}
                                        onChange={(value) => formSeasonalDemand.setFieldValue('fltNum', value)}
                                        data={fltNumList}
                                        w={130}
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
    </>
    )
}

export default Main