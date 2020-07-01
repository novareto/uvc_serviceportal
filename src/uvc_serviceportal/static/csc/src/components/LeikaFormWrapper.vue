<template>
  <div>
    <h1> I am the Best Fuck the REST </h1>
    <vue-form-json-schema
      v-model="model"
      :schema="schema"
      :ui-schema="uiSchema"
      v-on:state-change="onChangeState"
      v-on:validated="onValidated"
    ></vue-form-json-schema>
  </div>
</template>

<script>
import VueFormJsonSchema from "vue-form-json-schema/dist/vue-form-json-schema.esm.js";
export default {
  components: {
    "vue-form-json-schema": VueFormJsonSchema
  },
  props: {
    schema_1: {
      type: String
    }
  },
  data() {
    return {
        model: {},
              uiSchema: [
        {
          component: "input",
          model: "firstName",
          fieldOptions: {
            class: ["form-control"],
            on: ["input"],
            attrs: {
              placeholder: "Please enter your first name"
            }
          }
        }
      ],
      schema: {
        type: "object",
        properties: {
          firstName: {
            type: "string"
          }
        }
      }
    };
  },
    methods: {
    onChangeState(value) {
      this.state = value;
    },
    onValidated(value) {
      this.valid = value;
    }
  }
};
</script>

<style lang="scss" scoped>
</style>