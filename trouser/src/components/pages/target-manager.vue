<template>
    <div :class="$options.name">
        <div class="header-all">
            <h2>All Targets</h2>
        </div>
        <div class="header-form">

        </div>
        <div class="targets-all">
            <ag-grid-vue
                    id="targets-grid"
                    class="targets-table ag-theme-balham"
                    :gridOptions="targetsGrid.gridOptions"
                    :datasource="targetsGrid.datasource"
                    :columnDefs="targetsGrid.columnDefs"
                    :defaulColDef="targetsGrid.defaultColDef"
                    :pagination="true"
                    :paginationAutoPageSize="true"
                    @row-selected="onRowSelected"
                    rowModelType='infinite'
                    rowSelection='single'
            />
        </div>
        <div class="target-selected">
            <form>
                <input-float
                        id="name"
                        label="name"
                        v-model="target.name"
                ></input-float>
                <input-float
                        id="slug"
                        label="slug"
                        v-model="target.slug"
                ></input-float>
                <input-checkbox
                        id="daily"
                        label="daily"
                        v-model="target.daily"
                ></input-checkbox>

                <input-float
                        id="description"
                        label="description"
                        :multiline="true"
                        v-model="target.description"
                ></input-float>

<!--                Generate pairs of inputs for each nutrient-->
                <div class="nutrient-input-row" v-for="nutrient in Object.keys(target.maximum)" :key="nutrient">
                    <span>
                        <fa-icon :icon="['fas', staticVals.icons.nutrients[nutrient]]" fixed-width></fa-icon>
                        {{nutrient}}
                    </span>
                    <input-float
                        :id="'min:' + nutrient"
                        :label="`min (${staticVals.units[nutrient] || 'unknown unit'})`"
                        v-model="target.minimum[nutrient]"
                    ></input-float>
                    <input-float
                        :id="'max:' + nutrient"
                        :label="`max (${staticVals.units[nutrient] || 'unknown unit'})`"
                        v-model="target.maximum[nutrient]"
                    ></input-float>
                </div>

                <button
                        class="oneline dark"
                        type="button"
                        @click="createTarget"
                >Create New
                </button>
                <button
                        class="oneline dark"
                        type="button"
                        :disabled="!canEdit"
                        @click="editTarget"
                >Edit</button>
                <button
                        class="oneline dark"
                        type="button"
                        :disabled="!canDelete"
                        @click="deleteTarget"
                >Delete</button>
            </form>
        </div>
    </div>
</template>

