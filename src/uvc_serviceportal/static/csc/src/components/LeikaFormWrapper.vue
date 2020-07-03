<template>
    <div>
      <h1> I am the Best Fuck the REST </h1>
      <JsonSchema :schema="schema" v-model="model"/>
    </div>
</template>

<script>
import JsonSchema from '@roma219/vue-jsonschema-form'

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
    components: { JsonSchema }
}
</script>

<style lang="scss" scoped>

</style>
