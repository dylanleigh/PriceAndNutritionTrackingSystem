<template>
    <div :class="$options.name">
        <h1 class="header-add">Add to Diary</h1>
        <h1 class="header-display">Current Diary</h1>
        <div class="display-forms">
            <!-- Shows how close user is to achieving their daily targets -->
            <div class="nutrientTargets">
                <div
                        v-for="nutrient in Object.keys(staticVals.nutrientValues)"
                        :key="nutrient"
                        class="dailyTargetNutrient"
                >
                    <fa-icon :icon="['fas', staticVals.icons.nutrients[nutrient]]" fixedWidth/>
                    <input-float
                            :id="nutrient"
                            :label="`${nutrient} (${staticVals.units[nutrient]})`"
                            v-model="oneOffFood[nutrient]"
                            :disabled="entryType !== staticVals.entryType.ONE_OFF_FOOD"
                    />
                    <target-summary
                            :value="diaryFoodNutrientTotals[nutrient] || 0"
                            :proposed-change="proposedEntryNutrients[nutrient] || 0"
                            :target-min-value="dailyTarget.min[nutrient] || 0"
                            :target-max-value="dailyTarget.max[nutrient] || 0"/>
                </div>
            </div>

            <!-- Shows all the foods recorded in the last 24 hours -->
            <div class="diaryFoods">
                <ul>
                    <li v-for="food in diaryFoods" :key="food.url">{{food.name}}</li>
                </ul>
            </div>
        </div>


        <div class="add-forms">
            <!-- The form for adding more diary entries -->
            <form id="diary_entry_form" class="flex-row-start">
                <button
                        id="time-text"
                        class="text-only"
                        type="button"
                        @click="changeTime"
                >{{staticVals.text.changeTimeBtn[timeSpecificity]}}
                </button>

                <input-float
                        id="date"
                        label="Date"
                        type="date"
                        v-show="timeSpecificity===staticVals.timeSpecificity.ON_DATETIME"
                />
                <input-float
                        id="time"
                        label="Time"
                        type="time"
                        v-show="timeSpecificity!==staticVals.timeSpecificity.JUST_NOW"
                />

                <span>I ate</span>

                <input-float
                        id="amount"
                        label="Amount"
                        v-model="entry.amount"
                        :extra="{style:'text-align:right;max-width:6em'}"
                />
                <input-float
                        id="unit"
                        type="select"
                        :hide-default-option="true"
                        v-model="entry.unit"
                >
                    <option value="weight">Grams</option>
                    <option value="servings">Servings</option>
                </input-float>

                <span>of</span>

                <input-float
                        id="entry-type"
                        type="select"
                        :hide-default-option="true"
                        v-model="entryType"
                >
                    <option :value="staticVals.entryType.RECIPE">Recipe</option>
                    <option :value="staticVals.entryType.INGREDIENT">Ingredient</option>
                    <option :value="staticVals.entryType.ONE_OFF_FOOD">One-off Food</option>
                </input-float>

                <button class="dark" type="button" @click="createDiaryFood">Add</button>
            </form>

            <!-- Shows the tables for picking an existing food to add -->
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
                        :rowSelection="componentsGrid.rowSelection"
                        :pagination="componentsGrid.pagination"
                        :paginationAutoPageSize="componentsGrid.paginationAutoPageSize"
                        :datasource="componentsGrid.datasource"
                        @row-selected="onIngredientRowSelected"
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
                // The current proposed entry
                entry: {
                    unit: "weight",
                    amount: 100
                    // For nutrition calculations (the server would normally handle this but we pre-calculate on the front end for visualization)
                    // See the 'proposedEntryNutrients' computed property.
                },
                // Stores the currently selected recipe/ingredient
                selected: {
                    recipe: null,
                    ingredient: null
                },
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
                    rowSelection: 'single',
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
                diaryFoods: []
            }
        },
        beforeMount() {
            this.pants.Target.getDaily()
                .then(resp => {
                    let target = resp.results[0];
                    for (let nutrient of Object.keys(this.staticVals.nutrientValues)) {
                        this.dailyTarget.max[nutrient] = parseFloat(target.maximum[nutrient]) || 0;
                        this.dailyTarget.min[nutrient] = parseFloat(target.minimum[nutrient]) || 0;
                    }
                });
            // Get all DiaryFood entries for the last 24 hours
            this.refreshTodaysDiaryFoods();
        },
        computed: {
            /**
             * The total for each nutrient we are tracking of all foods entered in the last 24 hours
             * @returns {{}}
             */
            diaryFoodNutrientTotals() {
                let totals = {...this.staticVals.nutrientValues};
                this.diaryFoods.forEach(entry => {
                    for (let nutrient of Object.keys(totals)) {
                        if (totals[nutrient] == null) totals[nutrient] = 0;
                        totals[nutrient] += parseFloat(entry[nutrient]) || 0;
                    }
                })
                return totals;
            },
            /**
             * The nutrients that would be added if we were to commit the currently selected amount and unit of chosen food item
             */
            proposedEntryNutrients() {
                let totals = {...this.staticVals.nutrientValues};

                if (this.entryType === this.staticVals.entryType.RECIPE && this.selected.recipe != null) {
                    let chosenGrams = 0; // How much of this recipe in grams did the user propose to add
                    let gramsInRecipe = this.selected.recipe.nutrition_data.grams; // How many grams the recipe creates if followed as is
                    if (this.entry.unit === 'servings') {
                        let gramsPerServing = gramsInRecipe / parseFloat(this.selected.recipe.serves) || 1; // g/recipe / servings/recipe = g/serving
                        chosenGrams = gramsPerServing * this.entry.amount;
                    } else {
                        chosenGrams = this.entry.amount; //
                    }
                    let ratio = chosenGrams / gramsInRecipe;
                    for (let nutrient of Object.keys(totals)) {
                        totals[nutrient] = (parseFloat(this.selected.recipe.nutrition_data[nutrient]) * ratio) || 0;
                    }
                } else if (this.entryType === this.staticVals.entryType.INGREDIENT && this.selected.ingredient != null) {
                    // Scale according to the desired number of grams
                    let storedGramUnit = 1000; // All nutrition info is stored per kg for an ingredient
                    let chosenAmountInGrams = 0; // need to know how many grams user has chosen
                    if (this.entry.unit === 'servings') {
                        // Convert servings to grams
                        let servingSize = parseFloat(this.selected.ingredient.serving);
                        chosenAmountInGrams = servingSize * this.entry.amount;
                    } else {
                        chosenAmountInGrams = this.entry.amount;
                    }
                    let ratio = chosenAmountInGrams / storedGramUnit;
                    for (let nutrient of Object.keys(totals)) {
                        totals[nutrient] = (parseFloat(this.selected.ingredient.nutrition_data[nutrient]) * ratio) || 0;
                    }
                } else {
                    // Use the one off food values
                    for (let nutrient of Object.keys(totals)) {
                        totals[nutrient] = (this.oneOffFood[nutrient]) || 0;
                    }
                }
                return totals;
            }
        },
        watch: {
            entryType(newValue) {
                if (newValue !== this.staticVals.entryType.ONE_OFF_FOOD) {
                    for (let nutrient of Object.keys(this.staticVals.nutrientValues)) {
                        this.oneOffFood[nutrient] = null;
                    }
                }
            }
        },
        methods: {
            /**
             * Gets the diary foods logged from the past day, updating the internally stored copy from the db
             */
            refreshTodaysDiaryFoods() {
                const yesterday = (new Date((new Date()) - 24 * 60 * 60 * 1000)).toISOString().replace('T', ' ');
                return this.pants.DiaryFood.get_all({
                    filterDict: {
                        'start_time': ['gte', yesterday]
                    }
                }).then(resp => {
                    this.diaryFoods = resp.results;
                })
            },
            createDiaryFood() {
                let requestObject = {
                    // @todo properly get start time
                    'start_time': (new Date(/*date.value + "T" + time.value*/)).toISOString(),
                    // Set 'servings' or 'weight'
                    [this.entry.unit]: this.entry.amount,
                };
                // What food gets added depends on what view we are in
                if (this.entryType === this.staticVals.entryType.RECIPE && this.selected.recipe !== null) {
                    requestObject["of_recipe"] = this.selected.recipe.url;
                } else if (this.entryType === this.staticVals.entryType.INGREDIENT && this.selected.ingredient !== null) {
                    requestObject["of_ingredient"] = this.selected.ingredient.url;
                } else {
                    // @todo allow specifying a name for this food
                    requestObject["name"] = "Custom Food"
                    // @todo properly set up one time food entry
                }
                this.pants.DiaryFood.create(requestObject).then(() => {
                    this.refreshTodaysDiaryFoods().then(() => {
                        if (requestObject['of_recipe']) {
                            this.recipeGrid.gridOptions.api.deselectAll();
                            this.selected.recipe = null;
                        } else if (requestObject['of_ingredient']) {
                            this.componentsGrid.gridOptions.api.deselectAll();
                            this.selected.ingredient = null;
                        }
                    });
                });
                /*
                let component_data = JSON.parse(component.value)[0];
                this.pants.create_diaryfood({
                    'start_time': (new Date(date.value + "T" + time.value)).toISOString(),
                    // Set 'servings' or 'weight'
                    [unit.value]: amount.value,
                    // Set 'of_ingredient', 'of_recipe' or 'name' depending on what has been entered
                    [component_data.url === undefined
                        ? 'name'
                        : (component_data.url.split("/").slice(-3)[0] === 'recipe'
                            ? 'of_recipe'
                            : 'of_ingredient')
                        ]: component_data.url === undefined ? component_data.name : component_data.url,
                })
                 */
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
                // This event fires if a row is selected OR deselected, we only care if something gets selected
                if (!args.node.selected) return;

                this.selected.recipe = args.data;
            },
            onIngredientRowSelected(args) {
                // This event fires if a row is selected OR deselected, we only care if something gets selected
                if (!args.node.selected) return;

                this.selected.ingredient = args.data;
            }
        }
    }
</script>

<style scoped lang="scss">
    .diary {
        display: grid;
        grid-template-columns: 1fr 30em;
        grid-template-rows: 4em 1fr;
        gap: 0 var(--padding);
        grid-template-areas: 'header-add header-display' 'diary-add diary-display';

        height: 100%;

        .header-add{
            grid-area: header-add;
        }
        .header-display{
            grid-area: header-display;
        }

        .add-forms{
            grid-area: diary-add;
            display: flex;
            flex-direction: column;

            .food-selection {
                flex: 1;

                .recipe-grid, .ingredient-grid {
                    height: 100%;
                }
            }
        }

        .display-forms{
            grid-area: diary-display;
        }

        #diary_entry_form {
            display: flex;

            > *:not(:last-child) {
                margin-right: 0.5em;
            }
        }



        .nutrient-input {
            display: flex;
            align-items: center;
        }

        .nutrientTargets {
            display: grid;
            grid-template-columns: max-content 9em 1fr;
            grid-gap: 0.5em;
            align-items: center;

            .dailyTargetNutrient {
                display: contents;
            }
        }
    }
</style>