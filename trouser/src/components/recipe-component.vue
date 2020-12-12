<template>
    <div :class="{[$options.name]: true}">
        <button
                type="button"
                @click="note===null?note='':note=null"
                class="text-only"
        >
            <fa-icon :icon="['fas', 'sticky-note']" size="2x"></fa-icon>
        </button>
        <label id="name">A Recipe Component</label>

        <input-float
                :id="`${id}:amount`"
                label="Amount"
                :extra='{style:"min-width: 0;text-align: right"}'
        ></input-float>
        <input-float
                :id="`${id}:unit`"
                type="select"
                label="Unit"
        >
            <option value="weight">grams</option>
            <option value="servings">servings</option>
        </input-float>
        <button
                type="button"
                @click="this.parentElement.remove()"
                class="text-only"
        >
            <fa-icon :icon="['fas', 'minus']" size="2x"></fa-icon>
        </button>

        <input-float
                :id="`${id}:note`"
                class="note"
                label='Note'
                hint="Information about this specific ingredient in this specific recipe"
                :multiline="true"
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
        props: {
            name: String,
            note: String,
            unit: String, // one of 'servings' or 'weight'
            amount: String,
            type: String,
            recipe_or_ingredient_id: Number,
            id: Number,
        },
        data() {
            return {
            }
        },
        computed: {
            hasNote() {
                return this.note !== null;
            }
        }
    }
</script>

<style>
    .recipe-component {
        display: contents;
    }
</style>