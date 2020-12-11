<template>
    <div id="recipe-manager">
        <div class="header-all-recipes flex-row-between flex-gap-regular">
            <h2>All Recipes</h2>
            <input-float
                    id='recipe_filter'
                    label='Search'
                    @keyup="recipeGrid.gridOptions.api.refreshInfiniteCache()"
            ></input-float>
        </div>
        <div class="all-recipes resizable-vertical">
            <ag-grid-vue
                    id="all_recipes_table"
                    class="ag-theme-balham fill-height"
                    :gridOptions="recipeGrid.gridOptions"
                    :components="recipeGrid.components"
                    :columnDefs="recipeGrid.columnDefs"
                    :defaultColDef="recipeGrid.defaultColDef"
                    :rowModelType="recipeGrid.rowModelType"
                    :rowSelection="recipeGrid.rowSelection"
                    :pagination="recipeGrid.pagination"
                    :paginationAutoPageSize="recipeGrid.paginationAutoPageSize"
                    :datasource="recipeGrid.datasource"
                    @row-selected="onRecipeRowSelected"
            ></ag-grid-vue>
        </div>
        <div class="header-all-ingredients flex-row-between flex-gap-regular">
            <h2>All Ingredients</h2>
            <input-float
                    id='ingredient_filter'
                    label='Search'
                    @keyup="componentsGrid.gridOptions.api.refreshInfiniteCache()"
            ></input-float>
        </div>
        <div class="all-ingredients resizable-vertical">
            <ag-grid-vue
                    id="ingredients"
                    class="ag-theme-balham fill-height"
                    :gridOptions="componentsGrid.gridOptions"
                    :components="componentsGrid.components"
                    :columnDefs="componentsGrid.columnDefs"
                    :defaultColDef="componentsGrid.defaultColDef"
                    :rowModelType="componentsGrid.rowModelType"
                    :pagination="componentsGrid.pagination"
                    :paginationAutoPageSize="componentsGrid.paginationAutoPageSize"
                    :datasource="componentsGrid.datasource"
            ></ag-grid-vue>
        </div>
        <div class="header-recipe">
            <h2>Selected Recipe</h2>
        </div>
        <div class="recipe">
            <form id="recipe-edit-form" autocomplete="off">
                <input type="hidden" id="selected_row_node">
                <input type="hidden" id="recipe_uri" name="recipe_uri">

                <input-float
                        id='introduction'
                        label='Introduction'
                        hint="A story about how the grilled cheese came to be"
                        :multiline="true"
                        v-model="recipe.introduction"
                ></input-float>

                <div class="flex-row-equalfill">
                    <input-float
                            id='name'
                            label='Name'
                            hint="Grilled Cheese"
                            v-model="recipe.name"
                    ></input-float>
                    <input-float
                            id='slug'
                            label='Slug'
                            hint="grilled-cheese"
                            input_mask_name="slug_mask"
                            v-model="recipe.slug"
                    ></input-float>
                </div>

                <input-float
                        id='description'
                        label='Description'
                        hint="A sandwich made with melted cheese"
                        :multiline="true"
                        v-model="recipe.description"
                ></input-float>

                <div class="flex-row-equalfill">
                    <input-float
                            id='serves'
                            label='Serves'
                            hint="1"
                            v-model="recipe.serves"
                    ></input-float>
                    <input-float
                            id='tags'
                            label='Tags'
                            hint="tag1,tag2,tag3"
                            input_mask=tag_mask
                            :extra='{style:"flex:2"}'
                            v-model="recipe.tags"
                    ></input-float>
                    <!-- @todo it is unclear what flag is used for, need to add support for it -->
                    <input-float
                            id="flag"
                            type="select"
                            label="Flag"
                            v-model="recipe.flag"
                    >
                        <option v-for="flag in allowedFlags" :key="flag.name" :value="flag.name">({{flag.char}})
                            {{flag.name}}
                        </option>
                    </input-float>
                </div>

                <h3>Recipe Ingredients</h3>
                <div id="recipe-components">
                    <!--                    <recipe-component v-for="component in recipe.components" :key="component.id"></recipe-component>-->
                </div>

                <input-float
                        id='method'
                        label='Method'
                        hint="Add cheese to bread, toast."
                        :multiline="true"
                        v-model="recipe.method"
                ></input-float>
                <input-float
                        id='notes'
                        label='Notes'
                        hint="Can use different cheeses than what is listed. Recipe is flexible."
                        :multiline="true"
                        v-model="recipe.notes"
                ></input-float>
            </form>
            <div class="flex-row-equalfill">
                <button
                        class="oneline dark"
                        @click="create_recipe"
                >Create New
                </button>
                <button
                        class="oneline dark"
                        :disabled="canEdit"
                        @click="edit_recipe"
                >Edit <span v-if="recipe.name"> {{recipe.name}}</span></button>
                <button
                        class="oneline dark"
                        :disabled="canDelete"
                        @click="delete_recipe"
                >Delete <span v-if="recipe.name"> {{recipe.name}}</span></button>
            </div>
        </div>
    </div>
