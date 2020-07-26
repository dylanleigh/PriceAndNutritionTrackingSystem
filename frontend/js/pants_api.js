/*
* This is a connector for javascript to the PANTS api.
*/

/**
 * Encompassing class for the API, manages connecting to the remote resource and ferrying results back
 */
class Pants {
    constructor(api_location, api_uname, api_pword) {
        this.api_location = api_location;
        this.api_uname = api_uname;
        this.api_pword = api_pword;
    }

    get_basic_auth_credentials() {
        return 'Basic ' + btoa('admin:admin')
    }

    /**
     * Gets a list of ingredients, supports searching, limit, offset, ordering
     *
     * @param {Object} options Options to pass to the api
     * @param {number} options.limit Maximum number of results to return
     * @param {number} options.offset Which ingredient to start returning results from
     * @param {string} options.ordering 
     *
     * @returns {Promise<void>}
     */
    async get_ingredients(options) {

        // Get the number of requested results
        let num_requested = params.endRow - params.startRow;

        let api_location = new URL('http://127.0.0.1:8000/api/1/ingredient/');
        api_location.searchParams.set('offset', params.startRow);
        api_location.searchParams.set('limit', num_requested);

        // Handle sorting options
        let ordering = [];
        for (let id of params.sortModel) {
            let param = '';
            param += id.sort === 'desc' ? '-' : '';
            param += id.colId;
            ordering.push(param)
        }
        api_location.searchParams.set('ordering', ordering.join(','));

        // Handle searching options
        api_location.searchParams.set('search', document.querySelector('#ingredient_filter').value);

        // Fetch the data
        let response = await fetch(api_location.toString(), {
            headers: new Headers({
                'Authorization': get_basic_auth_credentials()
            })
        });
        if (response.ok) {
            let data = await response.json();
            params.successCallback(data['results'], data['count'])
        } else {
            params.failCallback();
        }
    }


}

