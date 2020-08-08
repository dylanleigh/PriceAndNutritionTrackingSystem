customElements.define('float-input',
    class extends HTMLElement {
        connectedCallback() {
            let field;

            if (this.type === 'text' && this.multiline) {
                field = `<textarea class="field__input" name="${this.id}" type="${this.type}"
                          placeholder="${this.label}" ${this.extra}></textarea>`;
            } else if (this.type === 'select') {
                field = `<select class="field__input" name="${this.id}" ${this.extra}>
                    <option value="">${this.label}</option>
                    ${this.innerHTML}
                </select>`;
            } else {
                // A regular input, with the field determined by the type attribute
                field = `<input class="field__input" name="${this.id}" type="${this.type}"
                       placeholder="${this.label}" ${this.extra}>`;
            }
        
            const template = `
                <div class="field" ${this.container_extra}>
                    ${field}
                    <label class="field__label" for="${this.id}">${this.label}</label>
                </div>
            `;
            this.innerHTML = template;

            // Setup events and callbacks
            if(this.input_mask_name){
                window.addEventListener('load', ()=>{
                    let elem = this.querySelector(`[name="${this.id}"]`);
                    if(typeof elem.pants_data === "undefined"){
                        elem.pants_data = {};
                    }
                    this.input_mask = IMask(elem, this.named_masks[this.input_mask_name]);
                })
            }

            if(this.type === "select"){
                // Select elements need to know what the current option is in order to style "nothing chosen"
                this.querySelector(`[name="${this.id}"]`).dataset.picked_option = "";
                this.querySelector(`[name="${this.id}"]`).addEventListener('change', function(){
                    // 'this' is the select element
                    this.dataset.picked_option = this.value;
                })
            }
        }

        /* Input Mask */
        named_masks = {
            // Mask that ensures only 6 total digits, max 3 decimals
            'nutrition_mask': {mask: /^(?=^[\d.]{0,7}$)\d{0,6}(\.\d{0,3})?$/},
            // Mask that ensures only lowercase letters, numbers and dashes
            "slug_mask": {mask: /^[0-9a-z-]*$/},
            // Ensures only lowercase letters, numbers, dashes, and commas
            "tag_mask": {mask: /^[0-9a-z,-]*$/}
        }
        // The actual input mask created by IMask
        input_mask = undefined;

        /* Attributes */

        // Determines what name the input should have
        get name() {
            return this.getAttribute("name") || "";
        }

        set name(value) {
            return this.setAttribute("name", value)
        }

        // What type of input to create
        get type() {
            return this.getAttribute("type") || "text";
        }

        set type(value) {
            return this.setAttribute("type", value)
        }

        // If we expect multiline input
        get multiline() {
            return this.hasAttribute("multiline");
        }

        set multiline(value) {
            return this.setAttribute("multiline", value)
        }

        // What the floating label should say
        get label() {
            return this.getAttribute("label")
        }

        set label(value) {
            return this.setAttribute("label", value)
        }

        // An extra string to place in the attributes of the template input element
        get extra() {
            return this.getAttribute("extra") || "";
        }

        set extra(value) {
            return this.setAttribute("extra", value)
        }

        // An extra string to place in the attributes of the template wrapper element
        get container_extra() {
            return this.getAttribute("container_extra") || "";
        }

        set container_extra(value) {
            return this.setAttribute("container_extra", value)
        }

        // input mask is for js input masking options with IMask library.
        // Should be the name of a named mask in this element
        // TODO make it so that you can specify your own mask?
        get input_mask_name() {
            return this.getAttribute("input_mask_name");
        }

        set input_mask_name(value) {
            return this.setAttribute("input_mask_name", value)
        }

        // TODO hint
        // hint is a paragraph explaining what could be put in, or limitations to inputs. Possibly should be made visible on focus

        /* Replacements for Input properties */
        get value(){
            return this.querySelector(`[name="${this.id}"]`).value;
        }
        set value(value){
            this.querySelector(`[name="${this.id}"]`).value = value;
            // If this has an input mask, the mask's internal value will need to be synchronized.
            if(this.input_mask){
                this.input_mask.updateValue();
            }
        }

        get id(){
            return this.getAttribute("id");
        }
        set id(value){
            return this.setAttribute("id");
        }


    }
);