</template>

<script>
    import InputFloat from "@/components/inputs/input-float";
    import {AgGridVue} from 'ag-grid-vue';
    // import RecipeComponent from "@/components/recipe-component";

    import "ag-grid-community/dist/styles/ag-grid.css";
    import "ag-grid-community/dist/styles/ag-theme-balham.css";

    // Create cell renderers for specific columns
    class actionButtonCellRenderer {
        init(params) {
            this.cell = document.createElement('div');
            this.cell.innerHTML = '<button class="dark" style="padding: 0;margin: 0"><i class="fas fa-carrot"></i></button>';

            // get references to the elements we want
            this.add_recipe_btn = this.cell.querySelector('button');
            this.add_recipe_btn.addEventListener('click', e => {
                e.stopPropagation();
                params.onClick(params.data)
            });

            this.cell.setAttribute("class", "flex-row-equalfill");
            this.cell.setAttribute("style", "align-items:stretch;height:100%");
        }

        getGui() {
            return this.cell
        }

        refresh() {
            // return true to tell the grid we refreshed successfully
            return true;
        }

        destroy() {
            // do cleanup, remove event listener from button
        }
    }

    export default {
        name: "recipe-manager",
        components: {
            // RecipeComponent,
            InputFloat,
            AgGridVue
        },
        inject: ['pants'],
        data() {
            return {
                recipeGrid: {
                    gridOptions: {},
                    components: {
                        actionsCell: actionButtonCellRenderer,
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
                                }
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
                            params.searchKey = document.querySelector('#recipe_filter').value;
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
                    components: {
                        actionsCell: actionButtonCellRenderer,
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
                                }
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
                            params.searchKey = document.querySelector('#ingredient_filter').value;
                            let response = await this.pants.get_ingredients(params);

                            if (response.ok) {
                                let data = await response.json();
                                params.successCallback(data['results'], data['count'])
                            } else {
                                params.failCallback();
                            }
                        }
                    }
                },
                recipe: {
                    components: [],
                    uri: null,
                    introduction: null,
                    name: null,
                    slug: null,
                    description: null,
                    serves: null,
                    tags: null,
                    flag: null,
                    method: null,
                    notes: null,
                },
                focusedNode: null,
                allowedFlags: [],
            }
        },
        computed: {
            canEdit() {
                return this.focusedNode != null;
            },
            canDelete() {
                return this.focusedNode != null;
            }
        },
        mounted() {
            // Set flag options
            this.pants.get_recipe_flags()
                .then(data => {
                    this.allowedFlags = data.results;
                });
        },
        methods: {
            /**
             * Gets all the components in the components list and returns a list suitable for passing onto the api
             */
            get_components() {
                let output = [];
                this.recipe.components.forEach(component => {
                    let component_obj = {
                        name: component.name,
                        note: component.note || '',
                        // Set "servings" or "weight"
                        [component.unit]: component.amount,
                        // Set "of_ingredient" or "of_recipe"
                        ["of_" + component.type]: component.recipe_or_ingredient_id,
                    }
                    if (component.id) {
                        // Only set db id if it has been provided by the db
                        component_obj["id"] = component.id;
                    }
                    output.push(component_obj)
                })
                return output;
            },
            /**
             * Adds a component to the component list
             * @param {string} type either "recipe" or "ingredient"
             * @param {string} id the id number of the component (not the url) for this component relationship
             * @param {string} recipe_or_ingredient_id the original recipe or ingredient id for this component
             * @param {string} name the name of the component
             * @param {string} amount how much of the component in units
             * @param {string} unit what unit the amount is in. Should be "weight" for grams, or "servings" for servings
             * @param {string} note any additional notes
             */
            add_component(type, id, recipe_or_ingredient_id, name, amount, unit, note) {
                this.recipe.components.push({
                    type: type,
                    id: id,
                    recipe_or_ingredient_id: recipe_or_ingredient_id,
                    name: name,
                    amount: amount,
                    unit: unit,
                    note: note
                });
            },
            /**
             * Deletes the currently selected recipe
             */
            delete_recipe() {
                this.pants.delete_recipe(this.recipe.uri)
                    .then(() => {
                        this.recipeGrid.gridOptions.api.deselectAll();
                        this.recipeGrid.gridOptions.api.refreshInfiniteCache();
                    });
            },
            /**
             * Updates the recipe based on the values in the recipe form
             */
            edit_recipe() {
                this.pants.edit_recipe(this.recipe.uri, {
                    name: this.recipe.name,
                    slug: this.recipe.slug,
                    description: this.recipe.description,
                    // @todo Cannot edit owner? Remove this if there is no case where this is possible
                    // 'owner': form.querySelector('[name=owner]').value,
                    tags: this.recipe.tags.split(',').filter(tag => tag !== ''), // Remove empty tags
                    serves: this.recipe.serves,
                    introduction: this.recipe.introduction,
                    notes: this.recipe.notes,
                    method: this.recipe.method,
                    components: this.get_components(),
                    flag: this.recipe.flag,
                })
                    .then(resp => {
                        let row_node = this.focusedNode;
                        row_node.setData(resp);
                        this.recipeGrid.gridOptions.api.flashCells({
                            rowNodes: [row_node]
                        })
                    });
            },
            /**
             * Creates a new recipe using the information in the recipe form
             */
            create_recipe() {
                this.pants.create_recipe({
                    name: this.recipe.name,
                    slug: this.recipe.slug,
                    description: this.recipe.description,
                    // @todo Cannot edit owner? Remove this if there is no case where this is possible
                    // 'owner': form.querySelector('[name=owner]').value,
                    tags: this.recipe.tags.split(',').filter(tag => tag !== ''), // Remove empty tags,
                    serves: this.recipe.serves,
                    introduction: this.recipe.introduction,
                    notes: this.recipe.notes,
                    method: this.recipe.method,
                    components: this.recipe.components,
                    flag: this.recipe.flag,
                })
                    .then(() => {
                        this.recipeGrid.gridOptions.api.refreshInfiniteCache();
                    });
            },
            remove_all_components() {
                this.recipe.components = [];
            },
            onRecipeRowSelected(args) {
                // This event fires if a row is selected OR deselected, we only care if something gets selected
                if (!args.node.selected) return;
                let recipe = args.data;

                this.recipe.introduction = recipe.introduction;
                this.recipe.name = recipe.name;
                this.recipe.description = recipe.description;
                this.recipe.recipe_uri = recipe.url;
                this.recipe.serves = recipe.serves;
                this.recipe.flag = recipe.flag || "";
                this.recipe.method = recipe.method;
                this.recipe.notes = recipe.notes;
                this.recipe.tags = recipe.tags.join(',');
                this.recipe.slug = recipe.slug;

                // Components are not included in results for performance reasons, make a separate call to get those
                this.pants.get_recipe_full(recipe.url)
                    .then(response => response.json())
                    .then(json => {
                        // Empty current components
                        this.remove_all_components();

                        json.components.forEach(component => {
                            this.add_component(
                                component.of_ingredient == null ? "recipe" : "ingredient",
                                component.id,
                                component.of_ingredient || component.of_recipe,
                                component.name,
                                component.servings || component.weight,
                                component.servings == null ? "weight" : "servings",
                                component.note
                            );
                        })
                    })
                    .catch(e => {
                        console.log(e);
                        // Don't leave components from last recipe in there.
                        this.remove_all_components();
                    })

                // Also store a reference to this node so that we can refresh it
                this.focusedNode = args.node;

                // Label the buttons to indicate the node that will be affected
                let edit_btn_desc = document.querySelector('#edit-recipe-name');
                let delete_btn_desc = document.querySelector('#delete-recipe-name');
                edit_btn_desc.innerText = recipe.name;
                delete_btn_desc.innerText = recipe.name;
                // Since they start off disabled, enable them
                edit_btn_desc.parentNode.disabled = false;
                delete_btn_desc.parentNode.disabled = false;
            }
        }
    }
