<template>
    <div :class="$options.name">
        <form id="diary_entry_form" class="flex-row-start">
        <span>
            <button
                    id="time-text"
                    class="text-only"
                    type="button"
                    @click="changeTime"
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
            <input-float
                    id="entry-type"
                    label="Food"
                    type="select"
                    :hide-default-option="true"
                    v-model="entryType"
            >
                <option :value="staticVals.entryType.RECIPE">Recipe</option>
                <option :value="staticVals.entryType.INGREDIENT">Ingredient</option>
                <option :value="staticVals.entryType.ONE_OFF_FOOD">One-off Food</option>
            </input-float>
            <button class="dark" type="button" onclick="createDiaryFood()">Add</button>
        </form>

        <div class="nutrientTargets">
            <div
                v-for="nutrient in Object.keys(staticVals.nutrientValues)"
                :key="nutrient"
                class="dailyTargetNutrient"
        >
                <fa-icon :icon="['fas', staticVals.icons.nutrients[nutrient]]" fixedWidth/>
            <label>{{nutrient}}</label>
            <target-summary
                :value="diaryFoodNutrientTotals[nutrient] || 0"
                :target-min-value="dailyTarget.min[nutrient] || 0"
                :target-max-value="dailyTarget.max[nutrient] || 0"/>
        </div>
        </div>


        <div v-show="entryType === staticVals.entryType.RECIPE" class="food-selection">
            <ag-grid-vue
                    id="all_recipes_table"
                    class="ag-theme-balham recipe-grid"
                    :gridOptions="recipeGrid.gridOptions"
                    :frameworkComponents="recipeGrid.frameworkComponents"
                    :columnDefs="recipeGrid.columnDefs"
                    :defaultColDef="recipeGrid.defaultColDef"
                    :rowModelType="recipeGrid.rowModelType"
                    :rowSelection="recipeGrid.rowSelection"
                    :pagination="recipeGrid.pagination"
                    :paginationAutoPageSize="recipeGrid.paginationAutoPageSize"
                    :datasource="recipeGrid.datasource"
                    @row-selected="onRecipeRowSelected"
            />
        </div>
        <div v-show="entryType === staticVals.entryType.INGREDIENT" class="food-selection">
            <ag-grid-vue
                    id="ingredients"
                    class="ag-theme-balham ingredient-grid"
                    :gridOptions="componentsGrid.gridOptions"
                    :frameworkComponents="componentsGrid.frameworkComponents"
                    :columnDefs="componentsGrid.columnDefs"
                    :defaultColDef="componentsGrid.defaultColDef"
                    :rowModelType="componentsGrid.rowModelType"
                    :pagination="componentsGrid.pagination"
                    :paginationAutoPageSize="componentsGrid.paginationAutoPageSize"
                    :datasource="componentsGrid.datasource"
            />
        </div>
        <div v-show="entryType === staticVals.entryType.ONE_OFF_FOOD" class="food-selection">
            <div v-for="nutrient in Object.keys(oneOffFood)"
                 :key="nutrient"
                 class="nutrient-input"
            >
                <fa-icon :icon="['fas', staticVals.icons.nutrients[nutrient]]" fixedWidth/>
                <input-float
                        :id="nutrient"
                        :label="`${nutrient} (${staticVals.units[nutrient]})`"
                        v-model="oneOffFood[nutrient]"
                />
            </div>
        </div>
    </div>
</template>

