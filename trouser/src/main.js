import Vue from 'vue'

// Prepare reset of styles
import './assets/css/reset.css'

import App from './App.vue'


// Prepare Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faHome,
faCarrot,
faHamburger,
faBook,
faBullseye,
faUser } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(
    faHome,
    faCarrot,
    faHamburger,
    faBook,
    faBullseye,
    faUser)
Vue.component('fa-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
