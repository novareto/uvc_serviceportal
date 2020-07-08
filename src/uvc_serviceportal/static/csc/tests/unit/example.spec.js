import { shallowMount } from '@vue/test-utils'
import LeikaFormWrapper from '@/components/LeikaFormWrapper.vue'

describe('LeikaFormWrapper.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(LeikaFormWrapper, {
      propsData: { msg }
    })
    expect(wrapper.text()).toMatch(msg)
  })
})
