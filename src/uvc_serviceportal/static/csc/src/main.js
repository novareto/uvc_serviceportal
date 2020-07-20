import Vue from 'vue'
import LeikaFormWrapper from './components/LeikaFormWrapper'
import LandingPage from './components/LandingPage'
import CustomWrapper from './components/CustomWrapper'

//import VueFormJsonSchema from 'vue-form-json-schema';
Vue.config.productionTip = false

new Vue({
  el: '#app',
  name: 'app',
  components: { LeikaFormWrapper, LandingPage, 'custom-wrapper': CustomWrapper }
})

