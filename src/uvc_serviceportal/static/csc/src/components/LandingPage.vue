<template>
  <div>
    <div class="row">
      <div class="col-md-12">
        <div class="form-group">
          <label for="search_leika">Service Suchen</label>
          <input v-model="filter.text" type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" >
        </div>
      </div>
      <pre> {{filter}} </pre>
    </div>
    <div class="row">
      <div class="col-md-9">
        <div v-for="leika in leikas" :key="leika.id" >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{leika.id}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{leika.title}}</h6>
              <p class="card-text">{{leika.description}}</p>
              <a :href="'leikas/' + leika.id" class="btn btn-primary card-link" >
                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-plus" fill="currentColor" xmlns="http://www.w3.org/2000/svg" >
                  <path fill-rule="evenodd" d="M8 3.5a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5H4a.5.5 0 0 1 0-1h3.5V4a.5.5 0 0 1 .5-.5z" />
                  <path fill-rule="evenodd" d="M7.5 8a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1H8.5V12a.5.5 0 0 1-1 0V8z" />
                </svg>
                Anlegen
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
          PORTLET   
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    leikas: {
      type: Array
    }
  },
  data() {
    return {
      filter: {
        text: ""
      }
    };
  }
};
</script>

<style lang="scss" scoped>
</style>