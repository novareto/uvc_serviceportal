<template>
    <div>
      <form action="" @submit.prevent="submit">
        <JsonSchema v-model="model"
                    :schema="schema"
                    @validated="errors = event"
                    :wrapper="wrapper" />
      <input type="submit" class="btn btn-primary" @click.prevent="submit" />
      </form>
    </div>
</template>

<script>
import JsonSchema from '@roma219/vue-jsonschema-form'
import axios from 'axios'


export default {
    props: {
        schema: {
            type: Object
        },
    },
    data() {
        return {
            model: {},
            wrapper: {
                componentName: 'CustomWrapper',
                props: (propName, schema) => ({
                    title: schema.title || propName,
                    description: schema.description
                })
            }
        }
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
    components: { JsonSchema }
}
</script>

<style lang="scss" scoped>

</style>
