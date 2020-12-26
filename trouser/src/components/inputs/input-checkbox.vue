<template>
    <div :class="{[$options.name]: true, checked: internalValue}">
        <input :id="id" type="checkbox" v-model="internalValue">
        <label :for="id">
            <div class="fake-checkbox"><fa-icon :icon="['fas', 'check']" v-show="internalValue"></fa-icon></div>
            {{label}}
        </label>
    </div>
</template>

<script>
    export default {
        name: "input-checkbox",
        props:{
            // Unique id for this checkbox
            id: String,
            // The actual value for the checkbox
            value: Boolean,
            // The label for the checkbox
            label: String
        },
        data() {
            return {
            }
        },
        computed:{
            // Handles getting and setting value, which is controlled by a v-model
            internalValue:{
                get(){
                    return this.value;
                },
                set(newValue){
                    this.$emit('input', newValue)
                }
            }
        }
    }
</script>

<style scoped lang="scss">
    .input-checkbox{
        input{
            // Hide the real checkbox, it is hard to style, so we only use it to store the value
            display: none;
        }

        label{
            --label-spacing: calc(1.1em - 2px); // the -2px makes this the same as for other float inputs
            background: white;
            box-sizing: border-box;
            border: 1px solid var(--gunmetal);
            padding: calc(var(--label-spacing) / 2) 0.5em calc(var(--label-spacing) / 2);
            width: 100%;
            font-family: var(--font-family-content);
            border-radius: var(--border-radius);

            color: grey;
            line-height: 1;
            opacity: 1;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            top: 0;
            text-align: left;
            transform: none;
            transition: all .2s ease-out;
            -webkit-user-select: none;
            -moz-user-select: none;
            user-select: none;

            display: flex;
            align-items: center;
        }

        // What we use to show the current value as if it was a real checkbox
        .fake-checkbox{
            width: 1em;
            height: 1em;
            border: 1px solid var(--gunmetal);
            border-radius: var(--border-radius);
            padding: 0.1em;
            background: white;
            margin-right: 0.5em;
        }

        // Used to determine how this checkbox should look when checked
        &.checked{
            label{
                box-shadow: inset 0 0 5px 0 rgba(58, 165, 0, 0.75);
            }
        }
    }
</style>