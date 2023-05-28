import { Center, Flex, Paper, ScrollArea,Title } from "@mantine/core"
import Plot from 'react-plotly.js';

import { useSelector } from "react-redux"
import test1 from '../../images/test 1.png'
import test3 from '../../images/test3.png'
import test4 from '../../images/tect 4.png'

const Dashboard = () => {

    const tabs = useSelector(state => state.data.tabs);
    const seasonalDemandData = useSelector(state => state.data.seasonalDemandData);

    const BookingDynamics = () => {
        return (
            <Center>
                <Paper miw={'960px'} w={'70%'} h={'70vh'} p={'xs'} mt={'lg'}>
                    <ScrollArea h={'68vh'} w={'100%'}>
                        <Center >
                            <Flex align={'center'} direction={'column'}>
                                <Title>Проект</Title>
                                <img  style={{width:'100%'}}   src={test4}></img>
                            </Flex>
                        </Center>
                    </ScrollArea>
                </Paper >
            </Center>
        )
    }

    const SeasonalDemand = () => {

        let dataClassPlot = [];
        let dataTotalPlot = [];

        if ('items' in seasonalDemandData) {
            dataClassPlot = Object.keys(seasonalDemandData.items[0].fly_class).map((item) => {
                return {
                    name: item,
                    type: 'bar',
                    hovertemplate: '<b>%{x}</b><br>' + '<i>%{y}</i>',
                    x: seasonalDemandData.items.map((i) => i.date),
                    y: seasonalDemandData.items.map((i) => i.fly_class[item])

                }
            });
            dataTotalPlot = [
                {
                    x: seasonalDemandData.items.map((i) => i.date),
                    y: seasonalDemandData.items.map((i) => i.tt),
                    type: 'bar',

                    name: seasonalDemandData.items.map((i) => i.demcluster === 2
                        ?
                        'A'
                        :
                        i.demcluster === 1
                            ? 'B'
                            : 'C'),
                    marker: {
                        color: seasonalDemandData.items.map((i) => i.demcluster === 2
                            ?
                            'rgb(0, 217, 54)'
                            :
                            i.demcluster === 1
                                ? 'rgb(255, 201, 0)'
                                : 'rgb(255, 0, 0)')
                    }
                }
            ]
        }


        return (
            'items' in seasonalDemandData ?
                <Center>
                    <Paper miw={'960px'} w={'70%'} h={'70vh'} p={'xs'} mt={'lg'}>
                        <ScrollArea h={'68vh'} w={'100%'}>
                            <Center >
                                <Flex direction={'column'}>
                                    <Plot

                                        data={dataTotalPlot}
                                        layout={{
                                            yaxis: {
                                                title: {
                                                    text: 'Количество пассажиров',

                                                }
                                            },

                                            legend: {
                                                x: 0,
                                                y: 1,
                                                traceorder: 'normal'
                                            },
                                            width: 900,
                                            height: 310,
                                            title: 'Сезоны спроса',
                                            margin: { t: 40, l: 50, r: 0, b: 30 },
                                        }}
                                    />

                                    <Plot
                                        data={dataClassPlot}
                                        layout={{

                                            yaxis: {
                                                title: {
                                                    text: 'Количество пассажиров',

                                                }
                                            },
                                            legend: { orientation: 'h' },
                                            width: 900,
                                            height: 310,
                                            barmode: 'stack',
                                            title: 'Спрос по классам (сегментам) бронирования',
                                            margin: { t: 30, l: 50, r: 0, b: 40 }
                                        }}
                                    />
                                </Flex>
                            </Center>
                        </ScrollArea>
                    </Paper >
                </Center>
                : null

        )
    }

    const PemandProfiles = () => {
        return (
            <Center>
                <Paper miw={'960px'} w={'70%'} h={'70vh'} p={'xs'} mt={'lg'}>
                    <ScrollArea h={'68vh'} w={'100%'}>
                        <Center >
                            <Flex align={'center'} direction={'column'}>
                            <Title>Проект</Title>
                                <img  style={{width:'100%'}} src={test3}></img>
                            </Flex>
                        </Center>
                    </ScrollArea>
                </Paper >
            </Center>
        )
    }

    const DemandForecasting = () => {
        return (
            <Center>
                <Paper miw={'960px'} w={'70%'} h={'70vh'} p={'xs'} mt={'lg'}>
                    <ScrollArea h={'68vh'} w={'100%'}>
                        <Center >
                            <Flex align={'center'} direction={'column'}>
                            <Title>Проект</Title>
                                <img style={{width:'70%'}} src={test1}></img>
                            </Flex>
                        </Center>
                    </ScrollArea>
                </Paper >
            </Center>
        )
    }

    let dashBoarsContetn

    switch (tabs) {
        case 'Динамика бронирования':
            dashBoarsContetn = BookingDynamics();
            break;
        case 'Сезонность спроса':
            dashBoarsContetn = SeasonalDemand();
            break;
        case 'Профили спроса':
            dashBoarsContetn = PemandProfiles();
            break;
        case 'Прогнозирование спроса':
            dashBoarsContetn = DemandForecasting();
            break;
        default:

    }

    return (
        <>
            {dashBoarsContetn}
        </>
    )

}

export default Dashboard