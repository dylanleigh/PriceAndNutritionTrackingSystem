<template>
    <div id="app">
        <layout-default :menu_items="menu_items">
            <template slot="content">
                <router-view></router-view>
            </template>
        </layout-default>
    </div>
</template>

<script>
    //import Cookies from 'js-cookie';
    import Pants from "@/assets/js/pants_api";
    import LayoutDefault from "@/components/pages/layouts/layout-default";


    let pants = new Pants('1', {
            method: "Basic",
            username: 'admin',
            password: 'admin',
            // token: Cookies.get("csrftoken")
        },
        'localhost:8000');

    export default {
        name: 'App',
        components: {
            LayoutDefault
        },
        provide: {
            pants: pants
        },
        data() {
            return {
                menu_items: {
                        home: {
                            url: '/',
                            icon: 'home'
                        },
                        ingredient_manager: {
                            url: '/ingredient_manager',
                            icon: 'carrot'
                        },
                        recipe_manager: {
                            url: '/recipe_manager',
                            icon: 'hamburger'
                        },
                        diary: {
                            url: '/diary',
                            icon: 'book'
                        },
                        target_manager: {
                            url: '/target_manager',
                            icon: 'bullseye'
                        },
                        login: {
                            url: '/login',
                            icon: 'user'
                        },
                    }
            }
        }
    }
</script>

<style>
</style>
