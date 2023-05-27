import { MantineProvider } from '@mantine/core';
import { AppShell } from '@mantine/core';

import Main from '../Main/Main';
import AppHeader from '../Header/Header';

const AppView = () => {

    return (
        <MantineProvider
            withGlobalStyles
            withNormalizeCSS
            theme={
                {
                    components: {
                        Header: {
                            styles: (theme) => ({
                                root: {
                                    filter: `drop-shadow(0px 0.1rem ${theme.fn.rgba(
                                        theme.black, 0.05)})`
                                }
                            })
                        },
                        Container: {
                            styles: () => ({
                                root: {
                                    position: 'relative',
                                    maxWidth: 'none',
                                    zIndex: 105,
                                    minWidth: '900px'
                                }
                            })
                        },

                        Tabs: {
                            styles: (theme) => ({
                                root: {

                                },
                                panel: {
                                    background: 'white',
                                    padding: '1rem',
                                },
                                tab: {
                                    fontWeight: 'bold',
                                    fontSize: '1rem',
                                    background: 'white',
                                    // border: `1px solid ${theme.colors.gray[3]}`,
                                    // '&[data-active]:before': 'none'
                                    // color: ' rgba(0, 120, 171, 0.7)',
                                    // '&:focus:not(:focus-visible) ': { borderColor: 'rgba(0, 120, 171, 0.7)', color: 'rgba(0,0,0,.6)' }
                                },
                            })
                        },
                    },
                    black: '#202020',
                    // backgroundColor: '#02458d',
                    minWidth: '1000px'
                }}>
            <AppShell
                padding={'xl'}
                h={'100vh'}
                w={'100vw'}
                header={AppHeader()}
                styles={(theme) => ({
                    main: { backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[3], minWidth: '1000px', height: '100vh' },

                })}
            >
                <Main />

            </AppShell>
        </MantineProvider >
    )
}
export default AppView