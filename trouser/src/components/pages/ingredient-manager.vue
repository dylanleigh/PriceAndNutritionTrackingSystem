<template>
    <div id="ingredient-manager">
        <div class="header-all flex-row-between flex-gap-regular">
            <h2>All Ingredients</h2>
            <input-float id='ingredient_filter'
                         label='Search'
                         @keyup="onSearch"></input-float>
        </div>
        <div class="ingredients-all">

            <!-- A data grid to browse available ingredients -->
            <ag-grid-vue
                    id="ingredients"
                    class="contained_table ag-theme-balham"
                    :gridOptions="gridOptions"
                    :datasource="datasource"
                    :columnDefs="columnDefs"
                    :defaulColDef="defaultColDef"
                    :pagination="true"
                    :paginationAutoPageSize="true"
                    @row-selected="onRowSelected"
                    rowModelType='infinite'
                    rowSelection='single'
            />
        </div>
        <div class="header">
            <h2>Information</h2>
        </div>
        <div class="ingredient">
            <!-- A form to edit the given ingredient -->
            <form id="ingredient_edit_form" autocomplete="off">
                <input-float
                        id='introduction'
                        label='Introduction'
                        hint="Introductory paragraph explains ingredient"
                        :multiline="true"
                        v-model="ingredient.introduction"
                ></input-float>
                <div class="flex-row-equalfill">
                    <input-float
                            id='name'
                            label='Name'
                            hint="Grilled Cheese"
                            v-model="ingredient.name"
                    ></input-float>
                    <input-float
                            id='slug'
                            label='Slug'
                            hint="grilled-cheese"
                            input_mask_name="slug_mask"
                            v-model="ingredient.slug"
                    ></input-float>
                </div>

                <input-float
                        id='description'
                        label='Description'
                        hint="A sandwich made with melted cheese"
                        :multiline="true"
                        v-model="ingredient.description"
                ></input-float>
                <input-float
                        id='notes'
                        label='Notes'
                        hint="Additional information about usage, types, etc."
                        :multiline="true"
                        v-model="ingredient.notes"
                ></input-float>
                <div class="flex-row-equalfill">
                    <input-float
                            id='tags'
                            label='Tags'
                            hint="tag1,tag2,tag3"
                            input_mask_name="tag_mask"
                            v-model="ingredient.tags"
                    ></input-float>
                    <!-- You can't modify the owner, but I'm showing it here for this proof of concept -->
                    <input-float
                            id='owner'
                            label='Owner'
                            hint="A sandwich made with melted cheese"
                            :extra='{disabled: true, value:""}'
                            v-model="ingredient.owner"
                    ></input-float>
                </div>
                <h3>Nutrition</h3>
                <div class="flex-row-equalfill">
                    <input-float
                            id='serving'
                            label='Serving Size (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.serving"
                    ></input-float>
                    <input-float
                            id='kilojoules'
                            label='kilojoules'
                            input_mask_name=nutrition_mask
                            v-model="ingredient.kilojoules"
                    ></input-float>
                </div>
                <div class="flex-row-equalfill">
                    <input-float
                            id='protein'
                            label='protein (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.protein"
                    ></input-float>
                    <input-float
                            id='carbohydrate'
                            label='carbohydrate (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.carbohydrate"
                    ></input-float>
                    <input-float
                            id='fat'
                            label='fat (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.fat"
                    ></input-float>
                    <input-float
                            id='saturatedfat'
                            label='saturatedfat (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.saturatedfat"
                    ></input-float>
                </div>
                <div class="flex-row-equalfill">
                    <input-float
                            id='sugar'
                            label='sugar (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.sugar"
                    ></input-float>
                    <input-float
                            id='sodium'
                            label='sodium (mg)'
                            hint="in milligrams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.sodium"
                    ></input-float>
                    <input-float
                            id='fibre'
                            label='fibre (g)'
                            hint="in grams"
                            input_mask_name="nutrition_mask"
                            v-model="ingredient.fibre"
                    ></input-float>
                </div>
            </form>
            <div class="flex-row-equalfill">
                <button
                        class="oneline dark"
                        @click="createIngredient"
                >Create New
                </button>
                <button
                        class="oneline dark"
                        :disabled="!canEdit"
                        @click="editIngredient"
                        id="edit_desc"
                >Edit<span v-if="shortName"> {{shortName}}</span></button>
                <button
                        class="oneline dark"
                        :disabled="!canDelete"
                        @click="deleteIngredient"
                        id="delete_desc"
                >Delete<span v-if="shortName"> {{shortName}}</span></button>
            </div>
        </div>
    </div>
