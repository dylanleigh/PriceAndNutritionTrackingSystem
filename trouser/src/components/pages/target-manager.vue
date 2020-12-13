<template>
    <div :class="$options.name">
        <ag-grid-vue
                id="targets-grid"
                class="contained_table ag-theme-balham"
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
        <div class="form">
            <input-float
                    id="name"
            ></input-float>
        </div>
    </div>
</template>

<script>
    import InputFloat from '../inputs/input-float'
    import {AgGridVue} from 'ag-grid-vue'
    import "ag-grid-community/dist/styles/ag-grid.css";
    import "ag-grid-community/dist/styles/ag-theme-balham.css";

    export default {
        name: "target-manager",
        components: {
            InputFloat,
            AgGridVue
        },
        inject: ['pants'],
        data() {
            return {
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
                    // @todo Figure out these nested objects
                    minimum: null,
                    maximum: null
                }
            }
        },
        methods: {
            onRowSelected(args) {
                return args;
            }
        }
    }
</script>

<style scoped>

</style>