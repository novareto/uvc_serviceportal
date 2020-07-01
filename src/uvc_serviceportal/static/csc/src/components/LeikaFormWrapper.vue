<template>
    <div>
       <h1> I am the Best Fuck the REST </h1>
       {{JSON.parse( this.schema)}}
    </div>
</template>

<script>
    export default {
        props: {
            schema: {
                type: String 
            },
        },
    }
</script>

<style lang="scss" scoped>

</style>