<template>
    <div>
      <form action="" @submit.prevent="submit">
      <JsonSchema :schema="schema" v-model="model" :wrapper="customWrapper" />
      <input type="submit" class="btn btn-primary" @click.prevent="submit">
      </form>
    <custom-wrapper> </custom-wrapper>
    </div>
</template>

<script>
import JsonSchema from '@roma219/vue-jsonschema-form'
import axios from 'axios'
import CustomWrapper from './CustomWrapper'

export default {
    props: {
        schema: {
            type: Object
        },
    },
    data() {
        return {
            model: {},
        }
    },
    computed: {
      customWrapper() {
          console.log('I AM IN ')
      return {
        componentName: 'CustomWrapper',
        props: (propName, schema) => ({
          title: schema.title || propName
        })
      }
    },
    },
    methods: {
        submit() {
            var formData = new FormData()
            for ( var key in this.model ) {
                formData.append(key, this.model[key]);
            }
            axios.post('/leikas/leika1/add', formData).then((response) => {
                     console.log(response)
                        // success callback
                    }, (response) => {
                        console.log(response)
                        // error callback
                    });
        }
    },
    components: { JsonSchema, 'custom-wrapper': CustomWrapper }
}
</script>

<style lang="scss" scoped>

</style>