<script>
    import InputFloat from '../inputs/input-float'
    import {AgGridVue} from 'ag-grid-vue'
    import "ag-grid-community/dist/styles/ag-grid.css";
    import "ag-grid-community/dist/styles/ag-theme-balham.css";
    import InputCheckbox from "@/components/inputs/input-checkbox";

    // A blank nutrition object, to be used for both the target max and min
    // @todo extract to pants api?
    const nutritionObj = {
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

    const _static = {
        icons:{
            nutrients:{
                cost:"money-bill-alt",
                kilojoules:"bolt",
                protein:"egg",
                carbohydrate:"bread-slice",
                fat:"tint",
                saturatedfat:"tint-slash",
                fibre:"seedling",
                sodium:"stroopwafel",
                sugar:"cubes",
            }
        },
        units:{
            cost: '$',
            kilojoules: 'kcal',
            protein: 'g',
            carbohydrate: 'g',
            fat: 'g',
            saturatedfat: 'g',
            fibre: 'g',
            sodium: 'mg',
            sugar: 'g',
        }
    }

    export default {
        name: "target-manager",
        components: {
            InputCheckbox,
            InputFloat,
            AgGridVue
        },
        inject: ['pants'],
        data() {
            return {
                staticVals: _static,
                targetsGrid: {
                    columnDefs: [
                        {headerName: "Name", field: "name", sort: 'asc'},
                        {headerName: "Description", field: "description"},
                        {headerName: "Daily", field: "daily_target"},
                    ],
                    defaultColDef: {
                        flex: 1,
                        sortable: true,
                        resizable: true,
                    },
                    gridOptions: {},
                    datasource: {
                        getRows: async params => {
                            // @todo implement search
                            //params.searchKey = document.querySelector('#ingredient_filter').value;
                            let data = await this.pants.get_target(params);
                            params.successCallback(data['results'], data['count']);
                        }
                    },
                },
                target: {
                    url: null,
                    name: null,
                    slug: null,
                    description: null,
                    daily: false,
                    minimum: {...nutritionObj},
                    maximum: {...nutritionObj}
                },
                focusedNode: null
            }
        },
        computed:{
            canEdit(){
                return this.target.url != null;
            },
            canDelete(){
                return this.target.url != null;
            }
        },
        methods: {
            onRowSelected(args) {
                // This event fires if a row is selected OR deselected, we only care if something gets selected
                if (!args.node.selected) return;

                let target = args.data;
                this.target.name = target.name;
                this.target.slug = target.slug;
                this.target.url = target.url;
                this.target.daily = target.daily_target;
                this.target.description = target.description;

                // Deal with minimums and maximums
                this.target.minimum.cost = target.minimum.cost;
                this.target.minimum.kilojoules = target.minimum.kilojoules;
                this.target.minimum.protein = target.minimum.protein;
                this.target.minimum.carbohydrate = target.minimum.carbohydrate;
                this.target.minimum.fat = target.minimum.fat;
                this.target.minimum.saturatedfat = target.minimum.saturatedfat;
                this.target.minimum.fibre = target.minimum.fibre;
                this.target.minimum.sodium = target.minimum.sodium;
                this.target.minimum.sugar = target.minimum.sugar;

                this.target.maximum.cost = target.maximum.cost;
                this.target.maximum.kilojoules = target.maximum.kilojoules;
                this.target.maximum.protein = target.maximum.protein;
                this.target.maximum.carbohydrate = target.maximum.carbohydrate;
                this.target.maximum.fat = target.maximum.fat;
                this.target.maximum.saturatedfat = target.maximum.saturatedfat;
                this.target.maximum.fibre = target.maximum.fibre;
                this.target.maximum.sodium = target.maximum.sodium;
                this.target.maximum.sugar = target.maximum.sugar;

                this.focusedNode = args.node;
            },
            createTarget(){
                this.pants.Target.create({
                    name: this.target.name,
                    slug: this.target.slug,
                    description: this.target.description,
                    daily: this.target.daily,
                    minimum: this.target.minimum,
                    maximum: this.target.maximum,
                })
                    .then(()=>{
                        this.refreshTable();
                    })
            },
            editTarget(){
                this.pants.Target.update(this.target.url, {
                    name: this.target.name,
                    slug: this.target.slug,
                    description: this.target.description,
                    daily: this.target.daily,
                    minimum: this.target.minimum,
                    maximum: this.target.maximum,
                }).then(resp => {
                        let row_node = this.focusedNode;
                        row_node.setData(resp);
                        this.targetsGrid.gridOptions.api.flashCells({
                            rowNodes: [row_node]
                        })
                    });
            },
            deleteTarget(){
                this.pants.Target.delete(this.target.url).then(()=>this.refreshTable());
            },
            refreshTable() {
                this.targetsGrid.gridOptions.api.refreshInfiniteCache();
            }
        }
    }
</script>

<style scoped lang="scss">
    .target-manager {
        display: grid;
        grid-template-columns: 1fr 30em;
        grid-template-rows: 4em 1fr;
        gap: 0 var(--padding);
        grid-template-areas: "header-all header-form" "targets-all target-selected";
        min-height: calc(100vh - 7em); /* Make it fill as much of the screen as possible to start off*/
        .header-all {
            grid-area: header-all;
        }

        .header-form {
            grid-area: header-form;
        }

        .targets-all {
            grid-area: targets-all;

            .targets-table {
                height: 100%
            }
        }

        .target-selected {
            grid-area: target-selected;
            form{
                >*:not(.nutrient-input-row){
                    margin: 1px;
                }
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                #description-container{
                    grid-column: span 3;
                }
                .nutrient-input-row{
                    display: contents;
                    [data-icon]{
                        margin-right: 0.5em;
                    }
                    span{
                        align-self: center;
                    }
                    >*{
                        margin: 1px;
                    }
                }
            }
        }
    }
</style>