import { useToggle, upperFirst } from '@mantine/hooks';
import { useForm } from '@mantine/form';
import {
    TextInput,
    PasswordInput,
    Paper,
    Group,
    Button,
    Anchor,
    Stack,
    Center
} from '@mantine/core';

import { logIn } from "../../storage/slises/userSlice";

import { useDispatch } from 'react-redux';

export default function AuthenticationForm() {

    const dispatch = useDispatch();

    const [type, toggle] = useToggle(['Войти', 'зарегистрироваться']);
    const form = useForm({
        initialValues: {
            username: '',
            password: '',
            first_name: '',
            last_name: '',
            patronymic: '',
            token: null
        },
        validate: {

            password: (val) => (val.length <= 6 ? 'Password should include at least 6 characters' : null),
        },
    });
    const emailForm = useForm({
        initialValues: {
            email: '',
        },
        validate: {
            email: (val) => (/^\S+@\S+$/.test(val) ? null : 'Invalid email'),
        }
    })

    const formOnSubmit = (e) => {
        e.preventDefault();
        dispatch(logIn())

    }
    return (
        <Center h={'100%'}>
            <Paper radius="md" p="xl" shadow="xl" withBorder >

                <form onSubmit={(e) => formOnSubmit(e)}>
                    <Stack>

                        <TextInput
                            label="Имя пользователя"
                            required
                            placeholder="Введите имя пользователя"
                            value={form.values.username}
                            onChange={(event) => form.setFieldValue('username', event.currentTarget.value)}
                            radius="md"
                        />
                        {type === 'зарегистрироваться' && <TextInput
                            required={type === 'зарегистрироваться' ? true : false}
                            label="Email"
                            placeholder="hello@kor-teh.ru"
                            value={emailForm.values.email}
                            onChange={(event) => emailForm.setFieldValue('email', event.currentTarget.value)}
                            error={form.errors.email && 'Invalid email'}
                            radius="md"
                        />}

                        <PasswordInput
                            required
                            label="Password"
                            placeholder="Введите пароль"
                            value={form.values.password}
                            onChange={(event) => form.setFieldValue('password', event.currentTarget.value)}
                            error={form.errors.password && 'Password should include at least 6 characters'}
                            radius="md"
                        />
                    </Stack>

                    <Group position="apart" mt="xl">
                        <Anchor
                            component="button"
                            type="button"
                            color="dimmed"
                            onClick={() => toggle()}
                            size="xs"
                        >
                            {type === 'зарегистрироваться'
                                ? 'Есть аккаунт? Войдите'
                                : "Еще нет аккаунта? Зарегистрируйтесь"}
                        </Anchor>
                        <Button variant={'light'} type="submit" fz={'xs'} radius='md'>
                            {upperFirst(type)}

                        </Button>
                    </Group>
                </form>
            </Paper>
        </Center>
    );
}

