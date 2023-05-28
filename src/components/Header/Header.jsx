import { Header, Flex, Avatar, Menu, Text, ActionIcon, Button } from "@mantine/core"
import { IconLogout, IconUser } from '@tabler/icons-react';
import { logOut } from '../../storage/slises/userSlice';
 import { useDispatch, useSelector } from "react-redux";


const AppHeader = () => {

    const dispatch = useDispatch();
    const token = useSelector(state => state.user.token)

    return (
        <Header pr={'xl'} pl={'xl'} height={60}>

            <Flex h={60} align={'center'} justify={'end'}>
                {token && <Button onClick={()=>dispatch(logOut())} >Выйти</Button>}
            </Flex>
        </Header >
    )
}

export default AppHeader