<template>
    <div :class="$options.name">
        <form id="diary_entry_form" class="flex-row-start">
        <span>
            <button
                    id="time-text"
                    class="text-only"
                    type="button"
                    onclick="change_time()"
            >{{staticVals.text.changeTimeBtn[timeSpecificity]}}</button>
            <div class="float_input-group" v-show="timeSpecificity!==staticVals.timeSpecificity.JUST_NOW">
                <input-float
                        id="date"
                        label="Date"
                        type="date"
                        v-show="timeSpecificity!==staticVals.timeSpecificity.TODAY_AT"
                ></input-float>
                <input-float
                        id="time"
                        label="Time"
                        type="time"
                ></input-float>
            </div>
            <span>I ate</span>
        </span>

            <div class="float_input-group">
                <input-float
                        id="amount"
                        label="Amount"
                        :extra="{style:'text-align:right;max-width:6em'}"
                ></input-float>
                <input-float
                        id="unit"
                        label="Unit"
                        type="select"
                >
                    <option value="weight">Grams</option>
                    <option value="servings">Servings</option>
                </input-float>
            </div>
            <span>of</span>
            <!--        {#        <float-input id="component" label="Food" ></float-input>#}-->
            <input id="component">
            <button class="dark" type="button" onclick="create_diaryfood()">Add</button>
        </form>
        <div id="chart-container">
            <canvas id="chart"></canvas>
        </div>
    </div>
</template>

<script>
    /*
{#    TODO: Is this necessary? We don't really need time conversion between timezones if we can help it#}
    {#    script src="https://cdnjs.cloudflare.com/ajax/libs/luxon/1.24.1/luxon.min.js" integrity="sha512-IdHIbxMZbKEa2OSI0CcqlrgENti38ygeddwz6wOwjzSWygIYeJvHkvU1EFBCT1L471JM2QX36y8exP2QhgcB3A==" crossorigin="anonymous">/script>#}
    script src="https://cdnjs.cloudflare.com/ajax/libs/tagify/3.17.7/tagify.min.js"
            integrity="sha512-Kngmb6PkMXOkg76SHxpcsy2HQasqClt4KKl7jUe5IuG+Jg7l8PSjXtPNHKE+8wBIHARedIiOEqaca+hZQIzD/A=="
            crossorigin="anonymous"> /script>
    script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js">/script>
     */
    // Setup variables to access form inputs

        import InputFloat from "@/components/inputs/input-float";
    let date = document.getElementById('date');
        let time = document.getElementById('time');
        let amount = document.getElementById('amount');
        let unit = document.getElementById('unit');
        let component = document.getElementById('component');
/* @Todo translate this pre setup code

        // Setup obvious defaults, if you are coming here you probably want to record what happened right now
        let sysDate = new Date(),
            userDate = new Date(Date.UTC(sysDate.getFullYear(), sysDate.getMonth(), sysDate.getDate(), sysDate.getHours(), sysDate.getMinutes(), 0));
        date.valueAsDate = userDate;
        time.valueAsDate = userDate;
        */

        /* @todo figure out how to deal with tagify, or if I really want that.
            function suggestionItemTemplate(recipe) {
                return `
                    <div ${this.getAttributes(recipe)}
                        class='tagify__dropdown__item'
                        tabindex="0"
                        role="option">
                        <strong>${recipe.name}</strong>
                    </div>
                `
            }

            // Setup combobox for selecting/specifying ingredient/recipe/one off food
            function tagTemplate(recipe) {
                return `
                    <tag title="${recipe.url}"
                            contenteditable='false'
                            spellcheck='false'
                            tabIndex="-1"
                            class="tagify__tag"
                            ${this.getAttributes(recipe)}>
                        <x title='' class='tagify__tag__removeBtn' role='button' aria-label='remove tag'></x>
                        <div>
                            <span class='tagify__tag-text'>${recipe.name}</span>
                        </div>
                    </tag>
                `
            }

        let tagify = new Tagify(component, {
            maxTags: 1,
            whitelist: [],
            templates: {
                tag: tagTemplate,
                dropdownItem: suggestionItemTemplate,
                dropdownItemNoMatch: function (data) {
                    return `No match. Create one time entry for: ${data.value}`
                }
            },
            dropdown: {
                enabled: 0,
                searchKeys: ['name']
            }
        })

        // listen to any keystrokes which modify tagify's input
        tagify.on('input', onInput)
*/
    let tagify = {}

    const _static = {
        // Enum describing how specific the user wants to be when specifying the time of an entry
        timeSpecificity: {
            JUST_NOW: 'just-now',
            TODAY_AT: 'today-at',
            ON_DATETIME: 'on-datetime'
        },
        text:{
            changeTimeBtn:{
                'just-now': "Just now,",
                'today-at': "Today at",
                'on-datetime': "On",
            }
        }
    }

    export default {
        name: "diary",
        components: {InputFloat},
        inject: ['pants'],
        data(){
            return{
                staticVals: _static,
                timeSpecificity: _static.timeSpecificity.JUST_NOW,
                currentTarget: null
            }
        },
        mounted(){
            // Get the user's current daily target so that we can normalize all charts
        /* @todo figure out how to handle Chart, or if I really want it.
            this.pants.get_target()
                .then(resp=>this.currentTarget=resp.results)
                .then(()=>{
                    this.pants.get_diaryfood()
                    .then(()=> {
                        // Convert the response into a graphable set of categories.
                        var ctx = document.getElementById('chart').getContext('2d');
                        new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                                datasets: [{
                                    label: '# of Votes',
                                    data: [12, 19, 3, 5, 2, 3],
                                    backgroundColor: [
                                        'rgba(255, 99, 132, 0.2)',
                                        'rgba(54, 162, 235, 0.2)',
                                        'rgba(255, 206, 86, 0.2)',
                                        'rgba(75, 192, 192, 0.2)',
                                        'rgba(153, 102, 255, 0.2)',
                                        'rgba(255, 159, 64, 0.2)'
                                    ],
                                    borderColor: [
                                        'rgba(255, 99, 132, 1)',
                                        'rgba(54, 162, 235, 1)',
                                        'rgba(255, 206, 86, 1)',
                                        'rgba(75, 192, 192, 1)',
                                        'rgba(153, 102, 255, 1)',
                                        'rgba(255, 159, 64, 1)'
                                    ],
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                maintainAspectRatio: false,
                                scales: {
                                    yAxes: [{
                                        ticks: {
                                            beginAtZero: true
                                        }
                                    }]
                                }
                            },
                        });
                    })
                })
            */
        },
        methods:{
            onInput(e) {
                var value = e.detail.value;
                tagify.settings.whitelist.length = 0; // reset the whitelist

                // https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort
                // let controller; // for aborting the call, originally this was outside of the function.
                //controller && controller.abort();
                //controller = new AbortController();

                // show loading animation and hide the suggestions dropdown
                tagify.loading(true).dropdown.hide.call(tagify);

                this.pants.get_recipes({
                    startRow: 0,
                    endRow: 5,
                    searchKey: value,
                })
                    .then(RES => RES.json())
                    .then(function (response) {
                        // Give each recipe a 'value' that Tagify will use and the API will understand
                        let results = response.results.map(recipe => {
                            recipe['value'] = recipe['url'];
                            return recipe
                        })
                        // update whitelist Array in-place
                        tagify.settings.whitelist.splice(0, results.length, ...results)
                        tagify.loading(false).dropdown.show.call(tagify, value); // render the suggestions dropdown
                    })
            },
            create_diaryfood(){
                let component_data = JSON.parse(component.value)[0];
                this.pants.create_diaryfood({
                    'start_time':(new Date(date.value + "T" + time.value)).toISOString(),
                    // Set 'servings' or 'weight'
                    [unit.value]:amount.value,
                    // Set 'of_ingredient' or 'of_recipe' or 'name' depending on what has been entered
                    [component_data.url === undefined
                        ? 'name'
                        : (component_data.url.split("/").slice(-3)[0] === 'recipe'
                            ? 'of_recipe'
                            : 'of_ingredient')
                        ]: component_data.url === undefined ? component_data.name : component_data.url,
                })
            },
            // Setup progressively being able to specify more specifically when you ate the food
            change_time() {
                if(this.timeSpecificity === _static.timeSpecificity.JUST_NOW){
                    this.timeSpecificity = _static.timeSpecificity.TODAY_AT;
                } else if (this.timeSpecificity === _static.timeSpecificity.TODAY_AT){
                    this.timeSpecificity = _static.timeSpecificity.ON_DATETIME;
                }
            },
        }
    }
</script>

<style scoped lang="scss">
    /* @todo how to deal with this linked css?
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tagify/3.17.7/tagify.min.css"
          integrity="sha512-hqxNYuIWMQISqScYH0xQ3i8kH4MMxhJYlp7mfYvBGJKSGyliqk7SXRK3MxBuUnSwA1XeV+S+y3ad4oF+xD6kpA=="
          crossorigin="anonymous"/>
     */
#diary_entry_form > span
        {
            margin-left: 1em;
            margin-right: 1em;
        }
    #chart-container{
        width: 100%;
        height: 8em;
        position: relative;
    }
</style>