</script>

<style scoped>
    #recipe-manager {
        display: grid;
        grid-template-columns: 1fr 30em;
        grid-template-rows: max-content 1fr max-content 1fr;
        gap: 0 var(--padding);
        grid-template-areas: "header-all-recipes header-recipe" "all-recipes recipe" "header-all-ingredients recipe" "all-ingredients recipe";

        min-height: calc(100vh - 7em); /* Make it fill the screen as much as possible for less flash when picking a recipe*/
    }

    #recipe-manager > .header-all-recipes {
        grid-area: header-all-recipes;
    }

    #recipe-manager > .all-recipes {
        grid-area: all-recipes;
    }

    #recipe-manager > .header-all-ingredients {
        grid-area: header-all-ingredients;
    }

    #recipe-manager > .all-ingredients {
        grid-area: all-ingredients;
    }

    #recipe-manager > .header-recipe {
        grid-area: header-recipe;
    }

    #recipe-manager > .recipe {
        grid-area: recipe;
    }

    .fill-height {
        height: 100%;
    }

    #recipe-manager .field,
    #recipe-manager button {
        margin: 1px;
    }

    .resizable-vertical {
        resize: vertical;
        overflow: auto;
    }

    #recipe-components {
        display: grid;
        /*grid-template-columns: 1fr [note-start] 8em 7em 2em [note-end];*/
        /*A somewhat hacky way to make this align with the 3 way split of fields above it*/
        grid-template-columns: 2em calc(33% + 1px - 2em) [note-start] calc(33% + 3px) 1fr 2em [note-end];
        margin: var(--padding) 1px;
        align-items: center;
    }

    /* has-note on the component-wrapper class indicates note should show. It's absence means the opposite */
    .component-wrapper:not(.has-note) > #note {
        display: none;
    }
</style>