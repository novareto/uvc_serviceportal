<template>
  <div>
    <div class="row">
      <div class="col-md-12">
        <div class="form-group">
          <label for="search_leika">Service Suchen</label>
          <input
            v-model="filter.text"
            type="text"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
          >
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-9">
          <transition-group name="flip-list" tag="div">
        <div
          class="mt-2 shadow"
          v-for="leika in filterLeikas"
          :key="leika.id"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{leika.title}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{leika.description}}</h6>
              <!--<p class="card-text">{{leika.description}}</p>-->
              <p class="card-text"><small class="text-muted">{{leika.tags.join(' - ')}}</small></p>
              <p class="card-text"><small class="text-muted">{{leika.security_level}}</small></p>
              <a
                :href="'whowhat/' + leika.id"
                class="btn btn-primary card-link"
              >
                <svg
                  width="1em"
                  height="1em"
                  viewBox="0 0 16 16"
                  class="bi bi-plus"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8 3.5a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5H4a.5.5 0 0 1 0-1h3.5V4a.5.5 0 0 1 .5-.5z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M7.5 8a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1H8.5V12a.5.5 0 0 1-1 0V8z"
                  />
                </svg>
                Weiter
              </a>
            </div>
          </div>
        </div>
    </transition-group>
      </div>
      <div class="col-md-3">
        <div class="categories">
          <div class="form-check">
            <input v-model="filter.cat" class="form-check-input" type="checkbox" value="Unfallanzeige" id="defaultCheck1" >
            <label class="form-check-label" for="defaultCheck1" >
              Unfallanzeige 
            </label>
          </div>
          <div class="form-check">
            <input  v-model="filter.cat" class="form-check-input" type="checkbox" value="Sicherheitsfachkraft" id="defaultCheck1" >
            <label class="form-check-label" for="defaultCheck1" >
              Sicherheitsfachkraft
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" id="defaultCheck1" >
            <label class="form-check-label" for="defaultCheck1" >
              Default checkbox
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>


function containsAny(source, target)
{
  var result = source.filter(function(item){ return target.indexOf(item) > -1});
    return (result.length > 0);
}


export default {
  props: {
    leikas: {
      type: Array
    }
  },
  computed: {
    filterLeikas() {
      var leikas = this.leikas;
      if (this.filter.text != "") {
        leikas = this.leikas.filter(
          leika =>
            leika.title.toLowerCase().indexOf(this.filter.text.toLowerCase()) >=
              0 ||
            leika.description
              .toLowerCase()
              .indexOf(this.filter.text.toLowerCase()) >= 0
        );
      }
      if (this.filter.cat.length > 0){
           leikas = leikas.filter(leika => containsAny(this.filter.cat, leika.tags));
      }
      return leikas;
    }
  },
  data() {
    return {
      filter: {
        text: "",
        cat: []
      }
    };
  }
};
</script>

<style lang="css" scoped>
.flip-list-move {
  transition: transform 1s;
}
</style>