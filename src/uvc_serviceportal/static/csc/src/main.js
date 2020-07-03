import Vue from 'vue'
import LeikaFormWrapper from './components/LeikaFormWrapper'
//import VueFormJsonSchema from 'vue-form-json-schema';
Vue.config.productionTip = false

new Vue({
  el: '#form',
  name: 'app',
  components: { LeikaFormWrapper }
})

