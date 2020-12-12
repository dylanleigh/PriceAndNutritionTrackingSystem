<template>
    <div class="flex-row-equalfill">
        <button
                class="dark"
                @click.prevent="onClick(rowData)"
        >
            <fa-icon :icon="['fas', icon]"></fa-icon>
        </button>
    </div>
</template>

<script>
    import Vue from 'vue';

    export default Vue.extend({
        data(){
            return{
                icon: null,
                onClick: null,
                rowData: null,
            }
        },
        beforeMount(){
            this.rowData = this.params.data;
            this.onClick = this.params.onClick;
            this.icon = this.params.icon;
        }
    })
</script>

<style scoped>
    button{
        padding: 0;margin: 0
    }
    div{
        align-items:stretch;height:100%
    }
</style>