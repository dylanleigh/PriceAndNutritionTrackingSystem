<template>
    <div class="field" v-bind="container_extra">
        <textarea
                v-if="type==='text' && multiline"
                class="field__input"
                :name="id"
                :id="id"
                :type="type"
                :placeholder="label"
                v-bind="extra"
                v-model="content"
                @keyup="$emit('keyup')"
                @input="handleInput"
                ref="input"></textarea>
        <!--        For the select, we publish the selected option as the data-picked_option attribute to aid in styling -->
        <select
                v-else-if="type==='select'"
                class="field__input"
                :name="id"
                :id="id"
                v-bind="extra"
                v-model="content"
                :data-picked_option="content"
                @change="handleInput">
            <option value="" :hidden="hideDefaultOption">{{label}}</option>
            <slot></slot>
        </select>
        <input
                v-else
                class="field__input"
                :name="id"
                :id="id"
                :type="type"
                :placeholder="label"
                v-bind="extra"
                v-model="content"
                @keyup="$emit('keyup')"
                @input="handleInput"
                ref="input">
        <label class="field__label" :for="id">{{label}}</label>
    </div>
</template>

<script>
    import IMask from 'imask'
    export default {
        name: "input-float",
        props: {
            // Unique identifier for this input
            id: {
                type: String,
                required: true
            },
            // Determines what name the input should have
            name: {
                type: String,
                default: ''
            },
            // What type of input to create
            type: {
                type: String,
                default: 'text'
            },
            // If we expect multiline input
            multiline: {
                type: Boolean,
                default: false
            },
            // What the floating label should say
            label: {
                type: String,
                default: ''
            },
            // Object of additional attributes that should go on this input
            extra: Object,
            // Object of additional attributes that should go on the container for this input
            container_extra: Object,
            // input mask is for js input masking options with IMask library.
            // Should be the name of a named mask in this element
            // TODO make it so that you can specify your own mask?
            input_mask_name: String,

            // @todo hint support
            // hint is a paragraph explaining what could be put in, or limitations to inputs. Possibly should be made visible on focus
            hint: {
                type: String,
                default: ''
            },

            // Determines what value the input should currently hold
            value: {},
            /* @todo value getter setter

            get value(){
                return this.querySelector(`[name="${this.id}"]`).value;
            }
            set value(value){
                this.querySelector(`[name="${this.id}"]`).value = value;
                // If this has an input mask, the mask's internal value will need to be synchronized.
                if(this.input_mask){
                    this.input_mask.updateValue();
                }

                if(this.type === "select"){
                    // Need to trigger a change so that the data-picked_option updates
                    let evt = document.createEvent("HTMLEvents");
                    evt.initEvent("change", false, true);
                    this.querySelector(`[name="${this.id}"]`).dispatchEvent(evt);
                }
            }
             */

            /* Determines if the default option for select inputs should be hidden so that it cannot be picked manually*/
            hideDefaultOption: {
                type: Boolean,
                default: false
            }
        },
        data: function () {
            return {
                /* Input Mask */
                named_masks: {
                    // Mask that ensures only 6 total digits, max 3 decimals
                    'nutrition_mask': {mask: /^(?=^[\d.]{0,7}$)\d{0,6}(\.\d{0,3})?$/},
                    // Mask that ensures only lowercase letters, numbers and dashes
                    "slug_mask": {mask: /^[0-9a-z-]*$/},
                    // Ensures only lowercase letters, numbers, dashes, and commas
                    "tag_mask": {mask: /^[0-9a-z,-]*$/}
                },
                // The actual input mask created by IMask
                input_mask: undefined,
                // The actual contents of the input
                content: ""
            }
        },
        mounted(){
            if(this.input_mask_name){
                this.input_mask = IMask(this.$refs.input, this.named_masks[this.input_mask_name]);
            }
        },
        watch: {
            value(newVal) {
                if(this.input_mask){
                    this.input_mask.unmaskedValue = newVal;
                }
                else{
                    this.content = newVal;
                }
            }
        },
        methods: {
            /**
             * Add an option if the input type is a select
             * @param value {string} the value of the new option
             * @param text {string} the text of the new option
             */
            addOption(value, text) {
                if (this.type === 'select') {
                    let new_option = document.createElement('option');
                    new_option.value = value;
                    new_option.innerText = text;
                    this.querySelector(`[name="${this.id}"]`).appendChild(new_option)
                }
            },
            /**
             * Emits the input event with appropriate data when the value of the input field changes
             */
            handleInput() {
                this.$emit('input', this.input_mask ? this.input_mask.masked : this.content)
            }
        }
    }
</script>

<style scoped lang="scss">
    .field {
        position: relative;

        /*
        for inputs and text areas, we know it's empty when the placeholder is shown
        for selects, it's when the specially crafted data tag is empty

        In this case we make the label disappear and lower, so that it 'floats up and in' when needed
        */
        > .field__input:placeholder-shown + .field__label,
        > select.field__input[data-picked_option=""] + .field__label {
            opacity: 0;
            transform: translateY(1px);
        }


        > .field__label {
            color: #919293;
            display: block;
            box-sizing: border-box;
            font-size: .8em;
            line-height: 1;
            opacity: 1;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            padding: .5em 0.6rem;
            pointer-events: none;
            position: absolute;
            top: 0;
            text-align: left;
            transform: none;
            transition: all .2s ease-out;
            user-select: none;
            width: 100%;
            z-index: 1;
        }

        > .field__input {
            --label-spacing: 1.1em;
            background: white;
            box-sizing: border-box;
            border: 1px solid var(--gunmetal);
            padding: var(--label-spacing) .5em 0;
            transition: all .1s ease-out;
            width: 100%;
            resize: vertical;
            font-family: var(--font-family-content);
            border-radius: var(--border-radius);

            &::placeholder {
                font-family: var(--font-family-content);
            }

            &:hover, &:focus {
                border-color: var(--shamrock-green);
            }

            &:placeholder-shown {
                /* Padding when detected empty */
                padding: calc(var(--label-spacing) / 2) .5em calc(var(--label-spacing) / 2);
            }
        }

        /* For some reason select elements are 2 px wider than inputs, normalize by going 50/50 */
        > select.field__input {
            padding: calc(var(--label-spacing) - 2px) .5em 0;

            &[data-picked_option=""] {
                padding: calc(var(--label-spacing) / 2 - 1px) .5em calc(var(--label-spacing) / 2 - 1px);
                /* Any option with a value of "" will be considered unpicked, and thus should look like the placeholder */
                color: grey;
            }
        }

        > textarea.field__input {
            height: 4.875em;
        }
    }


</style>