import React, {Component, PureComponent, Fragment} from 'react';
import {Card, Icon, Layout, List, Page, Stack, Subheading} from '@shopify/polaris';
import {CashDollarMajorMonotone} from '@shopify/polaris-icons';

export default function BillingApp() {
    const plans = [
        {
            title: "FREE-НАВСЕГДА",
            price: "Свободно на всегда",
            options: [
                'Оптимизация изображения (до 50 изображений)',
                'Синхронизировать одну коллекцию',
                'Использование для канала Google, Facebook, Instagram, Yottos, Pinterest',
                'До 1000 продуктов',
                'Обновление раз в 48 час.'
            ]
        },
        {
            title: "GOLD ПЛАН 2 000 товаров",
            price: "$ 19/ месяц",
            options: [
                'Оптимизация изображения (до 500 изображений)',
                'Синхронизация одной или несколько коллекций',
                'Для канала Google, Facebook, Instagram, Yottos, Pinterest',
                '2 feeds с номераций, по 1 000 продуктов',
                'Обновления раз в 24 часа',
                'Utm метки'
            ]
        },
        {
            title: "PLATINUM ПЛАН 3 000 товаров",
            price: "$ 29/ месяц",
            options: [
                'Оптимизация изображения (до 1000 изображений)',
                'Синхронизация всех коллекций',
                'Для канала Google, Facebook, Instagram, Yottos, Pinterest',
                '3 feeds с номераций, по 1 000 продуктов',
                'Обновления раз в 12 часа',
                'Прокрутка изображений в нутри рекламного обьявления',
                'Отображение наличия товаров в магазине',
                'Индивидуальные названия вариаций товара',
                'Отображение скидки в обьявлении',
                'Выгрузка по рейтингу продоваемости',
                'Utm метки'
            ]
        },
        {
            title: "INFINITE ПЛАН 10 000 товаров",
            price: "$ 49/ месяц",
            options: [
                'Оптимизация изображения (до 10 000 изображений)',
                'Синхронизация всех коллекций',
                'Для канала Google, Facebook, Instagram, Yottos, Pinterest',
                '10 feeds с номераций, по 1 000 продуктов',
                'Асинхронное обновление',
                'Прокрутка изображений в нутри рекламного обьявления',
                'Отображение наличия товаров в магазине',
                'Индивидуальные названия вариаций товара',
                'Отображение скидки в обьявлении',
                'Выгрузка по рейтингу продоваемости',
                'Utm метки'
            ]
        },
    ];
    class ListOptions extends PureComponent {
      render() {
        return (
          <List>
            {this.props.items.map((item, index) => <List.Item key={index}>{item}</List.Item>)}
          </List>
        );
      }
    }
    const renderPlans = plans.map(
        (plan, index) =>
            <Layout.Section key={index}>
                <Card
                    title={plan.title}
                    primaryFooterAction={{content: 'Select'}}
                >
                    <Card.Section
                        title={
                            <Stack>
                                <Icon source={CashDollarMajorMonotone}/>
                                <Subheading>{plan.price}</Subheading>
                            </Stack>
                        }
                    >
                    <ListOptions items={plan.options || []} />
                    </Card.Section>
                </Card>
            </Layout.Section>
    );
    return (
        <Page>
            <Layout>
                {renderPlans}
            </Layout>
        </Page>
    );
}
