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
    import Cookies from 'js-cookie';
    import Pants from "@/assets/js/pants_api";
    import LayoutDefault from "@/components/pages/layouts/layout-default";

    // Configure the Pants API based on what authentication is available.
    // If django is serving this SPA, then we can use the csrftoken it provides (preferred)
    // If this SPA is being served elsewhere, then the user will need to provide their user name and password for PANTS
    // THIS REQUIRES HTTPS TO BE SECURE. If this frontend uses http to connect to the backend, then the user name and password will be transmitted in plain text as http headers.
    let pantsAuthentication = {}
    if(Cookies.get("csrftoken") === undefined){
        pantsAuthentication.method = "Basic";
        // @todo the the vue app should provide this username and password?
        pantsAuthentication.username = "";
        pantsAuthentication.password = "";
    } else {
        pantsAuthentication.method = "Token";
        pantsAuthentication.token = Cookies.get("csrftoken");
    }

    // If the API is served from the same hostname as the frontend, set this to undefined. If not, you should set this value
    // to the hostname the API will be served at e.g. "https://localhost:8000"
    // const API_HOSTNAME = undefined;
    const API_HOSTNAME = "http://localhost:8000";

    let pants = new Pants('1', pantsAuthentication, API_HOSTNAME);

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
