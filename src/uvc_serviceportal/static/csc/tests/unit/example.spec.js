import { mount } from '@vue/test-utils'
import LeikaFormWrapper from '@/components/LeikaFormWrapper.vue'

    /*
describe('LeikaFormWrapper.vue', () => {
  it('renders props.msg when passed', () => {
    const wrapper = mount(LeikaFormWrapper, {
      propsData: { schema }
    })
    console.log('HANS MEIER')
    expect(wrapper.text()).toMatch('msg')
  })
})
*/

test('mount a view component', () => {
      const schema = {
          "type": "object",
          "properties": {
              "firstName": {
                  "type": "string"
              }
          }
      }
    const wrapper = mount(LeikaFormWrapper, {
      propsData: { schema: schema }
    })
    expect(wrapper.html()).toMatchSnapshot()

})