</template>

<script>
    import InputFloat from '../inputs/input-float'
    import {AgGridVue} from 'ag-grid-vue'
    import "ag-grid-community/dist/styles/ag-grid.css";
    import "ag-grid-community/dist/styles/ag-theme-balham.css";

    export default {
        name: "ingredient-manager",
        components: {
            InputFloat,
            AgGridVue
        },
        inject: ['pants'],
        data() {
            return {
                all_ingredients: {},
                columnDefs: [
                    {headerName: "Name", field: "name", sort: 'asc'},
                    {headerName: "Description", field: "description"},
                    {headerName: "Serving", field: "serving"},
                    {headerName: "Notes", field: "notes"},
                ],
                defaultColDef: {
                    flex: 1,
                    sortable: true,
                    resizable: true,
                },
                gridOptions: {},
                datasource: {
                    getRows: async params => {
                        params.searchKey = document.querySelector('#ingredient_filter').value;
                        let response = await this.pants.get_ingredients(params);

                        if (response.ok) {
                            let data = await response.json();
                            params.successCallback(data['results'], data['count'])
                        } else {
                            params.failCallback();
                        }
                    }
                },
                ingredient: {
                    uri: null,
                    introduction: null,
                    name: null,
                    slug: null,
                    description: null,
                    notes: null,
                    tags: null,
                    owner: null,
                    serving: null,
                    kilojoules: null,
                    protein: null,
                    carbohydrate: null,
                    fat: null,
                    saturatedfat: null,
                    sugar: null,
                    sodium: null,
                    fibre: null,
                },
                // The node currently displayed in the ingredient form
                focusedNode: null,
            }
        },
        computed: {
            shortName() {
                let short_name = '';
                if (this.ingredient.name == null) return;

                if (this.ingredient.name.length > 13) {
                    short_name = this.ingredient.name.slice(0, 10) + '...';
                } else {
                    short_name = this.ingredient.name.slice(0, 13);
                }
                return short_name;
            },
            canEdit() {
                return this.focusedNode != null;
            },
            canDelete() {
                return this.focusedNode != null;
            }
        },
        methods: {
            /**
             * Updates the ingredient based on the values in the ingredients form
             */
            editIngredient() {

                this.pants.edit_ingredient(this.ingredient.uri, {
                    name: this.ingredient.name,
                    slug: this.ingredient.slug,
                    description: this.ingredient.description,
                    // @todo Cannot edit owner? Remove this if there is no case where this is possible
                    // 'owner': form.querySelector('[name=owner]').value,
                    tags: this.ingredient.tags.split(',').filter(tag => tag !== ''), // Remove empty tags
                    serving: this.ingredient.serving,
                    introduction: this.ingredient.introduction,
                    notes: this.ingredient.notes,

                    // Nutritional Data
                    kilojoules: this.ingredient.kilojoules,
                    protein: this.ingredient.protein,
                    fibre: this.ingredient.fibre,
                    carbohydrate: this.ingredient.carbohydrate,
                    fat: this.ingredient.fat,
                    sugar: this.ingredient.sugar,
                    saturatedfat: this.ingredient.saturatedfat,
                    sodium: this.ingredient.sodium,
                })
                    .then(resp => {
                        let row_node = this.focusedNode;
                        row_node.setData(resp);
                        this.gridOptions.api.flashCells({
                            rowNodes: [row_node]
                        })
                    });
            },
            /**
             * Deletes the currently selected ingredient
             */
            deleteIngredient() {
                this.pants.delete_ingredient(this.ingredient.uri)
                    .then(() => {
                        this.gridOptions.api.deselectAll();
                        this.refreshTable();
                        for (let key of Object.keys(this.ingredient)) {
                            this.ingredient[key] = ""
                        }
                    });
            },
            /**
             * Creates a new ingredient using the information in the input fields
             */
            createIngredient() {
                this.pants.create_ingredient({
                    name: this.ingredient.name,
                    slug: this.ingredient.slug,
                    description: this.ingredient.description,
                    // @todo Cannot edit owner? Remove this if there is no case where this is possible
                    // 'owner': form.querySelector('[name=owner]').value,
                    tags: this.ingredient.tags.split(',').filter(tag => tag !== ''), // Remove empty tags
                    serving: this.ingredient.serving,
                    introduction: this.ingredient.introduction,
                    notes: this.ingredient.notes,

                    // Nutritional Data
                    kilojoules: this.ingredient.kilojoules,
                    protein: this.ingredient.protein,
                    fibre: this.ingredient.fibre,
                    carbohydrate: this.ingredient.carbohydrate,
                    fat: this.ingredient.fat,
                    sugar: this.ingredient.sugar,
                    saturatedfat: this.ingredient.saturatedfat,
                    sodium: this.ingredient.sodium,
                })
                    .then(resp => {
                        console.log(resp);
                        this.refreshTable();
                    })
            },
            onRowSelected(args) {
                // This event fires if a row is selected OR deselected, we only care if something gets selected
                if (!args.node.selected) return;

                let ingredient = args.data;
                this.ingredient.uri = ingredient.url;
                this.ingredient.name = ingredient.name;
                this.ingredient.description = ingredient.description;
                this.ingredient.owner = ingredient.owner;
                this.ingredient.serving = ingredient.serving;
                this.ingredient.introduction = ingredient.introduction;
                this.ingredient.notes = ingredient.notes;
                this.ingredient.tags = ingredient.tags.join(',');
                this.ingredient.slug = ingredient.slug;

                // Nutritional Data
                this.ingredient.kilojoules = ingredient.kilojoules;
                this.ingredient.protein = ingredient.protein;
                this.ingredient.fibre = ingredient.fibre;
                this.ingredient.carbohydrate = ingredient.carbohydrate;
                this.ingredient.fat = ingredient.fat;
                this.ingredient.sugar = ingredient.sugar;
                this.ingredient.saturatedfat = ingredient.saturatedfat;
                this.ingredient.sodium = ingredient.sodium;

                // Also store a reference to this node so that we can refresh it
                this.focusedNode = args.node;
            },
            onSearch() {
                this.refreshTable();
            },
            refreshTable() {
                this.gridOptions.api.refreshInfiniteCache();
            }
        }
    }
</script>

<style scoped>
    #ingredient-manager {
        display: grid;
        grid-template-columns: 1fr 30em;
        grid-template-rows: 4em 1fr;
        gap: 0 var(--padding);
        grid-template-areas: "header-all header" "ingredients-all ingredient";

        min-height: calc(100vh - 7em); /* Make it fill as much of the screen as possible to start off*/
    }

    #ingredient-manager > .header-all {
        grid-area: header-all;
    }

    #ingredient-manager > .ingredients-all {
        grid-area: ingredients-all;
        resize: vertical;
        overflow: auto;
    }

    #ingredient-manager > .ingredient {
        grid-area: ingredient;
    }

    #ingredient-manager > .header {
        grid-area: header;
    }

    #ingredient-manager > .ingredients-all > .contained_table {
        height: 100%;
    }

    #ingredient-manager > .ingredient {
        max-width: 30em;
    }

    #ingredient-manager > .ingredient button {
        margin: 1px;
    }

    #ingredient-manager > .ingredient .field {
        margin: 1px;
    }
</style>