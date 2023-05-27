import { Header, Flex, Avatar, Menu, Text, ActionIcon } from "@mantine/core"
import { IconLogout, IconUser } from '@tabler/icons-react';
import { logOut } from "../../storage/slises/userSlice";
 import { useDispatch, useSelector } from "react-redux";


const AppHeader = () => {

    const dispatch = useDispatch();
    const token = useSelector(state => state.user.token)

    return (
        <Header pr={'xl'} pl={'xl'} height={60}>

            <Flex h={60} align={'center'} justify={'space-between'}>
                {token && <Menu shadow="md" width={200}>
                    <Menu.Target>
                        <ActionIcon>< Avatar size='lg' radius={'xl'} src={null}></Avatar></ActionIcon>
                    </Menu.Target>
                    <Menu.Dropdown>
                        <Menu.Item icon={<IconUser />} >
                            <Text>
                                Профиль
                            </Text>
                        </Menu.Item>
                        <Menu.Item icon={<IconLogout />} >
                            <Text onClick={() => dispatch(logOut())}>
                                Выйти
                            </Text>
                        </Menu.Item>
                    </Menu.Dropdown>
                </Menu>}
            </Flex>
        </Header >
    )
}

export default AppHeader