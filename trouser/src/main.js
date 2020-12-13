import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// Prepare reset of styles
import './assets/css/reset.css'

import App from './App.vue'


// Prepare Font Awesome
import {library} from '@fortawesome/fontawesome-svg-core'
import {
    faHome,
    faCarrot,
    faHamburger,
    faBook,
    faBullseye,
    faUser,
    faStickyNote,
    faMinus
} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add(
    faHome,
    faCarrot,
    faHamburger,
    faBook,
    faBullseye,
    faUser,
    faStickyNote,
    faMinus)
Vue.component('fa-icon', FontAwesomeIcon)

Vue.config.productionTip = false

// Import router components
import IngredientManager from './components/pages/ingredient-manager'
import RecipeManager from './components/pages/recipe-manager'
import Diary from './components/pages/diary'

new Vue({
    render: h => h(App),
    router: new VueRouter({
        routes: [
            {path: '/ingredient_manager', component: IngredientManager},
            {path: '/recipe_manager', component: RecipeManager},
            {path: '/diary', component: Diary},
        ]
    })
}).$mount('#app')
