import { Center, Flex, Paper, ScrollArea } from "@mantine/core"
import Plot from 'react-plotly.js';

import { useSelector } from "react-redux"


const Dashboard = () => {

    const tabs = useSelector(state => state.data.tabs);
    const seasonalDemandData = useSelector(state => state.data.seasonalDemandData);

    const bookingDynamics = () => {
        return (
            null
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
                    hovertemplate: '<i>${x}</i>',
                    x: seasonalDemandData.items.map((i) => i.date),
                    y: seasonalDemandData.items.map((i) => i.fly_class[item])

                }
            });
            dataTotalPlot = [{
                x: seasonalDemandData.items.map((i) => i.date),
                y: seasonalDemandData.items.map((i) => i.tt),
                type: 'bar',
                marker: {
                    color: seasonalDemandData.items.map((i) => i.demcluster === 2
                        ?
                        'rgb(0, 217, 54)'
                        :
                        i.demcluster === 1
                            ? 'rgb(255, 201, 0)'
                            : 'rgb(255, 0, 0)')
                }
            }]
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

                                            width: 900,
                                            height: 310,
                                            title: 'Сезоны спроса',
                                            hovertemplate: '<i>${x}</i>',
                                            margin: { t: 40, l: 0, r: 0, b: 30 },
                                        }}
                                    />

                                    <Plot
                                        data={dataClassPlot}
                                        layout={{
                                            legend: { orientation: 'h' },
                                            width: 900,
                                            height: 310,
                                            barmode: 'stack',
                                            title: 'Спрос по классам (сегментам) бронирования',
                                            hovertemplate: '<i>${x}</i>',
                                            margin: { t: 30, l: 0, r: 0, b: 40 }
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

    let dashBoarsContetn

    switch (tabs) {
        case 'Динамика бронирования':
            dashBoarsContetn = bookingDynamics();
            break;
        case 'Сезонность спроса':
            dashBoarsContetn = SeasonalDemand();
            break;
        case 'Профили спроса':
            dashBoarsContetn = null
            break;
        case 'Прогнозирование спроса':
            dashBoarsContetn = null
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