<script>
    // Setup variables to access form inputs

    import InputFloat from "@/components/inputs/input-float";
    import ActionButtonCellRenderer from "@/components/cell-renderers/action-button";


    import {AgGridVue} from 'ag-grid-vue';

    import "ag-grid-community/dist/styles/ag-grid.css";
    import "ag-grid-community/dist/styles/ag-theme-balham.css";
    import TargetSummary from "@/components/informational/target-summary";

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

    const _static = {
        // Enum describing how specific the user wants to be when specifying the time of an entry
        timeSpecificity: {
            JUST_NOW: 'just-now',
            TODAY_AT: 'today-at',
            ON_DATETIME: 'on-datetime'
        },
        text: {
            changeTimeBtn: {
                'just-now': "Just now,",
                'today-at': "Today at",
                'on-datetime': "On",
            }
        },
        icons: {
            nutrients: {
                cost: "money-bill-alt",
                kilojoules: "bolt",
                protein: "egg",
                carbohydrate: "bread-slice",
                fat: "tint",
                saturatedfat: "tint-slash",
                fibre: "seedling",
                sodium: "stroopwafel",
                sugar: "cubes",
            }
        },
        units: {
            cost: '$',
            kilojoules: 'kcal',
            protein: 'g',
            carbohydrate: 'g',
            fat: 'g',
            saturatedfat: 'g',
            fibre: 'g',
            sodium: 'mg',
            sugar: 'g',
        },
        entryType: {
            RECIPE: "recipe",
            INGREDIENT: "ingredient",
            ONE_OFF_FOOD: "one-off-food"
        },
        // A template object showing all the nutrient keys we care about
        nutrientValues: {
            cost: null,
            kilojoules: null,
            protein: null,
            carbohydrate: null,
            fat: null,
            saturatedfat: null,
            fibre: null,
            sodium: null,
            sugar: null,
        }
    }

    export default {
        name: "diary",
        components: {TargetSummary, InputFloat, AgGridVue},
        inject: ['pants'],
        data() {
            return {
                staticVals: _static,
                timeSpecificity: _static.timeSpecificity.JUST_NOW,
                // The users current daily target, by which all nutrient amounts are compared
                currentTarget: null,
                entryType: "recipe",
                // The currently input one off food values
                // @todo this is the same nutrient set as for target
                oneOffFood: {..._static.nutrientValues},
                recipeGrid: {
                    gridOptions: {},
                    frameworkComponents: {
                        actionsCell: ActionButtonCellRenderer,
                    },
                    columnDefs: [
                        {headerName: "Name", field: "name"},
                        {headerName: "Description", field: "description"},
                        {headerName: "Serves", field: "serves"},
                        {headerName: "Notes", field: "notes"},
                        {
                            headerName: "Actions",
                            cellRenderer: "actionsCell",
                            cellRendererParams: {
                                onClick: recipe => {
                                    this.add_component(
                                        "recipe",
                                        undefined, // There is no database id since this is a newly added component
                                        recipe.url.split("/").slice(-2)[0],
                                        recipe.name,
                                        "",
                                        "servings");
                                },
                                icon: "carrot"
                            },
                            cellStyle: {"padding": "0"},
                            maxWidth: 25
                        }
                    ],
                    defaultColDef: {
                        flex: 1,
                        sortable: true,
                        resizable: true,
                    },
                    rowModelType: 'infinite',
                    rowSelection: 'single',
                    pagination: true,
                    paginationAutoPageSize: true,
                    // Set up the grid to paginate using the server side API
                    datasource: {
                        getRows: async params => {
                            // params.searchKey = document.querySelector('#recipe_filter').value;
                            let response = await this.pants.get_recipes(params);

                            if (response.ok) {
                                let data = await response.json();
                                params.successCallback(data['results'], data['count'])
                            } else {
                                params.failCallback();
                            }
                        }
                    }
                },
                componentsGrid: {
                    gridOptions: {},
                    frameworkComponents: {
                        actionsCell: ActionButtonCellRenderer,
                    },
                    columnDefs: [
                        {headerName: "Name", field: "name"},
                        {headerName: "Description", field: "description"},
                        {headerName: "Serving", field: "serving"},
                        {headerName: "Notes", field: "notes"},
                        {
                            headerName: "Actions",
                            cellRenderer: "actionsCell",
                            cellRendererParams: {
                                onClick: ingredient => {
                                    this.add_component(
                                        "ingredient",
                                        undefined, // There is no database id since this is a newly added component
                                        ingredient.url.split("/").slice(-2)[0],
                                        ingredient.name,
                                        "",
                                        "weight");
                                },
                                icon: "carrot"
                            },
                            cellStyle: {"padding": "0"},
                            maxWidth: 25
                        }
                    ],
                    defaultColDef: {
                        flex: 1,
                        sortable: true,
                        resizable: true,
                    },
                    rowModelType: 'infinite',
                    pagination: true,
                    paginationAutoPageSize: true,
                    // Set up the grid to paginate using the server side API
                    datasource: {
                        getRows: async params => {
                            //params.searchKey = document.querySelector('#ingredient_filter').value;
                            let response = await this.pants.get_ingredients(params);

                            if (response.ok) {
                                let data = await response.json();
                                params.successCallback(data.results, data.count)
                            } else {
                                params.failCallback();
                            }
                        }
                    }
                },
                dailyTarget: {
                    min: {..._static.nutrientValues},
                    max: {..._static.nutrientValues}
                },
                // All the foods eaten in the last 24 hours
                diaryFoods:[]
            }
        },
        beforeMount(){
            this.pants.Target.getDaily()
            .then(resp=> {
                let target = resp.results[0];
                for(let nutrient of Object.keys(this.staticVals.nutrientValues)){
                    this.dailyTarget.max[nutrient] = parseFloat(target.maximum[nutrient]) || 0;
                    this.dailyTarget.min[nutrient] = parseFloat(target.minimum[nutrient]) || 0;
                }
            });
            // Get all DiaryFood entries for the last 24 hours
            const yesterday = (new Date((new Date()) - 24*60*60*1000)).toISOString().replace('T', ' ');
            this.pants.DiaryFood.get_all({
                filterDict:{
                    'start_time':['gte', yesterday]
                }
            }).then(resp=>{
                this.diaryFoods = resp.results;
            })
        },
        computed:{
            /**
             * The totals for each nutrient we are tracking
             * @returns {{}}
             */
            diaryFoodNutrientTotals(){
                let totals = {...this.staticVals.nutrientValues};
                this.diaryFoods.forEach(entry=>{
                    for(let nutrient of Object.keys(totals)){
                        if(totals[nutrient] == null) totals[nutrient] = 0;
                        totals[nutrient] += parseFloat(entry[nutrient]) || 0;
                    }
                })
                return totals;
            }
        },
        methods: {
            createDiaryFood() {
                let component_data = JSON.parse(component.value)[0];
                this.pants.create_diaryfood({
                    'start_time': (new Date(date.value + "T" + time.value)).toISOString(),
                    // Set 'servings' or 'weight'
                    [unit.value]: amount.value,
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
            changeTime() {
                if (this.timeSpecificity === _static.timeSpecificity.JUST_NOW) {
                    this.timeSpecificity = _static.timeSpecificity.TODAY_AT;
                } else if (this.timeSpecificity === _static.timeSpecificity.TODAY_AT) {
                    this.timeSpecificity = _static.timeSpecificity.ON_DATETIME;
                } else {
                    this.timeSpecificity = _static.timeSpecificity.JUST_NOW;
                    // @todo reset date, time to now
                }
            },
            onRecipeRowSelected(args) {
                console.log(args);
            }
        }
    }
</script>

<style scoped lang="scss">
    /* @todo how to deal with this linked css?
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tagify/3.17.7/tagify.min.css"
          integrity="sha512-hqxNYuIWMQISqScYH0xQ3i8kH4MMxhJYlp7mfYvBGJKSGyliqk7SXRK3MxBuUnSwA1XeV+S+y3ad4oF+xD6kpA=="
          crossorigin="anonymous"/>
     */
    #diary_entry_form > span {
        margin-left: 1em;
        margin-right: 1em;
    }

    #chart-container {
        width: 100%;
        height: 8em;
        position: relative;
    }

    .diary {
        height: 100%;
        display: flex;
        flex-direction: column;

        .food-selection {
            flex: 1;

            .recipe-grid, .ingredient-grid {
                height: 100%;
            }
        }

        .nutrient-input {
            display: flex;
            align-items: center;
        }

        .nutrientTargets{
            display: grid;
            grid-template-columns: max-content max-content 1fr;
            grid-gap: 0.5em;
            .dailyTargetNutrient{
                display: contents;
            }
        }
    }
</style>