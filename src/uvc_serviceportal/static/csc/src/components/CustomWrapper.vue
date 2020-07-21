<template>
  <div class="form-group" @errors="getError">
    <label class="title">{{ title }}</label>
    <slot/>
    <small id="emailHelp" class="form-text text-muted">{{description}}</small>
    {{error}}
  </div>
</template>

<script>
export default {
  name: 'CustomWrapper',
  props: {
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    error: {
      type: String,
      default: ''
    }
  },
  methods: {
    getError() {
      
    }
  },
}
</script>

<style>
input[type="text"] {
    display: block;
    width: 100%;
    height: calc(1.5em + .75rem + 2px);
    padding: .375rem .75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid #ced4da;
    border-radius: .25rem;
    transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
}
</style>