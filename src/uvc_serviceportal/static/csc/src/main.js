import Vue from 'vue'
import LeikaFormWrapper from './components/LeikaFormWrapper'

Vue.config.productionTip = false

new Vue({
  el: '#form',
  name: 'app',
  components: { LeikaFormWrapper }
})

