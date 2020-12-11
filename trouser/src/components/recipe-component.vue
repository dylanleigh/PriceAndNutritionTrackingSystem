<template>
    <div :class="{[$options.name]: true}">
        <button type="button" @click="note===null?note='':note=null" class="text-only">
            <fa-icon :icon="['fas', 'sticky-note']"></fa-icon>
            <i class="fas fa-sticky-note fa-2x"></i>
        </button>
        <label id="name">A Recipe Component</label>

        <input-float
                id="amount"
                label="Amount"
                :extra='{style:"min-width: 0;text-align: right"}'
        ></input-float>
        <input-float
                id="unit"
                type="select"
                label="Unit">
            <option value="weight">grams</option>
            <option value="servings">servings</option>
        </input-float>
        <button type="button" onclick="this.parentElement.remove()" class="text-only">
            <i class="fas fa-minus fa-2x"></i>
        </button>

        <input-float
                id='note'
                label='Note'
                hint="Information about this specific ingredient in this specific recipe"
                multiline="true"
                v-show="hasNote"
                :extra='{class:{"resizable-vertical":true}}'
        ></input-float>
    </div>
</template>

<script>
    import InputFloat from "@/components/inputs/input-float";
    export default {
        name: "recipe-component",
        components: {InputFloat},
        props:{
            name: String,
            note: String,
            unit: String, // one of 'servings' or 'weight'
            amount: String,
            type: String,
            recipe_or_ingredient_id: String,
            id: String,
        },
        data(){
            return {
                type: null,
                id: null,
                "recipe-or-ingredient-id": null,
                note: null
            }
        },
        computed:{
            hasNote(){
                return this.note !== null;
            }
        }
    }
</script>

<style scoped>
    /* has-note on the component-wrapper class indicates note should show. It's absence means the opposite */
    /*.recipe-component:not(.has-note) > #note {*/
    /*    display: none;*/
    /*}*/
    .recipe-component{
        display: contents;
    }
    #note{
        grid-column: note-start / note-end
    }

</style>