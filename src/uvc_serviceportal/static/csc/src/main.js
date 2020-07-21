import Vue from 'vue'
import LeikaFormWrapper from './components/LeikaFormWrapper'
import LandingPage from './components/LandingPage'
import CustomWrapper from './components/CustomWrapper'

Vue.config.productionTip = false
Vue.component('CustomWrapper', CustomWrapper);

new Vue({
    el: '#app',
    name: 'app',
    components: {
        LeikaFormWrapper,
        LandingPage
    }
})
