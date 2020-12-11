<template>
    <layout-default current-loc="ingredient_manager">
        <template v-slot:content>
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
                        <input
                                type="hidden"
                                id="selected_row_node"
                        >
                        <input
                                type="hidden"
                                id="ingredient_uri"
                                name="ingredient_uri"
                                v-model="ingredient.uri"
                        >

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
                                @click="create_ingredient"
                        >Create New</button>
                        <button
                                class="oneline dark"
                                :disabled="!canEdit"
                                @click="edit_ingredient"
                                id="edit_desc"
                        >Edit<span v-if="shortName"> {{shortName}}</span></button>
                        <button
                                class="oneline dark"
                                :disabled="!canDelete"
                                @click="delete_ingredient"
                                id="delete_desc"
                        >Delete<span v-if="shortName"> {{shortName}}</span></button>
                    </div>
                </div>
            </div>
        </template>
    </layout-default>
</template>

<script>
    import LayoutDefault from './layouts/layout-default'
    import InputFloat from '../inputs/input-float'
    import {AgGridVue} from 'ag-grid-vue'
    import "ag-grid-community/dist/styles/ag-grid.css";
    import "ag-grid-community/dist/styles/ag-theme-balham.css";

    export default {
        name: "ingredient-manager",
        components: {
            LayoutDefault,
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
                rowData: [],
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
        computed:{
            shortName(){
                let short_name = '';
                if(this.ingredient.name == null) return;

                if (this.ingredient.name.length > 13) {
                    short_name = this.ingredient.name.slice(0, 10) + '...';
                } else {
                    short_name = this.ingredient.name.slice(0, 13);
                }
                return short_name;
            },
            canEdit(){
                return this.focusedNode != null;
            },
            canDelete(){
                return this.focusedNode != null;
            }
        },
        watch:{

        },
        methods: {
            /**
             * Updates the ingredient based on the values in the ingredients form
             */
            edit_ingredient() {
                let form = document.querySelector('#ingredient_edit_form');
                let ingredient_uri = form.querySelector('#ingredient_uri').value;
                let tags = form.querySelector('[name=tags]').value.split(',');
                // Remove empty tags
                tags = tags.filter(tag => tag !== '');

                this.pants.edit_ingredient(ingredient_uri, {
                    'name': form.querySelector('[name=name]').value,
                    'slug': form.querySelector('[name=slug]').value,
                    'description': form.querySelector('[name=description]').value,
                    // @todo Cannot edit owner? Remove this if there is no case where this is possible
                    // 'owner': form.querySelector('[name=owner]').value,
                    'tags': tags,
                    'serving': form.querySelector('[name=serving]').value,
                    'introduction': form.querySelector('[name=introduction]').value,
                    'notes': form.querySelector('[name=notes]').value,

                    // Nutritional Data
                    'kilojoules': form.querySelector('[name=kilojoules]').value,
                    'protein': form.querySelector('[name=protein]').value,
                    'fibre': form.querySelector('[name=fibre]').value,
                    'carbohydrate': form.querySelector('[name=carbohydrate]').value,
                    'fat': form.querySelector('[name=fat]').value,
                    'sugar': form.querySelector('[name=sugar]').value,
                    'saturatedfat': form.querySelector('[name=saturatedfat]').value,
                    'sodium': form.querySelector('[name=sodium]').value,
                })
                    .then(resp => {
                        let row_node = document.querySelector('#selected_row_node').extra_data.ag_data;
                        row_node.setData(resp);
                        this.all_ingredients.gridOptions.api.flashCells({
                            rowNodes: [row_node]
                        })
                    });
            },
            /**
             * Deletes the currently selected ingredient
             */
            delete_ingredient() {
                this.pants.delete_ingredient(document.querySelector('#ingredient_uri').value)
                    .then(() => {
                        this.all_ingredients.gridOptions.api.deselectAll();
                        this.all_ingredients.gridOptions.api.refreshInfiniteCache();
                    });
            },
            /**
             * Creates a new ingredient using the information in the input fields
             */
            create_ingredient() {
                let form = document.querySelector('#ingredient_edit_form');
                let tags = form.querySelector('[name=tags]').value.split(',');
                // Remove empty tags
                tags = tags.filter(tag => tag !== '');

                this.pants.create_ingredient({
                    'name': form.querySelector('[name=name]').value,
                    'slug': form.querySelector('[name=slug]').value,
                    'description': form.querySelector('[name=description]').value,
                    // @todo Cannot edit owner? Remove this if there is no case where this is possible
                    // 'owner': form.querySelector('[name=owner]').value,
                    'tags': tags,
                    'serving': form.querySelector('[name=serving]').value,
                    'introduction': form.querySelector('[name=introduction]').value,
                    'notes': form.querySelector('[name=notes]').value,

                    // Nutritional Data
                    'kilojoules': form.querySelector('[name=kilojoules]').value,
                    'protein': form.querySelector('[name=protein]').value,
                    'fibre': form.querySelector('[name=fibre]').value,
                    'carbohydrate': form.querySelector('[name=carbohydrate]').value,
                    'fat': form.querySelector('[name=fat]').value,
                    'sugar': form.querySelector('[name=sugar]').value,
                    'saturatedfat': form.querySelector('[name=saturatedfat]').value,
                    'sodium': form.querySelector('[name=sodium]').value,
                })
                    .then(resp => {
                        console.log(resp);
                        this.all_ingredients.gridOptions.api.refreshInfiniteCache();
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
            onSearch(){
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